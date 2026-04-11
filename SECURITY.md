# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within the EXARCHON framework, please report it responsibly to ensure the safety of the community.

**Do NOT open public issues for security vulnerabilities.**

Instead, please report vulnerabilities via:
* **GitHub Private Vulnerability Reporting:** Use the "Security" tab in this repository to submit a private report.
* **Direct Contact:** [Встав свій імейл або лінк на профіль]

Please include:
1. A detailed description of the vulnerability.
2. Steps to reproduce the issue.
3. Potential impact (e.g., unauthorized file access, remote code execution).
4. Suggested remediation (if available).

We take security seriously and will acknowledge your report within 48 hours.

---

## Scope

This policy covers the core EXARCHON components:
* **Core Orchestrator:** Asynchronous execution logic and A2A protocols.
* **Drivers:** FileSystem, Terminal, and WebSearch execution interfaces.
* **CLI/Client:** Interface for interacting with the daemon.

---

## Best Practices for Users (Safety First)

EXARCHON is an autonomous execution environment. With great power comes great responsibility:

1. **API Key Safety:** Never hardcode your OpenRouter or LLM API keys. Use environment variables.
2. **Execution Monitoring:** Always monitor the `Reflection Loop` logs when running the system in highly sensitive environments.
3. **Sandbox Environments:** We recommend running EXARCHON within isolated environments (Docker, VM, or dedicated user accounts) to limit the impact of autonomous system modifications.
4. **Updates:** Always use the latest version to ensure you have the most recent security patches.
"""