import threading
import time
from datetime import datetime, timedelta

from core.log_service.log_service import Logger_Service


class ScheduleService(threading.Thread):

    def __init__(self, logger_Service: Logger_Service, delta: int):
        super().__init__()
        self.delta = delta
        self.logger_Service = logger_Service
        self.TAG = self.__class__.__name__
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            try:
                self.logger_Service.info(self.TAG, f'Started at {datetime.now()}')
                self.call_by_timer()
                while True:
                    current_time = datetime.now()
                    next_time = current_time + timedelta(hours=self.delta)
                    self.logger_Service.info(self.TAG, f'Next time {next_time}')
                    time.sleep((next_time - current_time).total_seconds())
                    self.call_by_timer()
            except Exception as e:
                self.logger_Service.error(self.TAG, f'Exception at {datetime.now()}: \n\t {e} ')
                self.stop()

    def call_by_timer(self):
        self.logger_Service.info(self.TAG, f'Starting called at {datetime.now()}')
        self.update()
        self.logger_Service.info(self.TAG, f'Starting called at {datetime.now()}')

    def stop(self):
        self.stop_event.set()
        self.logger_Service.warning(self.TAG, f'Stopped at {datetime.now()}')

    def update(self):
        raise Exception('Not implemented')
