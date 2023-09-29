import os
import sys
import subprocess
from nsls2api_for_mx import n2sn
import redis
import .ispyb_lib
import .nsls2api_lib


def check_active(server_log):
    active = False
    for line in server_log.readline()
        if line.startswith("  Active") and line.find("active") != -1:
            active = True
    return active


# TODO hard-coded values for initial testing
beamline = "fmx"
proposal_number = 310000
date = "20230929"  # date.strftime("%Y%d%m")
pi = "jaishima"

# inputs: beamline, proposal_number, date, pi
r = redis.Redis(host=f"epics-services-{beamline}.nsls2.bnl.local", port=6379, decode_responses=True)
r.set('currentProposal', proposal_number)
# n2sn - put people into NX
n2sn.add_n2sn_users_from_nx(proposal_number)
users = nsls2api_lib.get_users_from_proposal(proposal_number)
# ispyb - (add proposal), create a new blsession, add all current people from proposal
ispyb_lib.set_up_proposal(proposal_number, users)
# create visit directory - input: date of visit, PI username
# TODO update to check that PI is part of the group! maybe return directory so we can check it exists?
# TODO check whether the following script can be run from anywhere
# TODO can this script return the created directory's name?
os.system(f"/nsls2/software/mx/daq/mx-scripts/make_proposal_directory_service_user {proposal} {date} {pi}")
# start lsdc server - verify it wasn't running
lsdc_server_status = subprocess.run(["systemctl", "status", "lsdc-server"], stdout=subprocess.PIPE)
if not check_active(lsdc_server_status.stdout):
    sys.exit(1)
#handle output to check that server is stopped
os.system("dzdo systemctl start lsdc-server")
