from src.config.constant import ZillizCFG, RetrievalCFG
from src.models.search_model import SearchHybridModel
from src.module.chat_response.intent_handler.docs_qa_intent.docs_helpers import get_conversation_histories
from src.module.chat_response.intent_handler.docs_qa_intent.docs_retrieval import call_search_vector_hybrid
from src.module.databases.zillizdb.zilliz_client import ZillizClient
from src.module.llm.embedding.gemini_embedding import GeminiEmbeddingModel
from src.module.llm.gemini.gemini_services import call_model_gemini
from src.module.llm.prompts.prompt_docs import PROMPT_DOCS_QA
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
    )
    response_search = call_search_vector_hybrid(inputs=search_input)
    response_docs_qa: dict = await call_completion_qa(
        message=data.sender_message,
        language=chat_request.language,
        conversation_history=chat_request.histories,
        context=response_search,
    )
    logger.info("DOCS QA ANSWER: %s", response_docs_qa)
    return response_docs_qa


async def call_completion_qa(
        message,
        language,
        conversation_history,
        context,
):
    context_str = format_context(contexts=context)
    histories_str = get_conversation_histories(histories=conversation_history)
    formatted_prompt = PROMPT_DOCS_QA.format(
        message=message,
        context=context_str,
        language=language,
        histories=histories_str
    )
    logger.info("DOCS QA PROMPT: %s", formatted_prompt)
    docs_response = await call_model_gemini(formatted_prompt)

    qa_response = docs_response.get("response")
    source_response = docs_response.get("source")
    if source_response:
        qa_response += f"\n\nReference: {source_response}"
        docs_response["response"] = qa_response

    return docs_response


def format_context(contexts):
    context_str = ""
    for context in contexts:
        title = context["title"]
        content = context["content"]
        source = context["source"]
        context_str += f"\t<title>{title}</title>\n"
        context_str += f"\t<content>{content}</content>\n"
        context_str += f"\t<source>{source}</source>\n"
        context_str += "\n-----------------------\n"

    return context_str
