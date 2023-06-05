from N2SNUserTools.ldap import ADObjects
from N2SNUserTools.cli import read_config
from ldap3.core.exceptions import LDAPInsufficientAccessRightsResult
from N2SNUserTools.utils import n2sn_list_group_users


def add_n2sn_users_from_proposal(proposal):
    '''
    Get users from proposal, add them to
    current beamline's n2sn list
    '''
    instrument = "fmx"
    parser = object()
    common_config, config = read_config(parser, instrument) # TODO parser is just for passing errors/logging
    print(common_config, "div", config)
    groups = {'nx': 'n2sn-instusers-nxopen-fmx'} #config["rights"]
    users = n2sn_list_group_users(common_config['server'], common_config['group_search'], common_config['user_search'], common_config['ldap_ca_cert'], groups)
    print(users)
    


def remove_n2sn_users_from_proposal(proposal):
    '''
    Get users from proposal, remove them from
    current n2sn list
    '''
    #TODO users removed from proposal during the visit may remain on n2sn list
    pass
