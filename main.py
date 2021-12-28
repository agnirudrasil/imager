from re import M
import requests
import os
from flask import Request, abort, send_file
from cairosvg import svg2png
from io import BytesIO
import numpy as np
from PIL import Image
from cvutils import *

def to_svg(url):
    svg = requests.get(url).content
    return BytesIO(svg2png(bytestring=svg))

def to_bytes(img):
    image = Image.fromarray((img).astype(np.uint8))
    bytes = BytesIO()
    image.save(bytes, format='PNG')
    bytes.seek(0)
    return bytes


def imager(request: Request):
    url = request.args.get('url')
    token = request.args.get('token')
    task = request.args.get('task')

    if not token:
        return abort(401)
    if token != os.getenv("API_TOKEN"):
        return abort(401)
    if not url:
        return abort(401)
    if not task:
        return abort(401)
    
    if task == "svg":
        bytes = to_svg(url)


    elif task == "effects":
        img = GnP(url)
        name = request.args.get('name')
        if not name:return abort(401)
        if name == "cartoonify": img = cartoonify(img)
        elif name == "negative": img = negative(img)
        elif name == "econify": img = econify(img)
        elif name == "watercolor": img = watercolor(img)
        elif name == "pencil": img = pencil(img)
        elif name == "canny": img = canny_img(img)
        else: return abort(401)
        bytes = to_bytes(img)

    elif task == "st":
        img = GnP(url)
        model_name = request.args.get('model')
        if not model_name:return abort(401)

        model = getmodel(model_name)

        if not model:abort(401)
        
        img = style_transfer(img, model)
        bytes = to_bytes(img)



    return send_file(bytes, mimetype="image/png",
                     attachment_filename='hello.png')
