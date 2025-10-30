import pytest
from script import classify_ticket, mock_crm_send
from schema import ClassifiedTicket, TicketCategory, UrgencyLevel
from config import QWEN_MODEL
import io
import sys

def test_classify_billing_ticket():
    ticket = "My invoice shows an extra charge that I didn't authorize."
    result = classify_ticket(ticket, QWEN_MODEL)
    
    assert isinstance(result, ClassifiedTicket)
    assert result.category == TicketCategory.BILLING
    assert result.original_ticket == ticket
    assert isinstance(result.summary, str)
    assert isinstance(result.urgency_level, UrgencyLevel)
    assert isinstance(result.urgency_reason, str)

def test_classify_technical_ticket():
    ticket = "I can't log in to my account — the system says my password is invalid."
    result = classify_ticket(ticket, QWEN_MODEL)
    
    assert isinstance(result, ClassifiedTicket)
    assert result.category == TicketCategory.TECHNICAL_ISSUE
    assert result.original_ticket == ticket

def test_classify_sales_inquiry():
    ticket = "I'd like to learn more about your premium service plans."
    result = classify_ticket(ticket, QWEN_MODEL)
    
    assert isinstance(result, ClassifiedTicket)
    assert result.category == TicketCategory.SALES_INQUIRY
    assert result.original_ticket == ticket

def test_invalid_input():
    ticket = ""  # Empty ticket
    result = classify_ticket(ticket, QWEN_MODEL)
    assert result is None

def test_mock_crm_send(capsys):
    ticket_text = "My invoice shows an extra charge that I didn't authorize."
    classified = classify_ticket(ticket_text, QWEN_MODEL)
    
    from script import mock_crm_send
    assert classified is not None

    # clear any stdout produced during classification so we only assert mock_crm_send output
    _ = capsys.readouterr()

    mock_crm_send(classified)
    
    captured = capsys.readouterr()
    expected_output = (
        f'Ticket: "{ticket_text}"\n'
        f'Category: Billing\n'
        f'Pushed to CRM endpoint: Success\n\n'
    )
    assert captured.out == expected_output