
import asyncio
import json

from mashup.services.music_brainz import MusicBrainzService
from mashup.services.cover_art import CoverArtService
from mashup.services.wikipedia import WikipediaService


class MashupService():
    music_brainz_service = MusicBrainzService()
    cover_art_service = CoverArtService()
    wikipedia_service = WikipediaService()

    async def get_mashup(self, music_brainz_id):
        music_brainz = await self.music_brainz_service.get(music_brainz_id)
        albums_future = self.cover_art_service.get_albums(music_brainz)
        wikipedia_future = self.wikipedia_service.get_wikipedia_description(
            music_brainz
        )

        return {
            'name': music_brainz["name"],
            'albums': list(await albums_future),
            'description': await wikipedia_future
        }
