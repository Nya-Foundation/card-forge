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

> ⚠️ **Compatibility Notice**: This project is designed primarily for **Character Card V3 Specification (CCV3)** under [https://github.com/kwaroran/character-card-spec-v3](https://github.com/kwaroran/character-card-spec-v3). Legacy versions are technically supported but not guaranteed to work correctly with all features.

## 🚀 Key Features

- **📤 Extract**: Get character data from PNG files to JSON with full CCV3 support
- **📁 Repositorize**: Convert cards to version-control friendly file structures  
- **🔨 Rebuild**: Reconstruct cards from repositories with data integrity validation
- **✅ Validate**: Check card integrity and specification compliance using Pydantic models
- **📊 Analyze**: Get detailed character card information and statistics
- **⚙️ Configurable**: Flexible YAML-based configuration for custom workflows
- **🎨 Modern CLI**: Beautiful interface with helpful commands and clear feedback

## 🔧 Installation

```bash
# Install with uv (recommended)
uv add --dev card-forge

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
```

## 🏗️ Architecture & Data Models

Card Forge is built on robust **Pydantic v2** models that ensure data integrity and type safety throughout the entire workflow. Our models provide:

- **Full CCV3 Compliance**: Complete implementation of Character Card V3 specification
- **Type Safety**: All character data is validated using strongly-typed Pydantic models
- **Data Integrity**: Automatic validation during extraction, repositorization, and rebuilding
- **Extensibility**: Support for custom extensions and application-specific fields

### Core Models

```python
from forge.models import CharacterCardV3, CharacterCardV3Data, Lorebook, LorebookEntry, Asset

# All character cards are represented as validated Pydantic models
card: CharacterCardV3 = extract_card_data("character.png")

# Access typed data with full IDE support and validation
character_name: str = card.data.name
lorebook: Optional[Lorebook] = card.data.character_book
assets: Optional[List[Asset]] = card.data.assets
```

**Model Features:**
- **Automatic Validation**: Invalid data is caught early with clear error messages
- **Type Hints**: Full IDE support with autocompletion and type checking
- **Flexible Fields**: Support for optional fields, defaults, and custom extensions
- **JSON Serialization**: Seamless conversion between Python objects and JSON

## 📋 Command Reference

### Extract Command
```bash
card-forge extract card.png                     # Extract to character_name.json
card-forge extract card.png -o mychar.json      # Custom output filename
```

### Repository Command
```bash
card-forge repo card.png                        # From PNG file
card-forge repo character.json                  # From JSON file
card-forge repo card.png -c custom_config.yaml  # Custom configuration
```

**Repository Structure:**
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
    │   ├── 001.md
    │   └── 002.md
    ├── group_only_greetings/   # Group chat greetings
    │   └── 001.md
    ├── creator_notes_multilingual/  # Multi-language notes
    │   ├── en.md
    │   └── es.md
    ├── assets/                 # Character assets
    │   ├── main_icon.yaml
    │   └── background_image.yaml
    ├── extensions/             # Extensions and scripts
    │   ├── _metadata.yaml
    │   ├── TavernHelper_scripts/
    │   │   └── 001_script_name.yaml
    │   └── regex_scripts/
    │       └── 001_script_name.yaml
    └── character_book/         # Lorebook entries
        ├── _metadata.yaml
        └── entries/
            ├── 001_location.yaml
            └── 002_character.yaml
```

### Build Command
```bash
card-forge build my_character/                  # Rebuild to JSON
card-forge build my_character/ -f png           # Rebuild to PNG
card-forge build my_character/ -o rebuilt       # Custom output name
card-forge build my_character/ -f png -b base.png  # Custom base image
```

### Validation & Analysis
```bash
card-forge validate character.png               # Validate PNG
card-forge validate character.json              # Validate JSON
card-forge info character.png                   # Show detailed information
```

### Configuration
```bash
card-forge init-config                          # Generate config.yaml
card-forge init-config -o custom.yaml           # Custom filename
```

## 🛠️ Development Workflow

**1. Extract and Explore**
```bash
card-forge extract my_card.png
card-forge info my_card.png
```

**2. Convert to Repository**
```bash
card-forge repo my_card.png
```

**3. Edit Files** - Edit individual files in your favorite editor

**4. Rebuild and Test**
```bash
card-forge build my_character/
card-forge validate my_character_rebuilt.json
card-forge build my_character/ -f png
```

## 🔄 Common Use Cases

### Version Control for Character Development
```bash
card-forge repo character.png
git init character_name && cd character_name
git add . && git commit -m "Initial character import"
# Make changes to files...
git commit -am "Updated personality traits"
card-forge build . -f png
```

### Collaborative Character Creation
```bash
card-forge repo base_character.png
# Team members work on different files
# Person A: personality.md, Person B: lorebook entries, Person C: greetings
card-forge build character/ -f png
```

### Character Analysis and Debugging
```bash
card-forge info problematic_card.png
card-forge validate character.png
```

## 📦 API Usage

**Programmatic Access with Pydantic Models:**

```python
from forge.helper import extract_card_data, repositorize, rebuild_card
from forge.models import CharacterCardV3

# Extract character card with full type safety
card: CharacterCardV3 = extract_card_data("character.png")

# Access validated data
print(f"Character: {card.data.name}")
print(f"Creator: {card.data.creator}")
print(f"Lorebook entries: {len(card.data.character_book.entries) if card.data.character_book else 0}")

# Convert to repository structure  
repo_path: str = repositorize(card)

# Edit files in the repository...

# Rebuild with validation
rebuilt_card: CharacterCardV3 = rebuild_card(repo_path)
```

## ⚙️ Configuration System

Card Forge uses a flexible YAML-based configuration system for customizing how character data is organized into files and directories.

### Field Types and Options

```yaml
repositorize:
  fields:
    field_name:
      enabled: true/false          # Whether to process this field
      type: string|array|dict|nested  # How to handle the data
      filename: "custom.md"        # For string types
      file_pattern: "{template}"   # For arrays and dicts
      value_type: string|dict      # Type of values in arrays/dicts
```

### Template Variables

- `{idx}` - Array index (auto-padded with zeros)
- `{value.name}` - Access nested properties with dot notation
- `{value.id}_{value.title}` - Combine multiple properties

### Configuration Examples

**Custom Array Patterns:**
```yaml
alternate_greetings:
  enabled: true
  type: array
  file_pattern: "greeting_{idx}.md"
  value_type: string
```

**Complex Object Arrays:**
```yaml
assets:
  enabled: true
  type: array
  file_pattern: "{name}_{type}.yaml"
  value_type: dict
```

**Multilingual Content:**
```yaml
creator_notes_multilingual:
  enabled: true
  type: dict
  file_pattern: "notes_{key}.md"
  value_type: string
```

## 🎮 Compatibility

- ✅ **SillyTavern**: Full compatibility
- ✅ **RisuAI**: Full compatibility  
- ✅ **Character Card V3**: Complete specification support
- ✅ **Legacy formats**: Backward compatible

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