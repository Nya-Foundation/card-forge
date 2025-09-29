from forge.helper import (
    embed_card_data,
    extract_card_data,
    rebuild_card,
    repositorize,
)


def main():
    """Demonstrate the complete repositorize workflow with testing."""
    print("=== Card Forge Workflow Demo ===")

    # Extract card from PNG
    print("1. Extracting card data from PNG...")
    card = extract_card_data("cards/card.png")

    if not card:
        print("❌ Failed to extract card data")
        return

    print(f"✅ Successfully extracted card: {card.data.name}")

    # Repositorize the card
    print("\n2. Repositorizing card...")
    repo_path = repositorize(card)
    print(f"✅ Card repositorized to: {repo_path}")

    # Rebuild the card to test roundtrip
    print("\n3. Rebuilding card from repository...")
    rebuilt_card = rebuild_card(repo_path)
    print("✅ Card rebuilt successfully")

    # Create new PNG with rebuilt card data
    print("\n5. Creating new PNG with rebuilt data...")
    rebuilt_json = rebuilt_card.model_dump_json(indent=2)

    try:
        embed_card_data(rebuilt_json, "character.png", "cards/rebuilt_card.png")
        print("✅ New PNG created: cards/rebuilt_card.png")
    except Exception as e:
        print(f"❌ Failed to create new PNG: {e}")

    print(f"\n🎉 Workflow completed successfully!")
    print(f"📁 Repository structure: {repo_path}")
    print(f"🖼️  Original PNG: cards/card.png")
    print(f"🖼️  Rebuilt PNG: cards/rebuilt_card.png")


if __name__ == "__main__":
    main()
