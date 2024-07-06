import os

from dotenv import load_dotenv

load_dotenv()


class MySQLCFG:
    MYSQL_HOST = os.environ["MYSQL_HOST"]
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "argo_ai")
    MYSQL_USER = os.getenv("MYSQL_USER", "username")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")


class GeminiAiCFG:
    API_KEY = os.environ["GEMINI_API_KEY"]
    API_MODEL = os.getenv("GEMINI_API_MODEL", "gemini-pro")
    API_EMBEDDING_MODEL = os.getenv("GEMINI_API_EMBEDDING_MODEL", "models/embedding-001")


class IntentCFG:
    INTENT = "intent"
    LANGUAGE = "language"

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
    FS_COLLECTION = "argo_ai_chatbot_collection"
    FS_DOCUMENT = "argo_ai_chatbot_document"


class ZillizCFG:
    ZILLIZDB_USERNAME = os.environ["ZILLIZDB_USERNAME"]
    ZILLIZDB_PASSWORD = os.environ["ZILLIZDB_PASSWORD"]
    ZILLIZDB_HOST = os.environ["ZILLIZDB_HOST"]
    ZILLIZDB_PORT = os.environ["ZILLIZDB_PORT"]
    ZILLIZDB_COLLECTION_NAME_DOCUMENTS = os.environ["ZILLIZDB_COLLECTION_NAME_DOCUMENTS"]
