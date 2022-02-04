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
        # url = f"https://gitlab.com/api/v4/users/buddhitha/projects/"
        url = f"https://gitlab.com/api/v4/groups/16002910/projects/"
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
    
    def get_projects_info(self,project_id):
        url = f"https://gitlab.com/api/v4/projects/{project_id}"
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

    def unprotect_main(self,project_id):
        url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches/main"
        session = Session()
        session.headers.update(headers)

        response = session.delete(url)
        return response

    def proetct_branches(self, project_id):
        main_url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches?name=main"
        preview_url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches?name=preview"
        develop_url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches?name=develop&push_access_level=40&merge_access_level=30"
        feature_url = f"https://gitlab.com/api/v4/projects/{project_id}/protected_branches?name=feature/*&push_access_level=30&merge_access_level=30"
        session = Session()
        session.headers.update(headers)

        session.post(main_url)
        session.post(preview_url)
        session.post(develop_url)
        session.post(feature_url)
        return True

    def demo(self,url):
        subprocess.run(['/home/gitlab/workspace/gitlab/script.sh', url])
