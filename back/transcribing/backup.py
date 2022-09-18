'''
@log.catch
def run_speaker_identification(self, thread_count):
    log.info('Run speaker identification')
    futures = set()
    offset = 0
    log.info('Train models')
    thread_models = []
    for thread_id in range(thread_count):
        transcribing_models = []
        for model in self.models:
            transcribing_models.append(ModelTuple(TranscribingModel(model['path']), model['name']))
            transcribing_models[-1].model.train()
        thread_models.append(transcribing_models)
    log.info('Try read data from database')
    TASK_LIMIT = thread_count
    record_list: list = self.postwork_db.read_records_list(self.period_to, self.period_from, TASK_LIMIT)
    with ProcessPoolExecutor(max_workers=thread_count) as executor:
        for item, record in enumerate(record_list):
            futures.add(executor.submit(self._identification_proj_thread, record, thread_models[item]))
        wait(futures, return_when=ALL_COMPLETED)
        while record_list:

            for item in range(thread_count):
                futures.add(executor.submit(self._identification_proj_thread, record_list))
            completed, futures = wait(futures, return_when=FIRST_COMPLETED)
            record_list += self.postwork_db.read_records_list(self.period_to, self.period_from, TASK_LIMIT)

    log.info('speaker identification success')



    def run_transcribing_process(self, process_count):
        log.info('Run transcribing process')
        log.info('Read data from database')
        transcribing_models = []
        processes = []
        for model in self.models:
            transcribing_models.append(ModelTuple(TranscribingModel(model['path']), model['name']))
            transcribing_models[-1].model.train()
        records_list: list = self.postwork_db.read_records_list(self.period_to, self.period_from, TASK_LIMIT)
        asyncio.run(self.control_process(processes))
        while records_list:
            record = records_list.pop(-1)
            if len(processes) == process_count:
                semaphore = 1
                while semaphore:
                    for item, process in enumerate(processes):
                        if not process.is_alive():
                            processes.pop(item)
                            processes.append(
                                multiprocessing.Process(target=self._transcribing_proj_process,
                                                        args=(record, transcribing_models),
                                                        daemon=True))
                            processes[-1].start()
                            semaphore = 0
                            break
            else:
                processes.append(
                    multiprocessing.Process(target=self._transcribing_proj_process, args=(record, transcribing_models),
                                            daemon=True))
                processes[-1].start()
        for process in processes:
            process.join()
        log.info('Wait files')
        time.sleep(SLEEP_TIME)
'''
