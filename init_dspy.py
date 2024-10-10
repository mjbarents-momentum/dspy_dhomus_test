import dspy
import os
from dotenv import load_dotenv

def init_dspy():
    load_dotenv()
    mini4o = dspy.LM('openai/gpt-4o-mini')
    print("DSPy initialized with GPT-4o-mini.")

if __name__ == "__main__":
    init_dspy()
