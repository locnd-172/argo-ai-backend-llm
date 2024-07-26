from src.config.constant import ZillizCFG, RetrievalCFG, BotDefaultMSG, PROMPT_GUIDE_FEEDBACK
from src.models.search_model import SearchHybridModel
from src.module.chat_response.intent_handler.docs_qa_intent.docs_helpers import get_conversation_histories
from src.module.chat_response.intent_handler.docs_qa_intent.docs_retrieval import call_search_vector_hybrid
from src.module.databases.zillizdb.zilliz_client import ZillizClient
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_docs import PROMPT_DOCS_QA
from src.module.llm.prompts.prompt_generic import PROMPT_GENERIC
from src.utils.helpers import get_current_datetime, remove_empty_lines
from src.utils.logger import logger


def insert_docs_to_zilliz(doc):
    try:
        document = document_builder(doc)
        zilliz = ZillizClient(ZillizCFG.ZILLIZDB_COLLECTION_NAME_DOCUMENTS)
        zilliz.insert_records([document])
        return {"status": True}
    except Exception as e:
        logger.error(e)
        return {"status": False}


def document_builder(data):
    embedding = GeminiEmbeddingModel()

    doc_id = data.doc_id
    doc_name = data.doc_name.lower().strip()
    doc_content = data.doc_description

    doc_content_embedding = embedding.get_embedding(
        doc_content,
        task_type="retrieval_document",
        title="document"
    )

    document = {
        "id": doc_id,
        "source": doc_name,
        "title": doc_name,
        "content": doc_content,
        "language": "vi",
        "vector": doc_content_embedding.get("embedding"),
    }

    return document


async def get_docs_qa_response(chat_request):
    data = chat_request.data
    search_input = SearchHybridModel(
        search=chat_request.standalone_query,
        index=RetrievalCFG.SEARCH_INDEX,
        top=RetrievalCFG.SEARCH_TOP_K,
        output_fields=["id", "title", "content", "source"]
    )
    response_search = call_search_vector_hybrid(inputs=search_input)

    search_feedback_input = SearchHybridModel(
        search=chat_request.data.sender_message,
        index=RetrievalCFG.SEARCH_INDEX_FEEDBACK,
        top=RetrievalCFG.SEARCH_TOP_K_FEEDBACK,
        output_fields=["id", "query", "answer", "feedback"]
    )
    response_search_feedback = call_search_vector_hybrid(inputs=search_feedback_input)
    response_docs_qa: dict = await call_completion_qa(
        message=data.sender_message,
        language=chat_request.language,
        conversation_history=chat_request.histories,
        context=response_search,
        feedbacks=response_search_feedback
    )
    logger.info("DOCS QA ANSWER: %s", response_docs_qa)
    return response_docs_qa


async def call_completion_qa(
        message,
        language,
        conversation_history,
        context,
        feedbacks
):
    logger.info("LENGTH CONTEXT: %s", len(context))
    context = filter_threshold(context)
    logger.info("LENGTH FILTER CONTEXT: %s", len(context))

    logger.info("LENGTH FEEDBACKS: %s", len(feedbacks))
    feedbacks = filter_feedback(feedbacks)
    logger.info("LENGTH FILTER FEEDBACK: %s", len(feedbacks))
    docs_response = {}
    feedbacks_str = format_feedbacks(feedbacks)
    generic_prompt = PROMPT_GENERIC.format(
        message=message,
        language=language,
        now=get_current_datetime(),
        feedback_guide=PROMPT_GUIDE_FEEDBACK if feedbacks else "",
        feedbacks=feedbacks_str
    )

    if len(context) == 0:
        logger.info("GENERIC PROMPT: %s", generic_prompt)
        docs_response = await call_model_gemini(generic_prompt)
    else:
        context_str = format_context(contexts=context)
        histories_str = get_conversation_histories(histories=conversation_history)
        formatted_prompt = PROMPT_DOCS_QA.format(
            message=message,
            context=context_str,
            language=language,
            histories=histories_str,
            feedback_guide=PROMPT_GUIDE_FEEDBACK if feedbacks else "",
            feedbacks=feedbacks_str
        )
        logger.info("DOCS QA PROMPT: %s", formatted_prompt)
        docs_response = await call_model_gemini(formatted_prompt)

        qa_response = docs_response.get("response", "")
        source_response = docs_response.get("source", None)

        if source_response:
            qa_response += f"\n\nReference: [{source_response}]({source_response})"
            docs_response["response"] = qa_response

        if qa_response in [BotDefaultMSG.NOT_RELATED_DOCUMENT, BotDefaultMSG.CANNOT_FIND_ANSWER]:
            logger.info("GENERIC PROMPT: %s", generic_prompt)
            docs_response = await call_model_gemini(generic_prompt)

    return docs_response


def format_context(contexts):
    context_str = ""
    for context in contexts:
        title = context["title"]
        content = context["content"]
        source = context["source"]
        doc_content = ""
        doc_content += f"\t\t<title>{title}</title>\n"
        doc_content += f"\t\t<content>{content}</content>\n"
        doc_content += f"\t\t<source>{source}</source>\n"
        context_str += f"\n\t<document>\n{doc_content}\t</document>\n"

    context_str = remove_empty_lines(context_str)
    return context_str


def filter_threshold(context):
    context = [item for item in context if item.get("score") >= RetrievalCFG.SEARCH_THRESHOLD_RELEVANT]
    return context


def format_feedbacks(feedbacks):
    feedbacks_str = ""
    for feedback in feedbacks:
        query = feedback["query"]
        answer = feedback["answer"]
        feedback_text = feedback["feedback"]
        feedback_content = ""
        feedback_content += f"\t\t<query>{query}</query>\n"
        feedback_content += f"\t\t<feedback_score>{feedback_text}/5</feedback_score>\n"
        feedback_content += f"\t\t<answer>{answer}</answer>\n"
        feedbacks_str += f"\n\t<feedback>\n{feedback_content}\t</feedback>\n"

    feedbacks_str = remove_empty_lines(feedbacks_str)
    feedbacks_str = f"<feedbacks>\n\t{feedbacks_str}\n</feedbacks>"
    feedbacks_str = f"# Feedback from human:\n{feedbacks_str}"
    return feedbacks_str


def filter_feedback(feedbacks):
    feedbacks = [item for item in feedbacks if item.get("score") >= RetrievalCFG.SEARCH_THRESHOLD_RELEVANT_FEEDBACK]
    return feedbacks
