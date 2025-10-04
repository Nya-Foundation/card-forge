#!/usr/bin/env python3
"""
Card Forge CLI - Modern tool for AI character card management
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

from forge._version import __version__
from forge.constant import DEFAULT_CONFIG
from forge.helper import embed_card_data, extract_card_data, rebuild_card, repositorize


def get_ascii_art():
    """Get ASCII art with version information."""
    return f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗ █████╗ ██████╗ ██████╗     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗║
║  ██╔════╝██╔══██╗██╔══██╗██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝║
║  ██║     ███████║██████╔╝██║  ██║    █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  ║
║  ██║     ██╔══██║██╔══██╗██║  ██║    ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  ║
║  ╚██████╗██║  ██║██║  ██║██████╔╝    ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗║
║   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝║
║                                                                               ║
║                    🔨 AI Character Card Management Tool 🔨                    ║
║                                    v{__version__:<10}                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""


def print_header():
    """Print the ASCII art header."""
    print(get_ascii_art())


def print_success(message: str):
    """Print success message with emoji."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print error message with emoji."""
    print(f"❌ {message}")


def print_info(message: str):
    """Print info message with emoji."""
    print(f"ℹ️  {message}")


def print_warning(message: str):
    """Print warning message with emoji."""
    print(f"⚠️  {message}")


def extract_command(args):
    """Extract character card data from PNG image and save to JSON."""
    print_header()
    print_info(f"Extracting character card from: {args.input}")

    if not os.path.exists(args.input):
        print_error(f"Input file not found: {args.input}")
        return 1

    try:
        card = extract_card_data(args.input)
        if not card:
            print_error("Failed to extract character card data from image")
            return 1

        # Determine output path
        if args.output:
            output_path = args.output
        else:
            # Generate output filename based on character name or input filename
            base_name = card.data.name if card.data.name else Path(args.input).stem
            output_path = f"{base_name}.json"

        # Save to JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(card.model_dump(), f, indent=2, ensure_ascii=False)

        print_success(f"Character card extracted successfully!")
        print_info(f"Character: {card.data.name}")
        print_info(f"Creator: {card.data.creator}")
        print_info(f"Output saved to: {output_path}")

        return 0

    except Exception as e:
        print_error(f"Extraction failed: {e}")
        return 1


def repo_command(args):
    """Convert character card to repository structure."""
    print_header()

    # Determine input source
    if args.input.endswith(".png"):
        print_info(f"Extracting character card from PNG: {args.input}")
        card = extract_card_data(args.input)
        if not card:
            print_error("Failed to extract character card from PNG")
            return 1
    elif args.input.endswith(".json"):
        print_info(f"Loading character card from JSON: {args.input}")
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                card_data = json.load(f)
            from forge.models import CharacterCardV3

            card = CharacterCardV3.model_validate(card_data)
        except Exception as e:
            print_error(f"Failed to load JSON: {e}")
            return 1
    else:
        print_error("Input must be a PNG image or JSON file")
        return 1

    try:
        config_path = args.config if args.config else "config.yaml"
        repo_path = repositorize(card, config_path)

        print_success("Character card repositorized successfully!")
        print_info(f"Character: {card.data.name}")
        print_info(f"Repository created at: {repo_path}")
        print_info("Repository structure:")

        # Show directory structure
        for root, dirs, files in os.walk(repo_path):
            level = root.replace(repo_path, "").count(os.sep)
            indent = " " * 2 * level
            print(f"  {indent}📁 {os.path.basename(root)}/")
            subindent = " " * 2 * (level + 1)
            for file in sorted(files):
                if file.startswith("_"):
                    print(f"  {subindent}⚙️  {file}")
                else:
                    print(f"  {subindent}📄 {file}")

        return 0

    except Exception as e:
        import traceback

        print_error(
            f"Repositorization failed: {e}, traceback: {traceback.format_exc()}"
        )
        return 1


