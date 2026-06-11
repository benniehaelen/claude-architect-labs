# Questions: lab 04 Claude Code team workflow

Five scenario questions. Each carries at least one Branch A distractor (a fabricated feature) and at
least two Branch B distractors (valid but suboptimal under the stated constraints). See
`../../DISTRACTOR_TAXONOMY.md`. Answers and branch labels are in `answers.md`. Do not read the
answers until you have committed to a choice.

## Question 1

A team enforces a Markdown convention with a path-scoped rule in `.claude/rules`. It holds when
Claude edits existing files but is violated on files Claude creates from scratch. The convention must
always hold. What is the best fix?

A. Add a `loadOnWrite: true` field to the rule's frontmatter so it loads when a file is created.
B. Keep the rule as a guide and add a PostToolUse hook that runs on Write and Edit and fails on a
   violation.
C. Move the convention into `CLAUDE.md` so it is always in context.
D. Add a sentence to the rule telling Claude to apply it to new files too.

## Question 2

A team writes "never commit credentials" into `CLAUDE.md`. A secret is later committed anyway. Where
must the enforcement live?

A. In `CLAUDE.md`, stated more emphatically and in all capitals.
B. In a pre-commit check or a CI gate that blocks a commit containing a credential.
C. In a `secretScan: true` key in `settings.json` that makes Claude refuse to write secrets.
D. In a path-scoped rule on the files most likely to hold secrets.

## Question 3

A reviewer proposes governing every team convention, including stylistic preferences like heading
case, with a blocking pre-commit check. What is the soundest assessment?

A. Sound, because uniform enforcement is simplest to reason about.
B. Overbuilt, because a preference belongs in a guide and a blocking control should be reserved for
   must-hold conventions.
C. Sound once `enforcementLevel: "all"` is set so the team opts in deliberately.
D. Overbuilt, so the preferences should simply be dropped from the configuration entirely.

## Question 4

Two team configurations are proposed. Configuration X writes all conventions into memory and
path-scoped rules. Configuration Y keeps the rules as guides and adds hooks for write-time must-holds
and a CI gate for the commit-time security rule. Both are real configurations. Under a constraint that
must-hold conventions cannot silently fail, which is better and why?

A. Configuration X, because memory and rules keep everything in one place and are simpler.
B. Configuration Y, because it governs each must-hold with a control on its binding event while still
   using rules to guide, which is what the no-silent-failure constraint requires.
C. Neither, because configuration quality is set by a `claude config lint` step rather than by design.
D. Either, because Claude generally follows memory and rules in practice.

## Question 5

A team lead says the house-style convention is safe because the path-scoped rule is committed to the
repository and every member has it. New files keep violating it. Which statement is correct?

A. The convention is safe, because a committed rule applies to every file every member touches.
B. The convention is not safe, because a path-scoped rule loads on read and edit, not on create, so
   new files need a control such as a hook to govern them.
C. The convention is safe once `rules.applyOnCreate: true` is enabled in the project settings.
D. The convention is safe enough, because most files are edited rather than created.
