import ssl
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import certifi
from aiohttp import ClientResponse
from vkbottle.api import API
from vkbottle.bot import Bot
from vkbottle.http import AiohttpClient

from app.handlers import labeler
from config import API_KEY, state_dispenser


class SSLAiohttpClient(AiohttpClient):
    def __init__(self, ssl_context: ssl.SSLContext, **session_params):
        super().__init__(**session_params)
        self.ssl_context = ssl_context

    @asynccontextmanager
    async def request(
            self,
            url: str,
            method: str = "GET",
            data: dict[str, Any] | None = None,
            **kwargs,
    ) -> AsyncGenerator[ClientResponse, None]:
        kwargs.setdefault("ssl", self.ssl_context)
        async with super().request(url, method, data, **kwargs) as response:
            yield response


ssl_context = ssl.create_default_context(cafile=certifi.where())

http_client = SSLAiohttpClient(
    ssl_context=ssl_context,
    trust_env=True,
)

api = API(token=API_KEY, http_client=http_client)

bot = Bot(api=api, state_dispenser=state_dispenser)
bot.labeler.load(labeler)

bot.run_forever()
