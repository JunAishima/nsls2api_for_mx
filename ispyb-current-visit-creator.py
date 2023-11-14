import ispyb_lib
import nsls2api_lib
import argparse
import sys

#input
# proposal
# visit number

ispyb_beamlines = ["amx", "fmx", "nyx"]

def main(args=[]):
    parser = argparse.ArgumentParser(
        description="Create people, visit, and proposal information in ISPyB. Check whether these already exist."
    )
    parser.add_argument(
        "--cycle",
        type=str,
        help="The name of the proposal.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Show more log messages. (Use -vv for even more.)",
    )

    args = parser.parse_args(args or sys.argv[1:])
    if args.verbose:
        if args.verbose == 1:
            logging.basicConfig(level="INFO")
        if args.verbose == 2:
            logging.basicConfig(level="DEBUG")
        else:
            logging.basicConfig()  # "WARNING" by default

    cycle = args.proposal

    if not cycle:
        # just update everything
        raise RuntimeError("please define proposal, visit, AND beamline")

    proposals = nsls2api_lib.get_proposals_for_instrument(cycle=cycle, instruments=ispyb_beamlines) # also filter for ispyb_beamlines
    for proposal in proposals:
        ispyb_lib.add_users_for_proposal(proposal, visit, beamline)

if __name__ == "__main__":
    main()
