import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.prompt_builder import build_prompt

prompt = build_prompt(question="I forgot my password", context="Password reset procedure...")

print(prompt)