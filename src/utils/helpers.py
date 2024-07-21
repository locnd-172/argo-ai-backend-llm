from datetime import datetime


def get_text_size(text, encoding='utf-8'):
    encoded_text = text.encode(encoding)
    size_in_bytes = len(encoded_text)
    size_in_megabytes = round(size_in_bytes / (1024 * 1024), 4)
    return size_in_megabytes


def get_current_date():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y")
    return formatted_time


def get_current_datetime():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_time
