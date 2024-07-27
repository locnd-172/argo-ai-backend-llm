PROMPT_INTENT_DETECTION = """# Introduction
You will present with a conversation between the user and the assistant.
Your task is categorize user's intent.

# Instruction
The standalone query expresses the demand of the user. Do not answer and add irrelevant information from user request.

<conversation_history>
{histories}
<conversation_history/>

You must respond in the following structured JSON format, all fields are mandatory:
{{
    "reasoning": "a short analysis of the user's intent.",
    "intent": "one of the following: generic, report, recommendation, qna. Based on thinking from 'reasoning' step",
    "language": "primary language of user query, Vietnamese or English",
    "standalone_query": "generate a standalone query expresses the user intent plus the chat histories, respond in English",
}}

# Intent explanation:
- generic: casual conversations, greetings, expressions.
- report: The user asking for current status of their farm facility.
- recommendation: The user asking for advice on their farming and planting status.
- qna: The user's requests or questions about agriculture.
- diagnose: The user asking for a diagnosis of their farming and planting status.

Intent Example:
```
user: hello
intent: generics
```
```
user: who are you
intent: generics
```
```
user: who date is it today?
intent: generics
```

The user message is: {message}.
"""
