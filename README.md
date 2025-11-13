# Support Ticket Classification System

This project provides an automated system for classifying customer support tickets using AI. It offers two different approaches: direct script execution and an interactive ADK agent interface.

## Project Structure
```
Vonazon/
├── python_script/
│   ├── script.py         # Main classification script
│   ├── schema.py         # Data models and enums
│   ├── config.py         # Configuration settings
│   └── test_classifier.py # Unit tests
└── ticket_agent/
    └── agent.py          # ADK agent implementation
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Method 1: Direct Script Execution

Run the classifier directly for batch processing of tickets:

```bash
python -m python_script.script
```

Expected output:
```
Ticket: "My invoice shows an incorrect charge"
Category: Billing
Pushed to CRM endpoint: Success
```

### Method 2: Interactive ADK Agent

Use the conversational agent for interactive ticket classification:

```bash
adk web
```

Then interact with the agent:
```
> My invoice shows an extra charge that I didn’t authorize.

Agent:
{
  "Category": "Billing",
  "Urgency Level": "Medium",
  "Summary": "User reports an unauthorized extra charge on their invoice.",
  "Confidence Score": 1,
  "Is Ambiguous": false,
  "Original Ticket": "My invoice shows an extra charge that I didn’t authorize.",
  "Next Step": "A human agent will review this billing issue shortly."
}
```

## Features

- Automated ticket classification
- Urgency level assessment
- Ticket summarization
- Multiple interface options
- Mock CRM integration

---

## Further Enhancements

After setting up the ADK session and runner, you can extend the project with these advanced capabilities:

### 1. **Multi-Agent Architecture**

Create multiple specialized agents (e.g., `TicketClassifier`, `CRMUpdater`, `FeedbackAnalyzer`) and orchestrate them with a shared session service for context-aware collaboration.

### 2. **Persistent Session Management**

Replace the in-memory session service with a persistent backend:

#### Session and Runner

```python
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
```

## Testing

Run the test suite:
```bash
cd python_script
pytest test_classifier.py -v
```

## Configuration

The system uses the following models:
- Script: Qwen 7B (configured in `config.py`)
- ADK Agent: Qwen 3 8B (configured in `agent.py`) or Google flash agent via api key

## Error Handling

- Empty tickets are rejected
- Invalid inputs return appropriate error messages
- Network/model errors are gracefully handled

## License

[Your license information here]

## Contributing

[Your contribution guidelines here]

---

**Note**: Ensure Ollama is running locally before using either method. The system requires access to the specified language models through Ollama.

For issues or questions, please [create an issue](your-repo-link/issues).