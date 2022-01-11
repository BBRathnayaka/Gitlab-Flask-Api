from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import subprocess

token = "glpat-YJa-46Gnhyy9d1qxDXSu"
headers = {
        'Accepts': 'application/json',
        'Authorization': 'Bearer {}'.format(token),
        }

class Gitlab:
    def get(self):
        url = f"https://gitlab.com/api/v4/users/BBRathnayaka/projects/"

        session = Session()
        session.headers.update(headers)

        response = session.get(url)
        data = json.loads(response.text)
        return data
    
    def create_project(self,name):
        parameters = {
            'name': {name},
            'visibility': 'private',
            'auto_devops_enabled': 'no',
            'initialize_with_readme': 'true',
            'allow_force_push': 'true'
        }
        url = f"https://gitlab.com/api/v4/projects/"

        session = Session()
        session.headers.update(headers)

        response = session.post(url, params=parameters)
        data = json.loads(response.text)
        return data

    def unprotect_main(self,name):
        url = f"https://gitlab.com/api/v4/projects/BBRathnayaka%2f{name}/protected_branches/main"
        session = Session()
        session.headers.update(headers)

        response = session.delete(url)
        return True

    def proetct_branches(self, name):
        branches = ["main", "preview", "develop", "feature/*"]
        # for i in branches:
        # parameters = {
        #     'name': {name},
        #     'push_access_level': '40',
        #     'merge_access_level': '40'
        # }
        main_url = f"https://gitlab.com/api/v4/projects/BBRathnayaka%2f{name}/protected_branches?name=main"
        preview_url = f"https://gitlab.com/api/v4/projects/BBRathnayaka%2f{name}/protected_branches?name=preview"
        develop_url = f"https://gitlab.com/api/v4/projects/BBRathnayaka%2f{name}/protected_branches?name=develop&push_access_level=40&merge_access_level=30"
        feature_url = f"https://gitlab.com/api/v4/projects/BBRathnayaka%2f{name}/protected_branches?name=feature/*&push_access_level=30&merge_access_level=30"
        session = Session()
        session.headers.update(headers)

        session.post(main_url)
        session.post(preview_url)
        session.post(develop_url)
        session.post(feature_url)
        return True

    def run_command(self):
        # True
        stdout = subprocess.run('rm -rf /home/bbr/workspace/gitlab/*', shell = True)

        stdout = subprocess.run('git clone git@gitlab.com:BBRathnayaka/sample.git --bare /home/bbr/workspace/gitlab/sample', shell = True)
        stdout = subprocess.run("cd /home/bbr/workspace/gitlab/sample && git push --mirror git@gitlab.com:BBRathnayaka/3.git", shell = True)
        # stdout = subprocess.call('git clone git@gitlab.com:buddhitha/10.git /home/bbr/workspace/gitlab/10', shell = True)
    
        # return stdout