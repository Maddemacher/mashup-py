
from mashup.exceptions import NotFoundError, BadRequestError
from mashup.services.base_service import BaseService

headers = {
    "User-Agent": "mashup-py"
}


def _get_music_brainz_url(music_brainz_id):
    return f'https://musicbrainz.org/ws/2/artist/{music_brainz_id}?fmt=json&inc=url-rels+release-groups'


class MusicBrainzService(BaseService):
    def get(self, music_brainz_id):
        return self.fetch(_get_music_brainz_url(music_brainz_id))
