from flask import Flask
from flask import request
import json
import requests
import events
import projects


def readConfig():
    """
    Reads config.json to get configuration settings
    """
    d = json.load(open('config.json'))

    global application_host, application_port, application_debug
    application_host = d["application"]["host"]
    application_port = d["application"]["port"]
    application_debug = d["application"]["debug"]

    global error_color, alert_color, success_color
    error_color = d["colors"]["error"]
    alert_color = d["colors"]["alert"]
    success_color = d["colors"]["success"]

    global webhook_url, mattermost_user, mattermost_icon
    webhook_url = d["mattermost"]["webhook"]
    mattermost_user = d["mattermost"]["post_user_name"]
    mattermost_icon = d["mattermost"]["post_user_icon"]

    global jira_url
    jira_url = d["jira"]["url"]


"""
------------------------------------------------------------------------------------------
Flask application below
"""
readConfig()

app = Flask(__name__)


@app.route( '/jira/<project_id>', methods = [ 'POST' ] )
def hooks(project_id):

    if len(request.get_json()) > 0:
        print(project_id)
        print(request.get_json())
    return ""

if __name__ == '__main__':
   app.run(host = application_host, port = application_port, 
           debug = application_debug)
