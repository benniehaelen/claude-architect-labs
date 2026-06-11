# Answers: lab 04 Claude Code team workflow

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. The pattern to internalize: feature fluency removes
the Branch A fabrications, and architectural judgment picks the winner among the Branch B survivors
(see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is B

B keeps the rule as a guide and adds a PostToolUse hook that runs on Write and Edit, which governs
the convention deterministically on new files as well as edits. That closes the verified write-time
gap (see `../../VERIFIED.md`).

- A is Branch A, fabricated feature. There is no `loadOnWrite: true` frontmatter field that makes a
  path-scoped rule load on create. The convenient-sounding switch is the tell.
- C is Branch B, valid but suboptimal. Memory is a guide. It raises the likelihood of the behavior
  but does not govern it, so a must-hold can still slip. Wrong layer for a must-hold.
- D is Branch B, valid but suboptimal. Adding a sentence to the rule does not change when the rule
  loads. It still does not fire on create, so the gap remains.

## Question 2: correct answer is B

B enforces the security convention in a pre-commit check or a CI gate, which blocks the commit, the
event where the convention must hold. That is the control layer for a must-hold.

- A is Branch B, valid but suboptimal. Restating it in memory more emphatically is still a guide and
  still cannot block a commit. Wrong layer.
- C is Branch A, fabricated feature. There is no `secretScan: true` settings key that makes Claude
  refuse to write secrets. The real control runs at commit or in CI.
- D is Branch B, valid but suboptimal. A path-scoped rule is a guide and loads on read and edit of the
  files it matches, not at the commit. It cannot govern the commit and would miss secrets in unmatched
  files.

## Question 3: correct answer is B

B matches the layer to the kind: a preference belongs in a guide, and a blocking control should be
reserved for must-hold conventions. Governing a preference with a block pays for a control where a
guide would do.

- A is Branch B, valid but suboptimal. Uniform enforcement is simpler to describe but wastes effort
  blocking on preferences and trains the team to ignore the checks.
- C is Branch A, fabricated feature. There is no `enforcementLevel: "all"` key that makes uniform
  control correct. Naming a switch does not make the design sound.
- D is Branch B, valid but suboptimal. Dropping the preferences loses useful guidance. The fix is to
  guide them, not to delete them or to block them.

## Question 4: correct answer is B

B governs each must-hold with a control on its binding event while still using rules to guide, which
is exactly what the no-silent-failure constraint requires.

- A is Branch B, valid but suboptimal. One place and simpler is a real convenience, but memory and
  rules are guides and silently miss create and commit events, which is the failure the constraint
  forbids.
- C is Branch A, fabricated feature. There is no `claude config lint` step that sets configuration
  quality. Quality is a design property, not a tool that appears by naming it.
- D is Branch B, valid but suboptimal. "Generally follows" is not a guarantee, and a must-hold cannot
  depend on usual behavior.

## Question 5: correct answer is B

B states the verified fact precisely: a path-scoped rule loads on read and edit, not on create, so new
files need a control such as a hook to govern them. A committed rule does not change when it loads.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. Committing
  the rule distributes it to every member but does not make it fire on create.
- C is Branch A, fabricated feature. There is no `rules.applyOnCreate: true` setting. The real fix is a
  control that fires on the create event.
- D is Branch B, valid but suboptimal. "Most files are edited" is a guess about frequency, and a
  must-hold cannot rest on the create case being rare.
