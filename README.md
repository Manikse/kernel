# Manikse Kernel (MK-1)
> *A Cognitive Operating System Layer for Autonomous AI Agents.*

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.4.0--alpha-blue">
  <img src="https://img.shields.io/badge/status-experimental-orange">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## Vision

The next evolution of artificial intelligence requires moving beyond conversational interfaces. MK-1 is designed as a foundational Cognitive OS layer that bridges Large Language Models with independent, real-world execution.

It is not an API wrapper. It is the core infrastructure for an AI-native operating system capable of reasoning, persistent memory, and autonomous action.

---

## Core Architecture

MK-1 is built upon four architectural pillars of machine autonomy:

### 1. ACL (Agent Control Layer)
The cognitive routing engine of the system. It handles high-level reasoning, manages multiple LLM providers (e.g., OpenRouter, Gemini, OpenAI), and routes logic based on execution requirements.

### 2. UNMS (Unified Neural Memory System)
The persistent state management system. MK-1 retains context, learned data, and project objectives across execution cycles using a unified storage layer, simulating long-term memory.

### 3. A2A (Agent-to-Agent Protocol)
The delegation framework. MK-1 dynamically spawns specialized sub-agents (e.g., DevOps Administrator, Python Developer) to handle isolated, complex tasks. A built-in middleware filter ensures executable, syntax-clean code generation.

### 4. Drivers (A2E - Agent-to-Environment)
The execution interfaces allowing the Kernel to interact with the host environment:
* **WebSearch Driver:** Real-time data retrieval.
* **Terminal Driver:** Execution of native OS commands (PowerShell/Bash) with built-in self-correction.
* **FileSystem Driver:** Autonomous file management and I/O operations.

---

## Key Features

- **Reflection Loop (Self-Correction):** Automatically detects terminal execution errors (e.g., `SyntaxError`) and dynamically injects recovery plans to patch its own code during runtime.
- **Asynchronous Daemon Worker:** True multi-threading capability. MK-1 runs scheduled background tasks (system monitoring, log generation) concurrently with the interactive session.
- **Cognitive Planner & Data Piping:** Deconstructs complex goals into structured JSON execution steps. Standardized `{{STEP_N_RESULT}}` pipelines pass data seamlessly between operations.
- **Cross-Platform Environment Awareness:** Automatically identifies the host operating system (Windows, Linux, macOS) and adapts shell commands accordingly.
- **LLM-Agnostic & Bilingual Context:** Seamless model switching via OpenRouter and native support for dynamic language context switching based on user input.

---

## Installation

```bash
git clone [https://github.com/Manikse/kernel-core](https://github.com/Manikse/kernel-core)
cd manikse-kernel
pip install -r requirements.txt
```

**Environment Setup**

Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

**Run the Kernel**
```bash
python main.py
```

---

## Example Interaction

**User:**
> Create a file hello.txt and write "MK-1 is alive" in it. Where is that file exactly?

**Kernel (Autonomous Execution):**
```text
[MK-1 EXEC] Step 1: WRITE hello.txt [Tool: file_system]
[Driver: FileSystem] Processing file operation...

[MK-1 EXEC] Step 2: Get-ChildItem -Path hello.txt -Recurse | Select-Object -ExpandProperty FullName [Tool: terminal]
[Driver: Terminal] Executing command...

[MK-1] The file was successfully created. Its absolute path is: D:\games\VESTA\Kernel\kernel-core\kernel_workspace\hello.txt
```

---

## Roadmap

- [x] **Phase 1: Terminal Alpha** - Core logic, CLI interface, and fundamental execution drivers.
- [x] **Phase 2: Cognitive Autonomy** - A2A Protocol, Self-Correction Loop, Background Daemon, OS Awareness.
- [ ] **Phase 3: Web Interface** - Localhost UI for interaction, agent visualization, and node-graph planning.
- [ ] **Phase 4: Server Deployment Hub** - Headless mode for remote server management and telemetry.

---

## Disclaimer

This software is currently in **Alpha release**.

The Terminal Driver executes native commands on your host machine. While operations are sandboxed to `./kernel_workspace` by default, please review generated code before executing in production environments. Do not run as root/administrator unless strictly necessary.

---

## Author & Support

Created by **Manikse** — Building the infrastructure of the future.

<div align="center"> 
  <a href="https://ko-fi.com/manikse"> 
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" width="200"/> 
  </a> 
</div>