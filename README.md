## Installation 🔧

Clone the repository in a your work folder.

## Configuration

### Create a virtual environment
```
python -m venv .venv
```
### Activate virtul environment

#### Windows
```
.venv\Scripts\activate
```
#### Linux
```
source .venv/bin/activate
```
### Download all packages required
```
pip install -r requirements.txt
```
### Create an environment file

You must create a .env file for project configuration. It must contain following variables:

```
[path]
PATH_FILL_DATABASE = 
PATH_CREATE_REPORT = 
ROOT_INPUT_PATH = 
[dataBase]
SERVER_NAME = 
DB_NAME = 
USER = 
PASSWORD = 
TABLE_NAME = 
# Date format: YY-MM-DD or today
DATE_CONSULT = today
[email]
USERNAME = 
PASSWORD = 
PORT = 587
SERVER = smtp.gmail.com
# List of mails 
RECIPIENTS = 
SUBJECT= 
MESSAGE_FILE = message.txt
```
### Create a body email message file called message.txt with a custom text

## Running tests

## Run app
```
python run.py
