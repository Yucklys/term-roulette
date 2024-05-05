"""UI for the roulette game."""

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Footer, Header, Static, Button
from textual.reactive import reactive
from textual import on
from .picker import CharacterPicker
from GunMechanics import Gun, GunType


class PlayerBoard(Static):
    """A widget to display the player's board."""

    player_name = reactive("")

    def __init__(self, player_name="", **kwargs):
        """Initialize the player's board."""
        super().__init__(**kwargs)
        self.player_name = player_name
        self.update_border_title()

    def compose(self) -> ComposeResult:
        """Create the player's board."""
        yield Button("Shoot opponent", id="shoot_opponent", variant="error")
        yield Button("Shoot myself", id="shoot_myself", variant="warning")

    def update_border_title(self):
        """Set the title of the board."""
        self.border_title = self.player_name + "'s board"


class Chamber(Static):
    """A widget to display the chamber."""

    shot_bullet = reactive(-1)

    def __init__(self, gun_type, **kwargs):
        """Initialize the chamber."""
        super().__init__(**kwargs)
        gun = Gun(gun_type)
        gun.reload()
        self.gun = gun

    def render(self) -> RenderResult:
        """Render the chamber."""
        # Create textual representation of chambers
        chamber = self.gun.chamber
        chamber_str = ["•" for _ in range(len(chamber))]
        shot_bullet_desc = ""
        match self.shot_bullet:
            case 1:
                shot_bullet_desc = "L"
            case 2:
                shot_bullet_desc = "B"
            case 3 | 4:
                shot_bullet_desc = "P"

        return shot_bullet_desc + " " + " ".join(chamber_str)

    def reload(self) -> None:
        """Reload the revolver."""
        self.gun.reload()
        self.shot_bullet = -1
        self.update()

class RouletteGame(App):
    """A smart Russian Roulette Simulator."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "roulette_game.tcss"

    def __init__(self, gun_type, **kwargs):
        """Initialize the game."""
        super().__init__(**kwargs)
        self.chamber = Chamber(gun_type, id="chamber")

    def on_mount(self) -> None:
        """Update widgets on mount."""
        # watch the character picker to update the opponent

        def update_agent_name(selected: str):
            agent_board = self.query_one("#agent_board")
            agent_board.player_name = selected
            agent_board.update_border_title()

        picker = self.query_one(CharacterPicker)
        self.watch(picker, "selected", update_agent_name)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield CharacterPicker()
        yield PlayerBoard("Sam", id="agent_board")
        yield self.chamber
        yield PlayerBoard("Player", id="player_board")

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    @on(Button.Pressed, "#shoot_opponent")
    def handle_shoot_opponent(self):
        """Handle shoot opponent."""
        print("shoot opponent")
        self.shoot()

    @on(Button.Pressed, "#shoot_myself")
    def handle_shoot_myself(self):
        """Handle shoot myself."""
        print("shoot myself")
        self.shoot()

    def shoot(self) -> None:
        """Pull the trigger."""
        chamber_node = self.query_one(Chamber)
        gun = chamber_node.gun

        # reload the revolver when go through all chambers
        if len(gun.chamber) == 0:
            chamber_node.reload()
        else:
            shot_bullet = gun.shoot()
            chamber_node.shot_bullet = shot_bullet
            print("Shot bullet: ", shot_bullet)

        chamber_node.update()
        print(f"Remaining chambers: {len(gun.chamber)}")


if __name__ == "__main__":
    app = RouletteGame(GunType.REVOLVER)
    app.run()
