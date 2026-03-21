"""Indian API - combines Panchang, Kundli, MatchMaking, and Festival sub-modules."""

from ..client import BaseClient
from .festival import FestivalApi
from .kundli import KundliApi
from .match_making import MatchMakingApi
from .panchang import PanchangApi


class IndianApi:
    """Facade for all Indian API sub-modules."""

    def __init__(self, client: BaseClient) -> None:
        self.panchang = PanchangApi(client)
        self.kundli = KundliApi(client)
        self.match_making = MatchMakingApi(client)
        self.festival = FestivalApi(client)
