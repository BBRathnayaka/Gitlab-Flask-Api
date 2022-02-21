
# Gitlab Flask API

This API creates project in specified project group with all the brances and access level permissions and push the sample wordpress folder structure.

## Api.py

api.py file includes all the functions called by gitlab API.

Create a access token in gitlab.com and replace the token varibale in the api.py file.

token = "XXXX-XXXX-XXXX"

Shell script is called in the demo function , Replace the path as required in api.py demo fuction.

## Installation

#### Requirements

- Python 2.7. x or 3.4 and above
- Python development libraries - included in requirements.txt
- PIP3
- virtualenv

#### Steps

cd to the project directory
Activate your Python environment and install Flask using the pip package installer.
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```


