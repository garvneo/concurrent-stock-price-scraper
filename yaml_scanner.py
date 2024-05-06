import importlib
import threading
import time
from multiprocessing import Queue

import yaml


class YamlScanner(threading.Thread):
    def __init__(self, PIPELINE_PATH):
        super(YamlScanner, self).__init__()
        self._pipline_path = PIPELINE_PATH
        self._queues = {}
        self._workers = {}
        self._consumers_queue = {}
        self._downstream_queues = {}

    def _load_pipeline(self):
        with open(self._pipline_path) as inFile:
            self._yaml_data = yaml.safe_load(inFile)

    def _initialize_queues(self):
        for queue in self._yaml_data["queues"]:
            queue_name = queue["name"]
            self._queues[queue_name] = Queue()

    def _initialize_workers(self):
        for worker in self._yaml_data["workers"]:
            WorkerClass = getattr(
                importlib.import_module(worker["location"]), worker["class"]
            )
            input_queue = worker.get("input_queue")
            output_queues = worker.get("output_queues")
            worker_name = worker["name"]
            num_instances = worker.get("instances", 1)

            self._downstream_queues[worker_name] = output_queues
            if input_queue is not None:
                self._consumers_queue[input_queue] = num_instances
            init_params = {
                "input_queue": self._queues[input_queue]
                if input_queue is not None
                else None,
                "output_queue": [
                    self._queues[output_queue]
                    for output_queue in output_queues
                ]
                if output_queues is not None
                else None,
            }

            input_values = worker.get("input_values")
            if input_values is not None:
                init_params["input_values"] = input_values

            self._workers[worker_name] = []
            for i in range(num_instances):
                self._workers[worker_name].append(WorkerClass(**init_params))

    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()

    def process_pipeline(self):
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()
        # self._join_workers()

    def run(self):
        self.process_pipeline()

        while True:
            total_workers_alive = 0
            worker_stats = []
            to_del = []
            for worker_name in self._workers:
                total_worker_threads_alive = 0
                for worker_thread in self._workers[worker_name]:
                    if worker_thread.is_alive():
                        total_worker_threads_alive += 1
                total_workers_alive += total_worker_threads_alive
                if total_worker_threads_alive == 0:
                    if self._downstream_queues[worker_name] is not None:
                        for output_queue in self._downstream_queues[
                            worker_name
                        ]:
                            number_of_consumers = self._consumers_queue[
                                output_queue
                            ]
                            for i in range(number_of_consumers):
                                self._queues[output_queue].put("DONE")

                    to_del.append(worker_name)

                worker_stats.append([worker_name, total_worker_threads_alive])
            print(worker_stats)
            if total_workers_alive == 0:
                break

            for worker_name in to_del:
                del self._workers[worker_name]

            time.sleep(1)
