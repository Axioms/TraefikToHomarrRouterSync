import json
import os
from enum import Enum

import requests
from requests.api import request
from requests.models import Request, Response

MANIFEST_URL = "https://raw.githubusercontent.com/homarr-labs/dashboard-icons/refs/heads/main/metadata.json"
HOMARR_API_KEY = os.getenv("HOMAR_API_KEY")
HOMAR_URL = os.getenv("HOMAR_HOST_URL")


class HttpRequestType(Enum):
    POST = 0
    GET = 1
    PATCH = 2


class Homarr:
    def __init__(self):
        self.Manifest = {}

    def GrabManifest(self) -> list[str]:
        if len(self.Manifest) == 0:
            self._GetIconManifest()
        data = list(self.Manifest.keys())
        return data

    def GetAllApps(self) -> list[any]:
        response = self._httpClient("/api/apps", {}, HttpRequestType.GET)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        else:
            raise ValueError(f"Get All Apps' Host Returned a : {response.status_code}")

    def GetAllBoards(self) -> list[any]:
        response = self._httpClient("/api/boards", {}, HttpRequestType.GET)
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        else:
            raise ValueError(f"Get All Apps' Host Returned a : {response.status_code}")

    def AddApp(self, name: str, url: str, iconUrl: str) -> any:
        data = json.dumps({
            "name": f"{name}",
            "description": f"{name}",
            "iconUrl": f"{iconUrl}",
            "href": f"{url}",
            "pingUrl": f"{url}",
        })
        response = self._httpClient("/api/apps", data, HttpRequestType.POST)
        if response.status_code == 200:
            return json.loads(response.content)["appId"]
        else:
            raise ValueError(f"Create App Host Returned a : {response.status_code}")

    def CreateIconUrl(self, name: str) -> str:
        return f"https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/{self.Manifest[name]['base']}/{name}.{self.Manifest[name]['base']}"

    def _GetIconManifest(self):
        response = requests.get(MANIFEST_URL)
        if response.status_code == 200:
            self.Manifest = json.loads(response.content)

    def _httpClient(self, uri: str, data, requestType: HttpRequestType) -> Response:
        url = HOMAR_URL + uri
        headers = {
            "ApiKey": HOMARR_API_KEY,
            "accept": "application/json",
            "content-type": "application/json",
        }

        if requestType == HttpRequestType.GET:
            return requests.get(url, headers=headers)
        elif requestType == HttpRequestType.POST:
            return requests.post(url=url, data=data, headers=headers)
        else:
            raise ValueError("Not A valid HTTP Request Type")


def main():
    homarr = Homarr()
    # homarr.GrabManifest()
    homarr.GetAllBoards()


if __name__ == "__main__":
    main()
