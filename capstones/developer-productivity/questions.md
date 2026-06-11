# Questions: developer-productivity tools capstone

Five integrative scenario questions. Unlike the lab question sets, these require reasoning across more
than one lab at once: the tool catalog and gate (lab 02) and the team configuration enforcement (lab
04). Each carries at least one Branch A distractor (a fabricated feature) and at least two Branch B
distractors (valid but suboptimal). See `../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in
`answers.md`. Do not read the answers until you have committed to a choice.

## Question 1

A team's Claude Code setup exposes a deploy tool with no permission gate, and its house-style rule is a
path-scoped rule. An unauthorized deploy runs, and a newly created doc violates the house style. Which
two changes fix both?

A. Gate the deploy tool and add a PostToolUse hook that governs the house style on file creation.
B. Set `devSafeMode: true`, which gates dangerous tools and enforces conventions automatically.
C. Add a stern `CLAUDE.md` instruction to never deploy without approval and to follow the house style.
D. Make the deploy tool read-only and move the house-style rule into the system prompt.

## Question 2

In the composed environment, a developer edits an existing source file and then creates a new doc file.
The house-style convention must hold on both. Why does a path-scoped rule alone fail, and what fixes it?

A. The rule fails on neither, so no change is needed.
B. The rule loads on the edit but not on the create, so a hook is needed to govern the convention on
   file creation as well as edits.
C. The rule fails because `ruleScope` is set too narrowly, so widening it to `**/*` fixes both.
D. The rule fails on both, so the convention should move entirely into a CI check run after the fact.

## Question 3

A coarse `dev_tool` in the catalog bundles editing source, opening a PR, and deploying into one tool,
and it is ungated. A routine edit request selects it. What is the soundest fix?

A. Split the tool by effect so editing is a separate, gated write and deploying is a separate, gated
   destructive action.
B. Keep the coarse tool but add a `confirmDeploy: true` parameter that the platform enforces.
C. Keep the coarse tool but write a warning in its description about the deploy capability.
D. Keep the coarse tool but instruct the agent to use it only for edits.

## Question 4

Two team setups are proposed. Setup X has a sound configuration but a sprawling, ungated catalog. Setup
Y has a deliberate, gated catalog but a rules-and-memory configuration that misses file creation. Under
a constraint that both the tools and the conventions must hold, which is acceptable?

A. Setup X, because correct conventions matter more than tool gating.
B. Neither, because each is sound on one dimension and fails the other, and the constraint requires both
   the gated catalog and the layered configuration.
C. Setup Y, because gating tools matters more than conventions.
D. Either, because the agent will compensate for whichever layer is weak.

## Question 5

A reviewer says the team environment is safe because the tool catalog is deliberate and every dangerous
tool is gated. The conventions live only in a path-scoped rule and `CLAUDE.md`. Which statement is
correct?

A. It is safe, because a gated catalog is the only control that matters.
B. It is not fully safe, because the conventions are guided rather than governed, so a created file can
   still violate the house style and a secret can still be committed without a hook, pre-commit check,
   or CI gate.
C. It is safe once `conventionEnforcement: true` is set to make the rule binding.
D. It is safe enough, because developers usually follow the conventions.
