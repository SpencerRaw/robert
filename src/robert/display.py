import json
from .registry import Registry, Agent, HexagonPanel


def format_team_table(registry: Registry) -> str:
    """Format agent registry as a markdown table."""
    agents = registry.list_all()
    if not agents:
        return "No agents in registry."

    dims = agents[0].hexagon.dimensions
    lines = ["| Agent | " + " | ".join(d.title() for d in dims) + " | Load |"]
    lines.append("|" + "---|" * (len(dims) + 2))

    for a in agents:
        scores = [f"{a.hexagon.get(d):.1f}" for d in dims]
        lines.append(f"| {a.name} | {' | '.join(scores)} | {a.load:.0%} |")

    return "\n".join(lines)


def format_dispatch_plan(plan) -> str:
    """Format a dispatch plan for display."""
    return plan.explanation


def robert_says(template: str, **kwargs) -> str:
    """Robert's voice — format a message with his personality."""
    return f"🎮 {template.format(**kwargs)}"
