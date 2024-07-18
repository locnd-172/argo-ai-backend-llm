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


class ZillizCFG:
    ZILLIZDB_USERNAME = os.environ["ZILLIZDB_USERNAME"]
    ZILLIZDB_PASSWORD = os.environ["ZILLIZDB_PASSWORD"]
    ZILLIZDB_HOST = os.environ["ZILLIZDB_HOST"]
    ZILLIZDB_PORT = os.environ["ZILLIZDB_PORT"]
    ZILLIZDB_TOKEN = os.environ["ZILLIZDB_TOKEN"]
    ZILLIZDB_COLLECTION_NAME_DOCUMENTS = os.environ["ZILLIZDB_COLLECTION_NAME_DOCUMENTS"]


class AppMessages:
    SENSITIVE_MSG = {
        "english": "I can't answer sensitive content. Try another request please!",
        "vietnamese": "Tôi không thể trả lời về nội dung nhạy cảm. Hãy thử đặt câu hỏi khác!"
    }


class RetrievalCFG:
    SEARCH_INDEX = os.environ["SEARCH_INDEX"]
    SEARCH_TOP_K = os.environ["SEARCH_TOP_K"]
