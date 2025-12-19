"""String Utility Functions - Safe string operations to prevent NoneType errors"""


def safe_lower(text) -> str:
    """
    Safely convert text to lowercase, handling None and non-string types

    Args:
        text: Any type of input

    Returns:
        Lowercase string, or empty string if input is None/invalid
    """
    try:
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        return text.lower()
    except Exception as e:
        print(f"⚠️ Warning: safe_lower failed on {type(text)}: {e}")
        return ""


def safe_strip(text) -> str:
    """
    Safely strip whitespace from text

    Args:
        text: Any type of input

    Returns:
        Stripped string, or empty string if input is None/invalid
    """
    try:
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        return text.strip()
    except Exception as e:
        print(f"⚠️ Warning: safe_strip failed on {type(text)}: {e}")
        return ""


def safe_str(text) -> str:
    """
    Safely convert any type to string

    Args:
        text: Any type of input

    Returns:
        String representation, or empty string if None
    """
    try:
        if text is None:
            return ""
        return str(text)
    except Exception as e:
        print(f"⚠️ Warning: safe_str failed on {type(text)}: {e}")
        return ""
