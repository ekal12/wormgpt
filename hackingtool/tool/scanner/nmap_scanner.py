import nmap
import shutil
import json
import os
import subprocess
from datetime import datetime
from tool.config import RESULTS_DIR, DEFAULT_SCAN_ARGS
from tool.utils.logger import logger
from tool.utils.formatter import print_info, print_success, print_error, print_warning

class NmapScanner:
    def __init__(self):
        # Check if nmap is installed first
        if shutil.which("nmap") is None:
            logger.warning("Nmap not found in PATH.")
            print_warning("Nmap is not installed or not in PATH. Scanning features will be disabled.")
            self.available = False
            self.nm = None
            return

        try:
            self.nm = nmap.PortScanner()
            self.available = True
        except nmap.PortScannerError as e:
             # Fallback if shutil found it but python-nmap didn't for some reason, or other issues
            logger.error(f"Nmap initialization failed: {e}")
            print_error(f"Nmap initialization failed: {e}. Scanning will be disabled.")
            self.available = False
            self.nm = None
        except Exception as e:
            logger.error(f"Unexpected Nmap error: {e}")
            print_warning(f"Could not initialize Nmap: {e}")
            self.available = False
            self.nm = None
            
        os.makedirs(RESULTS_DIR, exist_ok=True)

    def scan_target(self, target, ports=None, arguments=None):
        if not self.available:
            print_error("Nmap is not available.")
            return None

        scan_args = arguments if arguments else DEFAULT_SCAN_ARGS
        scan_ports = ports if ports else "1-1000" # Default range if not specified content
        
        print_info(f"Starting scan on {target} (Ports: {scan_ports})...")
        logger.info(f"Starting scan: target={target}, ports={scan_ports}, args={scan_args}")
        
        try:
            # We can use nm.scan but for live progress wrapping subprocess is often better, 
            # however python-nmap is requested. providing a basic spinner or just wait.
            # python-nmap is blocking by default.
            
            self.nm.scan(hosts=target, ports=scan_ports, arguments=scan_args)
            
            # Process results
            scan_data = self.nm[target] if target in self.nm.all_hosts() else None
            
            if not scan_data:
                print_warning(f"No results found for {target}. Host might be down.")
                return None
                
            self._save_results(target, scan_data)
            self._display_summary(target, scan_data)
            
            return scan_data
            
        except nmap.PortScannerError as e:
            logger.error(f"Nmap error: {e}")
            print_error(f"Nmap scan failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected scan error: {e}")
            print_error(f"An unexpected error occurred during scan: {e}")
        
        return None

    def _save_results(self, target, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{RESULTS_DIR}/scan_{target}_{timestamp}"
        
        # Save JSON
        with open(f"{filename_base}.json", "w") as f:
            json.dump(data, f, indent=4)
            
        # Save Text Summary
        with open(f"{filename_base}.txt", "w") as f:
            summary = self._format_for_file(target, data)
            f.write(summary)
            
        logger.info(f"Results saved to {filename_base}.json/txt")
        print_success(f"Results saved to {RESULTS_DIR}/")

    def _display_summary(self, target, data):
        # Clean table output using basic formatted strings or rich table if we wanted
        if 'tcp' in data:
            print(f"\nHost: {target} ({data.get('status', {}).get('state', 'unknown')})")
            print("-" * 40)
            print(f"{'PORT':<10} {'STATE':<10} {'SERVICE':<15}")
            print("-" * 40)
            for port, info in data['tcp'].items():
                print(f"{port:<10} {info['state']:<10} {info['name']:<15}")
            print("-" * 40 + "\n")

    def _format_for_file(self, target, data):
        lines = [f"Scan Results for {target}", "="*30]
        if 'tcp' in data:
            for port, info in data['tcp'].items():
                lines.append(f"Port {port}: {info['state']} - {info['name']} (Product: {info.get('product','')})")
        return "\n".join(lines)

    def format_for_ai(self, target, data):
        """Prepares a concise summary string for the AI to analyze."""
        summary = f"Nmap scan results for target {target}:\n"
        summary += f"Host Status: {data.get('status', {}).get('state', 'unknown')}\n"
        
        open_ports = []
        if 'tcp' in data:
            for port, info in data['tcp'].items():
                if info['state'] == 'open':
                    service_detail = f"{info['name']}"
                    if info.get('product'):
                        service_detail += f" ({info['product']} {info.get('version','')})"
                    open_ports.append(f"- Port {port}/tcp: {service_detail}")
        
        if open_ports:
            summary += "Open Ports:\n" + "\n".join(open_ports)
        else:
            summary += "No open TCP ports found."
            
        return summary
