"""
python -m robert — Robert's command-line dispatch console.

Usage:
    python -m robert dispatch "write a literature review on..."
    python -m robert team                          # Show team hexagon panels
    python -m robert bond claude gpt-4o +0.2       # Grow a bond
    python -m robert save registry.json            # Persist team state
    python -m robert load registry.json            # Restore team state
    python -m robert scenario "brainstorm names"   # Detect scenario for a task
"""

import argparse
import sys
from pathlib import Path

from .registry import Registry
from .dispatch import decompose_task
from .display import format_team_table, robert_says
from .scenarios import detect_scenario, SCENARIOS


def main():
    parser = argparse.ArgumentParser(
        prog="robert",
        description="Robert — AI dispatch agent that builds teams.",
    )
    sub = parser.add_subparsers(dest="command")

    # dispatch
    cmd_d = sub.add_parser("dispatch", help="Dispatch a task to the best agents")
    cmd_d.add_argument("task", nargs="+", help="Task description")
    cmd_d.add_argument("--scenario", "-s", help="Force a scenario")

    # team
    sub.add_parser("team", help="Show the agent roster with hexagon panels")

    # bond
    cmd_b = sub.add_parser("bond", help="Update bond between two agents")
    cmd_b.add_argument("agent_a")
    cmd_b.add_argument("agent_b")
    cmd_b.add_argument("delta", type=float, help="Bond change (-1.0 to +1.0)")

    # save / load
    cmd_s = sub.add_parser("save", help="Save registry to JSON")
    cmd_s.add_argument("path", help="Output path")
    cmd_l = sub.add_parser("load", help="Load registry from JSON")
    cmd_l.add_argument("path", help="Input path")

    # scenario
    cmd_sc = sub.add_parser("scenario", help="Detect scenario for a task")
    cmd_sc.add_argument("task", nargs="+", help="Task description")

    # scenarios list
    sub.add_parser("scenarios", help="List all available scenarios")

    args = parser.parse_args()

    if not args.command:
        # Interactive mode — quick demo
        run_demo()
        return

    reg = Registry()
    reg.load_defaults()

    if args.command == "dispatch":
        task = " ".join(args.task)
        plan = decompose_task(task, reg, scenario_name=args.scenario or "")
        print(plan.explanation)

    elif args.command == "team":
        print("🎮 **Robert's Team**")
        print(format_team_table(reg))
        print(f"\nBonds: {len(reg.bond_graph)} connections tracked")

    elif args.command == "bond":
        reg.update_bond(args.agent_a, args.agent_b, args.delta)
        bond = reg.get_bond(args.agent_a, args.agent_b)
        print(robert_says(
            f"Bond between {args.agent_a} and {args.agent_b} → {bond:.2f} "
            f"({'+' if args.delta > 0 else ''}{args.delta:+.2f})"
        ))

    elif args.command == "save":
        reg.save_json(args.path)
        print(robert_says(f"Team state saved to {args.path}"))

    elif args.command == "load":
        reg.load_json(args.path)
        reg.load_defaults()  # fill gaps
        print(robert_says(f"Team loaded from {args.path} ({len(reg.agents)} agents)"))

    elif args.command == "scenario":
        task = " ".join(args.task)
        name = detect_scenario(task)
        sc = SCENARIOS[name]
        print(f"🎮 Detected: **{sc.name}** — {sc.description}")
        print(f"> *{sc.robert_intro}*")
        print(f"\nWeights: {sc.weights}")

    elif args.command == "scenarios":
        print("🎮 **Robert's Scenario Profiles**:\n")
        for name, sc in SCENARIOS.items():
            print(f"- **{sc.name}** ({name}): {sc.description}")


def run_demo():
    """Quick interactive demo."""
    reg = Registry()
    reg.load_defaults()
    reg.update_bond("claude-sonnet", "gpt-4o", 0.3)
    reg.update_bond("claude-sonnet", "deepseek", 0.1)

    print("🎮 **Robert** — Agent Dispatch Demo")
    print("=" * 50)
    print(format_team_table(reg))

    print(f"\nBonds: Claude↔GPT-4o={reg.get_bond('claude-sonnet','gpt-4o'):.2f}  "
          f"Claude↔DeepSeek={reg.get_bond('claude-sonnet','deepseek'):.2f}")

    test_tasks = [
        "Write a literature review on carbon dots for cancer therapy",
        "Debug the authentication middleware",
        "Brainstorm startup names for an AI agent company",
    ]

    for task in test_tasks:
        print(f"\n{'─' * 50}")
        print(f"📨 Task: {task}")
        plan = decompose_task(task, reg)
        print(plan.explanation)


if __name__ == "__main__":
    main()
