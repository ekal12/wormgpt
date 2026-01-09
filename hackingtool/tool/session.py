import os
from tool.config import RESULTS_DIR
from tool.utils.logger import logger
from tool.utils.formatter import print_success, print_info

class SessionManager:
    def __init__(self):
        self.target = None
        self.workspace = "default"
        self._ensure_workspace()

    def set_target(self, target):
        self.target = target
        logger.info(f"Target set to: {target}")
        print_success(f"Target set to: {target}")

    def set_workspace(self, name):
        self.workspace = name
        self._ensure_workspace()
        logger.info(f"Workspace switched to: {name}")
        print_success(f"Workspace switched to: {name}")

    def _ensure_workspace(self):
        # Create workspace directory inside results
        path = os.path.join(RESULTS_DIR, self.workspace)
        os.makedirs(path, exist_ok=True)
    
    def get_results_dir(self):
        return os.path.join(RESULTS_DIR, self.workspace)

    def get_prompt_suffix(self):
        t = self.target if self.target else "No Target"
        return f"[Workspace: {self.workspace}]─[Target: {t}]"
