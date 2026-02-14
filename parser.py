import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="Pipeline tool with upload and download modes"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # -------------------
    # DOWNLOAD COMMAND
    # -------------------
    download_parser = subparsers.add_parser(
        "download", help="Run download pipeline"
    )
    download_parser.add_argument(
        "--target-folder",
        required=True,
        help="Target folder for downloaded data"
    )
    download_parser.add_argument(
        "--log-folder",
        required=True,
        help="Target folder for logging"
    )
    download_parser.add_argument(
        "--source",
        required=True,
        help="Source (any string)"
    )
    download_parser.add_argument(
        "--email",
        required=True,
        help="Notification email"
    )
    download_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    # -------------------
    # UPLOAD COMMAND
    # -------------------
    upload_parser = subparsers.add_parser(
        "upload", help="Run upload pipeline"
    )
    upload_parser.add_argument(
        "--source-folder",
        required=True,
        help="Source folder to upload"
    )
    upload_parser.add_argument(
        "--log-folder",
        required=True,
        help="Target folder for logging"
    )
    upload_parser.add_argument(
        "--email",
        required=True,
        help="Notification email"
    )
    upload_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "download":
        print("Running DOWNLOAD pipeline")
        print(args.verbose)
        print(args)

    elif args.command == "upload":
        print("Running UPLOAD pipeline")
        print(args.upload)


if __name__ == "__main__":
    main()
