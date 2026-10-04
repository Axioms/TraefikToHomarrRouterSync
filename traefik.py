import json
import os

import requests


class Traefik:
    traefikHost = os.getenv("TRAEFIK_HOST_URL")
    user = os.getenv("TRAEFIK_AUTH_USERNAME")
    password = os.getenv("TRAEFIK_AUTH_PASSWORD")

    def routeAndName(self, item) -> tuple[str, str, str]:
        rule = item["rule"]
        path = "/"
        checkForPaths = rule.split("&&")
        CheckForMultipleDomains = checkForPaths[0].split("||")
        if len(checkForPaths) > 1:
            if "PathPrefix(" in checkForPaths[1]:
                path = checkForPaths[1].strip()[13:-2]
            elif "Path(" in checkForPaths[1]:
                path = checkForPaths[1].strip()[7:-2]

        if len(CheckForMultipleDomains) > 1:
            domain = "https://" + CheckForMultipleDomains[0].strip()[6:-2]
        else:
            domain = "https://" + CheckForMultipleDomains[0].strip()[6:-2]

        return (item["service"], domain, path)

    def GetNetworkResources(self) -> dict[str, str]:

        Traefiksession = requests.Session()
        Traefiksession.auth = (Traefik.user, Traefik.password)
        response = Traefiksession.get(Traefik.traefikHost + "/api/http/routers")

        if response.status_code == 200:
            body = response.content
            jsonBody = json.loads(body)
            data = list(map(self.routeAndName, jsonBody))
            services = dict()
            for item in data:
                if item[0] == "prometheus@internal":
                    continue
                services[item[0]] = item[1] + item[2]

            return services
        raise ValueError("Failed to retreve Resources from Traefik")


if __name__ == "__main__":
    print("Traefik")
