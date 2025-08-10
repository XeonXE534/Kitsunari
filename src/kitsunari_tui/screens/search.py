from textual.screen import Screen
from textual.widgets import Input, ListView, ListItem, Static, Footer
from textual.app import ComposeResult
from ..backend import backend
from .anime_detail import AnimeDetailScreen

class SearchScreen(Screen):
    def compose(self) -> ComposeResult:
        # The UI: search input, results list, footer
        yield Input(placeholder="Search for anime...", id="search_input")
        yield ListView(id="search_results")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.input.value.strip()
        if not query:
            return  # no empty searches, thanks

        # Get anime list from backend search
        anime_list = backend.get_anime_by_query(query)

        # Store raw anime data for future reference (optional but handy)
        self.search_results_data = anime_list

        # Grab the ListView widget and clear old results
        list_view = self.query_one("#search_results", ListView)
        list_view.clear()

        # Fill ListView with new items
        for idx, anime in enumerate(anime_list):
            info = anime.get_info()
            title = info.name
            synopsis = backend.clean_html(info.synopsis or "No synopsis available.")

            # Create a Static widget to show the title
            item_widget = Static(title)

            # Wrap it in a ListItem for selection
            list_item = ListItem(item_widget)

            # Attach extra data to the list item for later use
            list_item.index = idx
            list_item.synopsis = synopsis
            list_item.anime = anime

            # Append to the ListView
            list_view.append(list_item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item

        # Pull out stored anime and synopsis from the selected item
        anime = getattr(selected, "anime", None)
        synopsis = getattr(selected, "synopsis", "No synopsis available.")

        # If you have a widget to display synopsis, update it
        try:
            synopsis_display = self.query_one("#synopsis_display", Static)
            synopsis_display.update(synopsis)
        except Exception:
            # No synopsis display widget found, no biggie
            pass

        # Push the detail screen only if anime object exists
        if anime:
            self.app.push_screen(AnimeDetailScreen(anime, synopsis))
        else:
            print("[Error] Selected item has no anime data attached.")
