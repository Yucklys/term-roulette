"""UI for the roulette game."""

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Footer, Header, Static, Button
from textual.reactive import reactive
import random


class PlayerBoard(Static):
    """A widget to display the player's board."""

    def __init__(self, player_name, **kwargs):
        """Initialize the player's board."""
        super().__init__(**kwargs)
        self.player_name = player_name

    def compose(self) -> ComposeResult:
        """Create the player's board."""
        yield Button("Shoot!", id="shoot", variant="error")

    def on_mount(self) -> None:
        """Set the title of the board."""
        self.border_title = self.player_name + "'s board"


class Chamber(Static):
    """A widget to display the chamber."""

    chambers = reactive("")
    barrel = reactive(0)

    def render(self) -> RenderResult:
        """Render the chamber."""
        # Create textual representation of chambers
        chamber_str = []
        for i in range(len(self.chambers)):
            if i < self.barrel:
                chamber_str += "⁍" if self.chambers[i] else "⦾"
            else:
                chamber_str += "•"
        return ' '.join(chamber_str)


class RouletteGame(App):
    """A smart Russian Roulette Simulator."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "roulette_game.tcss"

    def __init__(self, total_n, bullet_n, **kwargs):
        """Initialize the game."""
        super().__init__(**kwargs)
        self.total_n = total_n
        self.bullet_n = bullet_n

    def on_mount(self) -> None:
        """Update widgets on mount."""
        self.reload()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield PlayerBoard("Sam", id="agent_board")
        yield Chamber(id="chamber")
        yield PlayerBoard("Player", id="player_board")

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id

        if button_id == "shoot":
            print("shoot pressed")
            self.shoot()

    def shoot(self) -> None:
        """Pull the trigger."""
        chamber_node = self.query_one(Chamber)
        chamber_node.barrel += 1

        # reload the revolver when go through all chambers
        print(self.total_n, chamber_node.barrel)
        if chamber_node.barrel == self.total_n + 1:
            self.reload()
        # TODO: Add more checks to see if the chamber is loaded

    def reload(self) -> None:
        """Reload the revolver."""
        chamber_node = self.query_one("#chamber")
        chambers = [False] * self.total_n
        loaded_chambers = random.sample(range(self.total_n), self.bullet_n)
        for i in loaded_chambers:
            chambers[i] = True

        chamber_node.chambers = chambers
        chamber_node.barrel = 0


if __name__ == "__main__":
    app = RouletteGame(6, 1)
    app.run()
