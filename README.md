🤖 AI-SEC Tool v2.0: The AI-Powered Hacking Environment
Python Nmap AI

A professional, interactive Python security console that combines State-of-the-Art AI with Nmap automation. Designed for ethical hackers and security researchers, it transforms a simple terminal into a high-powered hacking environment.

🚀 Features
🧠 Interactive AI Chat: Powered by Dolphin Mistral 24B, specialized in security and code generation.
📦 Workspace Management: Isolate your assessments into separate workspaces (workspace internal_audit).
🎯 Global Target Context: Set a target once (target 10.10.10.1) and use it across all tools.
🛰️ Nmap Integration: Fast, automated scanning with instant AI Analysis (scan --analyze).
🌐 Web Recon: Quick HTTP header inspection and robots.txt analysis.
💾 Payload Generator: Instant AI-generated reverse shells (Python, Bash, PHP, etc.).
⚡ Pro UI: MSF/SQLMap style interactive terminal with code block extraction and syntax highlighting.
IT,S UNSENSERD!!!!!

🛠️ Installation
Clone the Repository:

git clone https://github.com/ekal12/wormgpt.git
cd wormgpt
Install Dependencies:

pip install -r requirements.txt
Ensure Nmap is Installed:

Windows: winget install Insecure.Nmap
Linux: sudo apt install nmap
📖 Usage
Launch the environment:

python main.py
Core Commands
Command	Description
target <ip/url>	Set global target context
workspace <name>	Switch to a new results workspace
scan [args]	Start Nmap scan (uses global target)
scan --analyze	Scan and have AI explain potential risks
web [url]	Basic web reconnaissance & header analysis
payload <type> <ip> <port>	Generate a custom reverse shell payload
help	Show the help terminal
exit	Leave the environment
⚙️ Configuration
The tool comes pre-configured with free public API keys for immediate use. You can modify settings in config.py.

# API Keys (Public Free Keys Included)
API_KEYS = [
    "sk-or-v1-...", # Shared keys for public use
]
🛡️ Disclaimer
This tool is for EDUCATIONAL AND ETHICAL USE ONLY. Unauthorized scanning or hacking of systems is illegal. The developers assume no responsibility for misuse.

Made with ❤️ for the security community. FOLLOW ME ON INSTAGRAM @itz_ekalx
