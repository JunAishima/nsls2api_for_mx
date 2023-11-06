import ispyb_lib

proposal_id = 312064
session_number = 1
ispyb_lib.create_proposal(proposal_id)
ispyb_lib.create_session(proposal_id, session_number, "amx")