def build_command(args):
    """Rebuild character card from repository structure."""
    print_header()
    print_info(f"Rebuilding character card from repository: {args.repo}")

    if not os.path.exists(args.repo):
        print_error(f"Repository directory not found: {args.repo}")
        return 1

    try:
        config_path = args.config if args.config else "config.yaml"
        card = rebuild_card(args.repo, config_path)

        # Determine output format and path
        if args.output:
            output_path = args.output
        else:
            output_path = f"{card.data.name}_rebuilt"

        if args.format == "json":
            output_file = f"{output_path}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(card.model_dump(), f, indent=2, ensure_ascii=False)

            print_success("Character card rebuilt successfully!")
            print_info(f"Character: {card.data.name}")
            print_info(f"JSON saved to: {output_file}")

        elif args.format == "png":
            legacy_support = args.legacy
            output_file = f"{output_path}.png"
            base_image = args.base_image if args.base_image else "character.png"

            if not os.path.exists(base_image):
                print_error(f"Base image not found: {base_image}")
                return 1

            card_json = card.model_dump_json(indent=2)
            embed_card_data(
                metadata=card_json,
                image_path=base_image,
                output_path=output_file,
                legacy=legacy_support,
            )

            print_success("Character card rebuilt and embedded in PNG!")
            print_info(f"Character: {card.data.name}")
            print_info(f"PNG saved to: {output_file}")

        return 0

    except Exception as e:
        print_error(f"Rebuild failed: {e}")
        return 1


def validate_command(args):
    """Validate character card file."""
    print_header()
    print_info(f"Validating character card: {args.input}")

    try:
        if args.input.endswith(".png"):
            card = extract_card_data(args.input)
            if not card:
                print_error("No valid character card found in PNG")
                return 1
        elif args.input.endswith(".json"):
            with open(args.input, "r", encoding="utf-8") as f:
                card_data = json.load(f)
            from forge.models import CharacterCardV3

            card = CharacterCardV3.model_validate(card_data)
        else:
            print_error("Input must be a PNG image or JSON file")
            return 1

        print_success("Character card is valid!")
        print_info(f"Character: {card.data.name}")
        print_info(f"Creator: {card.data.creator}")
        print_info(f"Spec: {card.spec} v{card.spec_version}")

        # Additional validation info
        data = card.data
        print_info(f"Tags: {', '.join(data.tags) if data.tags else 'None'}")
        print_info(f"Alternate greetings: {len(data.alternate_greetings)}")
        print_info(f"Group greetings: {len(data.group_only_greetings)}")

        if data.character_book and data.character_book.entries:
            print_info(f"Lorebook entries: {len(data.character_book.entries)}")

        if data.assets:
            print_info(f"Assets: {len(data.assets)}")

        return 0

    except Exception as e:
        print_error(f"Validation failed: {e}")
        return 1


def info_command(args):
    """Show detailed information about a character card."""
    print_header()
    print_info(f"Analyzing character card: {args.input}")

    try:
        if args.input.endswith(".png"):
            card = extract_card_data(args.input)
            if not card:
                print_error("No valid character card found in PNG")
                return 1
        elif args.input.endswith(".json"):
            with open(args.input, "r", encoding="utf-8") as f:
                card_data = json.load(f)
            from forge.models import CharacterCardV3

            card = CharacterCardV3.model_validate(card_data)
        else:
            print_error("Input must be a PNG image or JSON file")
            return 1

        data = card.data

        print("=" * 80)
        print(f"🎭 CHARACTER: {data.name}")
        print("=" * 80)
        print(f"👤 Creator: {data.creator}")
        print(f"🏷️  Tags: {', '.join(data.tags) if data.tags else 'None'}")
        print(f"📝 Version: {data.character_version}")
        print(f"🔧 Spec: {card.spec} v{card.spec_version}")

        if data.nickname:
            print(f"📛 Nickname: {data.nickname}")

        if data.creation_date:
            from datetime import datetime

            created = datetime.fromtimestamp(data.creation_date)
            print(f"📅 Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")

        if data.modification_date:
            from datetime import datetime

            modified = datetime.fromtimestamp(data.modification_date)
            print(f"📝 Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n📋 CONTENT OVERVIEW:")
        print(f"  • Description: {len(data.description)} characters")
        print(f"  • Personality: {len(data.personality)} characters")
        print(f"  • Scenario: {len(data.scenario)} characters")
        print(f"  • System prompt: {len(data.system_prompt)} characters")
        print(f"  • Example messages: {len(data.mes_example)} characters")
        print(f"  • First message: {len(data.first_mes)} characters")
        print(f"  • Alternate greetings: {len(data.alternate_greetings)}")
        print(f"  • Group-only greetings: {len(data.group_only_greetings)}")

        if data.character_book and data.character_book.entries:
            book = data.character_book
            print(f"\n📚 LOREBOOK:")
            print(f"  • Name: {book.name or 'Unnamed'}")
            print(f"  • Entries: {len(book.entries)}")
            if book.description:
                print(f"  • Description: {book.description}")
            if book.scan_depth:
                print(f"  • Scan depth: {book.scan_depth}")
            if book.token_budget:
                print(f"  • Token budget: {book.token_budget}")

        if data.assets:
            print(f"\n🖼️  ASSETS ({len(data.assets)}):")
            for asset in data.assets:
                print(f"  • {asset.name} ({asset.type}): {asset.ext}")

        if data.source:
            print(f"\n🔗 SOURCES:")
            for source in data.source:
                print(f"  • {source}")

        return 0

    except Exception as e:
        print_error(f"Analysis failed: {e}")
        return 1


