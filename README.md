# DivineAPI Python SDK

Official Python SDK for the [Divine API](https://divineapi.com) -- Astrology, Horoscopes, Numerology, Tarot, Kundli, and more.

## Installation

```bash
pip install divineapi
```

Or install from source:

```bash
git clone https://github.com/niceDevelopers/divine-api-python.git
cd divine-api-python
pip install -e .
```

## Quick Start

```python
from divineapi import DivineApi

client = DivineApi(api_key="your-api-key", auth_token="your-bearer-token")

# Daily Horoscope (h_day = today, tomorrow, or yesterday)
result = client.horoscope.daily(
    sign="aries", h_day="today", tzone=5.5
)
print(result)
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
    place="Delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
client.indian.panchang.find_nakshatra(
    day=10, month=3, year=2024,
    place="Mumbai", lat=19.076, lon=72.8777, tzone=5.5
)
client.indian.panchang.auspicious_timings(
    day=10, month=3, year=2024,
    place="Delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
client.indian.panchang.find_gowri_panchangam(
    day=10, month=3, year=2024,
    place="Chennai", lat=13.0827, lon=80.2707, tzone=5.5
)

# Planetary transits
client.indian.panchang.grah_gochar(
    planet="jupiter", month=3, year=2024,
    place="Delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
```

### Indian Astrology - Kundli

```python
birth = dict(
    full_name="John Doe", day=1, month=1, year=1990,
    hour=10, min=30, sec=0, gender="male",
    place="Mumbai", lat=19.076, lon=72.8777, tzone=5.5,
)

client.indian.kundli.basic_astro_details(**birth)
client.indian.kundli.planetary_positions(**birth)
client.indian.kundli.manglik_dosha(**birth)
client.indian.kundli.vimshottari_dasha(**birth)
client.indian.kundli.sadhe_sati(**birth)
client.indian.kundli.yogas(**birth)
client.indian.kundli.horoscope_chart("D1", **birth)

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
    p1_place="Delhi", p1_lat=28.6, p1_lon=77.2, p1_tzone=5.5,
    p2_full_name="Bride", p2_day=5, p2_month=5, p2_year=1992,
    p2_hour=14, p2_min=0, p2_sec=0, p2_gender="female",
    p2_place="Mumbai", p2_lat=19.07, p2_lon=72.87, p2_tzone=5.5,
)
```

### Indian Astrology - Festivals

```python
client.indian.festival.chaitra_festivals(
    year=2024, place="Delhi", lat=28.6, lon=77.2, tzone=5.5
)
client.indian.festival.english_calendar(
    year=2024, month=3, place="Delhi", lat=28.6, lon=77.2, tzone=5.5
)
# festival is a lowercase snake_case slug from the Divine festival list
client.indian.festival.find_festival(
    festival="maha_shivratri", year=2024,
    place="Delhi", lat=28.6, lon=77.2, tzone=5.5
)
client.indian.festival.malayalam_festivals(
    year=2027, place="Kochi", lat=9.9312, lon=76.2673, tzone=5.5
)
client.indian.festival.tamil_festivals(
    year=2027, place="Chennai", lat=13.0827, lon=80.2707, tzone=5.5
)
client.indian.festival.sankranti_festivals(
    year=2027, place="New Delhi", lat=28.6139, lon=77.2090, tzone=5.5
)
```

### Western Astrology - Natal

```python
birth_w = dict(
    full_name="Jane Smith", day=15, month=6, year=1995,
    hour=8, min=0, sec=0, gender="female",
    place="New York", lat=40.7128, lon=-74.0060, tzone=-5.0,
)

client.western.natal.planetary_positions(**birth_w)
client.western.natal.house_cusps(**birth_w)
client.western.natal.aspect_table(**birth_w)
client.western.natal.natal_wheel_chart(**birth_w)
client.western.natal.natal_insights(**birth_w)
client.western.natal.dominants(method="TRADITIONAL", **birth_w)
```

### Western Astrology - Synastry

```python
client.western.synastry.planetary_positions(
    p1_full_name="Person A", p1_day=1, p1_month=1, p1_year=1990,
    p1_hour=10, p1_min=0, p1_sec=0, p1_gender="male",
    p1_place="London", p1_lat=51.5, p1_lon=-0.12, p1_tzone=0,
    p2_full_name="Person B", p2_day=15, p2_month=6, p2_year=1992,
    p2_hour=14, p2_min=0, p2_sec=0, p2_gender="female",
    p2_place="Paris", p2_lat=48.85, p2_lon=2.35, p2_tzone=1,
)
client.western.synastry.emotional_compatibility(...)
```

### Western Astrology - Transit

```python
client.western.transit.daily(**birth_w)
client.western.transit.planet_retrograde(
    planet="mercury", month=3, year=2024,
    place="New York", lat=40.71, lon=-74.0, tzone=-5.0,
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
# The six branding fields (company_url, logo_url, footer_text, company_name,
# company_email, company_bio) are REQUIRED by the PDF backend.
client.pdf.kundali_sampoorna(
    full_name="John", day=1, month=1, year=1990,
    hour=10, min=30, sec=0, gender="male",
    place="Mumbai", lat=19.07, lon=72.87, tzone=5.5,
    company_name="AstroCo", company_url="https://example.com",
    company_email="hello@example.com", company_bio="We do astrology.",
    logo_url="https://example.com/logo.png", footer_text="(c) AstroCo",
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
| `api_key` | required | Your Divine API key |
| `auth_token` | required | Bearer token for Authorization header |
| `timeout` | 30 | Request timeout in seconds |
| `max_retries` | 2 | Number of retry attempts on failure |

## License

MIT
