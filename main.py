"""
Entry point.

Usage:
    python main.py
    python main.py "Which cities have the most seller locations?"
"""

import sys
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

load_dotenv()

console = Console()


def main():
    question = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Which product categories have the most sellers, and what are the top 3?"
    )

    console.print()
    console.print(Rule("[bold white]Agentic Analytics System[/]", style="white"))
    console.print(Panel(
        f"[bold white]{question}[/]",
        title="[bold cyan]❓ Question[/]",
        border_style="cyan",
        padding=(1, 2),
    ))

    # Build Chroma schema index if not already built
    console.print("\n[dim]Building schema index (skips if already done)...[/]")
    from agent.schema_rag import build_index
    build_index()

    # Build and run the graph
    from agent.graph import build_graph

    console.print("[dim]Compiling LangGraph...[/]")
    app = build_graph()

    initial_state = {
        "question":        question,
        "logic_sentences": [],
        "current_idx":     0,
        "temp_files":      [],
        "current_sql":     "",
        "step_results":    [],
        "ra_retries":      0,
        "cod_retries":     0,
        "error":           None,
        "final_answer":    None,
    }

    start = time.time()
    console.print("\n[dim]Running agent pipeline...[/]\n")

    final_state = app.invoke(initial_state)

    elapsed = time.time() - start
    console.print(f"\n[dim]Total time: {elapsed:.1f}s[/]")
    console.print(Rule(style="white"))

    if not final_state.get("final_answer"):
        console.print("[red bold]Pipeline did not produce a final answer.[/]")
        if final_state.get("error"):
            console.print(f"[red]Last error: {final_state['error']}[/]")
        sys.exit(1)


if __name__ == "__main__":
    main()
