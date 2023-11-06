import nsls2api
import ispyb.factory
import nsls2api_lib
from datetime import datetime
import time

conn = ispyb.open("/etc/ispyb/ispybConfig.cfg")
cnx = conn.conn
cursor = cnx.cursor()
core = ispyb.factory.create_data_area(ispyb.factory.DataAreaType.CORE, conn)

def queryDB(q):
  cursor.execute(q)
  try:
    return list(cursor.fetchall())
  except TypeError:
    return 0

def queryOneFromDB(q):
  cursor.execute(q)
  try:
    return list(cursor.fetchone())[0]
  except TypeError:
    return 0

# get list numbers from a queryDB() call
# be able to handle input from a query result or raw list
def get_unique_ids(id_list):
    id_set = set()
    for _id in id_list:
        if type(_id) == tuple:
            id_set.add(_id[0])
        elif type(_id) == int:
            id_set.add(_id)
    return list(id_set)

# works for query results
def get_in_string(ids):
    if len(ids)> 1:
        multi_id_string = ""
        for _id in get_unique_ids(ids):
            id_string = str(_id)
            multi_id_string += f"'{id_string}', "
        return multi_id_string[:-2]  # get rid of trailing comma
    else:
        return f"'{str(ids[0])}'"

def get_ispyb_proposal_ids():
    '''
    Get all proposals in the ISPyB database by starting from
    BLSessions
    '''
    # go through all of Session_has_person and get all BLSessions
    query = "SELECT sessionId FROM Session_has_Person;"
    session_ids = queryDB(query)
    session_id_string = ""
    if len(session_ids)> 1:
        for session_id in get_unique_ids(session_ids):
            session_str = str(session_id)
            session_id_string += f"'{session_str}', "
        session_id_string = session_id_string[:-2]
    else:
        session_id_string = f"'{str(session_ids[0])}'"
    # get proposals
    query = f"SELECT proposalId from BLSession where sessionId in {session_id_string};"
    proposal_ids = queryDB(query)
    return get_unique_ids(proposal_ids)

def get_proposal_numbers(proposal_ids):
    query = f"SELECT proposalNumber from Proposal where proposalId in ({get_in_string(proposal_ids)});"
    proposal_nums = queryDB(query)
    return get_unique_ids(proposal_nums)


def get_session_ids_for_proposal(proposal_id):
    query = f"SELECT proposalId from Proposal where proposalNumber={proposal_id}"
    proposal_ids = queryDB(query)
    query = f"SELECT sessionId FROM BLSession where proposalId={proposal_ids}"  # note difference of what we call proposal_id vs BLSession's name, which is proposal_number
    session_ids = queryDB(query)
    return session_ids

def remove_all_usernames_for_proposal(proposal_id, dry_run=True):
    '''
    Not within the name is the fact that associations with visits
    (sessions/BLSessions) are also removed here
    '''
    if dry_run:
        print(f"Clearing usernames for proposal {proposal_id}")
    try:
        persons_on_proposal = core.retrieve_persons_for_proposal("mx", proposal_id)
    except ispyb.NoResult:
        print("No people found for proposal")
        return
    session_ids = get_session_ids_for_proposal(proposal_id)
    people_in_sessions = set()
    for session_id in session_ids:
        query = f"SELECT personId FROM Session_has_Person WHERE sessionId={session_id[0]}"
        people_in_session = queryDB(query)
        for person in people_in_session:
            #print() do something to show the username of this person
            people_in_sessions.add(person[0])
    if dry_run:
        print(f"Dry run: remove usernames from Session_has_Person: {people_in_sessions}")
    # clear all Session_has_Person for the proposal
    if not dry_run:
        for session_id in session_ids:
            for person in people_in_sessions:
                query = f"DELETE Session_has_Person where sessionId={session_id},personId={person.person_id}"
                delete_session_has_person = queryDB(query)
                print(delete_session_has_person)


