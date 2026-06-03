# 🎮 Robert — Product Plan

> Last updated: 2026-06-03
> Status: Design + Hermes Skill MVP

---

## 1. Product Thesis

**Multi-agent systems are powerful. But they're cold.**

You can orchestrate 5 different LLMs to tackle a research problem. But who decides which model does what? Who remembers that Claude + GPT-4o paired well last time? Who notices that DeepSeek has been running 6 hours straight and maybe needs a break?

Current orchestration frameworks (mAestro, crewAI, AutoGen) treat agents as interchangeable tools. Robert treats them as **team members.** He knows their strengths, tracks their chemistry, and dispatches with judgment — not just rules.

**The bet**: Teams with a human-like dispatcher perform better than teams with a cold scheduler. Trust and chemistry matter — even between AI agents.

---

## 2. Core Concepts

### The Hexagon Panel

Every agent (AI or human) has a 6-axis radar. This is Robert's understanding of "who can do what."

```json
{
  "id": "claude-sonnet",
  "name": "Claude",
  "type": "ai",
  "provider": "anthropic",
  "hexagon": {
    "reasoning": 9.2,
    "speed": 6.5,
    "creativity": 7.8,
    "accuracy": 9.0,
    "cost": 5.0,
    "reliability": 9.5
  },
  "personality": "thoughtful, thorough, occasionally pedantic",
  "mood": "ready",
  "load": 0.3,
  "bonds": {
    "gpt-4o": 0.72,
    "deepseek": 0.45
  }
}
```

### The Bond Graph

Tracks collaboration history. When two agents work together repeatedly:

- Bond score increases
- Robert starts recommending that pairing
- Task completion quality improves (team XP bonus)

```
Claude ←→ GPT-4o:  0.72  ("They wrote that paper together. Solid.")
GPT-4o ←→ DeepSeek: 0.68  ("Good for batch + creative combo.")
Claude ←→ DeepSeek: 0.45  ("Haven't worked together much.")
```

### Dispatch = Capability × Chemistry × Context

Robert's dispatch decision isn't just "who has the highest reasoning score."

```
Dispatch Score = 
    Capability Match (how well does this agent's hexagon fit the task?)
  × Chemistry Bonus (have they worked with other assigned agents before?)
  × Context Factor (current load, mood, recent performance)
  × Cost Weight (how much does budget matter for this task?)
```

---

## 3. MVP Scope — Phase 1: Hermes Skill

**Robert is a Hermes Agent skill.** It lives in `~/.hermes/skills/robert/`.

### In Scope
- [x] Agent Registry: define agents with hexagon panels
- [x] Task Decomposer: break complex task into subtasks
- [x] Dispatch Engine: match subtasks to best agents
- [x] Execution Log: track outcomes, update bonds
- [x] Robert's Voice: dispatch decisions explained with personality

### Out of Scope (v1)
- [ ] Human team members
- [ ] Real-time mood tracking
- [ ] Multi-project persistence
- [ ] Dashboard UI

### How It Works

```
User: "Write a literature review on carbon dots for cancer therapy"

Robert (skill loaded):
  1. Decompose: [search papers, summarize, synthesize, format, review]
  2. Dispatch:
     - search papers → DeepSeek (cheap, fast, good at bulk)
     - summarize → Claude (accurate, thorough)
     - synthesize → GPT-4o (creative, sees patterns)
     - format → Claude (detail-oriented)
     - review → GPT-4o (fresh eyes)
  3. Execute each with delegate_task
  4. Log outcomes, update bonds
  5. Deliver: assembled literature review + dispatch report
```

---

## 4. Hexagon Dimensions by Scenario

### Scenario: Research Paper
| Dimension | What It Measures |
|-----------|-----------------|
| Literature | Ability to search/synthesize papers |
| Writing | Quality of prose, clarity |
| Critical | Can identify flaws, gaps |
| Formatting | LaTeX, references, figures |
| Speed | Words per minute equivalent |
| Cost | Token cost per task |

### Scenario: Code Review
| Dimension | What It Measures |
|-----------|-----------------|
| Architecture | Can spot structural issues |
| Security | Finds vulnerabilities |
| Readability | Assesses code clarity |
| Testing | Suggests test cases |
| Speed | Review turnaround |
| Diplomacy | Delivers feedback constructively |

### Scenario: Data Analysis
| Dimension | What It Measures |
|-----------|-----------------|
| Stats | Statistical rigor |
| Viz | Visualization quality |
| Coding | pandas/matplotlib fluency |
| Domain | Field-specific knowledge |
| Speed | Analysis turnaround |
| Explanation | Can explain results clearly |

---

## 5. Communication Protocol

Robert speaks in a specific voice. Rules:

1. **Know the team**: reference past work, acknowledge strengths
2. **Explain the why**: not just "Claude does X" but "Claude does X because he's better at reasoning and you need fresh eyes on Y"
3. **Be warm, not robotic**: contractions, humor, occasional sass
4. **Respect autonomy**: "This is my recommendation. Want to override?"
5. **Celebrate**: "That section was 94th percentile. Tell Claude he crushed it."

---

## 6. Phase 2 — Human-in-the-Loop

Add human team members:

```json
{
  "id": "yiwei",
  "name": "Yiwei",
  "type": "human",
  "hexagon": {
    "carbon_dots": 9.0,
    "paper_writing": 7.5,
    "ai_agents": 8.5,
    "availability": 0.4,
    "review_speed": 7.0,
    "decision_quality": 8.5
  },
  "preferences": {
    "working_hours": "9-18 CST",
    "review_method": "comment on draft",
    "max_daily_tasks": 3
  }
}
```

Robert then:
- Checks human availability before assigning
- Sends notifications: "Claude finished the intro. Ready when you are."
- Respects working hours: doesn't ping at 2 AM (unless urgent)

---

## 7. Phase 3 — Standalone Framework

Decouple from Hermes:

```
robert-core/           # Python package
├── robert/
│   ├── registry.py    # Agent Registry
│   ├── hexagon.py     # Hexagon panel logic
│   ├── bonds.py       # Bond graph
│   ├── dispatch.py    # Dispatch engine
│   ├── decompose.py   # Task decomposer
│   └── voice.py       # Robert's communication style
├── api/               # REST API
│   └── server.py
├── dashboard/         # Web UI
│   └── app.py
└── integrations/
    ├── hermes.py      # Hermes integration
    ├── openai.py      # OpenAI agent wrapper
    └── anthropic.py   # Claude agent wrapper
```

---

## 8. Success Metrics (Phase 1)

- **3 agents registered** with hexagon panels
- **1 complex task** decomposed + dispatched across 3 agents
- **Dispatch quality**: user agrees with Robert's choices ≥80% of the time
- **Voice test**: user finds Robert's communication "human-like"

---

## 9. Risks

| Risk | Mitigation |
|------|------------|
| Hexagon scores are subjective | Start with user-assigned scores; later auto-calibrate from outcomes |
| Dispatch feels random | Always explain the WHY; allow overrides |
| Over-engineering bonds | Start with simple cosine similarity of hex profiles + manual pair ratings |
| Robert tries too hard to be funny | Tone slider: "professional ↔ casual ↔ snarky" |

---

*"A good dispatcher doesn't just assign tasks. They build a team." — Robert*
