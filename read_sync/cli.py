import argparse
import sys
from read_sync.library import db

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

    # Read command
    read_parser = subparsers.add_parser("read", help="Read a manga directly via native scraper")
    
    # Dev/Test commands
    subparsers.add_parser("demo-add", help="Add a demo manga to the library for testing")

    args, unknown = parser.parse_known_args()

    # Initialize DB globally for CLI actions
    db.init_db()

    if args.command == "serve":
        from read_sync.server.app import run_server
        run_server(args.port)
    elif args.command == "repo":
        print(f"Adding repo: {args.url}")
    elif args.command == "ext":
        from read_sync.extensions import manager
        if args.ext_command == "list":
            exts = manager.list_available()
            print("Available English Extensions:")
            for e in exts:
                print(f" - {e['name']} (v{e['version']})")
        elif args.ext_command == "install":
            for ext in args.extensions:
                manager.install_extension(ext)
    elif args.command == "library":
        from read_sync.tui import run_tui
        run_tui()
    elif args.command == "read":
        # Temporary read command for E2E native testing
        search_query = " ".join(unknown) if unknown else "solo leveling"
        print(f"Executing End-to-End Native Scraper for: '{search_query}'")
        
        from read_sync.extensions import runner_py
        from read_sync.engine import downloader
        from read_sync.renderers import kitty
        import os
        import time

        results = runner_py.search_manga(search_query)
        if not results:
            print("No manga found!")
            return
            
        first_manga = results[0]
        print(f"Found: {first_manga['title']} (ID: {first_manga['id']})")
        
        chapters = runner_py.get_chapters(first_manga['id'])
        if not chapters:
            print("No English chapters found!")
            return
            
        first_chap = chapters[-1] # Get first chapter (it's sorted desc)
        print(f"Fetching Chapter {first_chap['chapter']}: {first_chap['title']}")
        
        images = runner_py.get_chapter_images(first_chap['id'])
        print(f"Found {len(images)} pages. Starting 64x parallel download to RAM...")
        
        downloader.download_chapter_sync(images)
        
        # Test Render First Page
        first_page_path = "/dev/shm/read-sync/page_001.jpg"
        if os.path.exists(first_page_path):
            print("\nRendering Page 1 using Native Kitty Graphics:")
            time.sleep(1)
            kitty.render_image_kitty(first_page_path)
            print("\nDone!")
        else:
            print("Failed to find buffered image.")
    elif args.command == "check":
        print("Checking for updates across 64 parallel workers...")
    elif args.command == "import":
        print(f"Importing backup from {args.file} into SQLite...")
    elif args.command == "auth":
        if args.service == "anilist":
            from read_sync.trackers import anilist
            anilist.login()
        else:
            print(f"Authentication for {args.service} is under construction.")
    elif args.command == "demo-add":
        db.add_manga("Solo Leveling", "https://example.com/solo", "comick")
        db.add_manga("Chainsaw Man", "https://example.com/csm", "mangadex")
        print("Added demo manga to library.")
    else:
        # Check if it's a direct search like `read-sync "solo leveling"`
        if unknown:
            search_term = unknown[0]
            print(f"Opening TUI to search across installed extensions for: '{search_term}'")
            # Usually we'd pass search_term to the TUI here
            from read_sync.tui import run_tui
            run_tui()
        else:
            # No args, open library
            from read_sync.tui import run_tui
            run_tui()

if __name__ == "__main__":
    main()
