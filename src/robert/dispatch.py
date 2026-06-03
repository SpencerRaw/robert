"""
Dispatch Engine — match tasks to best agents with scenario-aware scoring.

Robert doesn't just pick the highest stats. He considers:
  - Scenario (different jobs value different dimensions)
  - Load (overworked agents get penalized)
  - Bonds (agents who work well together get a synergy bonus)
"""

from dataclasses import dataclass, field
from typing import Optional
from .registry import Registry, Agent
from .scenarios import get_scenario, Scenario


@dataclass
class SubTask:
    id: str
    description: str
    required_dimensions: list[str] = field(default_factory=list)
    assigned_to: Optional[str] = None
    reason: str = ""


@dataclass
class DispatchPlan:
    tasks: list[SubTask]
    scenario: str = "general"
    explanation: str = ""


def decompose_task(
    task: str,
    registry: Registry,
    scenario_name: str = "",
) -> DispatchPlan:
    """
    Break a complex task into subtasks and assign agents.
    
    Uses scenario-aware scoring: dimensions are weighted per task domain.
    Bond scores between agents provide synergy bonuses.
    """
    task_lower = task.lower()
    scenario = get_scenario(task=task, scenario_name=scenario_name)
    subtasks = _decompose(task_lower)

    # Assign each subtask to best agent
    agents = registry.list_all()
    if not agents:
        return DispatchPlan(
            tasks=subtasks, scenario=scenario.name,
            explanation="No agents registered."
        )

    for st in subtasks:
        best_agent, best_score, reason = _find_best_agent(
            st, agents, registry, scenario
        )
        st.assigned_to = best_agent.id
        st.reason = reason

    # Build explanation
    lines = [
        f"🎮 **Robert's Dispatch** — {scenario.name} scenario",
        f"> *{scenario.robert_intro}*",
        "",
        "📋 **Assignments**:",
    ]
    for st in subtasks:
        agent = registry.get(st.assigned_to or "")
        name = agent.name if agent else "unassigned"
        lines.append(f"- **{st.description}** → {name} ({st.reason})")
    lines.append(
        f"\n*{len(subtasks)} subtasks across "
        f"{len(set(s.assigned_to for s in subtasks))} agents.*"
    )

    return DispatchPlan(
        tasks=subtasks, scenario=scenario.name,
        explanation="\n".join(lines)
    )


def _decompose(task_lower: str) -> list[SubTask]:
    """Break a task description into subtasks (rule-based)."""
    # Research / lit review
    if any(w in task_lower for w in [
        "literature", "review", "search", "survey", "papers",
        "research", "academic", "citation", "bibliography",
    ]):
        return [
            SubTask("1", "Search and collect relevant papers", ["speed", "cost"]),
            SubTask("2", "Read and summarize each paper", ["reasoning", "accuracy"]),
            SubTask("3", "Synthesize findings into narrative", ["creativity", "reasoning"]),
            SubTask("4", "Format with proper citations", ["accuracy", "reliability"]),
            SubTask("5", "Review and quality check", ["reasoning", "accuracy"]),
        ]

    # Writing
    if any(w in task_lower for w in [
        "write", "draft", "paper", "article", "blog", "essay",
        "proposal", "grant", "manuscript", "abstract",
    ]):
        return [
            SubTask("1", "Outline structure and key points", ["creativity", "reasoning"]),
            SubTask("2", "Draft each section", ["creativity", "speed"]),
            SubTask("3", "Polish and refine language", ["accuracy", "reasoning"]),
            SubTask("4", "Format and add references", ["accuracy", "reliability"]),
            SubTask("5", "Final review", ["reasoning", "accuracy"]),
        ]

    # Code
    if any(w in task_lower for w in [
        "code", "implement", "debug", "refactor", "program",
        "pipeline", "deploy", "build", "compile",
    ]):
        return [
            SubTask("1", "Architecture design", ["reasoning", "creativity"]),
            SubTask("2", "Implementation", ["speed", "reasoning"]),
            SubTask("3", "Testing", ["accuracy", "reliability"]),
            SubTask("4", "Documentation", ["reliability", "speed"]),
            SubTask("5", "Code review", ["reasoning", "accuracy"]),
        ]

    # Data analysis
    if any(w in task_lower for w in [
        "analyze", "data", "statistics", "visualize", "chart",
        "graph", "plot", "insight", "metrics", "trend",
    ]):
        return [
            SubTask("1", "Clean and prepare data", ["reliability", "accuracy"]),
            SubTask("2", "Exploratory analysis", ["speed", "creativity"]),
            SubTask("3", "Statistical modeling", ["reasoning", "accuracy"]),
            SubTask("4", "Visualization and reporting", ["creativity", "reliability"]),
            SubTask("5", "Review findings", ["reasoning", "accuracy"]),
        ]

    # Creative / brainstorming
    if any(w in task_lower for w in [
        "brainstorm", "ideate", "design", "name", "brand",
        "creative", "story", "plot", "character",
    ]):
        return [
            SubTask("1", "Generate diverse ideas", ["creativity", "speed"]),
            SubTask("2", "Evaluate and filter concepts", ["reasoning", "accuracy"]),
            SubTask("3", "Develop top ideas", ["creativity", "reasoning"]),
            SubTask("4", "Polish final output", ["accuracy", "reliability"]),
        ]

    # Generic fallback
    return [
        SubTask("1", "Analyze requirements", ["reasoning", "creativity"]),
        SubTask("2", "Execute core work", ["speed", "accuracy"]),
        SubTask("3", "Review and refine", ["reasoning", "accuracy"]),
    ]


def _find_best_agent(
    task: SubTask,
    agents: list["Agent"],
    registry: Registry,
    scenario: Scenario,
) -> tuple["Agent", float, str]:
    """
    Score each agent for this subtask. Factors:
    1. Hexagon dimensions × scenario weights
    2. Load penalty (overworked agents lose efficiency)
    3. Bond synergy (agents with strong bonds work better together)
    """
    best_agent = agents[0]
    best_score = -1.0
    best_reason = ""

    for agent in agents:
        score = 0.0
        reasons = []

        # 1. Dimension scoring with scenario weights
        for dim in task.required_dimensions:
            raw = agent.hexagon.get(dim)
            weight = scenario.weights.get(dim, 1.0)
            weighted = raw * weight
            score += weighted
            if raw >= 8.0:
                reasons.append(f"{dim}={raw:.1f}")

        # 2. Load penalty
        if agent.load > 0.7:
            score *= 0.7
            reasons.append("high load penalty")

        # 3. Bond synergy — check bonds with agents assigned to prior subtasks
        #    Agents who trust each other coordinate better
        bond_bonus = 0.0
        for other_id in set(a.id for a in agents if a.id != agent.id):
            bond = registry.get_bond(agent.id, other_id)
            if bond > 0.6:
                bond_bonus += (bond - 0.5) * 0.1  # small boost
        score += bond_bonus

        if score > best_score:
            best_score = score
            best_agent = agent
            if reasons:
                best_reason = ", ".join(reasons[:2])
            else:
                best_reason = "best overall"

    return best_agent, best_score, best_reason
