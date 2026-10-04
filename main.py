import importlib

from dotenv import dotenv_values, load_dotenv

load_dotenv()

TraefikModule = importlib.import_module("traefik")
HomarrModule = importlib.import_module("homarr")

traefik = TraefikModule.Traefik()
homarr = HomarrModule.Homarr()

traefik_list = traefik.GetNetworkResources()
homarr_apps = homarr.GetAllApps()
homarr_manifest = homarr.GrabManifest()

traefik_list = dict(
    filter(
        lambda x: len(list(filter(lambda y: y["name"] == x[0], homarr_apps))) == 0,
        traefik_list.items(),
    )
)

for item in traefik_list.items():
    name = item[0]
    url = item[1]
    iconUrl = (
        "https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/microsoft-bing.svg"
    )
    if name.lower() in homarr_manifest:
        iconUrl = homarr.CreateIconUrl(name.lower())

    homarr.AddApp(name, url, iconUrl)

# https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/type/name
