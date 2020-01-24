import json
import datetime
import requests
import re
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

import repl.utils as utils

config = utils.get_config_dict()
app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/repl/all.html', methods=['GET'])
def repl_all():
    req = requests.get("http://{}:{}/_scheduler/jobs".format(config["db"]["host"], config["db"]["port"]))
    res = req.json()

    template = utils.path_file(path=config['templates']['html'], file='all.html')
    return render_template(template, jobs=res.get("jobs", []))

@app.route('/js/<fn>', methods=['get'])
def js_folder(fn):
    app.logger.debug('hit js folder')
    return send_from_directory('static/js', fn)

@app.route('/css/<fn>', methods=['get'])
def css_folder(fn):
    app.logger.debug('hit css folder')
    return send_from_directory('static/css', fn)

@app.route('/logo/<fn>', methods=['get'])
def logo_folder(fn):
    app.logger.debug('hit logo folder')
    return send_from_directory('static/logo', fn)

@app.route('/update', methods=['post'])
def update():
    app.logger.debug('hit update')
    req = request.get_json()
    git_cmd.pull()
    app.logger.info("pulled {log}".format(log=git_cmd.log("-n 1")))
    return jsonify({'ok':True})


@app.route('/version', methods=['get'])
def version():
    app.logger.debug('hit version')
    return jsonify({'version': git_cmd.describe()})
    
if __name__ == '__main__':
    app.run(host=config['server']['host'], port=config['server']['port'])
