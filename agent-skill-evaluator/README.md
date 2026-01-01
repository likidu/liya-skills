# Agent Skill Evaluator

A specialized security and safety auditing tool for AI Agent Skills. This skill enables your agent to autonomously review, score, and verify the integrity of other `.skill` files and GitHub repositories before you install or use them.

> **Note:** This tool is part of the [Eval Marketplace](https://github.com/JeredBlu/eval-marketplace). And it was introduced in this YouTube video [OpenAI Adds Agent Skills to Codex (First Look & Walkthrough)](https://youtu.be/MsJzacfjzp8?t=340&si=UYxbiUYydqiyKhDA)

## 📖 Overview

As the ecosystem of AI skills grows, so does the risk of executing untrusted instructions. The **Agent Skill Evaluator** acts as a security checkpoint. It retrieves skill files (from GitHub or local paths), subjects them to a rigorous multi-step evaluation process, and generates a standardized risk report.

**Core Mission:** verify source authenticity, detect prompt injections, audit permissions, and ensure code safety.

## ✨ Key Features

* **🛡️ Automated Risk Scoring:** Generates a 0-100 safety score based on 5 security dimensions.
* **💉 Injection Detection:** Scans `SKILL.md` and prompt files for "jailbreak" patterns, hidden instructions, or prompt injection attempts.
* **🐛 Malicious Code Analysis:** Reviews executable scripts (Python, Bash, Node) for unauthorized network access, file system tampering, or data exfiltration.
* **⭐ Reputation Verification:** Checks GitHub metadata (stars, forks, author activity) to validate community trust.
* **📝 Standardized Reporting:** Produces a detailed Markdown or PDF assessment report with actionable recommendations.

## ⚙️ Prerequisites

To use this skill effectively, your environment (e.g., Claude Code, Claude Desktop) should have the following **MCP Servers** configured. These allow the evaluator to fetch external code and data:

1. **GitHub MCP Server** (`@modelcontextprotocol/server-github`)
* *Required for:* Fetching repositories, checking commit history, and analyzing code.


2. **Bright Data MCP** (Optional but Recommended)
* *Required for:* Scaping Reddit/Web for community feedback and reputation checks.


## 🚀 Installation

### Option 1: Via Claude Code (Recommended)

If you have the Eval Marketplace plugin configured:

```bash
/plugin install evaluator-tools

```

### Option 2: Manual Installation

1. Download the `agent-skill-evaluator` folder.
2. Place it in your skills directory (e.g., `~/.claude/skills/` or your project's `skills/` folder).
3. Ensure the folder structure is correct:
```text
skills/
└── agent-skill-evaluator/
    ├── SKILL.md
    ├── handler.py (or similar logic file)
    └── manifest.json

```


4. Restart your agent or run `/reset` to load the new skill.

## 💡 Usage

Once installed, you can ask your agent to evaluate any public skill or repository.

### Trigger Phrases

* *"Is this skill safe to use? [GitHub URL]"*
* *"Evaluate the security of this repo: [GitHub URL]"*
* *"Run a security assessment on the agent-skill-creator skill."*

### Example Workflow

**User:**

> "Can you evaluate if [https://github.com/username/cool-new-skill](https://www.google.com/search?q=https://github.com/username/cool-new-skill) is safe to install?"

**Agent (using Agent Skill Evaluator):**

1. **Fetches** the repository content using the GitHub MCP.
2. **Scans** the `SKILL.md` for suspicious prompt engineering.
3. **Checks** any associated `.py` or `.sh` files for dangerous imports (e.g., `os.system`, `subprocess`, `eval`).
4. **Reviews** the author's reputation (account age, previous contributions).
5. **Returns** a structured report.

## 📊 Evaluation Criteria

The evaluator checks for the following specific risks:

| Category | Checks Performed |
| --- | --- |
| **Prompt Safety** | Hidden text, "Ignore previous instructions", infinite loops, recursive calls. |
| **Code Security** | Obfuscated code, unauthorized outgoing requests, shell execution, crypto-mining patterns. |
| **Data Privacy** | Attempts to read `.env` files, uploading data to unknown servers, key logging. |
| **Integrity** | Verification that the code matches the description (no "bait and switch"). |

## ⚠️ Disclaimer

This tool provides a heuristic analysis based on known attack patterns and best practices. While it significantly reduces risk, it cannot guarantee 100% safety. Always review code manually if the evaluator flags high-risk items.

---

*Based on the [Eval Marketplace](https://github.com/JeredBlu/eval-marketplace) repository and tutorials by Jered Blumenfeld.*

By the way, to unlock the full functionality of all Apps, enable [Gemini Apps Activity](https://myactivity.google.com/product/gemini).
