
import pytest
import aiohttp
import asyncio
import json
from aioresponses import aioresponses

from mashup.services.music_brainz import _get_music_brainz_url
from mashup.services.cover_art import _get_cover_art_url
from mashup.services.wikipedia import _get_wiki_url, _get_wikidata_url


@pytest.mark.asyncio
async def test_get_missing_music_brainz_returns_404(client):
    with aioresponses() as mocked:
        mocked.get(_get_music_brainz_url('asd'), status=404)

        response = await client.get(f'/api/mashup/asd')

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_bad_request_music_brainz_returns_400(client):
    with aioresponses() as mocked:
        mocked.get(_get_music_brainz_url('asd'), status=400)

        response = await client.get(f'/api/mashup/asd')

        assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_artist_with_wikipedia_description(client,
                                                     music_brainz_response_with_wikipedia,
                                                     cover_art_response,
                                                     wikipedia_response):
    with aioresponses() as mocked:
        mocked.get(_get_music_brainz_url('asd'),
                   status=200, body=music_brainz_response_with_wikipedia)
        mocked.get(_get_cover_art_url('album-id'),
                   status=200, body=cover_art_response)
        mocked.get(_get_wiki_url('nirvana'),
                   status=200, body=wikipedia_response)

        response = await client.get(f'/api/mashup/asd')

        assert response.status_code == 200
        data = json.loads(await response.get_data())

        assert data['name'] == 'nirvana'
        assert data['description'] == 'some description'
        assert len(data['albums']) == 1
        assert data['albums'][0]['title'] == 'some album'


@pytest.mark.asyncio
async def test_get_artist_with_wikidata_description(client, music_brainz_response_with_wikidata, cover_art_response, wikidata_response, wikipedia_response):
    with aioresponses() as mocked:
        mocked.get(_get_music_brainz_url('asd'),
                   status=200, body=music_brainz_response_with_wikidata)
        mocked.get(_get_cover_art_url('album-id'),
                   status=200, body=cover_art_response)
        mocked.get(_get_wikidata_url('wikidata-id'),
                   status=200, body=wikidata_response)
        mocked.get(_get_wiki_url('nirvana'),
                   status=200, body=wikipedia_response)

        response = await client.get(f'/api/mashup/asd')

        assert response.status_code == 200
        data = json.loads(await response.get_data())

        assert data['name'] == 'nirvana'
        assert data['description'] == 'some description'
        assert len(data['albums']) == 1


@pytest.mark.asyncio
async def test_get_artist_with_missing_wikipedia(client, music_brainz_response_with_wikipedia, cover_art_response):
    with aioresponses() as mocked:
        mocked.get(_get_music_brainz_url('asd'),
                   status=200, body=music_brainz_response_with_wikipedia)
        mocked.get(_get_cover_art_url('album-id'),
                   status=200, body=cover_art_response)
        mocked.get(_get_wiki_url('nirvana'), status=404)

        response = await client.get(f'/api/mashup/asd')

        assert response.status_code == 200
        data = json.loads(await response.get_data())

        assert data['name'] == 'nirvana'
        assert data['description'] == ''
