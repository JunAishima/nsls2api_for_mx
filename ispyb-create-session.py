import sys
import argparse
import ispyb_lib

def main(args=[]):
    parser = argparse.ArgumentParser(
        description="Create visit and proposal information in ISPyB."
    )
    parser.add_argument(
        "--proposal",
        type=int,
        help="The names of the proposal (6-digit number).",
    )
    parser.add_argument(
        "--visit",
        type=str,
        help="Name of the visit (a number starting at 1)."
    )
    parser.add_argument(
        "--beamline",
        type=str,
        help="Beamline name"
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

    proposal_name = args.proposal
    visit_number = args.visit
    beamline = args.beamline
    ispyb_lib.create_proposal(proposal_name)
    ispyb_lib.create_session(proposal_name, visit_number, beamline)


if __name__ == "__main__":
    main()
