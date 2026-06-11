# Answers: developer-productivity tools capstone

Each answer names the correct option, then labels every distractor by branch (A fabricated feature,
B valid but suboptimal) and states why it fails. These questions reward composing the labs: feature
fluency removes the Branch A fabrications, and the integration judgment across labs 02 and 04 picks the
winner among the Branch B survivors (see `../../DISTRACTOR_TAXONOMY.md`).

## Question 1: correct answer is A

A fixes both dimensions: gating the deploy tool stops the unauthorized deploy (lab 02), and a PostToolUse
hook governs the house style on file creation, which closes the write-time gap a path-scoped rule leaves
(lab 04).

- B is Branch A, fabricated feature. There is no `devSafeMode: true` switch that gates tools and enforces
  conventions for you. The convenient-sounding switch is the tell.
- C is Branch B, valid but suboptimal. A `CLAUDE.md` instruction guides but governs neither the deploy nor
  the created file. Wrong layer for both must-holds.
- D is Branch B, valid but suboptimal. Making deploy read-only breaks a needed capability, and moving the
  rule into the prompt still does not govern file creation.

## Question 2: correct answer is B

B states the verified edge: a path-scoped rule loads on the edit but not on the create, so a hook is
needed to govern the convention on file creation as well as edits.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong claim. The rule does
  miss the create event, so a change is needed.
- C is Branch A, fabricated feature. There is no `ruleScope` setting whose width fixes the create gap. The
  rule loads on read and edit by design, not on create.
- D is Branch B, valid but suboptimal. A CI check after the fact catches the violation late, after the
  file was created, rather than governing it at the write.

## Question 3: correct answer is A

A splits the coarse tool by effect, so editing is a separate gated write and deploying is a separate gated
destructive action, which removes the over-privilege and the ambiguity (lab 02).

- B is Branch A, fabricated feature. There is no `confirmDeploy: true` parameter the platform enforces.
  The real control is gating a single-effect tool.
- C is Branch B, valid but suboptimal. A description warning is a guide and cannot stop the deploy
  capability the coarse tool still carries.
- D is Branch B, valid but suboptimal. A prompt instruction does not remove the bundled deploy capability
  or the ambiguity.

## Question 4: correct answer is B

B identifies that each setup is sound on one dimension and fails the other, and the constraint requires
both the gated catalog and the layered configuration. Composition means both must hold.

- A is Branch B, valid but suboptimal. Correct conventions do not rescue an ungated deploy, so Setup X is
  unsafe on the tool dimension.
- C is Branch B, valid but suboptimal. A gated catalog does not rescue a convention that silently fails on
  file creation, so Setup Y is unsafe on the convention dimension.
- D is Branch A in spirit: it asserts a capability that does not exist. An agent does not reliably
  compensate for a missing control layer.

## Question 5: correct answer is B

B states the composition thesis: the conventions are guided rather than governed, so a created file can
still violate the house style and a secret can still be committed without a hook, pre-commit check, or CI
gate.

- A is Branch B, valid but suboptimal in the sense that it is a coherent but wrong position. A gated
  catalog is one of two control layers, not the only one.
- C is Branch A, fabricated feature. There is no `conventionEnforcement: true` switch that makes a rule
  binding. A rule is a guide by nature.
- D is Branch B, valid but suboptimal. "Usually follow" is not a guarantee, and a must-hold convention
  cannot depend on usual behavior.
