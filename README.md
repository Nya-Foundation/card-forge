# Card Forge 🔨

> **[中文版README](README_zh.md) | [English README](README.md)**

**Modern CLI tool for AI character card management** - Extract, repositorize, and rebuild character cards with ease!

```
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
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🚀 Features

- **📤 Extract**: Get character data from PNG files to JSON
- **📁 Repositorize**: Convert cards to version-control friendly file structures  
- **🔨 Rebuild**: Reconstruct cards from repositories
- **✅ Validate**: Check card integrity and specification compliance
- **📊 Analyze**: Get detailed character card information
- **🎨 Modern CLI**: Beautiful interface with helpful commands

## 🔧 Installation

```bash
# Install with uv (recommended)
uv add card-forge

# Or with pip
pip install card-forge
```

## 🎯 Quick Start

```bash
# Extract character data from a PNG file
card-forge extract character.png

# Convert a character card to a repository structure
card-forge repo character.png

# Rebuild a character card from repository
card-forge build my_character/

# Validate a character card
card-forge validate character.png

# Get detailed information about a character
card-forge info character.png

# Generate default configuration file
card-forge init-config

# Show version information
card-forge --version
```

## 📋 Commands

### `extract` - Extract card data to JSON

```bash
card-forge extract card.png                     # Extract to character_name.json
card-forge extract card.png -o mychar.json      # Custom output filename
```

### `repo` - Convert to repository structure

```bash
card-forge repo card.png                        # From PNG file
card-forge repo character.json                  # From JSON file
card-forge repo card.png -c custom_config.yaml  # Custom configuration
```

Creates a clean, organized directory structure:
```
character_name/
├── _metadata.yaml              # Card metadata (spec, version)
└── data/
    ├── _metadata.yaml          # Remaining character data
    ├── description.md          # Character description
    ├── personality.md          # Personality traits
    ├── scenario.md             # Scenario description
    ├── system_prompt.md        # System instructions
    ├── first_message.md        # First message
    ├── example_messages.md     # Example dialogue
    ├── creator_notes.md        # Creator notes
    ├── alternate_greetings/    # Alternative greetings
    │   ├── 1.txt
    │   └── 2.txt
    ├── group_only_greetings/   # Group chat greetings
    │   └── 1.txt
    ├── creator_notes_multilingual/  # Multi-language notes
    │   ├── en.md
    │   └── es.md
    ├── assets/                 # Character assets
    │   ├── main_icon.yaml
    │   └── background_image.yaml
    ├── extensions/             # Extensions and scripts
    │   ├── _metadata.yaml
    │   ├── TavernHelper_scripts/
    │   │   └── script_name.yaml
    │   └── regex_scripts/
    │       └── script_name.yaml
    └── character_book/         # Lorebook entries
        ├── _metadata.yaml
        └── entries/
            ├── 1-location.yaml
            └── 2-character.yaml
```

### `build` - Rebuild from repository

```bash
card-forge build my_character/                  # Rebuild to JSON
card-forge build my_character/ -f png           # Rebuild to PNG
card-forge build my_character/ -o rebuilt       # Custom output name
card-forge build my_character/ -f png -b base.png  # Custom base image
```

### `validate` - Check card integrity

```bash
card-forge validate character.png               # Validate PNG
card-forge validate character.json              # Validate JSON
```

### `info` - Detailed character analysis

```bash
card-forge info character.png                   # Show detailed information
```

### `init-config` - Generate configuration file

```bash
card-forge init-config                          # Generate config.yaml
card-forge init-config -o custom.yaml           # Custom filename
```

Example output:
```
🎭 CHARACTER: Alice Wonderland
================================================================================
👤 Creator: CardMaker
🏷️  Tags: fantasy, adventure, curious
📝 Version: 1.0
🔧 Spec: chara_card_v3 v3.0

📋 CONTENT OVERVIEW:
  • Description: 1,250 characters
  • Personality: 890 characters
  • Scenario: 1,100 characters
  • Alternate greetings: 3
  • Group-only greetings: 1

📚 LOREBOOK:
  • Name: Wonderland Guide
  • Entries: 12
```

## 🛠️ Development Workflow

### 1. Extract and Explore
```bash
# Extract a character card to see its structure
card-forge extract my_card.png
card-forge info my_card.png
```

### 2. Convert to Repository
```bash
# Create editable file structure
card-forge repo my_card.png
```

### 3. Edit Files
Edit the individual files in your favorite editor:
- Modify `description.md` for character description
- Update `personality.md` for personality traits
- Add alternate greetings in `alternate_greetings/`
- Edit lorebook entries in `character_book/entries/`

### 4. Rebuild and Test
```bash
# Rebuild to verify changes
card-forge build my_character/
card-forge validate my_character_rebuilt.json

# Create final PNG
card-forge build my_character/ -f png
```

## 🔄 Use Cases

### Version Control for Character Development
```bash
# Initial setup
card-forge repo character.png
git init character_name
cd character_name
git add .
git commit -m "Initial character import"

# Make changes to files...
git commit -am "Updated personality traits"

# Rebuild for distribution
card-forge build . -f png
```

### Collaborative Character Creation
```bash
# Split work among team members
card-forge repo base_character.png

# Person A works on personality.md
# Person B works on lorebook entries
# Person C works on greetings

# Merge changes and rebuild
card-forge build character/ -f png
```

### Character Analysis and Debugging
```bash
# Quick analysis
card-forge info problematic_card.png

# Deep validation
card-forge validate character.png
card-forge extract character.png
card-forge repo character.json
card-forge build character/
```

## 🎮 Compatibility

- ✅ **SillyTavern**: Full compatibility
- ✅ **RisuAI**: Full compatibility  
- ✅ **Character Card V3**: Complete specification support
- ✅ **Legacy formats**: Backward compatible

## 📦 API Usage

For programmatic use:

```python
from forge.helper import extract_card_data, repositorize, rebuild_card

# Extract character card from PNG
card = extract_card_data("character.png")

# Convert to repository structure  
repo_path = repositorize(card)

# Edit files in the repository...

# Rebuild the card
rebuilt_card = rebuild_card(repo_path)
```

## ⚙️ Configuration

The tool uses `config.yaml` for customization. The default configuration works great for most use cases, but you can customize field handling, file patterns, and repository structure as needed.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch  
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Card Forge** - Making character card management simple, organized, and version-control friendly! 🎭✨