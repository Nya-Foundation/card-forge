# Default configuration following simplified structure
DEFAULT_CONFIG = {
    "repositorize": {
        "enabled": True,
        "type": "nested",
        "fields": {
            "description": {
                "enabled": True,
                "type": "string",
                "filename": "description.md",
            },
            "personality": {
                "enabled": True,
                "type": "string",
                "filename": "personality.md",
            },
            "scenario": {"enabled": True, "type": "string", "filename": "scenario.md"},
            "system_prompt": {
                "enabled": True,
                "type": "string",
                "filename": "system_prompt.md",
            },
            "post_history_instructions": {
                "enabled": True,
                "type": "string",
                "filename": "post_history_instructions.md",
            },
            "first_mes": {
                "enabled": True,
                "type": "string",
                "filename": "first_message.md",
            },
            "mes_example": {
                "enabled": True,
                "type": "string",
                "filename": "example_messages.md",
            },
            "creator_notes": {
                "enabled": True,
                "type": "string",
                "filename": "creator_notes.md",
            },
            "alternate_greetings": {
                "enabled": True,
                "type": "array",
                "file_pattern": "{idx}.md",
                "value_type": "string",
            },
            "group_only_greetings": {
                "enabled": True,
                "type": "array",
                "file_pattern": "{idx}.md",
                "value_type": "string",
            },
            "tags": {"enabled": False, "type": "array", "value_type": "string"},
            "source": {"enabled": False, "type": "array", "value_type": "string"},
            "assets": {
                "enabled": True,
                "type": "array",
                "file_pattern": "{name}_{type}.yaml",
                "value_type": "dict",
            },
            "creator_notes_multilingual": {
                "enabled": True,
                "type": "dict",
                "file_pattern": "{key}.md",
                "value_type": "string",
            },
            "extensions": {
                "enabled": True,
                "type": "nested",
                "fields": {
                    "TavernHelper_scripts": {
                        "enabled": True,
                        "type": "array",
                        "file_pattern": "{idx}_{value.name}.yaml",
                        "value_type": "dict",
                    },
                    "regex_scripts": {
                        "enabled": True,
                        "type": "array",
                        "file_pattern": "{idx}_{scriptName}.yaml",
                        "value_type": "dict",
                    },
                },
            },
            "character_book": {
                "enabled": True,
                "type": "nested",
                "fields": {
                    "entries": {
                        "enabled": True,
                        "type": "array",
                        "file_pattern": "{insertion_order}_{comment}.yaml",
                        "value_type": "dict",
                    },
                },
            },
        },
    }
}
