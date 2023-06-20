import time
from datetime import datetime
from multiprocessing import Queue, Value
from typing import Dict

from loguru import logger
from transcribing.mixins import SetupSprutMixin


class ControlProcess(SetupSprutMixin):
    period_from: datetime
    period_to: datetime
    options: Dict

    def __init__(self, alias: str):
        self.logger_ = logger.bind(**{alias: True})

    def setup_period(self, period_from: datetime, period_to: datetime):
        self.period_from = period_from
        self.period_to = period_to

    def setup_options(self, selection: bool = False, post: str = '', limit: int = 10):
        self.options = dict()
        self.options['selection'] = selection
        self.options['post'] = post
        self.options['limit'] = limit

    def _get_records(self):
        while True:
            records = self.sprut_service.select_records(
                self.period_from,
                self.period_to,
                **self.options,
            )
            if records:
                return records
            time.sleep(5)

    def control_handler(self, queue: Queue):
        records = self._get_records()
        for record in records:
            self.sprut_service.mark_pre_proc_record(record)
            queue.put(record)

    def __call__(self, is_run: Value, queue: Queue):
        while is_run.value:
            try:
                self.control_handler(queue)
            except Exception as e:
                self.logger_.error(f'Read from database error {repr(e)}')
                time.sleep(5)
