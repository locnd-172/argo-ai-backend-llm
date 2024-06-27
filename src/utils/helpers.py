from datetime import datetime


def get_current_date():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y")
    return formatted_time

def get_current_datetime():
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_time