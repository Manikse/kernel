<div align="center">
  <a href="https://github.com/Manikse/kernel">
    <img src="docs/logo.png" alt="EXARCHON Logo" width="200">
  </a>

  <h1>EXARCHON</h1>

  <p>
    <b>The Headless Cognitive Operating System Layer for Autonomous AI Agents.</b><br>
    Bridging probabilistic reasoning with deterministic execution.
  </p>

---
## Core Architecture

> 📖 **Deep Dive:** For an in-depth technical breakdown of the system's cognitive framework and execution loop, please refer to the [Architecture Documentation](docs/architecture.md).

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.5.1--alpha-blue">
  <img src="https://img.shields.io/badge/status-experimental-orange">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---


## Vision

The next evolution of artificial intelligence requires moving beyond conversational interfaces. EXARCHON is designed as a foundational Cognitive OS layer that bridges Large Language Models with independent, real-world execution.

It is not an API wrapper. It is the core infrastructure for an AI-native operating system capable of reasoning, persistent memory, and autonomous action.

---

## Core Architecture

EXARCHON is built upon four architectural pillars of machine autonomy:

### 1. ACL (Agent Control Layer)
The cognitive routing engine of the system. It handles high-level reasoning, manages multiple LLM providers (e.g., OpenRouter, Gemini, OpenAI), and routes logic based on execution requirements.

### 2. UNMS (Unified Neural Memory System)
The persistent state management system. EXARCHON retains context, learned data, and project objectives across execution cycles using a unified storage layer, simulating long-term memory.

### 3. A2A (Agent-to-Agent Protocol)
The delegation framework. EXARCHON dynamically spawns specialized sub-agents (e.g., DevOps Administrator, Python Developer) to handle isolated, complex tasks. A built-in middleware filter ensures executable, syntax-clean code generation.

### 4. Drivers (A2E - Agent-to-Environment)
The execution interfaces allowing the Kernel to interact with the host environment:
* **WebSearch Driver:** Real-time data retrieval.
* **Terminal Driver:** Execution of native OS commands (PowerShell/Bash) with built-in self-correction.
* **FileSystem Driver:** Autonomous file management and I/O operations.

---

## Key Features

- **Reflection Loop (Self-Correction):** Automatically detects terminal execution errors (e.g., `SyntaxError`) and dynamically injects recovery plans to patch its own code during runtime.
- **Asynchronous Daemon Worker:** True multi-threading capability. EXARCHON runs scheduled background tasks (system monitoring, log generation) concurrently with the interactive session.
- **Cognitive Planner & Data Piping:** Deconstructs complex goals into structured JSON execution steps. Standardized `{{STEP_N_RESULT}}` pipelines pass data seamlessly between operations.
- **Cross-Platform Environment Awareness:** Automatically identifies the host operating system (Windows, Linux, macOS) and adapts shell commands accordingly.
- **LLM-Agnostic & Bilingual Context:** Seamless model switching via OpenRouter and native support for dynamic language context switching based on user input.

---

## Installation

```bash
git clone [https://github.com/Manikse/kernel](https://github.com/Manikse/kernel)
cd exarchon-core
pip install -r requirements.txt
```

**Environment Setup**

Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

**Run the System**
```bash
python main.py
```

---

## Example Interaction

**User:**
> Create a file status.log and write "EXARCHON is online" in it. Where is that file exactly?

**EXARCHON (Autonomous Execution):**
```text
[EXARCHON EXEC] Step 1: WRITE status.log [Tool: file_system]
[Driver: FileSystem] Processing file operation...

[EXARCHON EXEC] Step 2: Get-ChildItem -Path status.log -Recurse | Select-Object -ExpandProperty FullName [Tool: terminal]
[Driver: Terminal] Executing command...

[EXARCHON] The file was successfully created. Its absolute path is: D:\workspace\exarchon-core\status.log
```

---

## Roadmap

- [x] **Phase 1: Terminal Alpha** - Core logic, CLI interface, and fundamental execution drivers.
- [x] **Phase 2: Cognitive Autonomy** - A2A Protocol, Self-Correction Loop, Background Daemon, OS Awareness.
- [ ] **Phase 3: Web Interface (Mission Control)** - Localhost UI for interaction, agent visualization, and node-graph planning.
- [ ] **Phase 4: Server Deployment Hub** - Headless mode for remote server management and telemetry.

---

## Disclaimer

This software is currently in **Alpha release**.

The Terminal Driver executes native commands on your host machine. While operations are sandboxed locally, please review generated code before executing in production environments. Do not run as root/administrator unless strictly necessary.

---

## Author & Support

Created by **Manikse** — Building the infrastructure of the future.

<div align="center"> 
  <a href="https://ko-fi.com/manikse"> 
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" width="200"/> 
  </a> 
</div>
