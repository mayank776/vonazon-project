# --- 1. ADK Agent Import ---
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from python_script.script import classify_ticket , mock_crm_send

# --- 2. Model Configuration ---
OLLAMA_MODEL = 'ollama_chat/qwen3:8b'

if True:
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
        "When the user provides a support ticket, your *only* job is to use the 'classify_ticket' tool. "
        "Do not try to answer the ticket yourself. "
        "After the tool returns the classification, **you MUST output the final result as a SINGLE JSON object ONLY.** "
        "The JSON object must follow this strict schema, ensuring the keys and data types match exactly: "
        
        "\n\n**JSON Schema:**"
        "\n```json"
        "\n{"
        '\n  "Category": "string",'
        '\n  "Urgency Level": "string",'
        '\n  "Summary": "string",'
        '\n  "Confidence Score": "number",'
        '\n  "Is Ambiguous": "boolean",'
        '\n  "Original Ticket": "string",'
        '\n  "Next Step": "string"'
        "\n}"
        "\n```\n\n"
        
        "Map the classification results into this JSON structure. For the **'Next Step'** key, use the required closing message: 'A human agent will review this billing issue shortly.' (adjusting the category if needed)."
    ),
    tools=[
        classify_ticket,
        # send_to_crm,
    ],
)