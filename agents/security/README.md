# Security Agent

## Responsibilities
- Conduct automated Static Application Security Testing (SAST) on generated source code.
- Audit dependencies for known Common Vulnerabilities and Exposures (CVEs).
- Detect accidental inclusion of hardcoded secrets, tokens, or private credentials.
- Verify that SQL queries, shell executions, and HTML renders are properly parameterized and sanitized.

## Interfaces
- **Input**: Complete generated codebase, configuration files, and package manifests.
- **Output**: Security audit reports, vulnerability scorecards, patch diffs.
- **Capability Requirements**: High security domain reasoning, deep vulnerability knowledge.
