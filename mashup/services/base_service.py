
import aiohttp

from mashup.exceptions import NotFoundError, BadRequestError


class BaseService():
    async def fetch(self, url):
        async with aiohttp.ClientSession() as client:
            async with client.get(url) as resp:
                if resp.status == 404:
                    raise NotFoundError

                if resp.status == 400:
                    raise BadRequestError

                assert resp.status == 200

                return await resp.json()
