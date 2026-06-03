> 🌐 [中文文档](README.zh-CN.md) | **English**

# 🎮 Robert — The Dispatch Agent

> *"You're not a team because you work together. You're a team because you trust each other."*

**Robert** is an AI orchestration layer that dispatches tasks across different models and humans — with personality. He knows every agent's strengths, tracks team chemistry, and makes the call on who does what. Not a cold scheduler. A dispatcher who builds bonds.

Named after Robert from the game *Dispatch* — the handler who turned a team of ex-supervillains into actual heroes.

```
                  ┌──────────────────┐
                  │     ROBERT       │
                  │  "I know my team"│
                  └────────┬─────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   ┌─────────┐       ┌─────────┐       ┌─────────┐
   │ Claude  │       │ GPT-4o  │       │ DeepSeek│
   │ (深思)  │       │ (创意)  │       │ (批量)  │
   └─────────┘       └─────────┘       └─────────┘
   推理 S-tier        创意 S-tier        性价比 S-tier
   速度 B-tier        成本 C-tier        速度 A-tier
```

---

## What Robert Does

| Feature | What It Means |
|---------|---------------|
| **Hexagon Panels** | Every agent has a 6-axis radar: reasoning, speed, creativity, accuracy, cost, reliability. Scenario-adaptable. |
| **Bond Graph** | Tracks who's worked with whom. Recommends pairings that have chemistry. |
| **Smart Dispatch** | Task in → Robert picks the best agent(s). Considers: capability match, current load, growth opportunity, cost. |
| **Human Touch** | Robert remembers your last task. Asks if you're tired. Celebrates wins. Sometimes sasses you. |
| **Team Building** | Over time, agents get better at collaborating. Robert tracks "team XP." |

---

## The Hexagon Panel

Each agent gets a 6-axis radar. Dimensions change per scenario:

**Default (General)**: Reasoning · Speed · Creativity · Accuracy · Cost · Reliability

**Scenario: Paper Writing**: Literature · Writing · Critical Thinking · Formatting · Citation · Speed

**Scenario: Code**: Architecture · Debugging · Speed · Documentation · Testing · Creativity

Robert adapts the radar to *what matters for this job.*

---

## Architecture

```
┌────────────────────────────────────────────────────┐
│                    ROBERT                          │
│                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │  Agent   │  │   Bond   │  │    Dispatch      │ │
│  │ Registry │  │  Graph   │  │    Engine        │ │
│  │          │  │          │  │                  │ │
│  │ Claude   │  │ A+B: 0.9 │  │ Task → Decompose │ │
│  │ GPT-4o   │  │ A+C: 0.4 │  │ → Match → Assign │ │
│  │ DeepSeek │  │ B+C: 0.7 │  │ → Execute → Rate │ │
│  └──────────┘  └──────────┘  └──────────────────┘ │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │              Robert's Voice                  │ │
│  │  "Claude handles the deep reasoning.         │ │
│  │   DeepSeek runs the batch analysis.          │ │
│  │   You? You review the results and decide."   │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

---

## MVP — Phase 1 (Hermes Skill)

Robert as a Hermes Agent skill that orchestrates other skills and agents.

| Module | Function |
|--------|----------|
| **Agent Registry** | Define agents with hexagon panels (editable) |
| **Task Decomposer** | Break "write a paper" into [lit review, draft, format, review] |
| **Dispatch Engine** | Match subtasks to best agents |
| **Execution Log** | Track who did what, how well, bond changes |

### Phase 2 — Human-in-the-loop
- Add human team members with editable hexagons
- Robert checks in: "Ready to review Section 3? Claude's been working on it."

### Phase 3 — Standalone Framework
- Decouple from Hermes
- REST API + dashboard
- Multi-project, team persistence

---

## Robert's Voice

Robert is not a robot. Examples:

> 🎮 *"Claude's been staring at this abstract for 3 hours. I'm sending it to GPT-4o for a fresh pair of eyes. Claude, take a walk."*

> 🎮 *"Last time you two collaborated on the results section, it was fire. Let's run that pairing again."*

> 🎮 *"DeepSeek can handle this batch analysis in its sleep. Save Claude for the hard stuff."*

---

## Inspiration

- **Dispatch** (game) — Robert, the handler who builds a hero team from broken people
- **Polsia** — AI that runs your company 24/7
- **mAestro** — Multi-agent orchestration framework
- **Hermes Agent** — The platform Robert rides on

---

## License

MIT
