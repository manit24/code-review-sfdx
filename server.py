import os
import httpx
from mcp.server.fastmcp import FastMCP
from typing import Optional, List
import re
 
# ── Load .env manually ────────────────────────────────────
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
 
# ── Config ────────────────────────────────────────────────
mcp = FastMCP(name="Code Review Server")
 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get(
    "OPENAI_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
)
MODEL = os.environ.get("OPENAI_MODEL", "models/gemini-2.5-flash")
 
 
# ── LLM Helper ────────────────────────────────────────────
async def call_llm(prompt: str) -> str:
    """Call the LLM with a prompt and return the response text."""
    if not OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY is not set. Add it to your .env file."
 
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert code reviewer. "
                    "Provide structured, actionable feedback. "
                    "Format: Summary, Issues (numbered), Recommendations."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
 
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                BASE_URL, headers=headers, json=payload, timeout=120.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"HTTP Error {e.response.status_code}: {e.response.text}"
    except httpx.TimeoutException:
        return "Error: Request timed out. Please try again."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
 
 
# ── Tool 1: Review a code snippet ─────────────────────────
@mcp.tool()
async def review_code(
    code: str,
    language: str = "python",
    context: Optional[str] = None,
) -> str:
    """
    Review a code snippet for quality, bugs, security issues, and best practices.
 
    Args:
        code: The source code to review
        language: Programming language (python, apex, javascript, etc.)
        context: Optional context about what the code is supposed to do
    """
    context_section = f"\nContext: {context}" if context else ""
    prompt = (
        f"Review this {language} code:{context_section}\n\n"
        f"```{language}\n{code}\n```\n\n"
        "Check for:\n"
        "1. Bugs and logical errors\n"
        "2. Security vulnerabilities\n"
        "3. Performance issues\n"
        "4. Code style and best practices\n"
        "5. Missing error handling\n"
        "6. Naming conventions\n"
        "Be specific with line references where possible."
    )
    return await call_llm(prompt)
 
 
# ── Tool 2: Review a file from disk ──────────────────────
@mcp.tool()
async def review_file(file_path: str, language: Optional[str] = None) -> str:
    """
    Read a source file from disk and review it.
 
    Args:
        file_path: Absolute or relative path to the file
        language: Language hint (auto-detected from extension if not provided)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        return f"Error: File not found at path: {file_path}"
    except PermissionError:
        return f"Error: Permission denied reading file: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
 
    if not language:
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".cls": "apex",
            ".trigger": "apex",
            ".html": "html",
            ".css": "css",
            ".java": "java",
            ".json": "json",
            ".xml": "xml",
        }
        ext = "." + file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
        language = ext_map.get(ext, "text")
 
    return await review_code(code=code, language=language)
 
 
# ── Tool 3: Explain code ─────────────────────────────────
@mcp.tool()
async def explain_code(
    code: str,
    language: str = "python",
    audience: str = "developer",
) -> str:
    """
    Explain what a piece of code does in plain language.
 
    Args:
        code: The source code to explain
        language: Programming language
        audience: Target audience - developer, junior, or non-technical
    """
    prompt = (
        f"Explain this {language} code for a {audience} audience:\n\n"
        f"```{language}\n{code}\n```\n\n"
        "Include:\n"
        "1. What the code does overall (1-2 sentences)\n"
        "2. Step-by-step breakdown of the logic\n"
        "3. Any important patterns or concepts used"
    )
    return await call_llm(prompt)
 
 
# ─────────────────────────────────────────────────────────
# 🔰 Workshop Exercise: Non‑LLM Tool (safe, deterministic)
# ─────────────────────────────────────────────────────────
 
def parse_apex_methods(code: str) -> List[dict]:
    """
    Very simple Apex method parser using regex.
    Not perfect, but good enough for a workshop.
    """
    lines = code.split("\n")
    pattern = re.compile(
        r"(?:(public|private|protected|global|testMethod|static|virtual|override)\s+)*"
        r"(void|[A-Z][A-Za-z0-9_]*)\s+([a-zA-Z0-9_]+)\s*\("  # return type + name
    )
 
    methods: List[dict] = []
    for i, line in enumerate(lines, start=1):
        m = pattern.search(line.strip())
        if m:
            visibility = m.group(1) or "default"
            returns = m.group(2)
            name = m.group(3)
            methods.append(
                {
                    "name": name,
                    "visibility": visibility,
                    "returns": returns,
                    "line": i,
                }
            )
    return methods
 
 
@mcp.tool()
async def list_apex_methods(file_path: str) -> str:
    """
    List methods in an Apex class file.
 
    Args:
        file_path: Path to a .cls or .trigger file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        return f"Error: File not found at path: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"
 
    methods = parse_apex_methods(code)
    if not methods:
        return "No methods detected in this file."
 
    # Format as markdown table (nice in Inspector / Slingshot)
    lines = [
        "| Method | Visibility | Returns | Line |",
        "|--------|-----------|---------|------|",
    ]
    for m in methods:
        lines.append(
            f"| {m['name']} | {m['visibility']} | {m['returns']} | {m['line']} |"
        )
    return "\n".join(lines)
 
# ─────────────────────────────────────────────────────────
# ⚠️ Advanced tools (not for today’s walkthrough)
# - suggest_refactor
# - generate_tests
# - review_large_apex_file (chunking, logging, quota handling)
# Keep them in another file or branch for reference.
# ─────────────────────────────────────────────────────────
 
# Entry point
if __name__ == "__main__":
    import sys
    if "--stdio" in sys.argv:
        mcp.run(transport="stdio")
    else:
        mcp.run(transport="streamable-http")

