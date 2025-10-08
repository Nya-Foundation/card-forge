import base64
import os
import re
from typing import Any, Dict, Optional, Union

import yaml
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from forge.constant import DEFAULT_CONFIG
from forge.models import CharacterCardV3

StrOrBytesPath = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file with fallback to defaults.

    Simple is better than complex.

    Args:
        config_path: Path to the configuration file

    Returns:
        Configuration dictionary with merged defaults

    Raises:
        None - errors are handled gracefully with fallback to defaults
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}

            # Merge with defaults - flat is better than nested
            result = DEFAULT_CONFIG.copy()
            if "repositorize" in config and "fields" in config["repositorize"]:
                result["repositorize"]["fields"].update(
                    config["repositorize"]["fields"]
                )

            return result
        else:
            return DEFAULT_CONFIG
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return DEFAULT_CONFIG


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.

    Although practicality beats purity.

    Args:
        name: The string to sanitize

    Returns:
        Sanitized filename safe for filesystem use

    Notes:
        Replaces illegal filename characters with underscores and
        removes leading/trailing problematic characters.
    """
    if not name:
        return "unnamed"

    # Illegal characters for filenames on most OSes
    illegal_chars = r"[\/\\\?\%\*\:\|\"\<\>\.]"
    sanitized = re.sub(illegal_chars, "_", name)
    sanitized = sanitized.strip(" _.")

    return sanitized or "unnamed"


def embed_card_data(
    metadata: str,
    image_path: StrOrBytesPath,
    output_path: StrOrBytesPath,
    legacy: bool = False,
) -> None:
    """
    Embed character card metadata into PNG image file.

    Explicit is better than implicit.

    Args:
        metadata: JSON string containing character card data
        image_path: Path to the source PNG image
        output_path: Path where the image with embedded data should be saved
        legacy: If True, add legacy support for v1, v2 cards via 'chara' text chunk

    Raises:
        FileNotFoundError: If source image doesn't exist
        IOError: If image processing fails
    """
    try:

        # Open the image
        image = Image.open(image_path)

        # Create PNG info object for text chunks
        png_info = PngInfo()

        # Encode the text content with base64
        encoded_data = base64.b64encode(metadata.encode("utf-8")).decode("utf-8")

        # Add data to PNG text chunks under the key 'ccv3'
        png_info.add_text("ccv3", encoded_data)

        # Optionally add legacy support under 'chara' key
        if legacy:
            png_info.add_text("chara", encoded_data)

        # Save the image with text chunk data
        image.save(output_path, pnginfo=png_info)

        print(f"Successfully embedded {len(metadata)} characters into '{output_path}'")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error: {e}")


def extract_card_data(
    image_path: StrOrBytesPath,
) -> CharacterCardV3 | None:
    """
    Extract character card data from PNG image file.

    In the face of ambiguity, refuse the temptation to guess.

    Args:
        image_path: Path to the PNG image containing embedded character data

    Returns:
        CharacterCardV3 instance if successful, None if extraction fails

    Notes:
        Looks for base64-encoded JSON data in PNG text chunks under 'ccv3' key
    """
    try:
        image = Image.open(image_path)
        # Get text chunks from PNG
        if hasattr(image, "text"):
            if "ccv3" in image.text:
                embedded_data = image.text["ccv3"]
            elif "chara" in image.text:
                embedded_data = image.text["chara"]
            else:
                print("No embedded text found in image text chunks")
                return None

            decoded_text = base64.b64decode(embedded_data).decode("utf-8")
            card = CharacterCardV3.model_validate_json(decoded_text)
            return card
        else:
            print("No embedded text found in image text chunks")
            return None

    except Exception as e:
        print(f"Error extracting data: {e}")
        return None


def ensure_dir(path: str):
    dirname = os.path.dirname(path)
    if not dirname:
        return
    os.makedirs(dirname, exist_ok=True)


class LiteralDumper(yaml.SafeDumper):
    pass


def str_presenter(dumper, data: str):
    data = re.sub(r"\s+\n", "\n", data)  # Normalize newlines
    # Use block style for multiline strings or long strings
    if "\n" in data or len(data) > 256:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


LiteralDumper.add_representer(str, str_presenter)


def yaml_safe_dump(data, path):
    ensure_dir(path)
    with open(path, "w") as f:
        yaml.dump(
            data,
            f,
            indent=2,
            Dumper=LiteralDumper,
            sort_keys=False,
            allow_unicode=True,
            width=float("inf"),
        )


def safe_file_write(content: str, path: str):
    ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _extract_filename_from_pattern(pattern: str, item: Any) -> str:
    """
    Extract filename from pattern using item fields with dot notation support.

    Args:
        pattern: File pattern with placeholders (supports dot notation like {value.name})
        item: Item to extract values from

    Returns:
        Generated filename
    """
    try:
        # Use a custom formatter that handles dot notation
        return _format_with_dot_notation(pattern, item)
    except Exception as e:
        print(
            f"Warning: Could not extract filename from pattern '{pattern}' with item {item}. Error: {e}"
        )
        return None


def _format_with_dot_notation(pattern: str, data: dict) -> str:
    """
    Format a string pattern with dot notation support.

    Args:
        pattern: Pattern string with placeholders like {value.name}
        data: Dictionary to extract values from

    Returns:
        Formatted string with values substituted
    """
    import re

    def replace_placeholder(match):
        placeholder = match.group(1)  # Get the content inside {}

        if "." in placeholder:
            # Handle dot notation
            keys = placeholder.split(".")
            value = data
            try:
                for key in keys:
                    value = value[key]
                return sanitize_filename(str(value))
            except (KeyError, TypeError):
                raise KeyError(f"Could not find '{placeholder}' in data")
        else:
            # Handle direct key access
            try:
                return sanitize_filename(str(data[placeholder]))
            except KeyError:
                raise KeyError(f"Could not find '{placeholder}' in data")

    # Find all placeholders like {key} or {key.subkey}
    return re.sub(r"\{([^}]+)\}", replace_placeholder, pattern)


def write_value(value: Any, file_path: str, value_type: str = "string") -> None:
    """
    Write a value to a file based on its type.

    There should be one obvious way to do it.

    Args:
        value: Value to write
        file_path: Full path to the file
        value_type: Type of value (string, dict)
    """
    if value_type == "string":
        safe_file_write(str(value), file_path)
    else:  # dict, list, or any other type
        yaml_safe_dump(value, file_path)


def read_value(file_path: str, value_type: str = "string") -> Any:
    """
    Read a value from a file based on its type.

    Args:
        file_path: Full path to the file
        value_type: Type of value (string, dict)

    Returns:
        Loaded value or appropriate default
    """
    if not os.path.exists(file_path):
        return "" if value_type == "string" else {}

    with open(file_path, "r", encoding="utf-8") as f:
        if value_type == "string":
            return f.read()
        else:  # dict, list, or any other type
            return yaml.safe_load(f) or {}


def dump_string_field(content: str, path: str, filename: str) -> None:
    """
    Dump string content to a file.

    Explicit is better than implicit.

    Args:
        content: String content to write
        path: Directory path where file should be created
        filename: Name of the file to create
    """
    if not content:
        return
    full_path = os.path.join(path, filename)
    write_value(content, full_path, "string")


def dump_array_field(
    items: list, config: Dict[str, Any], path: str, field_name: str
) -> None:
    """
    Dump array items based on configuration.

    There should be one obvious way to do it.

    Args:
        items: List of items to dump
        config: Field configuration dictionary
        path: Base directory path
        field_name: Name of the field (used as directory name)
    """
    if not items:
        return

    # Directory name is always the field name
    full_path = os.path.join(path, field_name)
    value_type = config.get("value_type", "string")
    zfill_length = min(len(items), 3)

    # Handle different array patterns
    if "file_pattern" in config:
        pattern: str = config["file_pattern"]

        for idx, item in enumerate(items):
            filename = pattern

            # Handle index pattern with {idx}, with zero-padding
            if "{idx}" in pattern:
                filename = pattern.replace("{idx}", str(idx + 1).zfill(zfill_length))

            # Handle complex patterns, dot notation from item fields
            if isinstance(item, dict):
                filename = (
                    _extract_filename_from_pattern(filename, item) or f"{idx + 1}.md"
                )

            file_path = os.path.join(full_path, filename)
            write_value(item, file_path, value_type)
    else:
        # Default pattern for arrays without explicit pattern
        for idx, item in enumerate(items):
            filename = f"{idx + 1}.md"
            file_path = os.path.join(full_path, filename)
            write_value(item, file_path, value_type)


def dump_dict_field(
    data: Dict[str, Any], config: Dict[str, Any], path: str, field_name: str
) -> None:
    """
    Dump dictionary data based on configuration.

    Readability counts.

    Args:
        data: Dictionary data to dump
        config: Field configuration dictionary
        path: Base directory path
        field_name: Name of the field (used as directory name)
    """
    if not data:
        return

    # Directory name is always the field name
    full_path = os.path.join(path, field_name)
    value_type = config.get("value_type", "string")

    # Handle pattern-based dictionaries (like multilingual fields)
    if "file_pattern" in config:
        pattern = config["file_pattern"]

        for key, value in data.items():
            filename = pattern.format(key=key)
            file_path = os.path.join(full_path, filename)
            write_value(value, file_path, value_type)
    else:
        # Store as metadata for non-pattern dicts
        yaml_safe_dump(data, os.path.join(full_path, "_metadata.yaml"))


def dump_nested_field(
    data: Dict[str, Any], config: Dict[str, Any], path: str, field_name: str
) -> None:
    """
    Dump nested field data based on configuration.

    Flat is better than nested, but sometimes nested is necessary.

    Args:
        data: Dictionary data to dump
        config: Field configuration dictionary
        path: Base directory path
        field_name: Name of the field (used as directory name)
    """
    if not data:
        return

    full_path = os.path.join(path, field_name)
    fields_config = config.get("fields", {})
    modified_data = data.copy()

    # Process each nested field
    for sub_field_name, sub_field_config in fields_config.items():
        if not sub_field_config.get("enabled", False):
            continue

        if sub_field_name not in modified_data:
            continue

        sub_field_data = modified_data.pop(sub_field_name)
        if not sub_field_data:
            continue

        sub_field_type = sub_field_config.get("type", "string")

        # Handle nested field based on its type
        if sub_field_type == "array":
            dump_array_field(
                sub_field_data, sub_field_config, full_path, sub_field_name
            )
            modified_data[sub_field_name] = os.path.join(full_path, sub_field_name)
        elif sub_field_type == "dict":
            dump_dict_field(sub_field_data, sub_field_config, full_path, sub_field_name)
            modified_data[sub_field_name] = os.path.join(full_path, sub_field_name)
        elif sub_field_type == "string":
            filename = sub_field_config.get("filename", f"{sub_field_name}.md")
            dump_string_field(sub_field_data, full_path, filename)
            modified_data[sub_field_name] = os.path.join(full_path, filename)

    # Store remaining metadata
    if modified_data:
        yaml_safe_dump(modified_data, os.path.join(full_path, "_metadata.yaml"))


# Legacy functions removed - all functionality is now configuration-driven


def repositorize(card: CharacterCardV3, config_path: str = "config.yaml") -> str:
    """
    Convert a CharacterCardV3 instance to a repository-friendly folder structure.

    Beautiful is better than ugly.
    In the face of ambiguity, refuse the temptation to guess.

    Args:
        card: The character card instance to convert
        config_path: Path to configuration file

    Returns:
        Path to the created repository structure

    Raises:
        ValueError: If card data is invalid
    """
    if not card or not card.data:
        raise ValueError("Invalid character card data")

    config = load_config(config_path)
    fields_config = config["repositorize"]["fields"]

    base_path = sanitize_filename(card.data.name)
    metadata = card.model_dump()
    data_path = os.path.join(base_path, "data")

    # Separate card structure from data
    data = metadata.pop("data")
    metadata["data"] = data_path
    yaml_safe_dump(metadata, os.path.join(base_path, "_metadata.yaml"))

    # Process each configured field based on its type
    for field_name, field_config in fields_config.items():
        if not field_config.get("enabled", False):
            continue

        if field_name not in data:
            continue

        field_data = data.pop(field_name, None)
        if not field_data:
            data[field_name] = field_data
            continue

        field_type = field_config.get("type", "string")

        # Handle field based on type using unified handler
        _handle_field(field_data, field_type, field_config, data_path, field_name, data)

    yaml_safe_dump(data, os.path.join(data_path, "_metadata.yaml"))
    return base_path


def _handle_field(
    field_data: Any,
    field_type: str,
    config: Dict[str, Any],
    base_path: str,
    field_name: str,
    data: Dict[str, Any],
) -> None:
    """
    Handle field repositorization based on type.

    Simple is better than complex.

    Args:
        field_data: The data to repositorize
        field_type: Type of field (string, array, dict, nested)
        config: Field configuration
        base_path: Base directory path
        field_name: Name of the field
        data: Parent data dictionary to update
    """
    if not field_data:
        # Keep empty data as-is in metadata
        data[field_name] = field_data
        return

    # Only process non-empty data
    if field_type == "string":
        filename = config.get("filename", f"{field_name}.md")
        dump_string_field(field_data, base_path, filename)
        data[field_name] = os.path.join(base_path, filename)
    elif field_type == "array":
        dump_array_field(field_data, config, base_path, field_name)
        data[field_name] = os.path.join(base_path, field_name)
    elif field_type == "dict":
        dump_dict_field(field_data, config, base_path, field_name)
        data[field_name] = os.path.join(base_path, field_name)
    elif field_type == "nested":
        dump_nested_field(field_data, config, base_path, field_name)
        data[field_name] = os.path.join(base_path, field_name)
    else:
        # Unknown type - keep as-is
        data[field_name] = field_data


def load_string_field(path: str, filename: str) -> Optional[str]:
    """
    Load string content from a file.

    Errors should never pass silently.

    Args:
        path: Directory path containing the file
        filename: Name of the file to load

    Returns:
        File content as string or None if file doesn't exist
    """
    full_path = os.path.join(path, filename)
    content = read_value(full_path, "string")
    return content if content else None


def load_array_field(config: Dict[str, Any], path: str, field_name: str) -> list:
    """
    Load array data based on configuration.

    Sparse is better than dense.

    Args:
        config: Field configuration dictionary
        path: Base directory path
        field_name: Name of the field (directory name)

    Returns:
        List of loaded items
    """
    full_path = os.path.join(path, field_name)

    if not os.path.exists(full_path):
        return []

    items = []
    value_type = config.get("value_type", "string")

    # Load all matching files keeping the original order
    for filename in sorted(os.listdir(full_path)):
        file_path = os.path.join(full_path, filename)
        item = read_value(file_path, value_type)
        if item or value_type == "string":  # Include empty strings
            items.append(item)

    return items


def load_dict_field(
    config: Dict[str, Any], path: str, field_name: str
) -> Dict[str, Any]:
    """
    Load dictionary data based on configuration.

    Special cases aren't special enough to break the rules.

    Args:
        config: Field configuration dictionary
        path: Base directory path
        field_name: Name of the field (directory name)

    Returns:
        Dictionary of loaded data
    """
    full_path = os.path.join(path, field_name)

    if not os.path.exists(full_path):
        return {}

    result = {}
    value_type = config.get("value_type", "string")

    # Handle pattern-based dictionaries
    if "file_pattern" in config:
        pattern = config["file_pattern"]

        for filename in os.listdir(full_path):
            if filename != "_metadata.yaml":
                # Extract key from filename based on pattern
                if pattern.endswith(".md") and filename.endswith(".md"):
                    key = filename[:-3]  # Remove .md extension
                elif pattern.endswith(".yaml") and filename.endswith(".yaml"):
                    key = filename[:-5]  # Remove .yaml extension
                else:
                    # Try to extract key by removing the extension
                    key = os.path.splitext(filename)[0]

                file_path = os.path.join(full_path, filename)
                result[key] = read_value(file_path, value_type)
    else:
        # Load from metadata file for non-pattern dicts
        metadata_path = os.path.join(full_path, "_metadata.yaml")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                result = yaml.safe_load(f) or {}

    return result


def load_nested_field(
    config: Dict[str, Any], path: str, field_name: str
) -> Dict[str, Any]:
    """
    Load nested field data based on configuration.

    Args:
        config: Field configuration dictionary
        path: Base directory path
        field_name: Name of the field (directory name)

    Returns:
        Dictionary of loaded nested data
    """
    full_path = os.path.join(path, field_name)

    if not os.path.exists(full_path):
        return {}

    # Load metadata first
    result = {}
    metadata_path = os.path.join(full_path, "_metadata.yaml")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            result = yaml.safe_load(f) or {}

    # Process nested fields
    fields_config = config.get("fields", {})
    for sub_field_name, sub_field_config in fields_config.items():
        if not sub_field_config.get("enabled", False):
            continue

        sub_field_type = sub_field_config.get("type", "string")

        # Check if this field was repositorized (path reference)
        if sub_field_name in result and isinstance(result[sub_field_name], str):
            if result[sub_field_name].startswith(full_path):
                # Load the actual data
                if sub_field_type == "array":
                    result[sub_field_name] = load_array_field(
                        sub_field_config, full_path, sub_field_name
                    )
                elif sub_field_type == "dict":
                    result[sub_field_name] = load_dict_field(
                        sub_field_config, full_path, sub_field_name
                    )
                elif sub_field_type == "string":
                    filename = sub_field_config.get("filename", f"{sub_field_name}.md")
                    result[sub_field_name] = load_string_field(full_path, filename)

    return result


def rebuild_card(base_path: str, config_path: str = "config.yaml") -> CharacterCardV3:
    """
    Rebuild a CharacterCardV3 from repository structure.

    Practicality beats purity.
    Although that way may not be obvious at first unless you're Dutch.

    Args:
        base_path: Path to the repository structure
        config_path: Path to configuration file

    Returns:
        Reconstructed CharacterCardV3 instance

    Raises:
        FileNotFoundError: If required metadata files are missing
        ValueError: If card validation fails
    """
    config = load_config(config_path)
    fields_config = config["repositorize"]["fields"]

    # Load main metadata
    main_metadata_path = os.path.join(base_path, "_metadata.yaml")
    if not os.path.exists(main_metadata_path):
        raise FileNotFoundError(f"Main metadata file not found: {main_metadata_path}")

    with open(main_metadata_path, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)

    # Load data metadata
    data_path = os.path.join(base_path, "data")
    data_metadata_path = os.path.join(data_path, "_metadata.yaml")

    if not os.path.exists(data_metadata_path):
        raise FileNotFoundError(f"Data metadata file not found: {data_metadata_path}")

    with open(data_metadata_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Rebuild each configured field based on its type
    for field_name, field_config in fields_config.items():
        if not field_config.get("enabled", False):
            continue

        if field_name not in data:
            continue

        # Check if this field was repositorized (path reference)
        if not isinstance(data[field_name], str) or not data[field_name].startswith(
            data_path
        ):
            continue

        field_type = field_config.get("type", "string")

        # Dispatch to appropriate loader based on type
        if field_type == "string":
            filename = field_config.get("filename", f"{field_name}.md")
            content = load_string_field(data_path, filename)
            if content is not None:
                data[field_name] = content
        elif field_type == "array":
            items = load_array_field(field_config, data_path, field_name)
            data[field_name] = items
        elif field_type == "dict":
            dict_data = load_dict_field(field_config, data_path, field_name)
            data[field_name] = dict_data
        elif field_type == "nested":
            nested_data = load_nested_field(field_config, data_path, field_name)
            data[field_name] = nested_data

    # Reconstruct the full card
    metadata["data"] = data

    try:
        return CharacterCardV3.model_validate(metadata)
    except Exception as e:
        raise ValueError(f"Card validation failed: {e}") from e
