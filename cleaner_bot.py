import click
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ── LLM client ────────────────────────────────────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Chain of Thought prompt template ──────────────────────────────────────────
def build_prompt(code: str, language: str) -> str:
    return f"""You are an expert software engineer and code reviewer.
Your task is to refactor the following {language} code step by step.

Follow this reasoning chain before writing any code:

STEP 1 - ANALYZE: Identify all problems in the code:
  - Missing or poor documentation (docstrings, JSDoc, comments)
  - SOLID principle violations
  - Poor naming, magic numbers, or bad structure
  - Any other code smells

STEP 2 - PLAN: For each problem found, describe the specific fix you will apply.

STEP 3 - REFACTOR: Write the fully refactored code that applies every fix.
  - Add comprehensive docstrings or JSDoc to every function and class
  - Apply SOLID principles (Single Responsibility, Open/Closed, etc.)
  - Use clean, descriptive naming
  - Add inline comments where logic is non-obvious

Format your response EXACTLY like this:

## ANALYSIS
<your analysis here>

## PLAN
<your plan here>

## REFACTORED CODE
```{language}
<only the refactored code here, nothing else>
```

Here is the code to refactor:

```{language}
{code}
```
"""

# ── LLM call ──────────────────────────────────────────────────────────────────
def refactor_code(code: str, language: str) -> dict:
    prompt = build_prompt(code, language)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content

    # Parse the three sections out of the response
    def extract_section(text, header, next_header=None):
        start = text.find(f"## {header}")
        if start == -1:
            return ""
        start += len(f"## {header}")
        end = text.find(f"## {next_header}") if next_header else len(text)
        return text[start:end].strip()

    analysis = extract_section(raw, "ANALYSIS", "PLAN")
    plan = extract_section(raw, "PLAN", "REFACTORED CODE")
    refactored_block = extract_section(raw, "REFACTORED CODE")

    # Strip markdown code fences from the refactored code
    lines = refactored_block.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    clean_code = "\n".join(lines).strip()

    return {"analysis": analysis, "plan": plan, "refactored": clean_code}

# ── CLI ───────────────────────────────────────────────────────────────────────
@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file path. Defaults to <input>_clean.<ext>")
@click.option("--language", "-l", default="python", show_default=True,
              help="Programming language of the input file.")
def main(input_file, output, language):
    """Clean Code Bot — refactors messy code into SOLID, documented code."""

    with open(input_file, "r") as f:
        dirty_code = f.read()

    click.echo(f"\n Reading: {input_file}")
    click.echo(f" Language: {language}")
    click.echo(f" Lines: {len(dirty_code.splitlines())}")
    click.echo("\n Sending to AI...\n")

    result = refactor_code(dirty_code, language)

    # Print reasoning to terminal
    click.echo("── ANALYSIS ──────────────────────────────────")
    click.echo(result["analysis"])
    click.echo("\n── PLAN ──────────────────────────────────────")
    click.echo(result["plan"])

    # Save refactored code to output file
    if output is None:
        name, ext = os.path.splitext(input_file)
        output = f"{name}_clean{ext}"

    with open(output, "w") as f:
        f.write(result["refactored"])

    click.echo(f"\n Saved to: {output}")

if __name__ == "__main__":
    main()