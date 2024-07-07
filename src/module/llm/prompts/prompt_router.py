PROMPT_INTENT_DETECTION = """# Introduction
You will present with a conversation between the user and the assistant.
Your task is categorize user's intent.

You must respond in the following structured JSON format, all fields are mandatory:
{{
    "reasoning": "a short analysis of the user's intent.",
    "intent": "one of the following: generic, report, recommendation, qna. Based on thinking from 'reasoning' step",
    "language": "primary language of user query, Vietnamese or English",
}}

# Intent explanation:
- generic: casual conversations, greetings, expressions.
- report: The user asking for current status of their farm facility.
- recommendation: The user asking for advice on their farming and planting status.
- qna: The user's requests or questions about agriculture.
- diagnose: The user asking for a diagnosis of their farming and planting status.

The user message is {message}.
"""
