"""Set static back to the state from a branch from github."""
import requests

BRANCH = "dev"
USER = "2dos"
REPO = "DK64-Randomizer"

def downloadStatic(file: str):
    """Download static file from github."""
    print(f"Downloading {file} from GitHub")
    r = requests.get(f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/{file}")
    with open(f"../../{file}", "wb") as af:
        af.write(r.content)


downloadStatic("static/patches/shrink-dk64.bps")
downloadStatic("static/patches/pointer_addresses.json")
print("Complete")