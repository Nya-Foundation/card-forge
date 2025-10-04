from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator


class Asset(BaseModel):
    """Asset object for character card assets like icons, backgrounds, etc."""

    type: str = Field(
        ..., description="Type of asset (icon, background, user_icon, emotion, etc.)"
    )
    uri: str = Field(
        ...,
        description="URI of the asset (HTTP/HTTPS URL, base64 data URL, embedded://, or ccdefault:)",
    )
    name: str = Field(
        ..., description="Name to identify the asset (e.g., 'main' for primary assets)"
    )
    ext: str = Field(
        ...,
        description="File extension in lowercase without dot (e.g., 'png', 'jpeg', 'webp')",
    )


class LorebookEntry(BaseModel):
    """Individual lorebook entry with all V3 fields and optional compatibility fields."""

    # Required fields
    keys: List[str] = Field(
        ..., description="Array of strings to match against for activation"
    )
    content: str = Field(
        ...,
        description="Content to add to prompt when entry matches (may contain decorators)",
    )
    extensions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extensions data for application-specific features",
    )
    enabled: bool = Field(
        default=True, description="Whether this entry can be activated"
    )
    insertion_order: int = Field(
        ...,
        description="Order for inserting into prompt (lower numbers insert earlier)",
    )

    # Optional fields with defaults
    case_sensitive: Optional[bool] = Field(
        default=None, description="Whether key matching is case sensitive"
    )
    use_regex: bool = Field(
        default=False,
        description="Whether to treat keys as regex patterns instead of plain text",
    )
    constant: Optional[bool] = Field(
        default=None,
        description="Whether entry should always match regardless of keys (V3 required field)",
    )

    # Optional compatibility fields
    name: Optional[str] = Field(
        default=None, description="Entry identifier name (AgnAI, Risu compatibility)"
    )
    priority: Optional[int] = Field(
        default=None,
        description="Priority for removal when hitting token budget (AgnAI compatibility)",
    )
    id: Optional[Union[int, str]] = Field(
        default=None, description="Entry identifier (ST, Risu compatibility)"
    )
    comment: Optional[str] = Field(
        default=None, description="Entry comments (ST, Risu compatibility)"
    )

    # Additional V3 fields
    selective: Optional[bool] = Field(
        default=None, description="Whether to use secondary_keys for selective matching"
    )
    secondary_keys: Optional[List[str]] = Field(
        default=None, description="Secondary keys required when selective=True"
    )
    position: Optional[Literal["before_char", "after_char"]] = Field(
        default=None, description="Position relative to character data"
    )


class Lorebook(BaseModel):
    """Lorebook object containing world information entries."""

    # Required field
    entries: List[LorebookEntry] = Field(
        default_factory=list, description="Array of lorebook entries"
    )

    # Optional lorebook-level fields
    name: Optional[str] = Field(default=None, description="Lorebook identifier name")
    description: Optional[str] = Field(
        default=None, description="Lorebook description/comments"
    )
    scan_depth: Optional[int] = Field(
        default=None,
        description="Default number of recent messages to scan for key matches",
    )
    token_budget: Optional[int] = Field(
        default=None, description="Maximum tokens to use for lorebook entries"
    )
    recursive_scanning: Optional[bool] = Field(
        default=None,
        description="Whether to scan lorebook content for additional matches",
    )
    extensions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extensions data for application-specific features",
    )


class CharacterCardV3Data(BaseModel):
    """Data object containing all character information for Character Card V3."""

    # Fields from Character Card V2
    name: str = Field(..., description="Character name")
    description: str = Field(..., description="Character description")
    tags: List[str] = Field(default_factory=list, description="Character tags")
    creator: str = Field(..., description="Creator of the character")
    character_version: str = Field(..., description="Version of the character")
    mes_example: str = Field(..., description="Example messages")
    extensions: Dict[str, Any] = Field(
        default_factory=dict, description="Extensions data"
    )
    system_prompt: str = Field(..., description="System prompt for the character")
    post_history_instructions: str = Field(
        ..., description="Instructions after chat history"
    )
    first_mes: str = Field(..., description="First message from character")
    alternate_greetings: List[str] = Field(
        default_factory=list, description="Alternative greeting messages"
    )
    personality: str = Field(..., description="Character personality description")
    scenario: str = Field(..., description="Character scenario description")

    # Changed fields from Character Card V2
    creator_notes: str = Field(
        default="",
        description="Creator notes (fallback for English if multilingual not present)",
    )
    character_book: Optional[Lorebook] = Field(
        default=None, description="Character-specific lorebook"
    )

    # New fields in Character Card V3
    assets: Optional[List[Asset]] = Field(
        default=None,
        description="Character assets (icons, backgrounds, etc.). If undefined, defaults to main icon with ccdefault: URI",
    )
    nickname: Optional[str] = Field(
        default=None,
        description="Character nickname to replace {{char}}, <char>, and <bot> placeholders",
    )
    creator_notes_multilingual: Optional[Dict[str, str]] = Field(
        default=None,
        description="Multilingual creator notes with ISO 639-1 language codes as keys",
    )
    source: Optional[List[str]] = Field(
        default=None,
        description="Array of IDs or HTTP/HTTPS URLs pointing to the source of the character card",
    )
    group_only_greetings: List[str] = Field(
        default_factory=list,
        description="Additional greetings used only in group chats",
    )
    creation_date: Optional[int] = Field(
        default=None, description="Creation date as Unix timestamp in seconds (UTC)"
    )
    modification_date: Optional[int] = Field(
        default=None,
        description="Last modification date as Unix timestamp in seconds (UTC)",
    )


class CharacterCardV3(BaseModel):
    """Character Card V3 specification model."""

    spec: str = Field(
        default="chara_card_v3",
        description="Specification identifier, must be 'chara_card_v3'",
    )
    spec_version: str = Field(
        default="3.0",
        description="Specification version, must be '3.0' for this version",
    )
    data: CharacterCardV3Data = Field(..., description="Character data object")

    @model_validator(mode="after")
    def validate_spec(self):
        """Validate that spec field is correct."""
        if self.spec != "chara_card_v3":
            raise ValueError("spec field must be 'chara_card_v3'")
        return self
