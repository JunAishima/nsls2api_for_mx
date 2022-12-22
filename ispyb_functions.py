import ispyb_lib
import nsls2api_lib

proposal_numbers = ispyb_lib.get_proposal_numbers(ispyb_lib.get_ispyb_proposal_ids())
print(proposal_numbers)
for proposal_number in proposal_numbers:
    print(f"usernames from proposal {proposal_number} are: {nsls2api_lib.get_usernames_from_proposal(proposal_number)}")
print(f"proposal numbers: {ispyb_lib.get_proposal_numbers(ispyb_lib.get_ispyb_proposal_ids())}")
