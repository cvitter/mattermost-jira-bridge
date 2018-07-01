from flask import Flask
from flask import request
import json
import requests
import events
import projects


def read_config():
    """
    Reads config.json to get configuration settings
    """
    d = json.load(open('config.json'))

    global application_host, application_port, application_debug
    application_host = d["application"]["host"]
    application_port = d["application"]["port"]
    application_debug = d["application"]["debug"]

    global use_attachments
    use_attachments = d["features"]["use_attachments"]

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


def get_channel(project_id):
    return projects.projects.get(project_id, default="")


def send_webhook(project_id, text_out, attachment_text, attachment_color):
    """
    """
    if len(project_id) > 0:
        channel = get_channel(project_id)

    data = {
        "channel": channel,
        "text": text_out,
        "username": mattermost_user,
        "icon_url": mattermost_icon,
        "attachments": [attach_dict]
    }

    response = requests.post(
        webhook_url,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    return response


def handle_actions(project_id, json_in):

    return send_webhook(project_id, "Test text", "", "")

"""
------------------------------------------------------------------------------------------
Flask application below
"""
read_config()

app = Flask(__name__)


@app.route('/jira/<project_id>', methods=['POST'])
def hooks(project_id):

    if len(request.get_json()) > 0:
        print(project_id)
        print(json.dumps(request.get_json()))

        handle_actions(project_id, request.get_json())
    return ""

if __name__ == '__main__':
    app.run(host=application_host, port=application_port,
            debug=application_debug)
