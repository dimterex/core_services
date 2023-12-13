import json
from typing import Awaitable

from aiohttp.abc import Request
from aiohttp import web
from aiohttp.web_response import Response, StreamResponse

from keenetic_prometheus_exporter.models.keenetic_api import KeeneticClient
from keenetic_prometheus_exporter.models.keenetic_collecor import KeeneticCollector
from modules.core.http_server.base_executor import BaseExecutor


class GetMetricsRequestExecutor(BaseExecutor):
    def __init__(self, keeneticClient: KeeneticClient, collectors: list[KeeneticCollector]):
        self.collectors = collectors
        self.kc = keeneticClient

    async def execute(self, request: Request) -> Awaitable[StreamResponse]:
        metrics = []
        self.kc.login()
        for collector in self.collectors:
            metrics += collector.collect(self.kc)

        self.kc.logout()

        return Response(text=''.join(metrics), status=200, content_type="text")
