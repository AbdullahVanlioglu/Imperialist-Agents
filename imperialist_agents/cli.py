import asyncio
import typer
from rich.console import Console
from imperialist_agents.run_demo import run_task


app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def demo(goal: str):
    """Run a single-shot demo task with the configured runtime."""
    console.rule("[bold cyan]Manus‑style Agent Demo")
    asyncio.run(run_task(goal))