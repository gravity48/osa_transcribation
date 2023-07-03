from multiprocessing import Process, Queue, Value

from loguru import logger

from .control_pr import control_process
from .keyword_pr import keyword_identification_process
from .pause_identify_pr import pause_identification_process
from .transcribing_pr import transcribing_process


class TranscribingTask:
    @staticmethod
    def options_parse(options):
        keywords = options.get('keywords', [])
        if keywords:
            keywords = keywords.split('\n')
        try:
            percent = options['recognize_percent']
            percent /= 100
        except KeyError:
            percent = 0.9
        return keywords, percent

    def __init__(
        self,
        db,
        model,
        task_type,
        alias,
        period_from,
        period_to,
        thread_count,
        time_processing,
        options,
        *args,
        **kwargs,
    ):
        self.db_init = db
        self.period_to = period_to
        self.period_from = period_from
        self.models = model
        self.thread_count = thread_count
        self.time_processing = time_processing
        self.alias = {alias: True}
        self.options = options
        self.keywords, self.percent = self.options_parse(self.options)
        # self.spk_model = kwargs['spk_model']
        self.log = f'logs/{alias}.log'
        self.task_logger = logger.add(
            self.log,
            filter=lambda record: alias in record["extra"],
            format="{time} {level} {message}",
            level="INFO",
        )
        self.process_pool = []
        self.control_process = None
        self.records_processed = Value('i', 0)
        self.is_run = Value('i', 1)

    def stop(self):
        self.is_run = 0
        self.control_process.kill()
        for process in self.process_pool:
            process.kill()
        logger.remove(self.task_logger)

    def status(self):
        context = {
            'record_processed': self.records_processed.value,
            'is_running': True,
        }
        return context

    def transcribing(self):
        logger.bind(**self.alias).info('Run transcribing')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(
                    target=transcribing_process,
                    args=(
                        queue,
                        self.is_run,
                        self.db_init,
                        self.models,
                        self.alias,
                        item,
                        self.records_processed,
                        self.options['speech_time'],
                    ),
                ),
            )
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(
            target=control_process,
            args=(queue, self.is_run, self.db_init, self.period_from, self.period_to, self.alias),
        )
        self.control_process.start()

    def pause_identification(self):
        logger.bind(**self.alias).info('Run pause identification')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(
                    target=pause_identification_process,
                    args=(
                        queue,
                        self.is_run,
                        self.db_init,
                        self.alias,
                        item,
                        self.records_processed,
                        self.options['speech_time'],
                    ),
                ),
            )
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(
            target=control_process,
            args=(queue, self.is_run, self.db_init, self.period_from, self.period_to),
        )
        self.control_process.start()
        pass

    def search_keywords(self):
        logger.bind(**self.alias).info('Run search keywords')
        logger.bind(**self.alias).info('Run processes')
        queue = Queue()
        for item in range(self.thread_count):
            self.process_pool.append(
                Process(
                    target=keyword_identification_process,
                    args=(
                        queue,
                        self.is_run,
                        self.db_init,
                        self.models,
                        self.alias,
                        item,
                        self.records_processed,
                        self.options['speech_time'],
                        self.keywords,
                        self.percent,
                    ),
                ),
            )
            self.process_pool[-1].start()
        logger.bind(**self.alias).info('Read data from database')
        self.control_process = Process(
            target=control_process,
            args=(queue, self.is_run, self.db_init, self.period_from, self.period_to, self.alias),
        )
        self.control_process.start()
