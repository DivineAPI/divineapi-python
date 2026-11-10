"""Astro Chatbot API (ask.divineapi.com): astrology answers grounded in a birth chart.

Conversations are scoped per end user. One api_key (you) has many ``user_id``
values (your end users), and each ``user_id`` has many ``session_id`` values
(separate conversations), each with its own birth details. The same
``session_id`` under two different ``user_id`` values is two separate sessions.

Needs an Astro Chatbot plan on the account. The SDK sends your api_key and
auth_token as the ``x-api-key`` and ``Authorization: Bearer`` headers.
"""

from typing import Any, Dict, Iterator

from .client import BaseClient
from .exceptions import ServerError

HOST = "ask"


def _body(params: Dict[str, Any]) -> Dict[str, Any]:
    """Drop ``None`` values and send numbers as strings.

    The chatbot accepts only JSON strings for its fields (``day=24`` or
    ``tzone=5.5`` get a 422), while the rest of the SDK takes numbers, so
    ints and floats are converted. Booleans stay booleans.
    """
    out: Dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            value = str(value)
        out[key] = value
    return out


class ChatbotApi:
    """Astro Chatbot endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    def chat(self, user_id: str, session_id: str, message: str, **options: Any) -> Dict[str, Any]:
        """Send one message in a conversation and get the answer.

        The first message of a session must carry the birth details: ``day``,
        ``month``, ``year``, ``hour``, ``min``, ``gender``, ``place``, ``lat``,
        ``lon`` and ``tzone`` (``full_name`` and ``sec`` are optional). Later
        messages in the same session reuse them until a new complete set is
        sent, which replaces them.

        Options, all optional:

        - ``depth``: ``"quick"`` (20 credits), ``"standard"`` (30, default) or ``"deep"`` (50)
        - ``length_cap``: ``"short"``, ``"medium"`` (default) or ``"full"``
        - ``language``: ``"English"`` (default), ``"Hindi"``, any language name,
          or ``"auto"`` to answer in the language of the message
        - ``school``: ``"western"`` (default), ``"vedic"``, ``"kp"`` or ``"lalkitab"``
        - ``lens``: ``"general"`` (default), ``"career"``, ``"love"``, ``"health"``,
          ``"money"`` or ``"spiritual"``
        - ``confidence``: ``"balanced"`` (default), ``"definitive"`` or ``"careful"``
        - ``sensitivity``: ``"standard"`` (default) or ``"strict"`` (for matrimony
          and relationship products)
        - free text: ``tone``, ``framing``, ``assistant_name``, ``brand_voice``,
          ``sign_off`` and ``style_notes`` (at most 500 characters)

        Returns ``request_id``, ``answer``, ``band``, ``credits_charged`` and
        ``credits_remaining``. A message the guardrails block gets a free
        reply with ``blocked: True`` and a ``block_reason``.

        Sent once, never retried, because every answer is charged. Use
        :meth:`chat_stream` to stream the answer.
        """
        if options.pop("stream", False):
            raise ValueError("chat() returns one JSON answer; use chat_stream() to stream it")
        body = _body({**options, "user_id": user_id, "session_id": session_id, "message": message})
        return self._c.post_json(HOST, "/chat", body, retry=False)

    def chat_stream(
        self, user_id: str, session_id: str, message: str, **options: Any
    ) -> Iterator[Dict[str, Any]]:
        """Same as :meth:`chat`, but streams the answer while it is written.

        Yields ``{"delta": "<text>"}`` events, then one last event with
        ``"done": True`` and the fields :meth:`chat` returns. That event's
        ``answer`` is the final cleaned-up text, which can differ slightly
        from the joined deltas. HTTP errors raise before the first event.
        Raises :class:`ServerError` if the answer fails part-way; nothing is
        charged then.

        Example::

            for event in client.chatbot.chat_stream("u_1", "s_1", "Will I travel this year?"):
                if "delta" in event:
                    print(event["delta"], end="", flush=True)
                elif event.get("done"):
                    print("\\ncredits left:", event["credits_remaining"])
        """
        options.pop("stream", None)
        body = _body({**options, "user_id": user_id, "session_id": session_id,
                      "message": message, "stream": True})
        return self._raise_stream_errors(self._c.post_json_stream(HOST, "/chat", body))

    @staticmethod
    def _raise_stream_errors(events: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
        try:
            for event in events:
                if isinstance(event, dict) and event.get("error") and not event.get("done"):
                    raise ServerError(message=str(event["error"]), status_code=502, response=event)
                yield event
        finally:
            close = getattr(events, "close", None)
            if close:
                close()

    def horoscope_prediction(self, user_id: str, date: str, **options: Any) -> Dict[str, Any]:
        """Short personal horoscope for one date, from the birth chart and that day's sky.

        ``date`` is ``YYYY-MM-DD``, from 1900-01-01 to 2100-12-30. Every call
        needs the complete birth details: ``day``, ``month``, ``year``, ``hour``,
        ``min``, ``gender``, ``place``, ``lat``, ``lon`` and ``tzone``
        (``full_name`` and ``sec`` are optional).

        Options: ``depth`` (``"quick"`` up to 20 words, ``"standard"`` 35-50,
        ``"deep"`` 50-80; same credits as :meth:`chat`) and ``language``.

        Returns ``request_id``, ``date``, ``prediction``, ``moon_phase_today``,
        ``credits_charged`` and ``credits_remaining``. Each prediction is also
        saved in the user's ``"horoscope-prediction"`` session, which
        :meth:`sessions` and :meth:`session` show.

        Sent once, never retried, because every prediction is charged.
        """
        options.pop("message", None)   # a message would turn this into a chat turn
        options.pop("stream", None)
        body = _body({**options, "user_id": user_id, "date": date})
        return self._c.post_json(HOST, "/chat", body, retry=False)

    def sessions(self, user_id: str) -> Dict[str, Any]:
        """Every conversation this end user has under your key, most recent first.

        Returns ``sessions``: each has ``session_id``, ``messages`` (count),
        ``started`` and ``last_active`` (Unix seconds) and ``has_birth_details``.
        Raises :class:`NotFoundError` if the user_id has no sessions yet.
        """
        return self._c.post_json(HOST, "/sessions", _body({"user_id": user_id}))

    def session(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """One conversation's full history, for restoring a chat screen.

        Returns ``session_id``, ``messages`` (oldest first, each with ``role``,
        ``text`` and ``ts`` in Unix seconds) and the stored ``birth_details``.
        Raises :class:`NotFoundError` if the user_id or this user's session_id
        is unknown.
        """
        return self._c.post_json(
            HOST, "/session", _body({"user_id": user_id, "session_id": session_id})
        )

    def delete_session(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Permanently delete one conversation: its messages and stored birth details.

        Use it when your end user asks to be forgotten. Returns ``deleted``,
        ``session_id`` and ``messages_removed``. Raises :class:`NotFoundError`
        if the user_id or this user's session_id is unknown. Sent once, so a
        timeout never turns a completed delete into a NotFoundError on retry.
        """
        return self._c.post_json(
            HOST, "/session/delete", _body({"user_id": user_id, "session_id": session_id}),
            retry=False,
        )

    def balance(self) -> Dict[str, Any]:
        """Astro Chatbot credit balance for your key. Free.

        Returns ``state`` (``"active"``, ``"expired"`` or ``"limit_reached"``),
        ``credits_remaining`` and ``expires`` (``YYYY-MM-DD``). Raises
        :class:`NotFoundError` if the account has no Astro Chatbot plan.
        """
        return self._c.post_json(HOST, "/balance", {})
