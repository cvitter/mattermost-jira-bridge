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
    with open('config.json') as config_file:
        d = json.loads(config_file.read())
    #d = json.load(open('config.json'))

    global application_host, application_port, application_debug
    application_host = d["application"]["host"]
    application_port = d["application"]["port"]
    application_debug = d["application"]["debug"]

    global use_project_to_channel_map, use_project_bugs_to_channel_map
    global use_project_to_channel_pattern, project_to_channel_pattern
    global use_bug_specific_channel, bug_channel_postfix
    global use_attachments
    use_project_to_channel_map = d["features"]["use_project_to_channel_map"]
    use_project_bugs_to_channel_map = d["features"]["use_project_bugs_to_channel_map"]
    use_project_to_channel_pattern = d["features"]["use_project_to_channel_pattern"]
    project_to_channel_pattern = d["features"]["project_to_channel_pattern"]
    use_bug_specific_channel = d["features"]["use_bug_specific_channel"]
    bug_channel_postfix = d["features"]["bug_channel_postfix"]
    use_attachments = d["features"]["use_attachments"]

    global attachment_color
    attachment_color = d["colors"]["attachment"]

    global webhook_url, mattermost_user, mattermost_icon
    webhook_url = d["mattermost"]["webhook"]
    mattermost_user = d["mattermost"]["post_user_name"]
    mattermost_icon = d["mattermost"]["post_user_icon"]

    global jira_url
    jira_url = d["jira"]["url"]


def get_project_from_json(project_key):
    with open('projects.json') as project_file:
        d = json.loads(project_file.read())
    try:
        return d[project_key]    
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""


def get_channel(project_key, issue_type):
    """
    Returns the Mattermost channel to post into based on
    settings in config.json or returns "" if no
    Mattermost channel has been configured
    """
    channel = ""
    if use_project_to_channel_map:
        if use_project_bugs_to_channel_map and issue_type.lower() == "bug":
            channel = get_project_from_json(project_key + "-bug")
        if len(channel) == 0:
            channel = get_project_from_json(project_key)
        print ("CHANNEL: " + channel)

    if use_project_to_channel_pattern and len(channel) == 0:
        channel = project_to_channel_pattern + project_key
        if use_bug_specific_channel and issue_type.lower() == "bug":
            channel += bug_channel_postfix

    return channel


def send_webhook(project_key, issue_type, text):
    """
    Sends the formatted message to the configured
    Mattermost webhook URL
    """
    if len(project_key) > 0:
        channel = get_channel(project_key, issue_type)

    data = {
        "channel": channel,
        "username": mattermost_user,
        "icon_url": mattermost_icon
    }

    if use_attachments:
        data["attachments"] = [{
            "color": attachment_color,
            "text": text
        }]
    else:
        data["text"] = text

    response = requests.post(
        webhook_url,
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    return response


def user_profile_link(user_id, user_name):
    return "[" + user_name + "](" + jira_url + \
        "secure/ViewProfile.jspa?name=" + user_id + ")"


def project_link(project_name, project_key):
    return "[" + project_name + "](" + jira_url + "projects/" + \
        project_key + ")"


def issue_link(project_key, issue_id):
    return "[" + issue_id + "](" + jira_url + "projects/" + \
        project_key + "/issues/" + issue_id + ")"


def comment_link(comment, issue_id, comment_id):
    return "[" + comment + "](" + jira_url + "browse/" + \
        issue_id + "?focusedCommentId=" + comment_id + \
        "&page=com.atlassian.jira.plugin.system.issuetabpanels%3A" + \
        "comment-tabpanel#comment-" + comment_id + ")"


def format_new_issue(event, project_key, issue_key, summary, description,
                     priority):
    return "" + \
        event + " " + issue_link(project_key, issue_key) + "\n" \
        "**Summary**: " + summary + " (_" + priority + "_)\n" \
        "**Description**: " + description


def format_changelog(changelog_items):
    """
    The changelog can record 1+ changes to an issue
    """
    output = ""
    if len(changelog_items) > 1:
        output = "\n"
    for item in changelog_items:
        output += "Field **" + item["field"] + "** updated from _" + \
                  str(item["fromString"]) + "_ to _" + \
                  str(item["toString"]) + "_\n"
    return output


def format_message(project_key, project_name, event, user_id, user_name):
    """
    """
    message = "" + \
        "**Project**: " + project_link(project_key, project_key) + "\n" \
        "**Action**: " + event + "\n" \
        "**User**: " + user_profile_link(user_id, user_name)
    return message


def handle_actions(project_key, data):
    """
    """
    message = ""

    jira_event = data["webhookEvent"]
    jira_event_text = events.jira_events.get(jira_event, "")
    issue_type = ""

    if len(jira_event_text) == 0:
        """
        Not a supported JIRA event, return None
        and quietly go away
        """
        return None

    if jira_event == "project_created":
        message = format_message(project_key, data["project"]["name"],
                                 jira_event_text,
                                 data["project"]["projectLead"]["key"],
                                 data["project"]["projectLead"]["displayName"])

    if jira_event.find("issue") > -1:
        issue_type = data["issue"]["fields"]["issuetype"]["name"]

    if jira_event == "jira:issue_created":
        message = format_message(project_key,
                                 data["issue"]["fields"]["project"]["name"],
                                 format_new_issue(jira_event_text, project_key,
                                                  data["issue"]["key"],
                                                  data["issue"]["fields"]["summary"],
                                                  data["issue"]["fields"]["description"],
                                                  data["issue"]["fields"]["priority"]["name"]),
                                 data["user"]["key"],
                                 data["user"]["displayName"])

    if jira_event == "jira:issue_updated":
        issue_event_type = data["issue_event_type_name"]
        if issue_event_type == "issue_generic" or issue_event_type == "issue_updated":
            message = format_message(project_key,
                                     data["issue"]["fields"]["project"]["name"],
                                     issue_link(project_key, data["issue"]["key"]) + " " + \
                                     format_changelog(data["changelog"]["items"]),
                                     data["user"]["key"],
                                     data["user"]["displayName"])

        formatted_event_type = events.issue_events.get(issue_event_type, "")
        if issue_event_type == "issue_commented" or issue_event_type == "issue_comment_edited":
            message = format_message(project_key,
                                     data["issue"]["fields"]["project"]["name"],
                                     issue_link(project_key, data["issue"]["key"]) + " " + \
                                     formatted_event_type + "\n" + \
                                     "**Comment**: " + \
                                     comment_link(data["comment"]["body"],
                                                  data["issue"]["key"],
                                                  data["comment"]["id"]),
                                     data["user"]["key"],
                                     data["user"]["displayName"])

        if issue_event_type == "issue_comment_deleted":
            message = format_message(project_key,
                                     data["issue"]["fields"]["project"]["name"],
                                     issue_link(project_key, data["issue"]["key"]) + " " + \
                                     formatted_event_type,
                                     data["user"]["key"],
                                     data["user"]["displayName"])

    return send_webhook(project_key, issue_type, message)


"""
------------------------------------------------------------------------------------------
Flask application below
"""
read_config()

app = Flask(__name__)


@app.route('/jira/<project_key>', methods=['POST'])
def hooks(project_key):

    if len(request.get_json()) > 0:
        print(json.dumps(request.get_json()))

        handle_actions(project_key, request.get_json())
    return ""

if __name__ == '__main__':
    app.run(host=application_host, port=application_port,
            debug=application_debug)
