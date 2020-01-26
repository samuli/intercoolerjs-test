#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from flask import Flask, request, render_template, jsonify
from flask_request_params import bind_request_params
import time

app = Flask(__name__, template_folder="templates")
app.before_request(bind_request_params)

data = {}
data['languages'] = {'fi': True, 'sv': True, 'en': True}
data['default_lan'] = 'fi'
data['facets'] = {
    'format':   {'label': {'fi': "Aineistotyyppi", 'sv': "Aineistotyyppi-sv", 'en': "Aineistotyyppi-en"}, 'enabled': True},
    'building': {'label': {'fi': "Organisaatio", 'sv': "Organisaatio-sv", 'en': "Organisaatio-en"}, 'enabled': True},
    'language': {'label': {'fi': "Kieli", 'sv': "Kieli-sv", 'en': "Kieli-en"}, 'enabled': True}
}
@app.route('/')
def home():
    """Landing page."""
    return render_template('/index.html', section=False, title="Lame Site")

@app.route('/general/languages', methods=['GET'])
def languages(error = False, saved = False):
    partial = True if saved or error or request.args.get("ic-request") == "true" else False
    return render_template('/general/languages.html', section="languages", data=data['languages'], default_lan=data['default_lan'], error=error, saved=saved, partial=partial)

@app.route('/general/languages', methods=['POST'])
def set_languages():
    default_lan = request.params["section-data"]["default"]
    error = False if default_lan in request.params["section-data"]["selected"] else True
    if error:
        return languages("Oletuskielen täytyy olla valittuna")

    data['default_lan'] = default_lan
    for key,val in data['languages'].items():
        data['languages'][key] = True if key in request.params["section-data"]["selected"] else False

    time.sleep(1)
    return languages(False, True)

@app.route('/general/facets', methods=['GET'])
def facets(partial = False):
    partial = True if partial or request.args.get("ic-request") == "true" else False
    return render_template('/general/facets.html', section="facets", data=data['facets'], partial=partial)

@app.route('/general/facets', methods=['POST'])
def set_facets():
    for key,val in data['facets'].items():
        data['facets'][key]['enabled'] = True if key in request.params["section-data"]["selected"] else False
    time.sleep(1)
    return facets(True)

@app.route('/general/facets/edit', methods=['GET'])
def edit_facet():
    facet = request.args.get("facet")
    return render_template("/general/facet_edit.html", data=data["facets"][facet], facet=facet, languages=[key for key,enabled in data["languages"].items() if enabled], partial=False)

@app.route('/general/facets/edit', methods=['POST'])
def save_edit_facet():
    facet = request.params["section-data"]["facet"]
    labels = request.params["section-data"]["label"]
    for lan,label in labels.items():
        data["facets"][facet]["label"][lan] = label

    time.sleep(1)

    return facets(True)
