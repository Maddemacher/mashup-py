import pytest

import json

import mashup


@pytest.fixture
def client():
    client = mashup.app.test_client()
    yield client


@pytest.fixture
def music_brainz_response_with_neither():
    return json.dumps({
        "name": "nirvana",
        "relations": [],
        "release-groups": [
            {
                "primary-type": "Album",
                "id": "album-id"
            }
        ]
    })


@pytest.fixture
def music_brainz_response_with_wikipedia():
    return json.dumps({
        "name": "nirvana",
        "relations": [
            {
                'type': 'wikipedia',
                'url': {
                    'resource': 'http://asd/nirvana'
                }
            }
        ],
        "release-groups": [
            {
                "primary-type": "Album",
                "id": "album-id"
            }
        ]
    })


@pytest.fixture
def music_brainz_response_with_wikidata():
    return json.dumps({
        "name": "nirvana",
        "relations": [
            {
                'type': 'wikidata',
                'url': {
                    'resource': 'http://asd/wikidata-id'
                }
            }
        ],
        "release-groups": [
            {
                "primary-type": "Album",
                "id": "album-id"
            }
        ]
    })


@pytest.fixture
def cover_art_response():
    return json.dumps({
        "title": "some album",
    })


@pytest.fixture
def wikipedia_response():
    return json.dumps({
        'query': {
            'pages': {
                'some-random-number-123123123': {
                    "extract": "some description",
                }
            }
        }
    })


@pytest.fixture
def wikidata_response():
    return json.dumps({
        'entities': {
            'wikidata-id': {
                'sitelinks': {
                    'enwiki': {
                        'title': 'nirvana'
                    }
                }
            }
        }
    })
