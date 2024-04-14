
TRACE_LOG_LEVEL = 'Trace'
DEBUG_LOG_LEVEL = 'Debug'
INFO_LOG_LEVEL = 'Info'
WARNING_LOG_LEVEL = 'Warning'
ERROR_LOG_LEVEL = 'Error'


class Logger_Service:
    def trace(self, tag: str, message: str):
        self.print_message(TRACE_LOG_LEVEL, f'{tag}\t{message}')

    def debug(self, tag: str, message: str):
        self.print_message(DEBUG_LOG_LEVEL, f'{tag}\t{message}')

    def info(self, tag: str, message: str):
        self.print_message(INFO_LOG_LEVEL, f'{tag}\t{message}')

    def warning(self, tag: str, message: str):
        self.print_message(WARNING_LOG_LEVEL, f'{tag}\t{message}')

    def error(self, tag: str, message: str):
        self.print_message(ERROR_LOG_LEVEL, f'{tag}\t{message}')

    def print_message(self, level: str, message: str):
        print(f'{level}\t{message}')
