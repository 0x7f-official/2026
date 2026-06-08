###
Create main.py
How to Run This Locally
Check for new SDK installed: pip install google-genai

Set your API Key in your terminal: export GEMINI_API_KEY="your-key-here" (or $env:GEMINI_API_KEY="your-key-here" if you are using Windows PowerShell).

Run it using: python main.py

Test: Enter example "I'm setting up a new Python fastAPI app", Orbit State Matrix dynamically formats the top of the output.

###

import os
import sys
from google import genai
from google.genai import types

# Initialize the Gemini Client
# Expects GEMINI_API_KEY to be set in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print("Error: Please ensure GEMINI_API_KEY is set in your environment.")
    sys.exit(1)

# Global application state
current_mode = "Generalist"

# The Differentiating Feature: The State Engine Prompt
SYSTEM_INSTRUCTION_TEMPLATE = """
You are Orbit, an advanced engineering partner running in a CLI environment.
Current Operating Mode: {mode}

CRITICAL STRUCTURAL RULE:
You MUST begin every single response with the following micro-dashboard layout, 
filling in the bracketed data accurately based on the conversation history:

=== ORBIT STATE MATRIX ===
[Active Mode] {mode}
[Current Task] <Briefly state what the user is working on>
[Context Focus] <List any files or topics currently active>
=========================

Keep your prose minimal, professional, and highly scannable. Prioritize clean code blocks over long paragraphs.
"""

def query_gemini(user_input: str, force_mode: str = None):
    """Sends the conversation to Gemini wrapped with our custom State Engine instructions."""
    global current_mode
    active_mode = force_mode if force_mode else current_mode
    
    formatted_instruction = SYSTEM_INSTRUCTION_TEMPLATE.format(mode=active_mode)
    
    print("\n🪐 [Orbit] Thinking...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=formatted_instruction,
                temperature=0.3 # Low temperature for more predictable engineering answers
            )
        )
        print(f"\n{response.text}\n")
    except Exception as e:
        print(f"\n❌ Error communicating with Gemini API: {e}\n")

def run_command(command: str, args: list):
    """Handles local slash commands without sending them to the cloud."""
    global current_mode
    
    if command == "/mode":
        if args:
            current_mode = args[0].capitalize()
        else:
            current_mode = "Generalist"
        print(f"\n🪐 [Orbit] Switched workspace mode to: {current_mode}\n")
        
    elif command == "/plan":
        print(f"\n🪐 [Orbit: Architect] Requesting high-level implementation strategy...")
        architecture_prompt = (
            f"Provide a unique, modular implementation plan for our current workspace context. "
            f"Break it down into simple, manageable components."
        )
        query_gemini(architecture_prompt, force_mode="Architect")
        
    elif command == "/verify":
        print(f"\n🪐 [Orbit: Auditor] Running local validation protocols...")
        # Placeholder where you can eventually add os.system("pytest") or lint checks
        verification_prompt = "Simulate a clean code audit of our current workspace and list any potential edge cases."
        query_gemini(verification_prompt, force_mode="Auditor")
        
    elif command == "/help":
        print("\nAvailable Commands:")
        print("  /mode [Name] - Change Orbit's persona (e.g., Security, TDD)")
        print("  /plan        - Trigger an architectural breakdown task")
        print("  /verify      - Trigger a mock workspace code audit")
        print("  /help        - Show this menu")
        print("  /exit        - Close the session\n")
        
    else:
        print(f"\n❌ Unknown command: {command}. Type /help for available options.\n")

def main():
    """Main terminal execution loop."""
    print("====================================================")
    print("🪐 Orbit CLI Initialized Successfully.")
    print("Type /help to see commands, or type your message normally.")
    print("====================================================")
    
    while True:
        try:
            user_raw = input("orbit> ").strip()
            
            if not user_raw:
                continue
                
            if user_raw.lower() == "/exit":
                print("Goodbye!")
                break
                
            # Intercept slash commands
            if user_raw.startswith("/"):
                parts = user_raw.split(" ")
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                run_command(command, args)
            else:
                # Normal chat handoff to Gemini
                query_gemini(user_raw)
                
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Orbit CLI. Goodbye!")
            break

if __name__ == "__main__":
    main()
