import requests
import os
from flask import Request, abort, send_file
from cairosvg import svg2png
from io import BytesIO


def imager(request: Request):
    url = request.args.get('url')
    token = request.args.get('token')
    if not token:
        return abort(401)
    if token != os.getenv("API_TOKEN"):
        return abort(401)
    if not url:
        return abort(401)
    svg = requests.get(url).content
    print(svg)
    return send_file(BytesIO(svg2png(bytestring=svg)), mimetype="image/png",
                     attachment_filename='hello.png')
