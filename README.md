# NEBULA API

## How to start
- Clone this repository
`git clone https://github.com/Squirrel-Network/api_nebula`

- Creating Virtual Environments
`python3 -m venv env`

- Activate Virtual Environments
`source env/bin/activate`

- Install requirements
`pip install -r requirements.txt`

- `python3 api.py`

## API Endpoints
- BLACKLIST: `example.com/blacklist?tgid=123456789 (Public API)`
- USERS: `example.com/users?limit=10&token=XXXXXXX (Private API)`
- USER: `example.com/user?tgid=123456789&token=XXXXXXX (Private API)`
- DELETE USER: `example.com/delete_user?tgid=123456789&token=XXXXXXX (Private API)`