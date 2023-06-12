import os
import sys
# stop LSDC server - assume this is running on LSDC server host
os.system("dzdo systemctl stop lsdc-server")
proposal = sys.argv[1]
# TODO verify that this looks like a proposal
n2sn_lib.remove_n2sn_users_from_nx(proposal)
