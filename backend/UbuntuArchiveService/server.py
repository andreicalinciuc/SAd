from flask import Flask, jsonify, send_file
from flask_cors import CORS

import db
from ubuntuarchive import get_all_package_lists, get_all_packages_in_list

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


@app.route("/package_id/<pkg_id>", methods=["GET"])
def get_package_by_id(pkg_id):
    try:
        return jsonify(db.get_package_by_id(pkg_id)), 200
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


@app.route("/rebuild_db", methods=["GET"])
def rebuild_db():
    try:
        pkg_lists = get_all_package_lists()
        for pkg_list in pkg_lists:
            packages = get_all_packages_in_list(pkg_list)
            db.update_packages_database(packages)
    except Exception as e:
        return jsonify({"errormsg": str(e)}), 500
    return jsonify({}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122)

# http://localhost:5000/search/nano
# http://localhost:5000/package/nano
# http://localhost:5000/package/nano/2.9.8-1
# http://localhost:5000/package/nano/2.9.8-1/amd64
# http://localhost:5000/package/nano/2.9.8-1/amd64/download
# http://localhost:5000/install
