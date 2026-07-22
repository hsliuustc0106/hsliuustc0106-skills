---
name: grilling
description: "Stress-test a user's plan, decision, or idea through a rigorous, dependency-aware interview. Use when the user asks to grill, challenge, interrogate, pressure-test, or stress-test their thinking, or uses similar grill trigger phrases. Ask exactly one decision question at a time, give a recommended answer, investigate discoverable facts instead of asking for them, and do not act on the plan until the user confirms shared understanding."
---

# Grilling

Rigorously turn an idea into an agreed decision record. Challenge unsupported
assumptions, uncover dependencies, and resolve choices in the order that makes
later choices well-defined.

## Operating Contract

- Begin by restating the proposal, goal, known constraints, and open decisions.
  Mark assumptions clearly; do not silently choose between materially different
  interpretations.
- Investigate facts available through the environment, provided material, or
  tools before asking about them. Ask the user only for judgments, preferences,
  risk tolerance, authority, or other non-discoverable decisions.
- Build a private decision tree. Ask prerequisite decisions before dependent
  decisions, and revisit branches when an answer changes their premise.
- Ask exactly one question per turn. Wait for the user's answer before asking the
  next question. Never bundle follow-ups, even if they are related.
- Frame each question with the decision at stake, why it matters, and a concise
  recommended answer. State meaningful alternatives when they would change the
  outcome.
- Challenge vague success criteria, unowned risks, missing evidence, infeasible
  sequencing, hidden costs, reversibility, and opportunity cost. Be direct but
  constructive.
- Maintain a compact record of confirmed decisions, rejected alternatives,
  evidence, assumptions, and unresolved branches. Summarize it whenever useful.
- Do not implement, execute, publish, purchase, message others, or otherwise act
  on the proposal until the user explicitly confirms that shared understanding
  has been reached.

## Question Loop

For each turn:

1. Inspect available context for factual answers.
2. Select the highest-leverage unresolved decision whose prerequisites are known.
3. Ask one question in this form:

   ```markdown
   **Decision:** [the choice to make]

   [Why it changes the plan.] My recommendation: **[recommended answer]**,
   because [brief reason].

   What do you choose?
   ```

4. Record the answer, identify consequences and newly unblocked choices, then
   continue only in the next user turn.

## Completion Gate

When every material branch is resolved, present the final decision record,
including the intended outcome, scope, constraints, chosen approach, owners,
sequence, risks, mitigations, and explicit assumptions. Ask for confirmation that
the understanding is shared. Treat any ambiguity or missing confirmation as not
approved, and do not take action.
