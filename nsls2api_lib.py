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

def get_active_safs_for_proposal(proposal_id):
    safs = get_all_proposals(proposal_id)['safs']

def get_all_active_safs_in_current_cycle(cycle="2023-1"):
    proposals = get_proposals_from_cycle(cycle)
    for proposal in proposals:
        safs = get_all_proposals(proposal.id)['safs']

def get_proposals_for_instrument(cycle="2023-1", instrument="FMX"):
    proposals_on_instrument = []
    proposals = get_proposals_from_cycle(cycle)[0]["proposals"]
    for proposal_num in proposals:
        proposal = get_all_proposals(proposal_num)
        if instrument in proposal['instruments']:
            proposals_on_instrument.append(proposal_num)
    return proposals_on_instrument
