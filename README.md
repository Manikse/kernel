# Manikse Kernel (MK-1)
> *A Cognitive Operating System Layer for Autonomous Agents.*

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.4.0--alpha-blue">
  <img src="https://img.shields.io/badge/status-experimental-orange">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## 👁‍🗨 Vision

Chatbots are obsolete.

The next evolution of AI is **autonomous, self-correcting systems** that can:
- think
- remember
- act

**Manikse Kernel (MK-1)** is a foundational **Cognitive OS layer** that bridges Large Language Models with real-world execution.

It is not an API wrapper.  
It is the beginning of an **AI-native operating system**.

---

## 🏗 Core Architecture
MK-1 is built on four pillars of machine autonomy:

### 1. ACL (Agent Control Layer)
The "Prefrontal Cortex" of the system. It handles high-level reasoning, manages multiple LLM providers (OpenRouter, Gemini, OpenAI), and routes logic based on mission requirements.

### 2. UNMS (Unified Neural Memory System)
The "Hippocampus." It provides persistent, long-term memory. MK-1 remembers past interactions, learned facts, and project contexts across sessions using a unified storage layer.

### 3. A2A (Agent-to-Agent Protocol)
The "Delegation System." MK-1 dynamically spawns specialized sub-agents (e.g., *DevOps-Master*, *Python-Guru*) for complex tasks. Built-in Middleware ensures 100% clean, executable code generation.

### 4. Drivers (A2E - Agent-to-Environment)
The "Hands" of the system. Drivers allow the Kernel to interact with the world:
* **WebSearch Driver:** Real-time internet access and data retrieval.
* **Terminal Driver:** Execution of native PC commands (PowerShell/Bash) with self-correction.
* **FileSystem Driver:** Autonomous file management and code generation.

---

## ⚡ Features

- **Self-Correcting Execution (Reflection Loop):** Detects terminal errors (e.g., `SyntaxError`) and dynamically injects Recovery Plans to fix its own code on the fly.
- **Asynchronous Daemon Worker:** True multi-threading. MK-1 runs scheduled background tasks (monitoring, logging) parallel to the interactive chat interface.
- **Cognitive Planner & Data Piping:** Breaks goals into JSON steps. Outputs from one step seamlessly pass to the next (`{{STEP_N_RESULT}}`).
- **Cross-Platform Environment Awareness:** Automatically detects the host OS (Windows, Linux, macOS) and adapts its terminal commands.
- **LLM Agnostic & Bilingual Context:** Easily switch models via OpenRouter. Seamless language switching based on Founder's input.

---

## 🛠 Installation

```bash
git clone [https://github.com/Manikse/kernel-core](https://github.com/Manikse/kernel-core)
cd manikse-kernel
pip install -r requirements.txt
```

🔑 **Environment Setup**

Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

**Run the Kernel**
```bash
python main.py
```

---

## 💻 Example Interaction

**User:**
> Create a file hello.txt and write "MK-1 is alive" in it. Where is that file exactly?

**Kernel (Autonomous Execution):**
```text
[MK-1 EXEC] Step 1: WRITE hello.txt [Tool: file_system]
[Driver: FileSystem] 💾 Processing file operation...

[MK-1 EXEC] Step 2: Get-ChildItem -Path hello.txt -Recurse | Select-Object -ExpandProperty FullName [Tool: terminal]
[Driver: Terminal] 💻 Executing command...

[MK-1] The file was successfully created. Its absolute path is: D:\games\VESTA\Kernel\kernel-core\kernel_workspace\hello.txt
```

---

## 🗺 Roadmap

- [x] **Phase 1: Terminal Alpha** - Core logic, CLI Cyberpunk interface, Basic Drivers.
- [x] **Phase 2: Cognitive Autonomy** - A2A Protocol, Self-Correction Loop, Background Daemon, OS Awareness.
- [ ] **Phase 3: Web Interface** - Localhost UI for seamless interaction, agent visualization, and node-graph planning.
- [ ] **Phase 4: Server Deployment Hub** - Headless mode for remote Ubuntu server management.

---

## ⚠️ Disclaimer

This is an **Alpha release**.

The Terminal Driver executes real commands on your machine.
While sandboxed to `./kernel_workspace`, **review the code** before use in production. Do not run as root unless strictly necessary.

---

## 👤 Author

Created by **Manikse** — Building the infrastructure of the future.

## ☕ Support the Project
<div align="center"> 
  <a href="https://ko-fi.com/manikse"> 
    <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" width="200"/> 
  </a> 
</div>