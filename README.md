# JIRA Webhook Bridge for Mattermost

This repository contains a Python Flask application that accepts webhooks from [JIRA
Server](https://www.atlassian.com/software/jira) and forwards them to the specified
channel or channels in a [Mattermost](https://mattermost.com) server via an incoming webhook.
You can configure the application to post to channels based on JIRA projects and issue type
as described below in the **Configuration** section.
 
 **Import Notes**:
 * This application has only been tested with JIRA Server 7.9.2. 
 * This application was written extremely quickly and could use additional work in the form of refactoring, the addition of error handling, and testing (including on different versions of JIRA). Please feel free to jump in and help with pull requests, issues, etc.
 * This application is an example of how to bridge JIRA webhooks to Mattermost and is not 
 meant to be used in a production environment.

# Installation, Configuration, and Execution

The following section describes how to install, configure and run the Flask application.

## Installation

The easiest way to install this application is to:

1. Log into the machine that will host the Python Flask application;
2. Clone this repository to your machine: `git clone https://github.com/cvitter/mattermost-jira-bridge.git`;

## Configuration

Once the application has been cloned it needs to be configured for your environment and
how your organization uses JIRA. The following instructions cover configuration:

1. Change directories to the application's root: `cd mattermost-jira-bridge`;
2. Make a copy of `config.sample` as `config.json`: `cp config.sample config.json`
3. Open the `config.json` file using your favorite editor (e.g. `sudo nano config.json`) and make the
edits to each section as described below:

### Application

The `application` section setups up the runtime environment of the Flask application. For most uses
you can leave this as-is or simply update the port to the desired port for your environment.

```
	"application" : {
		"host" : "0.0.0.0",
		"port" : 5007,
		"debug" : false
	}
```

If you do not want the Flask application to be accessible from other machines you can 
update the host address to `127.0.0.1`. You can also enable Flask's debug mode by 
changing `debug` to `true`.

### Features

The `features` section allows you to configure how messages map to Mattermost channels based 
on JIRA project and whether or not the issue is labeled as a bug. The channel mapping has
the following options:

* All messages are sent to the default channel configured in the Mattermost webhook;
* Messages are mapped to Mattermost channels based on mappings in the `projects.json` file;
* Messages are mapped to Mattermost channels based on a naming pattern configured in the 
`project_to_channel_pattern` setting.

Specific configuration settings are described in more detail below.

```
	"features" : {
		"use_project_to_channel_map" : true,
		"use_project_bugs_to_channel_map" : true,
		"use_project_to_channel_pattern" : true,
		"project_to_channel_pattern" : "jira-", 
		"use_bug_specific_channel" : false,
		"bug_channel_postfix" : "-bugs",
		"use_attachments" : true
	}
```

* `use_project_to_channel_map` - when set to true the application will check the `projects.json`
file and select the Mattermost channel based on the JIRA Project Key. In the example file
below the `PRJX` project key would map to the `prjx-jira' channel in Mattermost.

```
{
	"projects" : {
    	"prjx": "prjx-jira",
    	"prjx-bug": "prjx-jira-bugs",
    	"prjz": "prjz-jira"
    }
}
```

**Note**: In the example above the `prjx-jira` channel is named `PRJX: JIRA`. Mattermost converted 
the channel name to `prjx-jira` for the channel URL by replacing spaces with `-` and removing 
special characters. When specifying the channel to send messages to you need to use this
modified URL friendly format. If you need to find the correct format you can select `View Info` 
for the channel in Mattermost and select the channel portion of the URL, e.g.:
`https://mymattermostserver.com/myteam/channels/prjx-jira`.

* `use_project_bugs_to_channel_map` - when set to true the application will check the `projects.json`
file when the issue type equals `bug` and select the Mattermost channel based on the JIRA Project 
Key with `-bug` appended to it. In the example above a bug submitted in the PRJX project
would be mapped as `prjx-bug` and the corresponding message would be posted to the 
`prjx-jira-bugs` channel.

* `use_project_to_channel_pattern` - when set to true the application will prepend the value found
in the `roject_to_channel_pattern` field to the project key to generate the channel name to post
the message to.

**Notes**: 
* This setting will work if both `use_project_to_channel_map` and `use_project_bugs_to_channel_map` 
are set to true. In scenarios where the project key being tested does not have a match in the
`projects.json` folder the application will try and match the message to a folder based on
the `project_to_channel_pattern` field.
* The channel in the `project_to_channel_pattern` field must exist in Mattermost for the 
message to post.

* `project_to_channel_pattern` - 


### Colors

The `colors` section has one setting, `attachment`,  which sets the highlight color
of the message if sent as a 
[Message Attachment](https://docs.mattermost.com/developer/message-attachments.html).
**Note**: The default color that the application ships with is green.

```
	"colors" : {
		"attachment" : "#28c12b"
	}
```

### Mattermost

The `mattermost` section is used to configure the Mattermost web hook that the application
will post messages to. You can optionally add a user name and icon to override the 
default configured in Mattermost.

```
	"mattermost" : {
		"webhook" : "https://mattermost.url/hooks/webhookid",
		"post_user_name" : "JIRA",
		"post_user_icon" : ""
	}
```

### JIRA

The `jira` section has one setting for the base URL of your JIRA server. This setting is used
to generate links in messages the application posts to Mattermost.

```
	"jira" : {
		"url" : "http://jira.url:8080/"
	}
```

## Execution

Once the application is configured that are a number of ways to run it. The simplest for 
testing purposes is:

`sudo python jira.py`

For longer term execution I use the following command that runs the application headlessly 
and captures output into a log file for troubleshooting:

```
sudo python jira.py >> jira.log 2>&1 &
```


# Make this Project Better (Questions, Feedback, Pull Requests Etc.)

**Help!** If you like this project and want to make it even more awesome please contribute your ideas,
code, etc.

If you have any questions, feedback, suggestions, etc. please submit them via issues here: https://github.com/cvitter/mattermost-jira-bridge/issues

If you find errors please feel to submit pull requests. Any help in improving this resource is appreciated!

# License
The content in this repository is Open Source material released under the MIT License. Please see the [LICENSE](LICENSE) file for full license details.

# Disclaimer

The code in this repository is not sponsored or supported by Mattermost, Inc.

# Authors
* Author: [Craig Vitter](https://github.com/cvitter)

# Contributors 

Please submit Issues and/or Pull Requests.
