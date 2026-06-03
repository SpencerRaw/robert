"""
Scenario Profiles — Robert adapts his dispatch weights per task domain.

Robert knows that "good" means different things for different jobs.
Search papers? Speed & cost. Write a grant? Creativity & reasoning.
He switches lenses like a pro dispatcher.
"""

from dataclasses import dataclass, field


@dataclass
class Scenario:
    """A task domain with its own dimension weightings."""
    name: str
    description: str
    # Weight multipliers per dimension (1.0 = normal, 2.0 = double importance)
    weights: dict[str, float] = field(default_factory=dict)
    # Robert's intro when dispatching in this scenario
    robert_intro: str = ""


# ── Built-in scenario profiles ──

SCENARIOS: dict[str, Scenario] = {
    "research": Scenario(
        name="Research",
        description="Literature review, paper survey, academic discovery",
        weights={
            "reasoning": 1.5,
            "speed": 0.8,
            "creativity": 1.0,
            "accuracy": 1.8,
            "cost": 1.3,
            "reliability": 1.5,
        },
        robert_intro="Let's dig through the literature. Accuracy is everything here — one wrong citation and the whole review crumbles.",
    ),
    "writing": Scenario(
        name="Writing",
        description="Drafting papers, articles, blog posts, documentation",
        weights={
            "reasoning": 1.2,
            "speed": 0.7,
            "creativity": 1.8,
            "accuracy": 1.3,
            "cost": 0.8,
            "reliability": 1.2,
        },
        robert_intro="Words matter. I need someone who can craft a narrative, not just spit facts. Creativity leads here.",
    ),
    "coding": Scenario(
        name="Coding",
        description="Implementation, debugging, architecture, code review",
        weights={
            "reasoning": 1.6,
            "speed": 1.0,
            "creativity": 1.2,
            "accuracy": 1.7,
            "cost": 0.8,
            "reliability": 1.5,
        },
        robert_intro="Code doesn't forgive mistakes. Reasoning and accuracy — I'm not sending the joker to fix a production bug.",
    ),
    "creative": Scenario(
        name="Creative",
        description="Brainstorming, ideation, design, naming, storytelling",
        weights={
            "reasoning": 0.8,
            "speed": 0.9,
            "creativity": 2.0,
            "accuracy": 0.6,
            "cost": 1.0,
            "reliability": 0.7,
        },
        robert_intro="Let the ideas fly. I need wild creativity here, not someone who plays it safe. Surprise me.",
    ),
    "data_analysis": Scenario(
        name="Data Analysis",
        description="Statistics, visualization, data cleaning, insights",
        weights={
            "reasoning": 1.3,
            "speed": 1.2,
            "creativity": 0.8,
            "accuracy": 2.0,
            "cost": 1.0,
            "reliability": 1.5,
        },
        robert_intro="Numbers don't lie, but bad analysis does. Pinpoint accuracy. Double-check everything.",
    ),
    "general": Scenario(
        name="General",
        description="Default scenario — balanced weights",
        weights={
            "reasoning": 1.0,
            "speed": 1.0,
            "creativity": 1.0,
            "accuracy": 1.0,
            "cost": 1.0,
            "reliability": 1.0,
        },
        robert_intro="Alright team, standard deployment. Let's see who's ready.",
    ),
}


def detect_scenario(task: str) -> str:
    """Auto-detect the best scenario from task description."""
    t = task.lower()

    research_kw = [
        "literature", "review", "paper", "survey", "research",
        "academic", "citation", "arxiv", "pubmed", "scholar",
        "bibliography", "reference", "manuscript",
    ]
    writing_kw = [
        "write", "draft", "article", "blog", "essay", "story",
        "proposal", "grant", "cover letter", "abstract",
        "press release", "script",
    ]
    coding_kw = [
        "code", "implement", "debug", "refactor", "test",
        "deploy", "api", "function", "class", "module",
        "pipeline", "build", "compile", "commit",
    ]
    creative_kw = [
        "brainstorm", "ideate", "design", "name", "brand",
        "story", "plot", "character", "visual", "logo",
        "tagline", "slogan", "creative",
    ]
    data_kw = [
        "analyze", "data", "statistics", "visualize", "chart",
        "graph", "plot", "insight", "trend", "metrics",
        "dashboard", "sql", "query", "spreadsheet",
    ]

    scores = {
        "research": sum(1 for kw in research_kw if kw in t),
        "writing": sum(1 for kw in writing_kw if kw in t),
        "coding": sum(1 for kw in coding_kw if kw in t),
        "creative": sum(1 for kw in creative_kw if kw in t),
        "data_analysis": sum(1 for kw in data_kw if kw in t),
    }

    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "general"


def get_scenario(task: str = "", scenario_name: str = "") -> Scenario:
    """Get scenario by name or auto-detect from task."""
    if scenario_name and scenario_name in SCENARIOS:
        return SCENARIOS[scenario_name]
    if task:
        return SCENARIOS[detect_scenario(task)]
    return SCENARIOS["general"]
