from __future__ import annotations

from dataclasses import dataclass, asdict
import re


@dataclass
class Listing:
    title: str
    price: int


@dataclass
class CardResult:
    title: str
    card_name: str
    set_name: str
    card_number: str
    grade: str
    price: int
    estimated_value: int
    percent_difference: float
    verdict: str


LISTINGS = [
    Listing(title="Pokemon Charizard Base Set 4/102 PSA 8", price=4200),
    Listing(title="Pikachu VMAX Trainer Gallery TG17 Lost Origin", price=650),
    Listing(title="Umbreon H30/H32 Skyridge BGS 9.5", price=16000),
    Listing(title="Mewtwo GX Hidden Fates SV59 CGC 9", price=1900),
]

MARKET_PRICES = {
    "charizard|base set|4/102|PSA 8": 5000,
    "pikachu vmax|lost origin|TG17|RAW": 600,
    "umbreon|skyridge|H30/H32|BGS 9.5": 14500,
    "mewtwo gx|hidden fates|SV59|CGC 9": 2100,
}

KNOWN_SETS = [
    "base set",
    "lost origin",
    "skyridge",
    "hidden fates",
]

KNOWN_CARDS = [
    "charizard",
    "pikachu vmax",
    "umbreon",
    "mewtwo gx",
]


def find_first_match(text: str, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if candidate in text:
            return candidate
    return None


def extract_card_number(text: str) -> str | None:
    match = re.search(r"\b([A-Z]{0,3}\d{1,3}/\d{1,3}|[A-Z]{1,3}\d{1,3})\b", text, re.IGNORECASE)
    return match.group(1).upper() if match else None


def extract_grade(text: str) -> str:
    match = re.search(r"\b(PSA|BGS|CGC)\s?(\d+(?:\.\d)?)\b", text, re.IGNORECASE)
    if not match:
        return "RAW"
    return f"{match.group(1).upper()} {match.group(2)}"


def title_case_or_unknown(value: str | None) -> str:
    if not value:
        return "Ukjent"
    return " ".join(part.capitalize() for part in value.split())


def build_market_key(card_name: str | None, set_name: str | None, card_number: str | None, grade: str) -> str:
    return "|".join([
        card_name or "ukjent",
        set_name or "ukjent",
        card_number or "ukjent",
        grade or "RAW",
    ])


def get_verdict(percent_difference: float) -> str:
    if percent_difference <= -15:
        return "underpriced"
    if percent_difference >= 15:
        return "overpriced"
    return "fair"


def analyze_listing(listing: Listing) -> CardResult:
    lower_title = listing.title.lower()
    card_name = find_first_match(lower_title, KNOWN_CARDS)
    set_name = find_first_match(lower_title, KNOWN_SETS)
    card_number = extract_card_number(listing.title)
    grade = extract_grade(listing.title)
    market_key = build_market_key(card_name, set_name, card_number, grade)
    estimated_value = MARKET_PRICES.get(market_key, 0)

    if estimated_value == 0:
        percent_difference = 0.0
    else:
        percent_difference = ((listing.price - estimated_value) / estimated_value) * 100

    return CardResult(
        title=listing.title,
        card_name=title_case_or_unknown(card_name),
        set_name=title_case_or_unknown(set_name),
        card_number=card_number or "Ukjent",
        grade=grade,
        price=listing.price,
        estimated_value=estimated_value,
        percent_difference=round(percent_difference, 1),
        verdict=get_verdict(percent_difference),
    )


def analyze_all() -> list[CardResult]:
    return [analyze_listing(listing) for listing in LISTINGS]


def as_dicts() -> list[dict]:
    return [asdict(result) for result in analyze_all()]
