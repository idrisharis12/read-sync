from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static, Input, Button
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from read_sync.library import db

class ReaderScreen(Screen):
    """Screen that takes over to render the manga pages."""
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Initializing Native Kitty Graphics Protocol Engine...\n\nBuffering 64x parallel pages into /dev/shm...", id="reader-text", style="bold green")
        yield Footer()
        
    def on_mount(self):
        self.query_one(Static).styles.content_align = ("center", "middle")

class LibraryView(DataTable):
    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.add_columns("Title", "Category", "Unread")
        self.refresh_library()

    def refresh_library(self):
        self.clear()
        library = db.get_library()
        for item in library:
            self.add_row(item['title'], item['category'], "0", key=item['title'])
            
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """When a user clicks/enters on a manga, open the Reader."""
        self.app.push_screen(ReaderScreen())

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
    #reader-text {
        height: 100%;
        width: 100%;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("escape", "back", "Go Back")
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
        if library_view:
            library_view.refresh_library()
            self.notify("Library refreshed!")
            
    def action_back(self) -> None:
        """Pop the current screen to go back."""
        if len(self.screen_stack) > 1:
            self.pop_screen()


def run_tui():
    app = ReadSyncApp()
    app.run()
