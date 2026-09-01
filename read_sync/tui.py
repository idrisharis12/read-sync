from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Input
from textual.containers import Container, Horizontal, Vertical
from read_sync.library import db

class LibraryView(DataTable):
    def on_mount(self) -> None:
        self.add_columns("Title", "Category", "Unread")
        self.refresh_library()

    def refresh_library(self):
        self.clear()
        library = db.get_library()
        for item in library:
            self.add_row(item['title'], item['category'], "0")

class ReadSyncApp(App):
    """A Textual TUI for read-sync."""

    CSS = """
    Screen {
        layout: vertical;
    }
    #search-bar {
        dock: top;
        height: 3;
    }
    LibraryView {
        height: 100%;
        width: 100%;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh Library")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Search library or extensions...", id="search-bar")
        yield LibraryView(id="library-view")
        yield Footer()

    def on_mount(self) -> None:
        db.init_db()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_refresh(self) -> None:
        library_view = self.query_one(LibraryView)
        library_view.refresh_library()
        self.notify("Library refreshed!")

def run_tui():
    app = ReadSyncApp()
    app.run()
