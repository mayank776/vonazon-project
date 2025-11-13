import json
from pydantic import BaseModel , Field
from typing import Optional
import ollama

from .schema import ClassifiedTicket , TicketAnalysis
from .config import QWEN_MODEL , LLAMA_MODEL

client = ollama.Client()
# IMPORTANT: Change to whichever model you have pulled
# (e.g., 'QWEN_MODEL', 'LLAMA_MODEL')
MODEL_TO_USE = QWEN_MODEL

def classify_ticket(ticket_text: str) -> Optional[ClassifiedTicket]:
    """
    Classifies a single support ticket using a local Ollama model.
    """
    # Reject empty/whitespace input early so tests expecting None pass
    if ticket_text is None or not str(ticket_text).strip():
        return None

    print("\n" + "="*60)
    print(f"   🔍  Classifying Ticket:  {ticket_text}")
    print("="*60 + "\n")


    system_prompt = f"""
    You are a highly efficient AI Triage Specialist. Your task is to analyze incoming user support tickets. You must classify them, assess their urgency, and provide a concise summary.

    You MUST respond *only* with a valid JSON object that strictly adheres to the following JSON Schema. Do not add any explanatory text before or after the JSON.

    **JSON Schema:**
    {TicketAnalysis.model_json_schema()}

    ---
    **Classification Rules:**

    * **category:**
        * `BILLING`: For any issue related to invoices, charges, refunds, or payments.
        * `TECHNICAL_ISSUE`: For errors, bugs, "can't log in", "app crashing", or "feature not working".
        * `SALES_INQUIRY`: For questions about pricing, plans, upgrades, or new features.
        * `FEEDBACK`: For user suggestions, opinions, or general praise/complaints.
        * `OTHER`: Use this only as a last resort if no other category fits.

    * **summary:**
        * Write a single, concise sentence that captures the user's *core problem*.

    * **urgency_level:**
        * `HIGH`: User is blocked *now*. (e.g., "cannot log in", "app crashing", "fraudulent charge").
        * `MEDIUM`: Time-sensitive but not a critical blocker. (e.g., "incorrect invoice", "when is my refund?").
        * `LOW`: General questions or feedback. (e.g., "how does X work?", "I have a feature idea").

    * **urgency_reason:**
        * In one sentence, *justify* your `urgency_level` choice, referencing the user's problem.

    * **is_ambiguous:**
        * Set to `true` if the user's request is very vague (e.g., "it's broken", "help") or if it's a 50/50 split between categories.
        * Set to `false` if the intent is reasonably clear.

    * **confidence_score:**
        * Give a score from 0.0 to 1.0.
        * Use 1.0 for a perfect match (e.g., "invoice" -> BILLING).
        * Use 0.5 for a guess (e.g., "my account" -> could be TECHNICAL or BILLING).
        * Use 0.0 for a total guess on a vague ticket.
    
    * **next_step:**
        * Provide the immediate follow-up action or message to relay to the user.
        * For example, for a billing issue, use: 'A human agent will review this billing issue shortly.'
    ---
    """

    try:
        response = client.chat(
            model=MODEL_TO_USE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": ticket_text}
            ],
            format="json",
            options={
                "temperature": 0.0
            }
        )
        
        json_response = response['message']['content']
        print("\n" + "="*60)
        print(f"   MODEL RESPONSE:  {json_response}")
        print("="*60 + "\n")
        
        analysis = TicketAnalysis.model_validate_json(json_response)

        classified = ClassifiedTicket.model_construct(
            **analysis.model_dump(),
            original_ticket=ticket_text
        )
        
        # print(f"[Classified Ticket]: {classified.json()}")
        return classified

    except json.JSONDecodeError:
        print(f"[Error]: Model did not return valid JSON.")
        return None
    except Exception as e:
        print(f"[Error] An unexpected error occurred: {e}")
        return None

# --- 3. The Main Workflow (Identical to before) ---

def mock_crm_send(ticket: ClassifiedTicket):
    """Simulates sending the categorized result to a mock CRM."""
    print(f'Ticket: "{ticket.original_ticket}"')
    print(f'Category: {ticket.category.value.title()}')
    print(f'Pushed to CRM endpoint: Success')
    print()  # Empty line for better readability between tickets

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    support_tickets = [
        "My invoice shows an extra charge that I didn’t authorize.",
        "I’d like to learn more about your premium service plans.",
        "When will my refund be processed? This is holding up my entire accounting department!",
        "The app keeps crashing every time I click the 'submit' button.",
        "The add to cart button could be bigger for better usability.",
        "How to update the delivery details after shipping?",
        "Could delivery details be changed after order is shipped?",
    ]
    
    categorized_tickets = []
    for ticket in support_tickets:
        classified = classify_ticket(ticket)
        if classified:
            categorized_tickets.append(classified)
            mock_crm_send(classified)
        
    print("\n=== All tickets processed. ===")