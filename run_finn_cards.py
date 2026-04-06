from finn_cards import analyze_all


def format_currency(value: int) -> str:
    return f"{value:,} kr".replace(",", " ")


def main() -> None:
    results = analyze_all()

    for item in results:
        print("=" * 60)
        print(item.title)
        print(f"card_name: {item.card_name}")
        print(f"set_name: {item.set_name}")
        print(f"card_number: {item.card_number}")
        print(f"grade: {item.grade}")
        print(f"price: {format_currency(item.price)}")
        print(f"estimated value: {format_currency(item.estimated_value)}")
        print(f"% difference: {item.percent_difference}%")
        print(f"verdict: {item.verdict}")


if __name__ == "__main__":
    main()
