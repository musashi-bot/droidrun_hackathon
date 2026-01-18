def READ_WHATSAPP_MESSAGES_GOAL():
    return """
1. Open WhatsApp using package name com.whatsapp.android
2. Go to the Chats tab.
3. Open the first chat with unread messages.
4. Read the latest unread message without sending any reply.
5. Return the following details in JSON format:

{
  "sender_name": "string",
  "message_text": "string",
  "timestamp": "string",
  "chat_type": "personal | group"
}

Output only the JSON string, do not include any other text.
"""


def CLASSIFY_MESSAGE_GOAL(message_data: dict):
    return f"""
You are a message classification agent.

Given the message below:
{message_data}

Classify it into the following fields and return JSON:

{
  "intent": "deadline | meeting | question | info | casual",
  "urgency": "high | medium | low",
  "action_required": True | False,
  "suggested_action": "calendar | reminder | reply | note | ignore"
}

Output only JSON.
"""

def CREATE_REMINDER_GOAL(reminder_text: str, time: str):
    return f"""
1. Open Google Calendar using package name com.google.android.calendar.
2. Click on create new event.
3. Enter the following details:
   - Title: {reminder_text}
   - Time: {time}
4. Save the event.
"""

def DRAFT_REPLY_GOAL(sender_name: str, reply_text: str):
    return f"""
1. Open WhatsApp using package name com.whatsapp.android.
2. Open the chat with {sender_name}.
3. Type the following reply in the message box:
"{reply_text}"
4. Do not send the message. Keep it ready for review.
"""

def DAILY_SUMMARY_GOAL(task_list: list):
    return f"""
1. Open Google Keep using package name com.google.android.keep.
2. Create a new note titled "WhatsApp Productivity Summary".
3. Add the following content:
{task_list}
4. Save the note.
"""

