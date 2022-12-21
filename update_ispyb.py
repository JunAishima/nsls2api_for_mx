import nsls2api
import ispyb.factory

conn = ispyb.open("/etc/ispyb/ispybConfig.cfg")
cnx = conn.conn
cursor = cnx.cursor()

def queryDB(q):
  cursor.execute(q)
  try:
    return list(cursor.fetchone()) # TODO fetch all instead
  except TypeError:
    return 0

def get_ispyb_proposals():
    # go through all of Session_has_person and get all BLSessions
    query = "SELECT sessionId FROM Session_has_Person"
    session_ids = queryDB(query)
    session_id_string = ", ".join(session_ids)
    print(session_id_string)
    # get proposals
    query = "SELECT proposalId from BLSession where sessionId in {session_ids}"
    proposal_ids = queryDB(query)
    return proposal_ids

def clear_usernames_for_proposal(proposal_id):
    persons_on_proposal = core.retrieve_persons_for_proposal("mx", proposal_id)
    query = "SELECT usernames from BLSession where "
    #probably manual for the following, no stored procedures
    query = "DELETE proposal_has_person where person_id={uid}"
    query = "DELETE session_has_person where person_id={uid}"

def modify_usernames_for_proposal(proposal_id, previous_usernames, current_usernames):
    # previous_usernames and current_usernames must be sets
    if previous_usernames is not set or current_usernames is not set:
        raise ValueError("previous and current usernames must be sets")
    usernames_to_delete = previous_usernames - current_usernames
    usernames_to_add = current_usernames - previous_usernames
    query = "DELETE proposal_has_person where username={username}"
    for person in usernames_to_add:
        get_session_id()
        person_id=get_person_id(person) # personIdFromProposal()
        params = core.get_session_has_person()
        params['session_id'] = session_id
        params['person_id'] = person_id
        #params['role']  #define? can we identify from nsls2api? perhaps going into the user info?
        params['remove'] = True
        core.upsert_session_has_person(params)

def set_usernames_for_proposal(proposal_id):


def reset_users_for_proposal(proposal_id):
    ''' given a proposal id, take all of the users off an existing set of visits
        in ispyb and add the current users in '''
    # first, clear all existing usernames for the proposal_id in ISPyB
    # alternative, get usernames here, then remove/add as necessary at the bottom
    clear_usernames_for_proposal(proposal_id)
    # next, get the users who should be on the current proposal
    current_usernames = nsls2api.get_from_api(f"proposal/{proposal_id}/usernames")
    # finally, set all visits of the proposal to these users
    # alternative, modify the tables as necessary given the previous and current user lists
    modify_user_tables(proposal_id, previous_usernames, current_usernames)
