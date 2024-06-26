import os

from dotenv import load_dotenv

load_dotenv()


class GeminiAiCFG:
    API_KEY = os.environ["GEMINI_API_KEY"]
    API_MODEL = os.getenv("GEMINI_API_MODEL", "gemini-pro")
    API_EMBEDDING_MODEL = os.getenv("GEMINI_API_EMBEDDING_MODEL", "models/embedding-001")


class ZillizCFG:
    ZILLIZDB_USERNAME = os.environ["ZILLIZDB_USERNAME"]
    ZILLIZDB_PASSWORD = os.environ["ZILLIZDB_PASSWORD"]
    ZILLIZDB_HOST = os.environ["ZILLIZDB_HOST"]
    ZILLIZDB_PORT = os.environ["ZILLIZDB_PORT"]
    ZILLIZDB_COLLECTION_NAME_DOCUMENTS = os.environ["ZILLIZDB_COLLECTION_NAME_DOCUMENTS"]


class IntentCFG:
    INTENT = "intent"
    LANGUAGE = "language"

    GENERIC = "generic"
    SENSITIVE = "sensitive"
    REPORT = "report"
    RECOMMENDATION = "recommendation"
    QNA = "qna"


class LanguageCFG:
    EN = "en"
    VI = "vi"

    ENGLISH = "English"
    VIETNAMESE = "Vietnamese"
