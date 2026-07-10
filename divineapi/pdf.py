"""PDF Report endpoints (pdf.divineapi.com)."""

from typing import Any, Dict

from .client import BaseClient

HOST = "pdf"


class PdfReportApi:
    """PDF report generation endpoints."""

    def __init__(self, client: BaseClient) -> None:
        self._c = client

    # ------------------------------------------------------------------ #
    # Shared payload builders
    # ------------------------------------------------------------------ #

    @staticmethod
    def _birth_company(
        full_name: str, day: int, month: int, year: int,
        hour: int, min: int, sec: int, gender: str,
        place: str, lat: float, lon: float, tzone: float,
        company_name: str, company_url: str, company_email: str,
        company_bio: str, logo_url: str, footer_text: str,
        lan: str = "en", company_mobile: str = "",
        **extra: Any,
    ) -> Dict[str, Any]:
        # The six branding fields are REQUIRED by the PDF backend (it rejects
        # requests without them). company_mobile is optional and sent only when
        # provided.
        d: Dict[str, Any] = {
            "full_name": full_name, "day": day, "month": month, "year": year,
            "hour": hour, "min": min, "sec": sec, "gender": gender,
            "place": place, "lat": lat, "lon": lon, "tzone": tzone,
            "lan": lan,
            "company_name": company_name, "company_url": company_url,
            "company_email": company_email,
            "company_bio": company_bio, "logo_url": logo_url,
            "footer_text": footer_text,
        }
        if company_mobile:
            d["company_mobile"] = company_mobile
        d.update(extra)
        return d

    @staticmethod
    def _couple_company(
        p1_full_name: str, p1_day: int, p1_month: int, p1_year: int,
        p1_hour: int, p1_min: int, p1_sec: int, p1_gender: str,
        p1_place: str, p1_lat: float, p1_lon: float, p1_tzone: float,
        p2_full_name: str, p2_day: int, p2_month: int, p2_year: int,
        p2_hour: int, p2_min: int, p2_sec: int, p2_gender: str,
        p2_place: str, p2_lat: float, p2_lon: float, p2_tzone: float,
        company_name: str, company_url: str, company_email: str,
        company_bio: str, logo_url: str, footer_text: str,
        lan: str = "en", company_mobile: str = "",
        **extra: Any,
    ) -> Dict[str, Any]:
        # The six branding fields are REQUIRED by the PDF backend.
        d: Dict[str, Any] = {
            "p1_full_name": p1_full_name, "p1_day": p1_day, "p1_month": p1_month,
            "p1_year": p1_year, "p1_hour": p1_hour, "p1_min": p1_min,
            "p1_sec": p1_sec, "p1_gender": p1_gender, "p1_place": p1_place,
            "p1_lat": p1_lat, "p1_lon": p1_lon, "p1_tzone": p1_tzone,
            "p2_full_name": p2_full_name, "p2_day": p2_day, "p2_month": p2_month,
            "p2_year": p2_year, "p2_hour": p2_hour, "p2_min": p2_min,
            "p2_sec": p2_sec, "p2_gender": p2_gender, "p2_place": p2_place,
            "p2_lat": p2_lat, "p2_lon": p2_lon, "p2_tzone": p2_tzone,
            "lan": lan,
            "company_name": company_name, "company_url": company_url,
            "company_email": company_email,
            "company_bio": company_bio, "logo_url": logo_url,
            "footer_text": footer_text,
        }
        if company_mobile:
            d["company_mobile"] = company_mobile
        d.update(extra)
        return d

    def _post_birth(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post(HOST, path, self._birth_company(**kw))

    def _post_couple(self, path: str, **kw: Any) -> Dict[str, Any]:
        return self._c.post(HOST, path, self._couple_company(**kw))

    # ------------------------------------------------------------------ #
    # Kundali PDFs (3)
    # ------------------------------------------------------------------ #

    def kundali_sampoorna(self, **kw: Any) -> Dict[str, Any]:
        """Kundali Sampoorna PDF."""
        return self._post_birth("/indian-api/v2/kundali-sampoorna", **kw)

    def kundali_ananta(self, **kw: Any) -> Dict[str, Any]:
        """Kundali Ananta PDF."""
        return self._post_birth("/indian-api/v2/kundali-ananta", **kw)

    def kundali_prakash(self, **kw: Any) -> Dict[str, Any]:
        """Kundali Prakash PDF."""
        return self._post_birth("/indian-api/v2/kundali-prakash", **kw)

    # ------------------------------------------------------------------ #
    # Match Making PDF
    # ------------------------------------------------------------------ #

    def match_making(self, **kw: Any) -> Dict[str, Any]:
        """Match Making PDF (couple params)."""
        return self._post_couple("/indian-api/v2/match-making", **kw)

    # ------------------------------------------------------------------ #
    # Specialized PDFs
    # ------------------------------------------------------------------ #

    def government_job(self, **kw: Any) -> Dict[str, Any]:
        """Government Job Report PDF."""
        return self._post_birth("/indian-api/v2/government-job-report", **kw)

    def foreign_travel(self, **kw: Any) -> Dict[str, Any]:
        """Foreign Travel Settlement PDF."""
        return self._post_birth("/indian-api/v2/foreign-travel-settlement", **kw)

    def vedic_yearly_5_year(self, **kw: Any) -> Dict[str, Any]:
        """Vedic Yearly Prediction 5-Year PDF."""
        return self._post_birth("/indian-api/v2/vedic-yearly-prediction-5-year", **kw)

    def vedic_yearly_10_year(self, **kw: Any) -> Dict[str, Any]:
        """Vedic Yearly Prediction 10-Year PDF."""
        return self._post_birth("/indian-api/v2/vedic-yearly-prediction-10-year", **kw)

    def vedic_yearly_15_year(self, **kw: Any) -> Dict[str, Any]:
        """Vedic Yearly Prediction 15-Year PDF."""
        return self._post_birth("/indian-api/v2/vedic-yearly-prediction-15-year", **kw)

    # ------------------------------------------------------------------ #
    # Astrology / Numerology reports with report_code
    # ------------------------------------------------------------------ #

    def natal_report(self, report_code: str, theme: str, **kw: Any) -> Dict[str, Any]:
        """Natal Report PDF.

        Both ``report_code`` (e.g. 'CAREER-REPORT') and ``theme`` (e.g. '001')
        are required by the API, along with the six company branding fields.
        """
        kw["report_code"] = report_code
        kw["theme"] = theme
        return self._post_birth("/astrology/v2/report", **kw)

    def natal_couple_report(self, report_code: str, **kw: Any) -> Dict[str, Any]:
        """Natal Couple Report PDF."""
        kw["report_code"] = report_code
        return self._post_couple("/astrology/v1/couple", **kw)

    def prediction_report(self, report_code: str, **kw: Any) -> Dict[str, Any]:
        """Prediction Report PDF."""
        kw["report_code"] = report_code
        return self._post_birth("/numerology/v1/prediction_reports", **kw)

    def numerology_report(self, report_code: str, **kw: Any) -> Dict[str, Any]:
        """Numerology Report PDF."""
        kw["report_code"] = report_code
        return self._post_birth("/numerology/v2/report", **kw)

    def reports_generate(self, report_code: str, **kw: Any) -> Dict[str, Any]:
        """Reports V2 Generate PDF."""
        kw["report_code"] = report_code
        return self._post_birth("/api/v1/reports/generate", **kw)
