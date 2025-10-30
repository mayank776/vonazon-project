import json
import ollama
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
import os
import sys

# --- 1. ADK Agent Import ---
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

OLLAMA_MODEL = 'ollama_chat/qwen3:8b'

from python_script.script import classify_ticket

root_agent = Agent(
    model=LiteLlm(OLLAMA_MODEL),
    name='triage_agent',
    description="A helpful assistant that analyzes and classifies customer support tickets.",
    instruction=(
        "You are a friendly and efficient customer support agent. "
        "When the user provides a support ticket (a problem or question), "
        "your *only* job is to use the 'analyze_support_ticket' tool to classify it. "
        "Do not try to answer the ticket yourself. "
        "After the tool returns the classification, present the results clearly to the user. "
        "Confirm that it has been received and routed."
    ),
    tools=[
        classify_ticket
    ],
)