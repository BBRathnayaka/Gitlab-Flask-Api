from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import subprocess

token = "glpat--pDg7rv9EV9L_7LWqgAX"
headers = {
        'Accepts': 'application/json',
        'Authorization': 'Bearer {}'.format(token),
        }

class Gitlab:
    def get(self):
        url = f"https://gitlab.com/api/v4/users/buddhitha/projects/"
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        data = json.loads(response.text)
        return data

    def get_group_projects(self,path):
        url = f"https://gitlab.com/api/v4/groups/{path}/projects"
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        data = json.loads(response.text)
        return data
    
    def create_group_project(self,name,group_id):
        parameters = {
            'name': {name},
            'namespace_id': {group_id},
            'visibility': 'private',
            'auto_devops_enabled': 'no',
            'initialize_with_readme': 'true',
            'allow_force_push': 'true'
        }
        # url = f"https://gitlab.com/api/v4/projects?name={name}&namespace_id={group_id}"
        url = f"https://gitlab.com/api/v4/projects/"
        session = Session()
        session.headers.update(headers)
        response = session.post(url, params=parameters)
        data = json.loads(response.text)
        return data

    def get_branches(self,name):
        url = f"https://gitlab.com/api/v4/projects/{name}/repository/branches"
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

    def demo(self,url):
        # stdout = subprocess.run('bash /home/bbr/workspace/gitlab/script.sh',{url}, shell = True)
        # stdout = subprocess.run('echo `date`',{url}, shell = True)
        subprocess.run(['/home/bbr/workspace/gitlab/script.sh', url])


    def run_command(self):
        stdout = subprocess.run('rm -rf /home/bbr/workspace/gitlab/*', shell = True)
        # stdout = subprocess.run('git clone git@gitlab.com:BBRathnayaka/sample.git --bare /home/bbr/workspace/gitlab/sample', shell = True)
        # stdout = subprocess.run("cd /home/bbr/workspace/gitlab/sample && git push --mirror git@gitlab.com:BBRathnayaka/3.git", shell = True)
    