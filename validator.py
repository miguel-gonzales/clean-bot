import os
import re

# ── Constants ─────────────────────────────────────────────────────────────────
MAX_FILE_SIZE_KB = 50
ALLOWED_EXTENSIONS = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rb"}

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?prior\s+instructions",
    r"you\s+are\s+now\s+a",
    r"act\s+as\s+(a\s+)?(?!.*function)",
    r"forget\s+(all\s+)?previous",
    r"new\s+instruction[s]?:",
    r"system\s*prompt",
    r"<\s*script\s*>",
    r"eval\s*\(",
    r"exec\s*\(",
]

# ── Validators ────────────────────────────────────────────────────────────────
def validate_extension(filepath: str) -> None:
    """Check the file extension is in the allowed set."""
    _, ext = os.path.splitext(filepath)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'.\n"
            f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )


def validate_file_size(filepath: str) -> None:
    """Reject files larger than MAX_FILE_SIZE_KB to avoid huge LLM payloads."""
    size_kb = os.path.getsize(filepath) / 1024
    if size_kb > MAX_FILE_SIZE_KB:
        raise ValueError(
            f"File is too large ({size_kb:.1f} KB). "
            f"Maximum allowed is {MAX_FILE_SIZE_KB} KB."
        )


def validate_not_empty(code: str) -> None:
    """Reject blank or whitespace-only files."""
    if not code.strip():
        raise ValueError("Input file is empty. Nothing to refactor.")


def validate_no_injection(code: str) -> None:
    """
    Scan the code content for prompt injection patterns.
    Attackers may embed instructions inside comments or strings
    to manipulate the LLM's behavior.
    """
    lowered = code.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            raise ValueError(
                f"Potential prompt injection detected (pattern: '{pattern}').\n"
                "Refusing to process this file."
            )


def sanitize_code(code: str) -> str:
    """
    Lightweight sanitization — strips null bytes and normalizes
    line endings without altering the actual code logic.
    """
    code = code.replace("\x00", "")
    code = code.replace("\r\n", "\n").replace("\r", "\n")
    return code


def validate_and_sanitize(filepath: str) -> str:
    """
    Master validation function. Runs all checks and returns
    sanitized code if everything passes.
    """
    validate_extension(filepath)
    validate_file_size(filepath)

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    validate_not_empty(code)
    validate_no_injection(code)
    code = sanitize_code(code)

    return code