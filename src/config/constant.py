import os

from dotenv import load_dotenv

load_dotenv()


class GeminiAiCFG:
    API_KEY = os.environ["GEMINI_API_KEY"]
    API_MODEL = os.getenv("GEMINI_API_MODEL", "gemini-pro")
    API_EMBEDDING_MODEL = os.getenv("GEMINI_API_EMBEDDING_MODEL", "models/embedding-001")


class IntentCFG:
    INTENT = "intent"
    LANGUAGE = "language"
    STANDALONE_QUERY = "standalone_query"

    GENERIC = "generic"
    SENSITIVE = "sensitive"
    REPORT = "report"
    RECOMMENDATION = "recommendation"
    QNA = "qna"
    DIAGNOSE = "diagnose"


class LanguageCFG:
    EN = "en"
    VI = "vi"
    ENGLISH = "English"
    VIETNAMESE = "Vietnamese"


class FirebaseCFG:
    FS_CERTIFICATE_PATH = "src/config/argoai-63051-firebase-adminsdk-ykwbi-a14bbb8c68.json"
    FS_COLLECTION_EMISSION_FACTORS = "emission_factors"
    FS_COLLECTION_MRV = "mrv_system"
    FS_COLLECTION_CONVERSATION = "conversations"


class ZillizCFG:
    ZILLIZDB_USERNAME = os.environ["ZILLIZDB_USERNAME"]
    ZILLIZDB_PASSWORD = os.environ["ZILLIZDB_PASSWORD"]
    ZILLIZDB_HOST = os.environ["ZILLIZDB_HOST"]
    ZILLIZDB_PORT = os.environ["ZILLIZDB_PORT"]
    ZILLIZDB_TOKEN = os.environ["ZILLIZDB_TOKEN"]
    ZILLIZDB_COLLECTION_NAME_DOCUMENTS = os.environ["ZILLIZDB_COLLECTION_NAME_DOCUMENTS"]
    ZILLIZDB_COLLECTION_NAME_HUMAN_FEEDBACKS = os.environ["ZILLIZDB_COLLECTION_NAME_HUMAN_FEEDBACKS"]


class AppMessages:
    SENSITIVE_MSG = {
        "english": "I can't answer sensitive content. Try another request please!",
        "vietnamese": "Tôi không thể trả lời về nội dung nhạy cảm. Hãy thử đặt câu hỏi khác!"
    }


class RetrievalCFG:
    SEARCH_INDEX = os.environ["SEARCH_INDEX"]
    SEARCH_TOP_K = os.environ["SEARCH_TOP_K"]
    SEARCH_THRESHOLD_RELEVANT = float(os.environ["SEARCH_THRESHOLD_RELEVANT"])

    SEARCH_INDEX_FEEDBACK = os.environ["SEARCH_INDEX_FEEDBACK"]
    SEARCH_TOP_K_FEEDBACK = os.environ["SEARCH_TOP_K_FEEDBACK"]
    SEARCH_THRESHOLD_RELEVANT_FEEDBACK = float(os.environ["SEARCH_THRESHOLD_RELEVANT_FEEDBACK"])


class EmissionCFG:
    CH4_CONVERSION_VALUE = 25
    N2O_CONVERSION_VALUE = 298
    SCALING_FACTOR_VALUE = 0.59


class SourceType:
    URL = "url"
    TEXT = "text"
    FILE = "file"


class DocumentStatus:
    ACTIVE = "active"
    INACTIVE = "inactive"


class BotDefaultMSG:
    NOT_RELATED_DOCUMENT = "not_related_document"
    CANNOT_FIND_ANSWER = "cannot_find_answer"
    NO_ANSWER_MSG = "I'm sorry! ArgoAI can not find answer for your question from our knowledge base."


class TextSplitterCFG:
    WORD_CHUNK_SIZE = 1500
    TOKEN_CHUNK_SIZE = 600
    HTML_HEADERS_TO_SPLIT_ON = [
        ("h1", "h1"),
        ("h2", "h2"),
        ("h3", "h3"),
        ("h4", "h4"),
    ]
    CHUNK_OVERLAP = 20
    MD_HEADERS_TO_SPLIT_ON = [("#" * (i + 1), "h" + str(i + 1)) for i in range(4)]
    SEPARATORS = ["\r\n", "\n", ".\n", ". ", " ", ""]


PROMPT_GUIDE_FEEDBACK = """There may be some feedbacks. A feedback contains question, answer and feedback_content. 
You should follow answers with high score feedback_content like 4/5 or 5/5, and avoid bad feedback_content ones like 0/5 or 1/5. 
You should put the feedbacks on a higher priority than given documents."""
