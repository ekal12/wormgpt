import sys
import re
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from tool.config import PROMPT_SYMBOL
from tool.ai.openrouter_client import OpenRouterClient
from tool.scanner.nmap_scanner import NmapScanner
from tool.utils.logger import logger
from tool.utils.formatter import (
    print_banner, print_user_msg, print_ai_msg, print_code_box,
    print_error, print_info, print_warning
)

from tool.modules.web_recon import WebRecon
from tool.modules.payload_gen import PayloadGenerator
from tool.session import SessionManager

class InteractiveShell:
    def __init__(self):
        self.session_manager = SessionManager() # Renaming to avoid conflict with PromptSession
        self.ai = OpenRouterClient()
        self.scanner = NmapScanner()
        self.web_recon = WebRecon()
        self.payload_gen = PayloadGenerator(self.ai)
        
        self.prompt_session = PromptSession()
        self.running = True
        
        # Style for the prompt
        self.style = Style.from_dict({
            'prompt': 'ansicyan bold',
            'info': 'ansigreen',
        })

    def start(self):
        while self.running:
            try:
                # Dynamic prompt
                prompt_text = f"\n{self.session_manager.get_prompt_suffix()}\n{PROMPT_SYMBOL} "
                user_input = self.prompt_session.prompt(prompt_text, style=self.style).strip()
                
                if not user_input:
                    continue
                
                logger.info(f"User input: {user_input}")
                
                cmd_lower = user_input.lower()
                
                if cmd_lower in ['exit', 'quit']:
                    self.running = False
                    print_info("Goodbye!")
                    break
                elif cmd_lower == 'clear':
                    print("\033c", end="")
                    continue
                elif cmd_lower == 'help':
                    self._show_help()
                    continue
                
                # Check commands
                if cmd_lower.startswith('scan '):
                    self._handle_scan(user_input)
                elif cmd_lower == 'scan':
                    # Scan current target
                    if self.session_manager.target:
                        self._handle_scan(f"scan {self.session_manager.target}")
                    else:
                        print_error("No target set. Use 'target <ip>' or 'scan <ip>'")
                elif cmd_lower.startswith('target '):
                    self._handle_target(user_input)
                elif cmd_lower.startswith('workspace '):
                    self._handle_workspace(user_input)
                elif cmd_lower.startswith('web '):
                    self._handle_web(user_input)
                elif cmd_lower.startswith('payload '):
                    self._handle_payload(user_input)
                else:
                    self._handle_chat(user_input)

            except KeyboardInterrupt:
                print()
                print_info("Use 'exit' to quit.")
            except EOFError:
                self.running = False
                break
            except Exception as e:
                logger.error(f"Shell loop error: {e}")
                print_error(f"An unexpected error occurred: {e}")

    def _show_help(self):
        help_text = """
        [AI-SEC TOOL v2.0 - Hacking Environment]
        ----------------------------------------
        target <ip/url>         : Set the current Global Target.
        workspace <name>        : Switch workspace (creates isolated results folder).
        
        scan [target] [flags]   : Run Nmap scan (uses Global Target if omitted).
        scan <t> --analyze      : API Analysis of scan results.
        
        web <url>               : Run Basic Web Recon (headers, tech).
        payload <type> <ip> <p> : AI-Generated Reverse Shell (e.g. payload python 10.0.0.1 4444).
        
        exit / quit             : Exit.
        clear                   : Clear screen.
        
        <any other text>        : Chat with AI Security Assistant.
        """
        print(help_text)

    def _handle_target(self, cmd):
        parts = cmd.split()
        if len(parts) < 2:
            print_error("Usage: target <ip/url>")
            return
        self.session_manager.set_target(parts[1])

    def _handle_workspace(self, cmd):
        parts = cmd.split()
        if len(parts) < 2:
            print_error("Usage: workspace <name>")
            return
        self.session_manager.set_workspace(parts[1])

    def _handle_web(self, cmd):
        parts = cmd.split()
        target = parts[1] if len(parts) > 1 else self.session_manager.target
        self.web_recon.run(target)

    def _handle_payload(self, cmd):
        # payload <type> <lhost> <lport>
        parts = cmd.split()
        if len(parts) < 4:
            print_error("Usage: payload <type> <lhost> <lport>")
            return
        self.payload_gen.generate(parts[1], parts[2], parts[3])


    def _handle_scan(self, command):
        # Basic parsing: scan <target> [--analyze] [--ports <ports>]
        parts = command.split()
        if len(parts) < 2:
            print_error("Usage: scan <target> [options]")
            return

        target = parts[1]
        analyze = "--analyze" in command
        
        # Extract ports if present (simple regex or split)
        ports = None
        if "--ports" in command:
            try:
                p_index = parts.index("--ports")
                if p_index + 1 < len(parts):
                    ports = parts[p_index+1]
            except ValueError:
                pass
        
        # Remove custom flags from arguments passed to nmap
        # We need to construct pure nmap args or just pass defaults + ports
        # For simplicity here we assume standard nmap args are passed explicitly by user?
        # The request said "scan 192.168.1.1 --ports 1-1000", implied nmap args.
        # But we mostly use defaults in scanner unless user types raw nmap flags.
        # Let's keep it simple: strict specific args we support, everything else ignored or we'd need complex parsing.
        
        scan_result = self.scanner.scan_target(target, ports=ports)
        
        if analyze and scan_result:
            print_info("analyzing results with AI...")
            ai_summary = self.scanner.format_for_ai(target, scan_result)
            prompt = f"Analyze these Nmap scan results for {target}. Explain open ports, services, and potential security risks (ethical view only). Do not suggest specific exploits.\n\n{ai_summary}"
            self._handle_chat(prompt, is_system_prompt=False, is_analysis=True)

    def _handle_chat(self, input_text, is_system_prompt=False, is_analysis=False):
        if not is_analysis:
            # Normal chat
            # print_user_msg(input_text) # Interactive shell already shows what user typed
            pass
            
        print_info("Thinking...")
        response = self.ai.chat(input_text)
        
        if response:
            self._display_ai_response(response)

    def _display_ai_response(self, response):
        """
        Parses AI response for code blocks and displays them in boxes.
        Features 'Code Detection & Copy Box'.
        """
        # Regex to find code blocks: ```language\ncode\n```
        code_block_pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
        
        last_end = 0
        matches = list(code_block_pattern.finditer(response))
        
        if not matches:
            # No code, just print explanation
            print_ai_msg(response)
            return

        print_ai_msg("") # header
        
        for match in matches:
            # Print text before code
            text_before = response[last_end:match.start()].strip()
            if text_before:
                print(text_before)
            
            # Print code box
            lang = match.group(1) or "text"
            code = match.group(2)
            print_code_box(code, language=lang, title=f"{lang.upper()} Snippet")
            
            last_end = match.end()
            
        # Print remaining text
        text_after = response[last_end:].strip()
        if text_after:
            print(text_after)

