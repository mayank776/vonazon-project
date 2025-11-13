from pydantic import BaseModel, Field
from enum import Enum


class TicketCategory(str, Enum):
    """Types of categories for a raised ticket."""

    BILLING = "Billing"
    TECHNICAL_ISSUE = "Technical Issue"
    SALES_INQUIRY = "Sales Inquiry"
    FEEDBACK = "Feedback"
    OTHER = "Other"


class UrgencyLevel(str, Enum):
    """Priority of the ticket raised."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TicketAnalysis(BaseModel):
    """Structured analysis of a support ticket."""

    category: TicketCategory = Field(description="Most likely category of the issue.")
    summary: str = Field(
        description="A concise, one-sentence summary of the user's core problem."
    )
    urgency_level: UrgencyLevel = Field(
        description="Overall urgency level: Low, Medium, or High."
    )
    urgency_reason: str = Field(
        description="A short, 1-2 sentence explanation for *why* this urgency level was assigned."
    )
    is_ambiguous: bool = Field(
        description="Set to true if the ticket is vague or could fit multiple categories, otherwise false."
    )
    confidence_score: float = Field(
        description="A self-assessed confidence score from 0.0 (total guess) to 1.0 (very certain) for the chosen category."
    )
    next_step: str = Field(
        description="The immediate follow-up action or message to relay to the user (e.g., 'A human agent will review this issue shortly.')."
    )


class ClassifiedTicket(TicketAnalysis):
    """The final classified support ticket, combining the original text with the AI's analysis."""

    original_ticket: str = Field(description="Full text of the user's support request.")
