"""
Tests for Robert — the dispatch agent.
Run: PYTHONPATH=src python3 -m pytest tests/ -v
"""

import pytest
from robert import (
    Registry, Agent, HexagonPanel,
    decompose_task, DispatchPlan, SubTask,
    detect_scenario, get_scenario, SCENARIOS,
    format_team_table, robert_says,
)


# ── Registry ──

def test_registry_add_and_get():
    reg = Registry()
    agent = Agent(id="test", name="Test", type="ai")
    reg.add(agent)
    assert reg.get("test") is agent
    assert reg.get("nonexistent") is None


def test_registry_list_all():
    reg = Registry()
    reg.load_defaults()
    agents = reg.list_all()
    assert len(agents) == 6  # Claude, GPT-4o, DeepSeek, Gemini, Qwen, Grok


def test_hexagon_update():
    reg = Registry()
    reg.load_defaults()
    reg.update_hexagon("claude-sonnet", "speed", 7.0)
    assert reg.get("claude-sonnet").hexagon.get("speed") == 7.0


def test_bond_tracking():
    reg = Registry()
    reg.load_defaults()
    reg.update_bond("claude-sonnet", "gpt-4o", 0.3)
    bond = reg.get_bond("claude-sonnet", "gpt-4o")
    assert 0.79 < bond < 0.81  # 0.5 base + 0.3 delta


def test_bond_clamped():
    reg = Registry()
    reg.load_defaults()
    reg.update_bond("claude-sonnet", "gpt-4o", 10.0)
    assert reg.get_bond("claude-sonnet", "gpt-4o") == 1.0


# ── Persistence ──

def test_save_load_roundtrip(tmp_path):
    reg = Registry()
    reg.load_defaults()
    reg.update_bond("claude-sonnet", "deepseek", 0.2)
    
    path = tmp_path / "roster.json"
    reg.save_json(str(path))
    
    reg2 = Registry()
    reg2.load_json(str(path))
    assert len(reg2.list_all()) == 6
    assert reg2.get("deepseek") is not None
    assert reg2.get_bond("claude-sonnet", "deepseek") > 0.65


# ── Scenarios ──

def test_detect_research_scenario():
    assert detect_scenario("write a literature review on quantum dots") == "research"
    assert detect_scenario("search arxiv papers about protein folding") == "research"


def test_detect_coding_scenario():
    assert detect_scenario("debug the authentication middleware") == "coding"
    assert detect_scenario("implement a REST API pipeline") == "coding"


def test_detect_creative_scenario():
    assert detect_scenario("brainstorm names for a startup") == "creative"


def test_detect_data_scenario():
    assert detect_scenario("analyze the dataset for trends") == "data_analysis"


def test_detect_writing_scenario():
    assert detect_scenario("draft a grant proposal about AI safety") == "writing"


def test_detect_general_fallback():
    assert detect_scenario("do something random") == "general"


def test_all_scenarios_in_registry():
    assert len(SCENARIOS) == 6
    for name in ["research", "writing", "coding", "creative", "data_analysis", "general"]:
        assert name in SCENARIOS


def test_scenario_weights_sum():
    sc = SCENARIOS["general"]
    assert sc.weights["reasoning"] == 1.0


# ── Dispatch ──

def test_dispatch_produces_plan():
    reg = Registry()
    reg.load_defaults()
    plan = decompose_task("Write a paper on carbon dots for cancer therapy", reg)
    assert isinstance(plan, DispatchPlan)
    assert len(plan.tasks) > 0
    assert plan.scenario == "Research"
    for st in plan.tasks:
        assert st.assigned_to is not None
        assert st.reason


def test_dispatch_empty_registry():
    reg = Registry()
    plan = decompose_task("Do something", reg)
    assert "No agents registered" in plan.explanation


def test_dispatch_scenario_override():
    reg = Registry()
    reg.load_defaults()
    plan = decompose_task("debug something", reg, scenario_name="creative")
    assert plan.scenario == "Creative"


# ── Display ──

def test_format_team_table():
    reg = Registry()
    reg.load_defaults()
    table = format_team_table(reg)
    assert "Claude" in table
    assert "GPT-4o" in table
    assert "9.2" in table  # Claude reasoning


def test_robert_says():
    msg = robert_says("Dispatch complete")
    assert msg == "🎮 Dispatch complete"


# ── Hexagon Panel ──

def test_hexagon_default():
    h = HexagonPanel()
    assert h.get("reasoning") == 5.0
    assert h.get("nonexistent") == 5.0


def test_hexagon_custom():
    h = HexagonPanel(scores={"speed": 9.0, "cost": 2.0})
    assert h.get("speed") == 9.0
    assert h.get("cost") == 2.0
