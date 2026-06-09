---
paths: ["**/*.md"]
---

# House style for Markdown

These rules apply to every Markdown file in this repository. This rule loads when a matching file is
read. It does not load when a matching file is created or written (a known limitation, dated and
sourced in `VERIFIED.md`), so the same rules are enforced at runtime by a PostToolUse hook and a
git pre-commit check. Treat this rule as the guide and those checks as the control.

- Do not use em-dashes anywhere. Use commas, periods, parentheses, or colons instead.
- Use sentence-case headings.
- Avoid contractions at sentence boundaries.
- Keep any reference to a real healthcare client or named internal platform out of this public
  repository. Use generic phrasing such as "a large healthcare organization" and "a production
  NL-to-SQL platform."
- Prefer prose over bullet soup. Use lists only where the content is genuinely enumerable.
