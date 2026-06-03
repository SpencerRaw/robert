"""Agent Registry — hexagon panels for every agent Robert manages."""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class HexagonPanel:
    """Six-axis capability radar for an agent. Dimensions vary by scenario."""
    dimensions: list[str] = field(default_factory=lambda: [
        "reasoning", "speed", "creativity", "accuracy", "cost", "reliability"
    ])
    scores: dict[str, float] = field(default_factory=dict)

    def get(self, dim: str) -> float:
        return self.scores.get(dim, 5.0)

    def to_dict(self) -> dict:
        return {"dimensions": self.dimensions, "scores": self.scores}


@dataclass
class Agent:
    id: str
    name: str
    type: str  # "ai" or "human"
    provider: str = ""
    hexagon: HexagonPanel = field(default_factory=HexagonPanel)
    personality: str = ""
    mood: str = "ready"
    load: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["hexagon"] = self.hexagon.to_dict()
        return d


# Default agent registry
DEFAULT_AGENTS = [
    Agent(
        id="claude-sonnet",
        name="Claude",
        type="ai",
        provider="anthropic",
        hexagon=HexagonPanel(
            scores={"reasoning": 9.2, "speed": 6.5, "creativity": 7.8, "accuracy": 9.0, "cost": 5.0, "reliability": 9.5},
        ),
        personality="thoughtful, thorough, occasionally pedantic",
    ),
    Agent(
        id="gpt-4o",
        name="GPT-4o",
        type="ai",
        provider="openai",
        hexagon=HexagonPanel(
            scores={"reasoning": 8.5, "speed": 7.5, "creativity": 9.0, "accuracy": 8.0, "cost": 4.0, "reliability": 8.5},
        ),
        personality="creative, fast, sometimes too verbose",
    ),
    Agent(
        id="deepseek",
        name="DeepSeek",
        type="ai",
        provider="deepseek",
        hexagon=HexagonPanel(
            scores={"reasoning": 7.0, "speed": 9.0, "creativity": 6.5, "accuracy": 7.5, "cost": 9.0, "reliability": 8.0},
        ),
        personality="efficient, fast, no-nonsense",
    ),
]


class Registry:
    """Manages Robert's agent roster."""

    def __init__(self):
        self.agents: dict[str, Agent] = {}
        self.bond_graph: dict[str, dict[str, float]] = {}

    def add(self, agent: Agent):
        self.agents[agent.id] = agent

    def get(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def list_all(self) -> list[Agent]:
        return list(self.agents.values())

    def update_hexagon(self, agent_id: str, dimension: str, score: float):
        agent = self.agents.get(agent_id)
        if agent:
            agent.hexagon.scores[dimension] = score

    def update_bond(self, a_id: str, b_id: str, delta: float):
        """Update bond score between two agents."""
        key = tuple(sorted([a_id, b_id]))
        current = self.bond_graph.get(key[0], {}).get(key[1], 0.5)
        new_score = min(1.0, max(0.0, current + delta))
        self.bond_graph.setdefault(key[0], {})[key[1]] = new_score

    def get_bond(self, a_id: str, b_id: str) -> float:
        key = tuple(sorted([a_id, b_id]))
        return self.bond_graph.get(key[0], {}).get(key[1], 0.5)

    def load_defaults(self):
        for agent in DEFAULT_AGENTS:
            self.add(agent)
