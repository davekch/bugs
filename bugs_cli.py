from configparser import ConfigParser
import os
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
import fire
from functools import wraps
from contextlib import ExitStack


def wrap_errors(response, ok_status=200):
    """returns the json of response but marks it as an error response if the status_code does not match ok_status"""
    if response.status_code == ok_status:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return {"errors": {"Error": ["Oops! Something went wrong."]}}
    else:
        return {"errors": response.json()}


class BugsClient:
    """this class provides some methods to communicate with bugs-server
    """

    def __init__(self, host, port=8000):
        self.baseurl = f"{host}:{port}/bugs/api/"

    def create_project(self, projectname: str) -> dict:
        response = requests.post(self.baseurl, {
            "name": projectname,
        })
        return wrap_errors(response, ok_status=201)

    def list_projects(self) -> list:
        response = requests.get(self.baseurl)
        return wrap_errors(response)

    def list_issues(self, projectname: str) -> list:
        response = requests.get(f"{self.baseurl}{projectname}/issues/")
        return wrap_errors(response)

    def get_issue(self, projectname: str, issueid: int) -> dict:
        response = requests.get(f"{self.baseurl}{projectname}/issues/{issueid}")
        return wrap_errors(response)

    def create_issue(self, projectname: str, title: str, body: str=None, priority: int=0, tags: str=None) -> dict:
        data = {
            "title": title,
            "body": body,
            "priority": priority,
            "tags": tags,
        }
        data = {k: v for k,v in data.items() if v}
        response = requests.post(f"{self.baseurl}{projectname}/issues/", data)
        return wrap_errors(response, ok_status=201)

    def edit_issue(self, projectname: str, issueid: int, title: str=None, body: str=None, priority: int=0, tags: str=None, status: str=None) -> dict:
        data = {
            "title": title,
            "body": body,
            "priority": priority,
            "tags": tags,
            "status": status,
        }
        data = {k: v for k,v in data.items() if v}
        response = requests.put(f"{self.baseurl}{projectname}/issues/{issueid}/", data)
        return wrap_errors(response, ok_status=201)

    def delete_issue(self, projectname: str, issueid: int) -> dict:
        response = request.delete(f"{self.baserurl}{projectname}/issues/{issueid}")
        return wrap_errors(response)


def connection_required(f):
    @wraps(f)
    def _f(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except requests.exceptions.ConnectionError:
            self._console.print("Error: No connection to bugs-server", style="bold red")
            self._console.print("Please check if bugs-server is running and bugs-cli is properly configured.")

    return _f


def make_default_config(config_path):
    config = ConfigParser()
    config["host"] = {
        "url": "http://127.0.0.1",
        "port": 8003,
    }
    config["bugs-cli"] = {
        "pager": 15,
    }
    config["styles"] = {
        "pending": "red",
        "wip": "yellow",
        "done": "green",
        "wontfix": "dim",
    }
    with open(config_path, "w") as c:
        config.write(c)
    return config


class BugsCliCLI:
    """Command Line Interface for BugsClient"""

    def __init__(self, config="bugs.ini"):
        if not os.path.isfile(config):
            self._config = make_default_config(config)
        else:
            self._config = ConfigParser()
            self._config.read(config)

        self._console = Console()
        self._client = BugsClient(host=self._config["host"]["url"], port=self._config["host"]["port"])

    def _print_errors(self, errors):
        self._console.print("Something went wrong.", style="bold red")
        table = Table.grid()
        table.add_column()
        table.add_column()
        for error, description in errors.items():
            if isinstance(description, list):
                description = "\n".join(description)
            table.add_row(f"[bold]error: ", description)
        self._console.print(table)

    def _guess_projectname(self):
        if projectname := os.environ.get("BUGSPROJECT"):
            self._console.print("[i]Note:[/i] No projectname was given, so I'm using projectname from the environment variable BUGSPROJECT")
            return projectname
        else:
            self._console.print("[i]Note:[/i] No projectname was given, so I'm using the current directory as projectname")
            return os.path.basename(os.getcwd())

    @connection_required
    def create(self, projectname: str=None):
        """create a new project.
        If no projectname is given, the name of the project will be taken from
        the environment variable BUGSPROJECT or, if not set, the current directory name.
        """
        if not projectname:
            projectname = self._guess_projectname()
        response = self._client.create_project(projectname)
        if "errors" in response:
            self._print_errors(response["errors"])
        else:
            self._console.print(f":heavy_check_mark: Created new project: {response['name']}")

    @connection_required
    def projects(self):
        """list all projects"""
        response = self._client.list_projects()
        if "errors" in response:
            self._print_errors(response["errors"])
        else:
            if not response:
                self._console.print("There are no projects.", style="italic")
                return

            table = Table(title="Projects", expand=True)
            table.add_column("Name", style="bold")
            table.add_column("Open issues")
            for project in response:
                table.add_row(project["name"], str(project["open_issues"]))

            if len(response) > self._config["bugs-cli"].getint("pager"):
                with self._console.pager(styles=True):
                    self._console.print(table)
            else:
                self._console.print(table)

    @connection_required
    def ls(self, projectname: str=None, closed: bool=False):
        """list issues in project.
        If no projectname is given, the name of the project will be taken from
        the environment variable BUGSPROJECT or, if not set, the current directory name.
        """
        if not projectname:
            projectname = self._guess_projectname()
        response = self._client.list_issues(projectname)
        if "errors" in response:
            self._print_errors(response["errors"])
        else:
            if not response:
                self._console.print("There currently are no issues.", style="italic")
                return

            table = Table(title=f"Issues for [i]{projectname}[/i]", expand=True)
            table.add_column("ID", style="bold dim")
            table.add_column("Title", style="bold")
            table.add_column("Priority")
            table.add_column("Tags")
            table.add_column("Status")
            for issue in response:
                status = issue["status"]
                statuscolor = self._config["styles"][status.lower()]
                table.add_row(
                    f'#{issue["id"]}',
                    issue["title"],
                    str(issue["priority"]),
                    issue["tags"] or "-",
                    f"[{statuscolor}]{status}[/{statuscolor}]",
                )
            if len(response) > self._config["bugs-cli"].getint("pager"):
                with self._console.pager(styles=True):
                    self._console.print(table)
            else:
                self._console.print(table)

    @connection_required
    def show(self, issueid: int, projectname: str=None, nopager: bool=False):
        """show details of an issue.
        If no projectname is given, the name of the project will be taken from
        the environment variable BUGSPROJECT or, if not set, the current directory name.
        """
        if not projectname:
            projectname = self._guess_projectname()
        response = self._client.get_issue(projectname, issueid)
        if "errors" in response:
            self._print_errors(response["errors"])
            return

        # make pager optional
        with ExitStack() as stack:
            if not nopager:
                stack.enter_context(self._console.pager(styles=True))
            self._console.print(response["title"], style="underline bold")
            status = response["status"]
            statuscolor = self._config["styles"][status.lower()]
            self._console.print(f"Status: [{statuscolor}]{status}[/{statuscolor}]")
            self._console.print(f"Priority: {response['priority']}")
            self._console.print(f"Tags: {response['tags'] or '-'}")
            self._console.print(Panel(Markdown(response["body"])))


if __name__ == "__main__":
    fire.Fire(BugsCliCLI())
