"""Dispatch Engine — match tasks to best agents."""

from dataclasses import dataclass, field
from typing import Optional
from .registry import Registry, Agent


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
    explanation: str = ""


def decompose_task(task: str, registry: Registry) -> DispatchPlan:
    """
    Break a complex task into subtasks and assign agents.
    
    This is a rule-based decomposer for MVP. Future versions will use LLM.
    """
    task_lower = task.lower()
    subtasks = []

    # Research / lit review tasks
    if any(w in task_lower for w in ["literature", "review", "search", "survey", "papers"]):
        subtasks = [
            SubTask("1", "Search and collect relevant papers", ["speed", "cost"]),
            SubTask("2", "Read and summarize each paper", ["reasoning", "accuracy"]),
            SubTask("3", "Synthesize findings into narrative", ["creativity", "reasoning"]),
            SubTask("4", "Format with proper citations", ["accuracy", "reliability"]),
            SubTask("5", "Review and quality check", ["reasoning", "accuracy"]),
        ]

    # Writing tasks
    elif any(w in task_lower for w in ["write", "draft", "paper", "article"]):
        subtasks = [
            SubTask("1", "Outline structure and key points", ["creativity", "reasoning"]),
            SubTask("2", "Draft each section", ["writing", "speed"] if "writing" in task_lower else ["creativity", "speed"]),
            SubTask("3", "Polish and refine language", ["accuracy", "reasoning"]),
            SubTask("4", "Format and add references", ["accuracy", "reliability"]),
            SubTask("5", "Final review", ["reasoning", "accuracy"]),
        ]

    # Code tasks
    elif any(w in task_lower for w in ["code", "implement", "debug", "program"]):
        subtasks = [
            SubTask("1", "Architecture design", ["reasoning", "creativity"]),
            SubTask("2", "Implementation", ["speed", "reasoning"]),
            SubTask("3", "Testing", ["accuracy", "reliability"]),
            SubTask("4", "Documentation", ["reliability", "speed"]),
            SubTask("5", "Code review", ["reasoning", "accuracy"]),
        ]

    # Generic
    else:
        subtasks = [
            SubTask("1", "Analyze requirements", ["reasoning", "creativity"]),
            SubTask("2", "Execute core work", ["speed", "accuracy"]),
            SubTask("3", "Review and refine", ["reasoning", "accuracy"]),
        ]

    # Assign each subtask to best agent
    agents = registry.list_all()
    if not agents:
        return DispatchPlan(tasks=subtasks, explanation="No agents registered.")

    for st in subtasks:
        best_agent, best_score, reason = _find_best_agent(st, agents, registry)
        st.assigned_to = best_agent.id
        st.reason = reason

    # Build explanation
    lines = ["📋 **Dispatch Plan**:\n"]
    for st in subtasks:
        agent = registry.get(st.assigned_to)
        lines.append(f"- **{st.description}** → {agent.name} ({st.reason})")
    lines.append(f"\n*{len(subtasks)} subtasks assigned across {len(set(s.assigned_to for s in subtasks))} agents.*")

    return DispatchPlan(tasks=subtasks, explanation="\n".join(lines))


def _find_best_agent(task: SubTask, agents: list[Agent], registry: Registry) -> tuple[Agent, float, str]:
    """Score each agent for this subtask and return the best."""
    best_agent = agents[0]
    best_score = 0.0
    best_reason = ""

    for agent in agents:
        score = 0.0
        reasons = []

        for dim in task.required_dimensions:
            s = agent.hexagon.get(dim)
            score += s
            if s >= 8.0:
                reasons.append(f"{dim}={s:.1f}")

        # Penalty for high load
        if agent.load > 0.7:
            score *= 0.7
            reasons.append("high load penalty")

        if score > best_score:
            best_score = score
            best_agent = agent
            best_reason = ", ".join(reasons[:2]) if reasons else "best overall"

    return best_agent, best_score, best_reason
