from multiprocessing import Queue, Value

from loguru import logger
from transcribing.exceptions import ContinueProcessError, StopProcessError


class InfinityProcess:
    def __init__(self, log_name: str):
        self.logger_ = logger.bind(**{log_name: True})

    def handle_record(self, record_id: int) -> None:
        raise NotImplementedError

    def __call__(self, is_run: Value, queue: Queue, r_counts: Value, pr_number: int):
        while is_run.value:
            record_id = queue.get()
            try:
                self.logger_.info(f'Thread: {pr_number} Record {record_id} start process')
                self.handle_record(record_id)
                self.logger_.info(f'Thread: {pr_number} Record {record_id} success')
                r_counts.value = r_counts.value + 1
            except ContinueProcessError:
                continue
            except StopProcessError:
                break
            except Exception as e:
                self.logger_.info(f'Thread: {pr_number} Record {record_id} error: {repr(e)}')


class AbstractTask:
    def start(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError
