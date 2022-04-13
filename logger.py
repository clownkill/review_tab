import logger
from textwrap import dedent


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, telegram_chat_id):
        super().__init__()
        err_message_text = '''%(asctime)s - %(name)s - %(levelname)s:

        %(message)s
        '''
        formatter = logging.Formatter(dedent(err_message_text))
        self.setFormatter(formatter)
        self.telegram_chat_id = telegram_chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
            chat_id=self.telegram_chat_id,
            text=log_entry
        )
