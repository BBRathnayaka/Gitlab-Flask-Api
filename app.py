from os import name
from flask import Flask, render_template, request, redirect, url_for
import requests
from api import Gitlab

app = Flask(__name__)

gitlab = Gitlab()

command1 = "pwd"

@app.route("/")
def home():
    results = gitlab.get()
    # gitlab.run_command()
    username = results[0]['namespace']['name']
    return render_template("index.html",**locals())

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        domain = request.form["dname"]
        results = gitlab.create_project(domain)
        gitlab.unprotect_main(domain)
        gitlab.run_command()
        gitlab.proetct_branches(domain)
        # print(results)
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

