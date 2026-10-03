# Astrology API Python SDK (DivineAPI)

![Astrology API Python SDK (DivineAPI)](https://raw.githubusercontent.com/DivineAPI/DivineAPI/main/assets/divineapi-python.png)

[![PyPI](https://img.shields.io/pypi/v/divineapi)](https://pypi.org/project/divineapi/)
[![Docs](https://img.shields.io/badge/Docs-developers.divineapi.com-blue)](https://developers.divineapi.com)
[![Trial](https://img.shields.io/badge/Trial-14--day-green)](https://divineapi.com/start-trial)
[![Status](https://img.shields.io/badge/Status-status.divineapi.com-lightgrey)](https://status.divineapi.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/DivineAPI/divineapi-python)

Verified live against the DivineAPI API on 2 October 2026.

Official [DivineAPI](https://divineapi.com) Python client for Vedic, Western, horoscope, tarot and numerology astrology endpoints. Responses come back as Python dicts parsed from the API's JSON.

## Get your API key

1. Start the [14-day free trial](https://divineapi.com/start-trial) (credit card required to activate the trial).
2. Copy your **API key** and **auth token** from the DivineAPI dashboard. The SDK sends the token as an
   `Authorization: Bearer` header and the key as the `api_key` form field on every request.

## Installation

```bash
pip install divineapi
```

Requires Python 3.8+ and `requests`. Or install from source:

```bash
git clone https://github.com/DivineAPI/divineapi-python.git
cd divineapi-python
pip install -e .
```

## Quick Start

```python
from divineapi import DivineApi

client = DivineApi(api_key="YOUR_API_KEY", auth_token="YOUR_AUTH_TOKEN")

# Panchang for Mumbai on 2 October 2026; tzone is a decimal UTC offset
result = client.indian.panchang.find_panchang(
    day=2, month=10, year=2026,
    place="mumbai", lat=19.076, lon=72.8777, tzone=5.5,
)

data = result["data"]
print("Sunrise:", data["sunrise"], "| Sunset:", data["sunset"])
for t in data["tithis"]:
    print("Tithi:", t["paksha"], t["tithi"], "until", t["end_time"])
# Sunrise: 2026-10-02 06:29:07 | Sunset: 2026-10-02 18:27:01
# Tithi: Krishna Shasthi until 2026-10-02 10:15:42
# Tithi: Krishna Saptami until 2026-10-03 06:28:42
```

Real response (2 Oct 2026, Mumbai, trimmed with `...`):

```json
{
  "success": 1,
  "data": {
    "sunrise": "2026-10-02 06:29:07",
    "sunset": "2026-10-02 18:27:01",
    "nakshatras": {
      "zodiac_point": [
        { "sign": "Taurus", "end_time": "2026-10-02 15:40:07" },
        { "sign": "Gemini", "end_time": "" }
      ],
      "nakshatra_pada": [
        {
          "nak_name": "Mrigashira",
          "lord": "Mars",
          "deity": "Soma",
          "symbol": "Deer's Head",
          "syllables": "वे, वो, का, की",
          "gana": "Deva",
          "nak_number": 5,
          "nak_pada": 1,
          "end_time": "2026-10-02 10:03:07",
          "...": "..."
        },
        "..."
      ],
      "...": "..."
    },
    "tithis": [
      { "start_time": "2026-10-01 12:36:42", "end_time": "2026-10-02 10:15:42", "tithi": "Shasthi", "paksha": "Krishna", "deity": "Kartikeya", "...": "..." },
      { "start_time": "2026-10-02 10:16:42", "end_time": "2026-10-03 06:28:42", "tithi": "Saptami", "paksha": "Krishna", "deity": "Surya", "...": "..." }
    ],
    "...": "..."
  }
}
```

## API Categories

### Horoscope & Tarot

```python
# Daily / Weekly / Monthly / Yearly Horoscope
# daily h_day = today / tomorrow / yesterday; weekly/monthly/yearly = current / prev / next
client.horoscope.daily(sign="aries", h_day="today", tzone=5.5)
client.horoscope.weekly(sign="leo", week="current", tzone=5.5)
client.horoscope.monthly(sign="cancer", month="current", tzone=5.5)
client.horoscope.yearly(sign="virgo", year="current", tzone=5.5)

# Chinese & Numerology Horoscope
client.horoscope.chinese(sign="rat", h_day="today", tzone=5.5)
client.horoscope.numerology(number=7, day=10, month=3, year=2024, tzone=5.5)

# Tarot & Readings
client.horoscope.yes_or_no_tarot()
client.horoscope.daily_tarot()
client.horoscope.fortune_cookie()
client.horoscope.coffee_cup_reading()
client.horoscope.love_compatibility(sign_1="aries", sign_2="leo")
```

### Indian Astrology - Panchang

```python
# Panchang, Nakshatra, Tithi, Yoga, Karana
client.indian.panchang.find_panchang(
    day=10, month=3, year=2024,
    place="delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
client.indian.panchang.find_nakshatra(
    day=10, month=3, year=2024,
    place="mumbai", lat=19.076, lon=72.8777, tzone=5.5
)
client.indian.panchang.auspicious_timings(
    day=10, month=3, year=2024,
    place="delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
client.indian.panchang.find_gowri_panchangam(
    day=10, month=3, year=2024,
    place="chennai", lat=13.0827, lon=80.2707, tzone=5.5
)

# Planetary transits
client.indian.panchang.grah_gochar(
    planet="jupiter", month=3, year=2024,
    place="delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
```

### Indian Astrology - Kundli

```python
birth = dict(
    full_name="John Doe", day=1, month=1, year=1990,
    hour=10, min=30, sec=0, gender="male",
    place="mumbai", lat=19.076, lon=72.8777, tzone=5.5,
)

client.indian.kundli.basic_astro_details(**birth)
client.indian.kundli.planetary_positions(**birth)
client.indian.kundli.manglik_dosha(**birth)
client.indian.kundli.vimshottari_dasha(**birth)
client.indian.kundli.sadhe_sati(**birth)
client.indian.kundli.yogas(**birth)
client.indian.kundli.horoscope_chart("D1", **birth)

# Jaimini
client.indian.kundli.jaimini_planetary_positions(**birth)
client.indian.kundli.jaimini_padas(**birth)
client.indian.kundli.jaimini_karakamsha_lagna(**birth)   # D1 recast from the Karakamsha sign
client.indian.kundli.jaimini_chara_dasha(**birth)
client.indian.kundli.jaimini_swamsa_chart(**birth)       # D9 recast from the Karakamsha sign

# jaimini_swamsa_chart returns atmakaraka, swamsha_sign_no, swamsha_sign,
# lagnamsha_sign_no, lagnamsha_sign and the chart as svg plus base64_image
# (~10 KB in all). With lan="hi" the names are translated, the numbers are not.

# Dasha analysis (no birth data needed)
client.indian.kundli.maha_dasha_analysis(maha_dasha="Sun")

# Lal Kitab
client.indian.kundli.lal_kitab_planetary_positions(**birth)
client.indian.kundli.lal_kitab_teva(**birth)
client.indian.kundli.lal_kitab_debts(**birth)
client.indian.kundli.lal_kitab_planet_analysis("sun", **birth)
client.indian.kundli.lal_kitab_house_signification(1, **birth)
client.indian.kundli.lal_kitab_varshphal_chart(2026, **birth)

# Lal Kitab dasha content (no birth data needed)
client.indian.kundli.lal_kitab_mahadasha_content(maha_dasha="saturn")
client.indian.kundli.lal_kitab_antardasha_content(maha_dasha="saturn", antar_dasha="mercury")

# Additional kundli analysis
client.indian.kundli.vargottama_planets(**birth)
client.indian.kundli.bhav_bala(**birth)
client.indian.kundli.shani_ashtam_shani(**birth)
client.indian.kundli.bhava_analysis(**birth)
client.indian.kundli.bhava_group_predictions(**birth)
client.indian.kundli.planet_remedies("sun", **birth)   # analysis_planet + birth
```

### Indian Astrology - Match Making

```python
client.indian.match_making.ashtakoot_milan(
    p1_full_name="Groom", p1_day=1, p1_month=1, p1_year=1990,
    p1_hour=10, p1_min=0, p1_sec=0, p1_gender="male",
    p1_place="delhi", p1_lat=28.6, p1_lon=77.2, p1_tzone=5.5,
    p2_full_name="Bride", p2_day=5, p2_month=5, p2_year=1992,
    p2_hour=14, p2_min=0, p2_sec=0, p2_gender="female",
    p2_place="mumbai", p2_lat=19.07, p2_lon=72.87, p2_tzone=5.5,
)
```

### Indian Astrology - Festivals

```python
client.indian.festival.chaitra_festivals(
    year=2024, place="delhi", lat=28.6, lon=77.2, tzone=5.5
)
client.indian.festival.english_calendar(
    year=2024, month=3, place="delhi", lat=28.6, lon=77.2, tzone=5.5
)
# festival is a lowercase snake_case slug from the DivineAPI festival list
client.indian.festival.find_festival(
    festival="maha_shivratri", year=2024,
    place="delhi", lat=28.6, lon=77.2, tzone=5.5
)
client.indian.festival.malayalam_festivals(
    year=2027, place="kochi", lat=9.9312, lon=76.2673, tzone=5.5
)
client.indian.festival.tamil_festivals(
    year=2027, place="chennai", lat=13.0827, lon=80.2707, tzone=5.5
)
client.indian.festival.sankranti_festivals(
    year=2027, place="new delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
```

### Western Astrology - Natal

```python
birth_w = dict(
    full_name="Jane Smith", day=15, month=6, year=1995,
    hour=8, min=0, sec=0, gender="female",
    place="new york", lat=40.7128, lon=-74.0060, tzone=-5.0,
)

client.western.natal.planetary_positions(**birth_w)  # 18 bodies incl. Vertex; see note below
client.western.natal.house_cusps(**birth_w)
client.western.natal.aspect_table(**birth_w)
client.western.natal.natal_wheel_chart(**birth_w)
client.western.natal.natal_insights(**birth_w)
client.western.natal.dominants(method="TRADITIONAL", **birth_w)
client.western.natal.persona_chart(persona_planet="moon", **birth_w)

# persona_chart: chart for the moment, within the first year of life, that the
# transiting Sun reaches the natal degree of persona_planet. output_include
# defaults to "raw_data" (~21 KB); image tokens are ~0.5 MB per SVG and
# output_include="all" returns ~4.3 MB.
```

> **`planetary_positions` changed in 1.10.0.** It now calls astroapi-8 instead of astroapi-4, so the response includes **Vertex** (18 bodies instead of 17). Two behaviour changes come with it:
> - the envelope is `{"status": "success", "code": 200, "message": ..., "data": [...]}` - there is no longer a `success` key, so code checking `resp["success"] == 1` must switch to `resp["status"] == "success"` (or just read `resp["data"]`);
> - invalid input now raises `ValidationError` (HTTP 422) instead of returning `{"success": 2}`.
>
> The `data` list is otherwise unchanged: same fields, same types, identical values for the other 17 bodies.

### Western Astrology - Synastry

```python
client.western.synastry.planetary_positions(
    p1_full_name="Person A", p1_day=1, p1_month=1, p1_year=1990,
    p1_hour=10, p1_min=0, p1_sec=0, p1_gender="male",
    p1_place="london", p1_lat=51.5, p1_lon=-0.12, p1_tzone=0,
    p2_full_name="Person B", p2_day=15, p2_month=6, p2_year=1992,
    p2_hour=14, p2_min=0, p2_sec=0, p2_gender="female",
    p2_place="paris", p2_lat=48.85, p2_lon=2.35, p2_tzone=1,
)
client.western.synastry.emotional_compatibility(...)
```

### Western Astrology - Transit

```python
client.western.transit.daily(**birth_w)
client.western.transit.planet_retrograde(
    planet="mercury", month=3, year=2024,
    place="new york", lat=40.71, lon=-74.0, tzone=-5.0,
)
```

### Numerology

```python
# Chaldean numerology
client.numerology.loshu_grid(fname="John", lname="Doe", day=1, month=1, year=1990)
client.numerology.name_number(fname="John", lname="Doe", day=1, month=1, year=1990)
client.numerology.name_correction(full_name="John Doe", day=1, month=1, year=1990)

# Core numbers
client.numerology.core_numbers(
    full_name="John Doe", day=1, month=1, year=1990,
    gender="male", method="pythagorean",
)

# Mobile number analysis
client.numerology.new_mobile_number(fname="John", lname="Doe", day=1, month=1, year=1990)
client.numerology.analyze_mobile_number(
    fname="John", lname="Doe", day=1, month=1, year=1990,
    mobile_number="9876543210",
)
```

### Lifestyle

```python
client.lifestyle.zodiac_gift_guru(sign="aries", h_day="today", tzone=5.5)
client.lifestyle.beauty_by_the_stars(sign="leo", h_day="today", tzone=5.5)
client.lifestyle.astro_chic_picks(sign="virgo", h_day="today", tzone=5.5)
```

### Calculators

```python
client.calculators.flames(your_name="John", partner_name="Jane")
client.calculators.love_calculator(
    your_name="John", partner_name="Jane",
    your_gender="male", partner_gender="female",
)
```

### PDF Reports

```python
# The API requires seven branding fields on every PDF request: company_name,
# company_url, company_email, company_mobile, company_bio, logo_url and
# footer_text (a few legacy reports also need company_landline).
# Pass company_mobile even though the SDK treats it as optional.
client.pdf.kundali_sampoorna(
    full_name="John", day=1, month=1, year=1990,
    hour=10, min=30, sec=0, gender="male",
    place="mumbai", lat=19.07, lon=72.87, tzone=5.5,
    company_name="YOUR_COMPANY_NAME", company_url="YOUR_COMPANY_URL",
    company_email="YOUR_COMPANY_EMAIL", company_mobile="YOUR_COMPANY_MOBILE",
    company_bio="YOUR_COMPANY_BIO",
    logo_url="YOUR_LOGO_URL", footer_text="YOUR_FOOTER_TEXT",
)
```

## Error Handling

```python
from divineapi import DivineApi, AuthenticationError, ValidationError, RateLimitError

client = DivineApi(api_key="...", auth_token="...")

try:
    result = client.horoscope.daily(sign="aries", h_day="today", tzone=5.5)
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except ValidationError as e:
    print(f"Bad request: {e}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
```

## Context Manager

```python
with DivineApi(api_key="...", auth_token="...") as client:
    result = client.horoscope.daily(sign="aries", h_day="today", tzone=5.5)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | required | Your DivineAPI key |
| `auth_token` | required | Bearer token for Authorization header |
| `timeout` | 30 | Request timeout in seconds |
| `max_retries` | 2 | Number of retry attempts on failure |

## Related repos

| Type | Repo |
|---|---|
| SDK | [divineapi-node](https://github.com/DivineAPI/divineapi-node): Node.js / TypeScript SDK (`npm install divineapi`) |
| SDK | [divineapi-php](https://github.com/DivineAPI/divineapi-php): PHP SDK (`composer require divineapi/divineapi`) |
| REST API | [kundli-api](https://github.com/DivineAPI/kundli-api): Kundli / Kundali API (Vedic birth chart, dashas, doshas) |
| REST API | [kundli-matching-api](https://github.com/DivineAPI/kundli-matching-api): Kundli matching API (Ashtakoot, Dashakoot) |
| REST API | [lal-kitab-api](https://github.com/DivineAPI/lal-kitab-api): Lal Kitab API |
| REST API | [panchang-api](https://github.com/DivineAPI/panchang-api): Panchang API |
| REST API | [hindu-festival-api](https://github.com/DivineAPI/hindu-festival-api): Hindu Festival API |
| REST API | [birth-chart-api](https://github.com/DivineAPI/birth-chart-api): Birth Chart API |
| REST API | [horoscope-api](https://github.com/DivineAPI/horoscope-api): Horoscope API |
| REST API | [tarot-api](https://github.com/DivineAPI/tarot-api): Tarot API |
| REST API | [numerology-api](https://github.com/DivineAPI/numerology-api): Numerology API |
| REST API | [astrology-api](https://github.com/DivineAPI/astrology-api): Astrology API (overview of all domains) |
| Model Context Protocol (MCP) | [mcp-indian-astrology](https://github.com/DivineAPI/mcp-indian-astrology): Vedic astrology MCP server |
| MCP | [mcp-western-astrology](https://github.com/DivineAPI/mcp-western-astrology): Western astrology MCP server |
| MCP | [mcp-horoscope-numerology](https://github.com/DivineAPI/mcp-horoscope-numerology): Horoscope, tarot and numerology MCP server |

## Support

- API reference: [developers.divineapi.com](https://developers.divineapi.com)
- Postman collection: [documenter.getpostman.com/view/26759678/2sBYAysU8Y](https://documenter.getpostman.com/view/26759678/2sBYAysU8Y)
- API status: [status.divineapi.com](https://status.divineapi.com)
- Help centre: [support.divineapi.com](https://support.divineapi.com)
- Plans and prices: [divineapi.com/pricing](https://divineapi.com/pricing)
- SDK bugs: open an issue in this repo

## License

MIT
