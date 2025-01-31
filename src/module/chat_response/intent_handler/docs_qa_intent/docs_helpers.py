from src.utils.logger import logger


def get_conversation_histories(histories):
    last_conv = histories[-1] if len(histories) > 0 else []
    conv_str = ""
    logger.info("last conv: {}".format(last_conv))
    if len(last_conv) > 0:
        user_message = last_conv['user']
        bot_message = last_conv['bot']
        bot_message = [item.strip() for item in bot_message.split(".")]
        bot_message = bot_message[0]
        if len(bot_message) > 100:
            bot_message = bot_message[:100]
        conv_str = f"""user: {user_message}
bot: {bot_message}
"""
    return conv_str
