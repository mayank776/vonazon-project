# --- 1. ADK Agent Import ---
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from python_script.script import classify_ticket , mock_crm_send

# --- 2. Model Configuration ---
OLLAMA_MODEL = 'ollama_chat/qwen3:8b'

if False:
    model = LiteLlm(OLLAMA_MODEL)
else:
    model = 'gemini-2.5-flash'

# --- 2. Tool Definition ---
# send_to_crm = FunctionTool(func=mock_crm_send)

# --- 3. ADK Agent ---
root_agent = Agent(
    model=model,
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
        classify_ticket,
        # send_to_crm,
    ],
)