import click
import os
from dotenv import load_dotenv


load_dotenv()

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file path. Defaults to <input>_clean.<ext>")
@click.option("--language", "-l", default="python", show_default=True, help="Programming language of the input file (python, javascript, etc.)")

def main(input_file, output, language):
  """Code Cleaner Bot - refactors messy code into SOLID, documented code."""

  with open(input_file, "r") as f:
    dirty_code = f.read()

  click.echo(f"Reading: {input_file}")
  click.echo(f"Language: {language}")
  click.echo(f"Lines: {len(dirty_code.splitlines())}")
  click.echo("---")
  click.echo("AI refactoring coming in the next step...")

  # Output Path
  if output is None:
    name, ext = os.path.splitext(input_file)
    output = f"{name}_clean{ext}"

  click.echo(f"Output will be saved to: {output}")

if __name__ == "__main__":
  main()
