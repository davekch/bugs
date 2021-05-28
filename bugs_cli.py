from configparser import ConfigParser
import os
import requests
import json
from rich.console import Console
from rich.table import Table
import fire
from functools import wraps


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


class BugsCliCLI:
    """Command Line Interface for BugsClient"""

    def __init__(self, config="bugs.ini"):
        if not os.path.isfile(config):
            self._config = ConfigParser()
            self._config["host"] = {
                "url": "http://127.0.0.1",
                "port": 8003,
            }
            with open(config, "w") as c:
                self._config.write(c)
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

    @connection_required
    def create(self, projectname: str):
        """create a new project"""
        response = self._client.create_project(projectname)
        if "errors" in response:
            self._print_errors(response["errors"])
        else:
            self._console.print(f":heavy_check_mark: Created new project: {response['name']}")

    @connection_required
    def ls(self, projectname: str, closed: bool=False):
        """list issues in project"""
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
                table.add_row(
                    f'#{issue["id"]}',
                    issue["title"],
                    str(issue["priority"]),
                    issue["tags"] or "-",
                    issue["status"],
                )
            self._console.print(table)


if __name__ == "__main__":
    fire.Fire(BugsCliCLI())
