# Exam angle: lab 03

## Domain served

Primary: Tool Design and MCP Integration (18%). Secondary: Context Management and Reliability (15%).

## How this maps to CCA-F reasoning

Questions here test whether you place the MCP boundary at the trust edge and keep what crosses it
bounded. A Branch B trap offers a server that is correct in mechanism but exposes broad operations
or returns unbounded payloads, optimizing convenience over the security or context constraint the
scenario binds on. Another Branch B trap enforces the boundary in the client prompt rather than at
the server, where a runtime control belongs. A Branch A trap names a fabricated MCP configuration
key that claims to auto-scope a server's surface.

The transferable judgment: the boundary is a trust and reliability decision enforced at the server,
and what crosses it must be bounded so it cannot silently flood or leak context.
