# 🧠 Manikse Kernel (MK-1)
> *A Cognitive Operating System Layer for Autonomous Agents.*

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.1.0--alpha-blue">
  <img src="https://img.shields.io/badge/status-experimental-orange">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## ⚡ Vision

Chatbots are obsolete.

The next evolution of AI is **autonomous, self-correcting systems** that can:
- think
- remember
- act

**Manikse Kernel (MK-1)** is a foundational **Cognitive OS layer** that bridges Large Language Models with real-world execution.

It is not an API wrapper.  
It is the beginning of an **AI-native operating system**.

---

## 🏗 Architecture

MK-1 is built on three core pillars + an extensible driver system:

### 🧠 ACL — Agent Control Layer
The reasoning engine.  
Model-agnostic and powered via OpenRouter (Gemini 2.0 Flash by default).

Handles:
- decision-making
- ReAct-style tool usage
- execution planning

---

### 🧬 UNMS — Unified Neural Memory System
The memory core.

- Automatic context compression
- Warm storage for long-term coherence
- Prevents token overflow

---

### 🤝 A2A — Agent-to-Agent Protocol *(WIP)*
The foundation for swarm intelligence.

---

### 🛠 Driver Abstraction
The interface to reality.

- Sandboxed tools
- Extendable
- Enables real-world interaction

---

## 🚀 Features

- ⚡ **Self-Correcting Execution**  
  Detects terminal errors and fixes commands automatically

- 🌐 **Dynamic Web Search (`[SEARCH:]`)**  
  Real-time data via `ddgs`

- 💻 **Terminal Execution (`[EXECUTE:]`)**  
  File system + shell control in `kernel_workspace`

- 🔌 **LLM Agnostic**  
  Easily switch models via OpenRouter

- 🌍 **Bilingual Context Awareness**  
  Seamless language switching

---

## 🛠 Installation

```bash
git clone https://github.com/YOUR_USERNAME/manikse-kernel.git
cd manikse-kernel
pip install -r requirements.txt
🔑 Environment Setup

Create a .env file in the root:

OPENROUTER_API_KEY="sk-or-v1-your-key-here"
▶️ Run the Kernel
python main.py
💻 Example Interaction
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
🗺 Roadmap

 Core reasoning loop (ACL)

 Memory system (UNMS)

 Web search driver

 Terminal execution driver

 Vector DB integration (ChromaDB)

 Multi-agent system (A2A)

 Advanced file system + AST parsing

⚠️ Disclaimer

This is an alpha release.

The Terminal Driver executes real commands on your machine.
While sandboxed to ./kernel_workspace, review the code before use in production.

👤 Author

Manikse
Building the OS layer for the next generation of AI

☕ Support the Project
<div align="center"> <a href="https://ko-fi.com/manikse"> <img src="https://storage.ko-fi.com/cdn/kofi3.png?v=3" width="200"/> </a> </div> ```
🔧 І ще файл requirements.txt
openai
python-dotenv
ddgs