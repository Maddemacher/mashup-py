
from mashup.exceptions import NotFoundError
from mashup.services.base_service import BaseService


def _get_wiki_url(wikipedia_title):
    return f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&redirects=true&titles={wikipedia_title}'


def _get_wikidata_url(wikidata_id):
    return f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&format=json&props=sitelinks'


class WikipediaService(BaseService):
    def _get_wikipedia(self, title):
        return self.fetch(_get_wiki_url(title))

    def _get_from_wiki(self, wiki_relation):
        title = wiki_relation['url']['resource'].split('/')[-1]

        return self._get_wikipedia(title)

    async def _get_from_wikidata(self, wikidata_relation):
        wikidata_id = wikidata_relation['url']['resource'].split('/')[-1]
        wikidata_response = await self.fetch(_get_wikidata_url(wikidata_id))
        title = wikidata_response['entities'][wikidata_id]['sitelinks']['enwiki']['title']

        return await self._get_wikipedia(title)

    async def get_wikipedia_description(self, music_brainz):
        wikipedia_relation = next(
            filter(
                lambda r: r['type'] == "wikipedia", music_brainz['relations']
            ),
            None
        )

        wikidata_relation = next(
            filter(
                lambda r: r['type'] == "wikidata", music_brainz['relations']
            ),
            None
        )

        try:
            response = None
            if(wikipedia_relation):
                response = await self._get_from_wiki(wikipedia_relation)

            if(wikidata_relation):
                response = await self._get_from_wikidata(wikidata_relation)

            return list(response['query']['pages'].values())[0]['extract']

        except NotFoundError:
            return ''
