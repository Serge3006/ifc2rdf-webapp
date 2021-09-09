from flask import Flask, request, abort, jsonify
import os
import subprocess
import tempfile
import requests
import time

from flask_cors import CORS
from flask.helpers import make_response

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def converter():

    if request.method == "POST":

        if "data" not in request.files:
            abort(400)

        file = request.files["data"]
        filename = file.filename

        if filename[-4:] != ".ifc":
            abort(400)
        
        temporal_ifc_file = tempfile.NamedTemporaryFile(suffix=".ifc", dir="examples/ifc")
        temporal_rdf_file = tempfile.NamedTemporaryFile(suffix=".ttl", dir="examples/rdf")

        temporal_ifc_filepath = temporal_ifc_file.name
        temporal_rdf_filepath = temporal_rdf_file.name

        file.save(temporal_ifc_filepath)

        subprocess.run(["java", "-jar", "IFCtoRDF-0.4-shaded.jar", temporal_ifc_filepath, temporal_rdf_filepath])

        #server = sparql.SPARQLServer('http://172.18.0.1:9999/blazegraph/sparql', post_directly=True)

        #server.update('load <file://' + temporal_rdf_filepath + '> into graph <https://building>')

        with open(temporal_rdf_filepath, "r") as f:
            results = f.read()

        temporal_ifc_file.close()
        temporal_rdf_file.close()

        return results

    return "<h1>Welcome to the IFC to RDF Converter</h2>"


@app.errorhandler(400)
def handle_400_error(e):
    return make_response(jsonify({"error": "Mal formed request"}), 400)

@app.errorhandler(500)
def handle_500_error(e):
    return make_response(jsonify({"error": "Server error"}), 500)


if __name__ == "__main__":
    port = 5000
    app.run(host="0.0.0.0", debug=True, port=port)