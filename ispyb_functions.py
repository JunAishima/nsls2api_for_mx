import ispyb_lib
import nsls2api_lib

proposal_ids = ispyb_lib.get_ispyb_proposals()
for proposal_id in proposal_ids:
    print(f"usernames from proposal {proposal_id} are: {nsls2api_lib.get_usernames_from_proposal(proposal_id)}")
