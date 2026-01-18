from pydantic import BaseModel, Field

class MessageClassification(BaseModel):
    intent: str = Field(description="deadline | meeting | question | info | casual")
    urgency: str = Field(description="high | medium | low")
    action_required: bool = Field(description="Whether user action is required")
    suggested_action: str = Field(
        description="calendar | reminder | reply | note | ignore"
    )
