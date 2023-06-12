import os
import sys
import subprocess
from nsls2api_for_mx import n2sn


def check_active(server_log):
    active = False
    for line in server_log.readline()
        if line.startswith("  Active") and line.find("active") != -1:
            active = True
    return active


# n2sn - put people into NX
n2sn.add_n2sn_users_from_nx(proposal)
users = nsls2api_lib.get_users_from_proposal(proposal_number)
# ispyb - (add proposal), create a new blsession, add all current people from proposal
ispyb_lib.set_up_proposal(proposal_number, users)
# create visit directory - input: date of visit, PI username
# TODO update to check that PI is part of the group! maybe return directory so we can check it exists?
os.system(f"/nsls2/software/mx/daq/mx-scripts/make_proposal_directory_service_user {proposal} {date} {pi}")
# start lsdc server - verify it wasn't running
lsdc_server_status = subprocess.run(["systemctl", "status", "lsdc-server"], stdout=subprocess.PIPE)
if not check_active(lsdc_server_status.stdout):
    sys.exit(1)
#handle output to check that server is stopped
os.system("dzdo systemctl start lsdc-server")
