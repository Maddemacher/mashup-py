
from quart import abort

from mashup import app
from mashup.services.mashup import MashupService
from mashup.exceptions import NotFoundError, BadRequestError

service = MashupService()


@app.route("/api/mashup/<string:music_brainz_id>")
async def mashup(music_brainz_id):
    try:
        return await service.get_mashup(music_brainz_id)
    except NotFoundError:
        abort(404)
    except BadRequestError:
        abort(400)
