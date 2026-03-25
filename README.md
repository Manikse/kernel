#  Manikse Kernel (MK-1)
> *A Cognitive Operating System Layer for Autonomous Agents.*

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.3.0--alpha-blue">
  <img src="https://img.shields.io/badge/status-experimental-orange">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---

##  Vision

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
MK-1 is built on three pillars of machine autonomy:

### 1. ACL (Agent Control Layer)
The "Prefrontal Cortex" of the system. It handles high-level reasoning, manages multiple LLM providers (OpenRouter, Gemini, OpenAI), and routes logic based on mission requirements.

### 2. UNMS (Unified Neural Memory System)
The "Hippocampus." It provides persistent, long-term memory. MK-1 remembers past interactions, learned facts, and project contexts across sessions using a unified storage layer.
### 3. Drivers (A2E - Agent-to-Environment)
The "Hands" of the system. Drivers allow the Kernel to interact with the world:
* **WebSearch Driver:** Real-time internet access and data retrieval.
* **Terminal Driver:** Execution of native PC commands (PowerShell/CMD) with self-correction.
* **FileSystem Driver:** Autonomous file management and code generation.

---

##  Features

-  **Self-Correcting Execution**  
  Detects terminal errors and fixes commands automatically

-  **Dynamic Web Search (`[SEARCH:]`)**  
  Real-time data via `ddgs`

-  **Terminal Execution (`[EXECUTE:]`)**  
  File system + shell control in `kernel_workspace`

-  **LLM Agnostic**  
  Easily switch models via OpenRouter

-  **Bilingual Context Awareness**  
  Seamless language switching

---

## 🛠 Installation

```bash
git clone [https://github.com/Manikse/kernel-core]
cd manikse-kernel
pip install -r requirements.txt
```
🔑 Environment Setup

Create a .env file in the root:

OPENROUTER_API_KEY="sk-or-v1-your-key-here"

**Run the Kernel**
python main.py

# Example Interaction
User:
Create a file hello.txt in your workspace and write "MK-1 is alive" in it.

Kernel:
[Driver: Terminal] Executing: echo "MK-1 is alive" > hello.txt
[Kernel] Analysing output...

✔ File created
User:
Where is that file exactly?

Kernel:
[Driver: Terminal] Executing: pwd (fails on Windows)
[Kernel] Self-correcting...
[Driver: Terminal] Executing: dir hello.txt /s

✔ Absolute path returned
🛠 Roadmap
[x] Phase 1: Terminal Alpha - Core logic, CLI Cyberpunk interface, Basic Drivers.

[ ] Phase 2: Web Interface - Localhost UI for seamless interaction and visualization.

[ ] Phase 3: Swarm Protocol - Allowing multiple MK-1 instances to collaborate on a single task.

⚠️ Disclaimer

This is an alpha release.

The Terminal Driver executes real commands on your machine.
While sandboxed to ./kernel_workspace, review the code before use in production.

👤 Author

Created by **Manikse** — Building the infrastructure of the future.

☕ Support the Project
<div align="center"> <a href="https://ko-fi.com/manikse"> <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" width="200"/> </a> </div> ```
