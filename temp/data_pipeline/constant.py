class Chunking:
    LINE_BREAK = "\r\n"
    HEADERS_TO_SPLIT_ON = [("#" * (i + 1), "Level " + str(i + 1)) for i in range(6)]
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 0
    SEPARATORS = [LINE_BREAK, "\n", ".\n", ". ", " ", ""]
    TABLE_PATTERN = ["\n.*\|.*\|(\r?\n\|.*\|)+.*\r?\n", "<table[^>]*>.*?<\/table>"]
    TOP_K_KEYWORDS = 10

    ID = "id"
    DOC_ID = "doc_id"
    DOC_NAME = "doc_name"
    DOC_TITLE = "doc_title"
    DOC_CONTENT = "doc_content"
    CATEGORY = "category"
    DOC_LANGUAGE = "doc_language"
    RELATED_LINK = "related_link"
    CHUNK_ID = "chunk_id"
    CHUNK_CONTENT = "chunk_content"
    CHUNK_LANGUAGE = "chunk_language"
    KEYWORD = "keyword"
    STATUS = "status"
    TIME_STAMP = "time_stamp"
    CHUNK = "chunk"
    METADATA = "metadata"
    TYPE = "type"
    TYPE_NAME = "name"
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LANGUAGE_DICT = {"en": "en", "vi": "vi", "ja": "ja"}


class Status:
    DRAFT = "draft"
    DELETE = "delete"
    DONE = "done"
    HARD_DELETE = "hard_delete"
