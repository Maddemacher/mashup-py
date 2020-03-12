
import asyncio

from mashup.exceptions import NotFoundError, BadRequestError
from mashup.services.base_service import BaseService


def _get_cover_art_url(album_id):
    return f'http://coverartarchive.org/release-group/{album_id}'


class CoverArtService(BaseService):

    async def get_album(self, album_id):
        try:
            return await self.fetch(_get_cover_art_url(album_id))
        except NotFoundError:
            return {
                'album_id': album_id,
                'status': 'missing'
            }

    async def get_albums(self, music_brainz):
        album_futures = list(map(lambda a: self.get_album(a['id']), filter(
            lambda a: a['primary-type'] == 'Album',
            music_brainz['release-groups']
        )))

        return await asyncio.gather(*album_futures)
