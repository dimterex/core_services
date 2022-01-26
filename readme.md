# Transferring Outlook calendar to bug trackers


###Supported bug trackers:
1. Redmine
2. Jira

### Functions 

1. Transferring Outlook calendar 
2. Fill periodical issue (like code review, etc.)

### How use it
* Create categories for events in calendar
* Create ignorable category (assign this category for event, and this event can not transferring)
* Assign a category for events (only 1 category for 1 event)
* Append each category to settings into "categories" (see example of settings)
* Append some periodical task to settings into "periodical" (see example of settings)
* Append ignorable category into "ignore" (see example of settings)

### Settings example

```
{
    "login": "testLogin",
    "password": "testPassword",
    "email": "test@mail.ru",
    "domain": "DOMAIN",

    "outlook_url": "https://mail.***.ru",
    "jira_url": "https://jira.local",
    "redmine_url": "http://redmine.local",

    "categories": [
        {
            "name": "Not project",
            "jira_id": "SP-60273",
            "redmine_id": "46822"
        },{
            "name": "Interview",
            "jira_id": "SP-60273",
            "redmine_id": "53911"
        }
    ],
    "periodical": [
        {
            "name": "Code Review",
            "jira_id": "SP-60276",
            "redmine_id": "58279"
        },{
            "name": "Consultation",
            "jira_id": "SP-60272",
            "redmine_id": "58275"
        }
    ],

    "ignore": "Ignorable"
}
```


### Dependency 
1. https://pypi.org/project/python-redmine/
2. https://pypi.org/project/jira/
3. https://pypi.org/project/exchangelib/
