"""
Dictionary of supported JIRA events and output friendly format
"""
jira_events = {
    "project_created": "New Project Created",
    "jira:issue_created": "New Issue Created",
    "jira:issue_updated": "Issue Updated"
}

issue_events = {
    "issue_commented": "Comment Added",
    "issue_comment_edited": "Comment Edited",
    "issue_comment_deleted": "Comment Deleted"
}
