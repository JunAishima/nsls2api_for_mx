import httpx
import time

base_url = "https://api-staging.nsls2.bnl.gov"

def get_from_api(url):
    if url:
        response = httpx.get(f"{base_url}/{url}")
        time.sleep(0.5)
        if response.status_code == httpx.codes.OK:
            return response.json()
        raise RuntimeError(f"failed to get value from {url}. response code: {response.status_code}")
    else:
        raise ValueError("url cannot be empty")

def get_proposals_from_cycle(cycle):
    return get_from_api(f"proposals/{cycle}")
def get_usernames_from_proposal(proposal_id):
    return set(get_from_api(f"proposal/{proposal_id}/usernames")['usernames'])
def get_users_from_proposal(proposal_id):
    return get_from_api(f"proposal/{proposal_id}/users")
def get_all_proposals(proposal_id):
    return get_from_api(f"proposal/{proposal_id}")
