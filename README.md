# 2026
2026 Projects

# Orbit CLI: A Gemini-Native Developer Harness

Orbit CLI is a lightweight, single-responsibility development assistant built in Python. Instead of using complex automated tool hooks, it leverages a strict structural design based on **State, Commands, and Context** to bridge the gap between your terminal and the Gemini API.

## Features
- **Dynamic State Matrix:** Forces the AI to explicitly track the engineering context at the top of every single response.
- **Explicit Command Router:** Intercepts terminal commands starting with a slash (`/`) to run local workspace tasks or pivot agent focus.
- **Python-Native Architecture:** Built using the clean, modern `google-genai` SDK.

## Project Structure
