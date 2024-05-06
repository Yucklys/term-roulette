"""UI for the roulette game."""

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Footer, Header, Static, Button, ListView
from textual.reactive import reactive
from textual import on
from .picker import CharacterPicker, GunPicker
from GunMechanics import Gun, GunType
from enum import Enum


class GameState(Enum):
    """Game state enum."""

    GAME_START = 0
    PLAYER_TURN = 1
    AGENT_TURN = 2
    GAME_OVER = 3


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

    def watch_player_name(self, player_name: str) -> None:
        """
        Watch the player name.
        Update the border title when player_name changes.
        """
        self.player_name = player_name
        self.update_border_title()


class Chamber(Static):
    shot_bullet = reactive(0)
    
    """A widget to display the chamber."""
    def __init__(self, gun_type, **kwargs):
        """Initialize the chamber."""
        super().__init__(**kwargs)
        self.switch_gun(gun_type)

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

    def switch_gun(self, gun_type: str) -> None:
        """Switch the gun type."""
        self.gun = Gun(GunType[gun_type])
        self.gun.reload()

    def reload(self) -> None:
        """Reload the revolver."""
        self.gun.reload()
        self.shot_bullet = -1
        self.update()


class RouletteGame(App):
    """A smart Russian Roulette Simulator."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "roulette_game.tcss"

    game_state = reactive(GameState.GAME_START)

    def __init__(self, **kwargs):
        """Initialize the game."""
        super().__init__(**kwargs)
        self.chamber = Chamber("HANDGUN", id="chamber", classes="hidden")
        self.opponent = None
        self.option_selcted = 0

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield CharacterPicker(id="character_picker")
        yield GunPicker(id="gun_picker")
        yield PlayerBoard("Agent", id="agent_board", classes="hidden")
        yield self.chamber
        yield PlayerBoard("Player", id="player_board", classes="hidden")
        yield Static("Game Over!", id="game_over", classes="hidden")

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

    @on(ListView.Selected)
    def handle_list_view_selected(self, selected: ListView.Selected):
        """Handle the selected character."""
        list_view = selected.control
        match list_view.id:
            case "character_picker":
                self.opponent = selected.item.label
                print(f"Opponent: {self.opponent}")
                self.query_one("#agent_board").player_name = self.opponent
                self.option_selcted += 1
            case "gun_picker":
                gun_type = selected.item.label.upper()
                print(f"Gun type: {gun_type}")
                self.chamber.switch_gun(gun_type)
                self.option_selcted += 1

        if self.option_selcted == 2:
            self.game_start()

    def game_start(self) -> None:
        """Start the game and set the opponent."""
        print("Game start")
        self.game_state = GameState.PLAYER_TURN
        agent_board = self.query_one("#agent_board")
        player_board = self.query_one("#player_board")
        chamber = self.query_one(Chamber)
        # Show the player and agent boards
        player_board.remove_class("hidden")
        agent_board.remove_class("hidden")
        chamber.remove_class("hidden")

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
    app = RouletteGame()
    app.run()
