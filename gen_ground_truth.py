import asyncio
import time
from datetime import date
import pandas as pd
from src.module.llm.gemini.gemini_services import call_model_gemini

GEN_QUESTION_PROMPT = """You are a farmer trying to learn and discover about agriculture, farming, specific in sustainable agriculture.
# Instruction
You are given the documents which contains information about farming and agriculture knowledge, guideline.
You will ask about those documents as farmer's perspective.
The questions MUST be independent, not dependent on each other, SHORT, and SHOULD not be vague or unclear about what is mentioned.
A good question has a maximum of about 15 words.

### REMEMBER
1. Must have questions about overall subject/topic of the document and questions about document use case.
2. Questions are prohibited from using pronouns or articles to replace the previous subject.
3. Don't answer the questions.
4. When reading the question, you will be able to identify which document the first time.
5. Don't include document name in the generated question.

No yapping.

Your response should be in JSON format with the following mandatory fields:
{{
    "questions": "List of 3 question base on provided content in {language}.",
}}

Generate 3 questions in {language} about the following content:
{content}
"""


def expand_df(data):
    data['question'] = data['question'].str.split('\n')
    df_expanded = data.explode('question').reset_index(drop=True)
    return df_expanded


def export_to_excel(data, result, output):
    data["question"] = result
    data = expand_df(data)
    data.to_excel(output, index=False)


async def gen_question(input, output):
    data = pd.read_excel(input)
    contexts = data["content"].tolist()
    result = []
    for context in contexts:
        print(context)
        time.sleep(1)
        formatted_prompt = GEN_QUESTION_PROMPT.format(
            language="vietnamese",
            content=context
        )
        gemini_response = await call_model_gemini(formatted_prompt)
        questions = gemini_response.get("questions", [])
        questions_str = "\n".join(questions)
        print(questions_str)
        result.append(questions_str)
        print("-------------------")

    export_to_excel(data, result, output)


if __name__ == "__main__":
    formatted_date = date.today().strftime("%Y%m%d")
    name = "kb_data"
    input = f"./{name}.xlsx"
    output = f"./{formatted_date}_gt_{name}.xlsx"

    asyncio.run(gen_question(input, output))
