from abc import ABC

from executors.http_executor import HttpExecutor


class AbstractResource(ABC):

    def __init__(self, executor: HttpExecutor):
        self.executor = executor
