import httpx
import time

base_url = "https://api.nsls2.bnl.gov/v1"

ispyb_instruments = ("AMX", "FMX", "NYX")

def is_ispyb_instrument(instruments):
    for instrument in instruments:
        if instrument in ispyb_instruments:
            return True
    return False

def get_from_api(url):
    if url:
        response = httpx.get(f"{base_url}/{url}")
        if response.status_code == httpx.codes.OK:
            return response.json()
        raise RuntimeError(f"failed to get value from {url}. response code: {response.status_code}")
    else:
        raise ValueError("url cannot be empty")

def get_all_cycles():
    return get_from_api(f"facility/nsls2/cycles")
def get_proposals_from_cycle(cycle):
    return get_from_api(f"facility/nsls2/cycle/{cycle}/proposals")['proposals']

# return true if any of check_instruments are in proposal_instruments
def check_instruments_in_proposal(proposal_instruments, check_instruments):
    for instrument in check_instruments:
        if instrument.upper() in proposal_instruments:
            return True
    return False

def get_proposals_for_cycle_instruments(cycle, instruments):
    proposals_to_return = set()
    proposals_cycle = get_proposals_from_cycle(cycle)
    for proposal in proposals_cycle:
        proposal_info = get_proposal_info(proposal)
        if check_instruments_in_proposal(proposal_info['instruments'], instruments):
            proposals_to_return.add(proposal)
    return sorted(proposals_to_return)

def get_proposals_for_cycle_instruments_2(cycle, instruments):
    instruments_string = ""
    for index, instrument in enumerate(instruments):
        if index > 0:
            instruments_string += "&"
        instruments_string += f"beamline={instrument}"
    cycle_string = f"cycle={cycle}"
    proposal_query = f"proposals/?{instruments_string}&{cycle_string}&facility=nsls2"
    proposals_to_return = set()
    items_per_page = 50
    page = 1
    while 1:
        proposals = get_from_api(f"proposals/?{instruments_string}&{cycle_string}&facility=nsls2&page_size={items_per_page}&page={page}")
        for proposal in proposals['proposals']:
            proposals_to_return.add(proposal['proposal_id'])
        if proposals['count'] == items_per_page:
            page += 1
        else:
            break
    return sorted(proposals_to_return)

def get_usernames_from_proposal(proposal_id):
    return set(get_from_api(f"proposal/{proposal_id}/usernames")['usernames'])
def get_users_from_proposal(proposal_id):
    return get_from_api(f"proposal/{proposal_id}/users")
def get_proposal_info(proposal_id):
    return get_from_api(f"proposal/{proposal_id}")['proposal']

def get_active_safs_for_proposal(proposal_id):  # currently unused
    safs = get_all_proposals(proposal_id)['safs']

def get_all_active_safs_in_current_cycle(cycle="2023-1"):  # currently unused
    proposals = get_proposals_from_cycle(cycle)
    for proposal in proposals:
        safs = get_all_proposals(proposal.id)['safs']

def get_proposals_for_instrument(cycle="2023-1", instrument="FMX"):
    proposals_on_instrument = []
    proposals = get_proposals_from_cycle(cycle)
    for proposal_num in proposals:
        proposal = get_proposal_info(proposal_num)
        if instrument in proposal['instruments']:
            proposals_on_instrument.append(proposal_num)
    return proposals_on_instrument

def get_current_cycle():
    return get_from_api(f"facility/nsls2/cycles/current")["cycle"]
