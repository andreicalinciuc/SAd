from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

import db
import service

app = Flask(__name__)
CORS(app)


# /search/<pkg_name>
# /package/<pkg_name>/<version*>/<architecture**>
# /install (json with package id list)
@app.route("/search/<pkg_name>", methods=["GET"])
def find_packages_by_name(pkg_name):
    try:
        return jsonify(db.find_packages_by_name(pkg_name)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>", methods=["GET"])
def get_packages_by_name(pkg_name):
    try:
        return jsonify(db.get_packages_by_name(pkg_name)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>", methods=["GET"])
def get_packages_by_name_version(pkg_name, pkg_version):
    try:
        return jsonify(db.get_packages_by_name_version(pkg_name, pkg_version)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>", methods=["GET"])
def get_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    try:
        return jsonify(db.get_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/package/<pkg_name>/<pkg_version>/<pkg_architecture>/download", methods=["GET"])
def download_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture):
    try:
        return send_file(
            db.download_package_by_name_version_arch(pkg_name, pkg_version, pkg_architecture),
            "application/vnd.debian.binary-package",
            as_attachment=True,
            attachment_filename="{}_{}_{}.deb".format(pkg_name, pkg_version, pkg_architecture)
        ), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


@app.route("/install", methods=["GET"])
def generate_install_script(pkg_name):
    if not request.is_json:
        return {"error": "Request is not a valid json."}, 400
    try:
        return jsonify(service.generate_install_script(request.json)), 200
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# http://localhost:5000/search/nano
# http://localhost:5000/package/nano
# http://localhost:5000/package/nano/2.9.8-1
# http://localhost:5000/package/nano/2.9.8-1/amd64
# http://localhost:5000/package/nano/2.9.8-1/amd64/download
