"""The agent loop harness.

The harness is the reusable engine the labs build on. It runs a tool-calling agent loop and, in
the instrumented configuration, records a structured trace of every decision point and ties a
circuit breaker to a governed escalation. Lab 01 uses it directly, and later labs reuse it.
"""
