from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def print_banner(text):
    """Prints a styled banner."""
    console.print(Panel(Text(text, justify="center", style="bold green"), style="bold green"))

def print_user_msg(msg):
    """Prints user message style (if needed for logs, mostly shell handles input)."""
    console.print(f"[bold cyan]USER:[/bold cyan] {msg}")

def print_ai_msg(msg):
    """Prints AI message without code blocks (handled separately usually, or mixed)."""
    console.print(f"[bold magenta]AI:[/bold magenta] {msg}")

def print_code_box(code, language="python", title="Code Snippet"):
    """
    Renders a code snippet in a bordered box with syntax highlighting.
    """
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    panel = Panel(syntax, title=title, border_style="green", padding=(1, 2))
    console.print(panel)

def print_error(msg):
    console.print(f"[bold red]ERROR:[/bold red] {msg}")

def print_success(msg):
    console.print(f"[bold green]SUCCESS:[/bold green] {msg}")

def print_info(msg):
    console.print(f"[bold blue]INFO:[/bold blue] {msg}")

def print_warning(msg):
    console.print(f"[bold yellow]WARNING:[/bold yellow] {msg}")

def print_markdown(content):
    """Renders markdown content."""
    md = Markdown(content)
    console.print(md)