def create_person(first_name, last_name, login, is_pi, dry_run=True):
    query = f"INSERT Person (givenName, familyName, login) VALUES('{first_name}', '{last_name}', '{login}')"
    if not dry_run:
        queryDB(query)
        person_id = queryDB(f"SELECT personId from Person where login='{login}'")[0][0]
    else:
        person_id = -1
    return person_id


def create_people(proposal_id, current_usernames, users_info, dry_run=True):
    '''
    Only way to get information about people in the current API is to
    get it from the proposal. This should change in the next version
    of the nslsii API
    '''
    person_ids = set()
    for username in current_usernames:
        query = f"SELECT personId from Person where login='{username}'"
        person_id = queryDB(query)
        first_name = None
        last_name = None
        is_pi = False
        if not person_id:  # the Person doesn't exist in ISPyB yet
            # extract first and last names from proposal info
            for user_info in users_info:
                if username == user_info['username']:
                    first_name = user_info['first_name']
                    last_name = user_info['last_name']
                    is_pi = user_info['is_pi']
                    break
            if first_name and last_name:
                person_id = create_person(first_name, last_name, username, is_pi, dry_run)
                print(f"added new person {username} with id: {person_id}")
            else:
                raise RuntimeError(f"Username {person_id} not found, aborting!")
        else:
            person_id = person_id[0][0]
        person_ids.add(person_id)
    return person_ids


def add_usernames_for_proposal(proposal_id, current_usernames, users_info, dry_run=True):
    if type(current_usernames) != set:
        raise ValueError("current usernames must be a set")
    print(f"add_usernames_for_proposal: users to add: {current_usernames}")
    if dry_run:
        return
    user_ids = create_people(proposal_id, current_usernames, users_info, dry_run)  # TODO see how to get PI status from nsls2api
    session_ids = get_session_ids_for_proposal(proposal_id)
    for person_login in current_usernames:
        for session_id in session_ids:
            query = f"INSERT Session_has_Person (sessionId, personId, role) VALUES({session_id}, {person_id}, 'Co-Investigator')"
            session_has_person_id = queryOne(query)
            print(f"session add_person: {session_has_person_id}")


def reset_users_for_proposal(proposal_id, dry_run=False):
    ''' given a proposal id, take all of the users off an existing set of visits
        in ispyb and add the current users in '''
    # first, clear all existing usernames for the proposal_id in ISPyB
    # alternative, get usernames here, then remove/add as necessary at the bottom
    remove_all_usernames_for_proposal(proposal_id)
    # next, get the users who should be on the current proposal
    add_users_for_proposal(proposal_id, dry_run)


def add_users_for_proposal(proposal_id, dry_run=False):
    current_usernames = nsls2api.get_from_api(f"proposal/{proposal_id}/usernames")
    user_info = nsls2api.get_from_api(f"proposal/{proposal_id}")['users']
    # finally, set all visits of the proposal to these users
    # alternative, modify the tables as necessary given the previous and current user lists
    # TODO consider what should happen if old proposals have no users
    add_usernames_for_proposal(proposal_id, set(current_usernames['usernames']), user_info, dry_run=dry_run)


def proposalIdFromProposal(propNum):
  q = ("select proposalId from Proposal where proposalNumber = " + str(propNum))
  return (queryOneFromDB(q))


def maxVisitNumfromProposal(propNum):
  propID = proposalIdFromProposal(propNum)
  q = ("select max(visit_number) from BLSession where proposalId = " + str(propID))
  return (queryOneFromDB(q))

def setup_proposal(proposal, users):
    # if doesn't exist, make it
    #   highest visit number is 1
    # find highest visit number
    # create newest proposal (highest number)
    # add users to proposal
    # add users to session
    pass


def create_session(proposal_id, session_number, beamline_name):
    params = core.get_session_for_proposal_code_number_params()
    params['proposal_code'] = 'mx'
    params['proposal_number'] = proposal_id
    params['visit_number'] = session_number
    params['beamline_name'] = beamline_name
    params['startdate'] = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    params['enddate'] = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    params['comments'] = 'For software testing'  # TODO get more useful info from nsls2api
    sid = core.upsert_session_for_proposal_code_number(list(params.values()))
    cnx.commit()
