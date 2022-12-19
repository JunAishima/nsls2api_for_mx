import httpx
import time

base_url = "https://api-staging.nsls2.bnl.gov"

def get_from_api(url):
    if url:
        response = httpx.get(f"{base_url}/{url}")
        time.sleep(0.5)
        if response.status_code == httpx.codes.OK:
            return response.json()
        raise RuntimeError(f"failed to get value from {base_url}/{url}. response code: {response.status_code}")
    else:
        raise ValueError("url cannot be empty")
