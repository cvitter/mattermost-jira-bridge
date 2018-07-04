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
```

If you do not want the Flask application to be accessible from other machines you can update the host address to
`127.0.0.1`. You can also enable Flask's debug mode by changing `debug` to `true`.

## Execution

5. Run the Flask application - there are a number of ways to run the application but I use the following command that runs the application headlessly and captures output into a log file for troubleshooting:

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
