def READ_WHATSAPP_MESSAGES_GOAL():
    return """
You are a WhatsApp message reading agent. Your task is to read ONE message and stop.

EXECUTION STEPS:
1. Open WhatsApp (package: com.whatsapp.android)
2. Navigate to "Chats" tab
3. Find the FIRST chat with an unread badge/indicator
4. Tap to open that chat
5. Read the LAST message in the conversation (the most recent one)
6. Immediately close the chat
7. STOP - Do not proceed to other chats

CRITICAL RULES:
- Read ONLY ONE message from ONE chat
- Do NOT scroll through messages
- Do NOT open multiple chats
- Do NOT send any replies
- Exit WhatsApp after reading

OUTPUT REQUIRED:
Extract these details from the message you read:
- sender_name: The contact or group name
- message_text: The exact text of the message
- timestamp: The time shown next to the message
- chat_type: "personal" or "group"

TERMINATION:
After extracting the message details, close WhatsApp and stop all actions.
"""


def CLASSIFY_MESSAGE_GOAL(message_data: dict):
    return f"""
You are a message classification agent. Analyze this message ONCE and provide a decision.

MESSAGE TO CLASSIFY:
Sender: {message_data.get('sender_name', 'Unknown')}
Text: {message_data.get('message_text', '')}
Time: {message_data.get('timestamp', '')}
Type: {message_data.get('chat_type', 'personal')}

CLASSIFICATION TASK:
Determine the following without any external action:

1. intent: What is the primary purpose?
   - "deadline" = time-sensitive task or commitment
   - "meeting" = scheduling or event coordination
   - "question" = requires information or answer
   - "info" = sharing information only
   - "casual" = social/informal chat

2. urgency: How time-sensitive is it?
   - "high" = needs response within hours
   - "medium" = needs response within 1-2 days
   - "low" = can wait or is not time-sensitive

3. action_required: Does this need a response or action? (true/false)

4. suggested_action: What should be done?
   - "calendar" = schedule/deadline to add to calendar
   - "reminder" = task to remember
   - "reply" = needs a response message
   - "note" = save for reference
   - "ignore" = no action needed

RULES:
- Make a single-pass decision based on the information above
- Do NOT perform any actual actions (don't open apps, don't send messages)
- Do NOT loop or re-evaluate
- Stop immediately after producing the classification

Output only the classification JSON, no additional text.
"""


def CREATE_REMINDER_GOAL(reminder_text: str, time: str):
    return f"""
You are a calendar reminder creation agent.

TASK: Create ONE calendar event and stop.

STEPS:
1. Open Google Calendar (package: com.google.android.calendar)
2. Tap the "+" or "Create" button
3. Select "Event" or "Reminder"
4. Enter title: "{reminder_text}"
5. Set time: {time}
6. Save the event
7. STOP immediately after saving

RULES:
- Create ONLY ONE event
- Do NOT edit existing events
- Do NOT create multiple reminders
- Do NOT navigate to other screens after saving

TERMINATION:
Once the event is saved and visible in the calendar, stop all actions.
Return to idle state.
"""


def DRAFT_REPLY_GOAL(sender_name: str):
    return f"""
You are a WhatsApp reply drafting agent.

TASK: Draft a reply message WITHOUT sending it.

STEPS:
1. Open WhatsApp (package: com.whatsapp.android)
2. Navigate to the chat with "{sender_name}"
3. Read the most recent message to understand context
4. Tap the message input field
5. Type a brief, appropriate reply
6. DO NOT tap the send button
7. STOP - Leave the draft in the input field

CRITICAL RULES:
- Draft the reply but DO NOT SEND
- Keep the reply concise and professional
- Do NOT navigate away from this chat
- Do NOT open other conversations

TERMINATION:
Stop immediately after the draft text is visible in the input field.
The user will review and send manually.
"""


def DAILY_SUMMARY_GOAL(task_list: str):
    return f"""
You are a note creation agent for Google Keep.

TASK: Create ONE summary note and stop.

STEPS:
1. Open Google Keep (package: com.google.android.keep)
2. Tap the "+" or "New Note" button
3. Enter title: "WhatsApp Summary - Today"
4. Enter content:
{task_list}
5. Save the note (usually automatic or tap checkmark)
6. STOP immediately

RULES:
- Create ONLY ONE note
- Do NOT create duplicate notes
- Do NOT edit existing notes
- Do NOT navigate further

TERMINATION:
Once the note is saved and visible in the notes list, stop all actions.
"""