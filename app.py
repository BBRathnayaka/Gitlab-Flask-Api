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
    username = results[0]['namespace']['name']
    return render_template("index.html",**locals())
    # return jsonify(results)

@app.route('/help')
def help():
    return render_template("help.html",**locals())

@app.route('/get/<project_id>', methods=['GET'])
def get(project_id):
    results = gitlab.get_projects_info(project_id)
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
    results = gitlab.create_group_project(Project_name,group_id)

    ### get id of the project and unprotect main branch
    project_id = results['id']
    print(project_id)
    gitlab.unprotect_main(project_id)

    ## run shell script
    url = results['ssh_url_to_repo']
    ssh_url = str(url)
    gitlab.demo(ssh_url)
    print(url)

    ## proetct branches
    gitlab.proetct_branches(project_id)

    ## return final project information
    info = gitlab.get_projects_info(project_id)
    return jsonify(info)

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

