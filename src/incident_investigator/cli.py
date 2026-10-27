import argparse


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered incident investigation agent",
    )
    parser.add_subparsers(dest="command")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
