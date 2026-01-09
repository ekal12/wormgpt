import sys
import os
# Add the project directory to sys.path to ensure modules are found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tool.cli.shell import InteractiveShell
from tool.config import BANNER_TEXT
from tool.utils.formatter import print_banner, print_error
from tool.utils.logger import logger

def main():
    # Attempt to add Nmap to PATH if not found (common issue on Windows after fresh install)
    nmap_paths = [
        r"C:\Program Files (x86)\Nmap",
        r"C:\Program Files\Nmap",
        r"C:\Nmap"
    ]
    for p in nmap_paths:
        if os.path.exists(p) and p not in os.environ['PATH']:
            os.environ['PATH'] += f";{p}"
            logger.info(f"Added {p} to PATH for this session.")

    try:
        print_banner(BANNER_TEXT)
        logger.info("Starting AI-SEC TOOL...")
        
        shell = InteractiveShell()
        
        # Check scanner availability to warn user specifically about restart
        if not shell.scanner.available:
            print_warning("If you just installed Nmap, please RESTART YOUR TERMINAL to use it.")
            
        shell.start()
        
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print_error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