def init_config_command(args):
    """Generate default config.yaml file."""
    config_file = args.output if args.output else "config.yaml"

    try:
        with open(config_file, "w", encoding="utf-8") as f:
            yaml.dump(
                DEFAULT_CONFIG, f, default_flow_style=False, indent=2, sort_keys=False
            )

        print_success(f"Generated: {config_file}")
        return 0

    except Exception as e:
        print_error(f"Failed to generate config: {e}")
        return 1


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description="Card Forge - AI Character Card Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  card-forge extract card.png                     # Extract to JSON
  card-forge extract card.png -o character.json   # Extract with custom output
  card-forge repo card.png                        # Convert PNG to repository
  card-forge repo character.json                  # Convert JSON to repository
  card-forge build my_character/                  # Rebuild from repository to JSON
  card-forge build my_character/ -f png           # Rebuild to PNG
  card-forge validate card.png                    # Validate character card
  card-forge info card.png                        # Show detailed information
  card-forge init-config                          # Generate default config.yaml
        """,
    )

    # Add version argument
    parser.add_argument(
        "--version", action="version", version=f"Card Forge {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Extract command
    extract_parser = subparsers.add_parser(
        "extract", help="Extract character card from PNG to JSON"
    )
    extract_parser.add_argument("input", help="Input PNG file")
    extract_parser.add_argument(
        "-o", "--output", help="Output JSON file (default: based on character name)"
    )
    extract_parser.set_defaults(func=extract_command)

    # Repositorize command
    repo_parser = subparsers.add_parser(
        "repo", help="Convert character card to repository structure"
    )
    repo_parser.add_argument("input", help="Input PNG or JSON file")
    repo_parser.add_argument(
        "-c", "--config", help="Configuration file (default: config.yaml)"
    )
    repo_parser.set_defaults(func=repo_command)

    # Build command
    build_parser = subparsers.add_parser(
        "build", help="Rebuild character card from repository"
    )
    build_parser.add_argument("repo", help="Repository directory")
    build_parser.add_argument(
        "-o", "--output", help="Output file base name (default: character name)"
    )
    build_parser.add_argument(
        "-f",
        "--format",
        choices=["json", "png"],
        default="json",
        help="Output format (default: json)",
    )
    build_parser.add_argument(
        "-b", "--base-image", help="Base image for PNG output (default: character.png)"
    )
    build_parser.add_argument(
        "-c", "--config", help="Configuration file (default: config.yaml)"
    )
    # legacy support for v1, v2 character cards
    build_parser.add_argument(
        "-l",
        "--legacy",
        action="store_true",
        help="Support legacy character cards format, ccv1/ccv2",
    )
    build_parser.set_defaults(func=build_command)

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate character card file"
    )
    validate_parser.add_argument("input", help="Input PNG or JSON file")
    validate_parser.set_defaults(func=validate_command)

    # Info command
    info_parser = subparsers.add_parser(
        "info", help="Show detailed character card information"
    )
    info_parser.add_argument("input", help="Input PNG or JSON file")
    info_parser.set_defaults(func=info_command)

    # Init config command
    init_config_parser = subparsers.add_parser(
        "init-config", help="Generate default config.yaml file"
    )
    init_config_parser.add_argument(
        "-o", "--output", help="Output config file name (default: config.yaml)"
    )
    init_config_parser.set_defaults(func=init_config_command)

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        print_header()
        print_info(
            f"Welcome to Card Forge v{__version__}! Use --help to see available commands."
        )
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print_warning("Operation cancelled by user")
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
