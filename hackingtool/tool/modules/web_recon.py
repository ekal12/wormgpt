import requests
from tool.utils.logger import logger
from tool.utils.formatter import print_info, print_success, print_error, print_code_box, print_warning

class WebRecon:
    def __init__(self):
        pass

    def run(self, target):
        if not target:
            print_error("No target specified. Use 'target <url>' or provide URL.")
            return

        # Ensure scheme
        if not target.startswith("http"):
            url = f"http://{target}"
        else:
            url = target
            
        print_info(f"Starting Web Recon on {url}...")
        
        try:
            response = requests.get(url, timeout=10)
            
            # Extract headers
            headers = response.headers
            server = headers.get("Server", "Unknown")
            powered_by = headers.get("X-Powered-By", "Unknown")
            
            info_text = f"URL: {url}\n"
            info_text += f"Status Code: {response.status_code}\n"
            info_text += f"Server: {server}\n"
            info_text += f"X-Powered-By: {powered_by}\n"
            
            print_code_box(info_text, language="yaml", title="Web Basic Info")
            
            # Dump all headers
            header_dump = "\n".join([f"{k}: {v}" for k,v in headers.items()])
            print_code_box(header_dump, language="yaml", title="HTTP Headers")
            
            # Check robots.txt
            self._check_robots(url)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Web scan failed: {e}")
            print_error(f"Failed to connect to {url}: {e}")

    def _check_robots(self, base_url):
        robots_url = f"{base_url.rstrip('/')}/robots.txt"
        try:
            res = requests.get(robots_url, timeout=5)
            if res.status_code == 200:
                print_success("robots.txt found!")
                print_code_box(res.text, language="text", title="robots.txt")
            else:
                print_warning(f"robots.txt not found (Status {res.status_code})")
        except:
            pass
