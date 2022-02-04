from crypt import methods
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from requests.sessions import get_environ_proxies
from api import Gitlab

app = Flask(__name__)

gitlab = Gitlab()

@app.route("/")
def home():
    results = gitlab.get()
    gitlab.demo()
    # gitlab.run_command()
    # b = gitlab.get_branches()
    username = results[0]['namespace']['name']
    return render_template("index.html",**locals())
    # return jsonify(results)

@app.route('/help')
def help():
    return render_template("help.html",**locals())

@app.route('/get/<path>', methods=['GET'])
def get(path):
    results = gitlab.get_group_projects(path)
    return jsonify(results)

@app.route('/branches/<project_id>', methods=['GET'])
def get_branches(project_id):
    results = gitlab.get_branches(project_id)
    return jsonify(results)

@app.route('/createnew/', methods=["POST", "GET"])
def create_group_project():
    group_id  = request.args.get('group_id', None)
    Project_name  = request.args.get('Project_name', None)
    print(group_id)
    print(Project_name)
    # return("Hello")
    results = gitlab.create_group_project(Project_name,group_id)
    url = results['ssh_url_to_repo']
    ssh_url = str(url)
    gitlab.demo(ssh_url)
    print(url)
    return jsonify(results)

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        domain = request.form["dname"]
        results = gitlab.create_project(domain)
        gitlab.unprotect_main(domain)
        gitlab.run_command()
        gitlab.proetct_branches(domain)
        repo_name = results['name']
        id = results['id']
        url = results['ssh_url_to_repo']
        visi = results['visibility']
        return render_template("create.html",**locals())
    else:
        return render_template("create.html")

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(debug=True)

