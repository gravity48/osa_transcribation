from datetime import datetime
from multiprocessing import Process, Queue, Value
from typing import List

from settings import QUEUE_MAX_SIZE
from transcribing.base import AbstractTask
from transcribing.processes.control_pr import ControlProcess
from transcribing.processes.keyword_pr import KeywordIdentityProcess


class KeywordTask(AbstractTask):
    def __init__(self, alias: str, thread_count: int):
        self.alias = alias
        self.thread_count = thread_count
        self.ctl_proc_base = ControlProcess(self.alias)
        self.work_proc_base = KeywordIdentityProcess(self.alias)
        self.is_run = Value('i', 1)
        self.queue = Queue(QUEUE_MAX_SIZE)
        self.r_counts = Value('i', 0)
        self.workers: List[Process] = []
        self.ctl_proc: Process = None

    def setup_db_options(
        self,
        host: str,
        port: int,
        login: str,
        password: str,
        path: str,
        provider: str = 'Postgres',
    ):
        self.ctl_proc_base.setup_database(
            host=host,
            port=port,
            login=login,
            password=password,
            path=path,
            provider_name=provider,
        )
        self.work_proc_base.setup_database(
            host=host,
            port=port,
            login=login,
            password=password,
            path=path,
            provider_name=provider,
        )

    def setup_filter(self, period_from: str, period_to: str):
        self.ctl_proc_base.setup_period(
            period_from=datetime.strptime(period_from, '%Y-%m-%dT%H:%M:%S%z'),
            period_to=datetime.strptime(period_to, '%Y-%m-%dT%H:%M:%S%z'),
        )

    def setup_ctl_options(self, selection: bool = False, post: str = '', limit: int = 10):
        self.ctl_proc_base.setup_options(selection=selection, post=post, limit=limit)

    def setup_worker_options(self, speech_time: int, percent: float, keywords: str):
        self.work_proc_base.setup_options(
            speech_time=speech_time,
            percent=percent,
            keywords=keywords.split('\n'),
        )

    def setup_recognize_client(self, host: str, port: int, name: str):
        self.work_proc_base.setup_recognize_client(host=host, port=port, name=name)

    def start(self):
        for item in range(self.thread_count):
            work_proc = Process(
                target=self.work_proc_base,
                args=(self.is_run, self.queue, self.r_counts, item),
            )
            work_proc.start()
            self.workers.append(work_proc)
        self.ctl_proc = Process(target=self.ctl_proc_base, args=(self.is_run, self.queue))
        self.ctl_proc.start()

    def status(self) -> int:
        return self.r_counts.value

    def stop(self):
        self.is_run.value = 0
        self.ctl_proc.kill()
        for worker in self.workers:
            worker.kill()
