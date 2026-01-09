from tool.ai.openrouter_client import OpenRouterClient
from tool.utils.formatter import print_info, print_code_box, print_error

class PayloadGenerator:
    def __init__(self, ai_client):
        self.ai = ai_client

    def generate(self, payload_type, lhost, lport):
        print_info(f"Generating {payload_type} payload for {lhost}:{lport}...")
        
        prompt = (
            f"Generate a {payload_type} reverse shell one-liner connecting to {lhost} on port {lport}. "
            "Output ONLY the raw code or command, no explanation. "
            "If it's a script, provide the full script."
        )
        
        # Use a system prompt to enforce raw output if possible, but the client method handles chat
        # so we just send the user prompt.
        
        response = self.ai.chat(prompt, system_prompt="You are a payload generator. Output only raw code.")
        
        if response:
            # The shell's main AI handler usually does code boxes, but here we want to 
            # specifically show it as a result of this command.
            # We can reuse the shell's display logic or just print it here. 
            # Since AI might wrap it in ```, let's just print the raw response in a box 
            # if likely code, or just let AI formatting handle it?
            # Actually, our `shell.py` has `_display_ai_response`, we could use that if we had access,
            # but we are in a module. Let's just assume the AI returns markdown code block and we print it.
            
            # If the response doesn't have backticks, we might want to wrap it.
            if "```" not in response:
                print_code_box(response, language=payload_type, title="Generated Payload")
            else:
                 # Clean up and print. We can just print the raw response and let user see it, 
                 # OR parse it. For now, simple print matches expected behavior.
                 print(response) 
