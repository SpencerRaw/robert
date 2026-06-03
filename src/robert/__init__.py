"""
Robert — AI dispatch agent that builds teams.

Knows every agent's hexagon panel, tracks bonds between them,
and dispatches tasks with personality. From the game Dispatch.

    from robert import Registry, decompose_task
    
    reg = Registry()
    reg.load_defaults()
    
    plan = decompose_task("Write a paper on carbon dots", reg)
    print(plan.explanation)
"""

from .registry import Registry, Agent, HexagonPanel, DEFAULT_AGENTS
from .dispatch import decompose_task, DispatchPlan, SubTask
from .scenarios import get_scenario, detect_scenario, SCENARIOS, Scenario
from .display import format_team_table, format_dispatch_plan, robert_says

__all__ = [
    "Registry", "Agent", "HexagonPanel", "DEFAULT_AGENTS",
    "decompose_task", "DispatchPlan", "SubTask",
    "get_scenario", "detect_scenario", "SCENARIOS", "Scenario",
    "format_team_table", "format_dispatch_plan", "robert_says",
]
