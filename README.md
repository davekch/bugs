# Bugs

A dead simple local issuetracker for your sideprojects.

![project view](img/screenshot_project.png)
![issue view](img/screenshot_issue.png)

**Features**
 - create projects
 - create issues for projects
 - format the description of the issue with markdown
 - mark issues as pending, WIP (work in progress), done or wontfix
 - assign priority to issues
 - assign tags to issues

**Features yet to come**
 - filter issues by tag
 - a CLI
 - users (maybemaybe)


## Installation

Requirements: `python3.8`, `pipenv`

```
git clone https://github.com/davekch/bugs.git
cd bugs
pipenv install
./manage.py migrate
```
In development, run
```
export DJANGO_ENVIRONMENT=development
./manage.py runserver <port>
```
In production, run `./manage.py runserver` to create a config file at `bugtrack/settings/productionsettings.ini`. Edit the section server[allowed] to set the allowed hosts.
