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
    │   ├── 001.md
    │   └── 0012.md
    ├── group_only_greetings/   # Group chat greetings
    │   └── 0011.md
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

### 🛠️ Customizing Repositorization Behavior

Card Forge uses a flexible configuration system that lets you control exactly how character data gets organized into files and directories. Here's how to customize it:

#### Field Types and Options

Each field in your character card can be configured with different types and behaviors:

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

#### Template Variables

Card Forge supports powerful template variables for dynamic file naming:

**Basic Variables:**
- `{idx}` - Array index (auto-padded with zeros)
- `{key}` - Dictionary key name

**Dot Notation (for complex data):**
- `{value.name}` - Access nested properties
- `{value.id}_{value.title}` - Combine multiple properties

#### Configuration Examples

**1. Custom Array Patterns**
```yaml
# Default: alternate_greetings/001.md, 002.md, 003.md
alternate_greetings:
  enabled: true
  type: array
  file_pattern: "greeting_{idx}.md"
  value_type: string

# Result: alternate_greetings/greeting_001.md, greeting_002.md
```

**2. Complex Object Arrays**
```yaml
# For arrays of objects like assets or scripts
assets:
  enabled: true
  type: array
  file_pattern: "{name}_{type}.yaml"  # Uses object properties
  value_type: dict

# Result: assets/portrait_icon.yaml, background_image.yaml
```

**3. Multilingual Content**
```yaml
# Dictionary with language codes as keys
creator_notes_multilingual:
  enabled: true
  type: dict
  file_pattern: "notes_{key}.md"  # key = language code
  value_type: string

# Result: creator_notes_multilingual/notes_en.md, notes_es.md
```

**4. Nested Field Configuration**
```yaml
extensions:
  enabled: true
  type: nested
  fields:
    regex_scripts:
      enabled: true
      type: array
      file_pattern: "{idx}_{scriptName}.yaml"  # Uses script's name property
      value_type: dict
```

**5. Disabling Fields**
```yaml
# Keep some fields in metadata instead of separate files
tags:
  enabled: false  # Will remain in _metadata.yaml
  type: array
  value_type: string

source:
  enabled: false  # Keep URLs in metadata for easier management
  type: array
  value_type: string
```

#### Custom Configuration Workflow

1. **Generate default config:**
   ```bash
   card-forge init-config -o my_config.yaml
   ```

2. **Customize field handling:**
   ```yaml
   # Example: Change how greetings are organized
   alternate_greetings:
     enabled: true
     type: array
     file_pattern: "alt_greeting_{idx}.txt"
     value_type: string
   ```

3. **Use custom config:**
   ```bash
   card-forge repo character.png -c my_config.yaml
   card-forge build character/ -c my_config.yaml
   ```

#### Advanced Examples

**Organize scripts by functionality:**
```yaml
extensions:
  enabled: true
  type: nested
  fields:
    regex_scripts:
      enabled: true
      type: array
      file_pattern: "{idx}_{scriptName}_{id}.yaml"
      value_type: dict
```

**Lorebook entries with meaningful names:**
```yaml
character_book:
  enabled: true
  type: nested
  fields:
    entries:
      enabled: true
      type: array
      file_pattern: "{id}_{comment}.yaml"  # Uses entry ID and comment
      value_type: dict
```

**Custom string field organization:**
```yaml
# Group all text content in a 'content' subdirectory
description:
  enabled: true
  type: string
  filename: "content/character_description.md"

personality:
  enabled: true
  type: string
  filename: "content/personality_traits.md"
```

The configuration system is designed to be intuitive yet powerful - you can keep the defaults for quick workflows, or customize everything for complex projects with specific organization needs.

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