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

## Prerequisites

- Python 3.8+
- Ollama installed and running locally
- Required Python packages:
  ```bash
  pip install -r requirements.txt
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
cd python_script
python script.py "My invoice shows an incorrect charge"
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
cd ticket_agent
python -m google.adk.cli agent.py
```

Then interact with the agent:
```
> I need help with my login
Agent: I'll help classify your support ticket.
[Analyzing ticket...]
Category: Technical Issue
Your ticket has been received and routed to our technical support team.
```

## Features

- Automated ticket classification
- Urgency level assessment
- Ticket summarization
- Multiple interface options
- Mock CRM integration

## Testing

Run the test suite:
```bash
cd python_script
pytest test_classifier.py -v
```

## Configuration

The system uses the following models:
- Script: Qwen 7B (configured in `config.py`)
- ADK Agent: Qwen 3 8B (configured in `agent.py`)

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