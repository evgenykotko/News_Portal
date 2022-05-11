import logging

class CustomFormatter(logging.Formatter):
    default_fmt = logging.Formatter('{asctime} : {levelname} - {message}', style='{')
    warn_fmt = logging.Formatter('{asctime} : {levelname} - {message} - {pathname}', style='{')
    errandcrit_fmt = logging.Formatter('{asctime} : {levelname} - {message} - {pathname} - {exc_info}', style='{')

    def format(self, record):
        if record.levelno == logging.DEBUG:
            return self.default_fmt.format(record)
        elif record.levelno == logging.INFO:
            return self.default_fmt.format(record)
        elif record.levelno == logging.WARNING:
            return self.warn_fmt.format(record)
        elif record.levelno == logging.ERROR or logging.CRITICAL:
            return self.errandcrit_fmt.format(record)