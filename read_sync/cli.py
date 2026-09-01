import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="read-sync: Terminal native manga and comic reader"
    )
    
    subparsers = parser.add_subparsers(dest="command")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Run headless backend with local WebUI and OPDS server")
    serve_parser.add_argument("--port", type=int, default=4567, help="Port to run the server on")

    # Repo command
    repo_parser = subparsers.add_parser("repo", help="Manage extension repositories")
    repo_subparsers = repo_parser.add_subparsers(dest="repo_command")
    repo_add = repo_subparsers.add_parser("add")
    repo_add.add_argument("url", help="URL of the repository index")

    # Ext command
    ext_parser = subparsers.add_parser("ext", help="Manage extensions")
    ext_subparsers = ext_parser.add_subparsers(dest="ext_command")
    ext_subparsers.add_parser("list")
    ext_install = ext_subparsers.add_parser("install")
    ext_install.add_argument("extensions", nargs="+", help="Extensions to install")

    # Library command
    subparsers.add_parser("library", help="Browse categories and favorite series")
    subparsers.add_parser("check", help="Check remote sources for newly released chapters")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Restore library from backup")
    import_parser.add_argument("file", help="Backup file (e.g. backup.tachibk)")

    # Auth command
    auth_parser = subparsers.add_parser("auth", help="Connect cloud tracking accounts")
    auth_parser.add_argument("service", choices=["anilist", "mal", "kitsu", "mangaupdates"])

    # Read/Search fallback is a bit tricky with argparse, but we can capture it using unknown args or custom parsing
    
    args, unknown = parser.parse_known_args()

    if args.command == "serve":
        from read_sync.server.app import run_server
        run_server(args.port)
    elif args.command == "repo":
        print(f"Adding repo: {args.url}")
    elif args.command == "ext":
        if args.ext_command == "list":
            print("Listing extensions...")
        elif args.ext_command == "install":
            print(f"Installing extensions: {args.extensions}")
    elif args.command == "library":
        print("Opening library...")
    elif args.command == "check":
        print("Checking for updates...")
    elif args.command == "import":
        print(f"Importing from {args.file}")
    elif args.command == "auth":
        print(f"Authenticating with {args.service}")
    else:
        # Check if it's a direct search like `read-sync "solo leveling"`
        if unknown:
            search_term = unknown[0]
            print(f"Searching for: {search_term}")
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
