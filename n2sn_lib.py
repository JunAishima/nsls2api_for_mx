from N2SNUserTools.ldap import ADObjects
from N2SNUserTools.cli import read_config
from ldap3.core.exceptions import LDAPInsufficientAccessRightsResult
from N2SNUserTools.utils import n2sn_list_group_users
from nsls2api_lib import get_usernames_from_proposal

#logger = logging.

def add_n2sn_users_from_nx(proposal: str):
    '''
    Get users from proposal, add them to
    current beamline's n2sn list
    '''
    instrument = "fmx"
    parser = object()
    common_config, config = read_config(parser, instrument) # TODO parser is just for passing errors/logging
    #logger.debug(common_config, "div", config)
    groups = {'nx': 'n2sn-instusers-nxopen-fmx'} #config["rights"]
    users = n2sn_list_group_users(common_config['server'], common_config['group_search'], common_config['user_search'], common_config['ldap_ca_cert'], groups)
    user_list = []
    for user, user_info in users.items():
        #print(f'user: {user} user_info: {user_info}')
        user_list.append(user_info['sAMAccountName'])
    print(f"NX user_list length: {len(user_list)} list:{user_list}")
    users_to_add = get_usernames_from_proposal(proposal)
    print(f"users to add: {users_to_add}")
    list_after_addition = set(user_list) - users_to_add
    print(f"list after addition: {len(list_after_addition)} {list_after_addition}")
    print(f"interaction: {set(user_list) & users_to_add}")
    #replicate N2SNUserTools.utils.n2sn_list_group_users_as_table
    with ADObjects(common_config['server'], common_config['group_search'], common_config['user_search'],
                   ca_certs_file=common_config['ldap_ca_cert'],
                   authenticate=False) as ad:
        for username in users_to_add:
            pass
            #ad.add_user_to_group_by_dn("nx", username)


def remove_n2sn_users_from_nx(proposal):
    '''
    Get users from proposal, remove them from
    current n2sn list
    '''
    groups = {'nx': 'n2sn-instusers-nxopen-fmx'} #config["rights"]
    users = n2sn_list_group_users(common_config['server'], common_config['group_search'], common_config['user_search'], common_config['ldap_ca_cert'], groups)
    #print(users)
    user_list = []
    for user, user_info in users.items():
        print(f'user: {user} user_info: {user_info}')
        user_list.append(user_info['sAMAccountName'])
    print(f"NX user_list length: {len(user_list)} list:{user_list}")
    users_to_remove = get_usernames_from_proposal(proposal)
    print(f"users to remove: {users_to_remove}")
    list_after_removal = set(user_list) - users_to_remove
    print(f"list after removal: {len(list_after_removal)} {list_after_removal}")
    print(f"interaction: {set(user_list) & users_to_remove}")
    with ADObjects(server, group_search, user_search,
                   ca_certs_file=ca_certs_file,
                   authenticate=False) as ad:
        for username in users_to_add:
            pass
            #ad.remove_user_to_group_by_dn("nx", username)
