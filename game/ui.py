"""UI for the roulette game."""

from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Footer, Header, Static, Button, ListView, Label
from textual.reactive import reactive
from textual.containers import Vertical, Horizontal
from textual import on, log, work
from .picker import CharacterPicker, GunPicker
from GunMechanics import Gun, GunType
from player import *
from enum import Enum
import time


class GameState(Enum):
    """Game state enum."""

    GAME_START = 0
    PLAYER_TURN = 1
    AGENT_TURN = 2
    GAME_OVER = 3


class PlayerBoard(Static):
    """A widget to display the player's board."""

    player_name = reactive("")
    hp = reactive(5, recompose=True)

    def __init__(self, player_name="", **kwargs):
        """Initialize the player's board."""
        super().__init__(**kwargs)
        self.player_name = player_name
        match self.id:
            case "agent_board":
                self.player_type = PlayerType.AGENT
            case "player_board":
                self.player_type = PlayerType.PLAYER
        self.max_hp = 5
        self.update_border_title()

    def compose(self) -> ComposeResult:
        """Create the player's board."""
        with Vertical():
            yield Static(f"Health: {self.hp}/{self.max_hp}")
            with Horizontal():
                yield Button("Shoot opponent", id="shoot_opponent", variant="error")
                yield Button("Shoot myself", id="shoot_self", variant="warning")

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

    def handle_on_hit(self, bullet_type):
        """Respond to the shoot event. Return the damage taken from this shot."""
        hp_change = 0
        if bullet_type == 1:
            hp_change = -1
        elif bullet_type == 2:
            pass
        elif bullet_type == 3:
            hp_change = -2
        elif bullet_type == 4:
            hp_change = 1

        new_hp = self.hp + hp_change
        # Check if the new hp exceeds the max hp
        if new_hp > self.max_hp:
            hp_change = 0
        self.hp += hp_change

        return hp_change

    def reset(self):
        """Reset the player's board."""
        self.hp = self.max_hp


class Chamber(Static):
    shot_bullet = reactive(0)

    """A widget to display the chamber."""

    def __init__(self, **kwargs):
        """Initialize the chamber."""
        super().__init__(**kwargs)
        self.gun = None

    def render(self) -> RenderResult:
        """Render the chamber."""
        # Create textual representation of chambers
        chamber = self.gun.chamber
        chamber_str = ["•" for _ in range(len(chamber))]
        shot_bullet_desc = ""
        match self.shot_bullet:
            case 1:
                shot_bullet_desc = "Loaded"
            case 2:
                shot_bullet_desc = "Blank"
            case 3:
                shot_bullet_desc = "Double Damage"
            case 4:
                shot_bullet_desc = "Heal"

        return shot_bullet_desc + " " + " ".join(chamber_str)

    def switch_gun(self, gun_type: str) -> None:
        """Switch the gun type."""
        self.gun = Gun(GunType[gun_type])
        self.reload()

    def reload(self) -> None:
        """Reload the revolver."""
        self.gun.reload()
        self.shot_bullet = -1
        bullet_distribution = self.gun.bullet_distribution()
        live_count, blank_count, dd_count, heal_count = bullet_distribution
        log("Chamber distribution: ", bullet_distribution)
        log("Chamber: ", self.gun.chamber)
        # Notify the user about the chamber distribution
        self.notify(
            f"L: {live_count} D: {dd_count} B: {blank_count} H: {heal_count}",
            title="Gun reloaded!",
            timeout=30,
        )
        self.update()


class RouletteGame(App):
    """A smart Russian Roulette Simulator."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "roulette_game.tcss"

    game_state = reactive(GameState.GAME_START)

    def __init__(self, **kwargs):
        """Initialize the game."""
        super().__init__(**kwargs)
        self.chamber = Chamber(id="chamber", classes="hidden")
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
        yield Label("", id="game_over", classes="hidden")
        yield Button("Restart", id="restart", classes="hidden")

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.dark = not self.dark

    @on(Button.Pressed, "#shoot_opponent")
    def handle_shoot_opponent(self):
        """Handle shoot opponent."""
        # get board type by game state
        match self.game_state:
            case GameState.PLAYER_TURN:
                self_type = PlayerType.PLAYER
            case GameState.AGENT_TURN:
                self_type = PlayerType.AGENT
        opp_type = self_type.opp()
        log(f"{self_type} choose to shoot opponent")
        self.shoot(opp_type, self_type)

    @on(Button.Pressed, "#shoot_self")
    def handle_shoot_self(self):
        """Handle shoot myself."""
        # get board type by game state
        match self.game_state:
            case GameState.PLAYER_TURN:
                self_type = PlayerType.PLAYER
            case GameState.AGENT_TURN:
                self_type = PlayerType.AGENT
        log(f"{self_type} choose to shoot self")
        self.shoot(self_type, self_type)

    @on(Button.Pressed, "#restart")
    def handle_restart(self):
        """Handle the restart button."""
        self.game_state = GameState.GAME_START
        self.opponent = None
        self.option_selcted = 0
        self.query_one("#game_over").add_class("hidden")
        self.query_one("#restart").add_class("hidden")
        pickers = self.query(CharacterPicker)
        for picker in pickers:
            picker.remove_class("hidden")
        boards = self.query(PlayerBoard)
        for board in boards:
            board.reset()
            board.add_class("hidden")
        self.query_one(Chamber).add_class("hidden")

    @on(ListView.Selected)
    def handle_list_view_selected(self, selected: ListView.Selected):
        """Handle the selected character."""
        list_view = selected.control
        match list_view.id:
            case "character_picker":
                opponent = selected.item.label
                self.opponent = Agent(opponent)
                log(f"Opponent: {self.opponent}")
                self.query_one("#agent_board").player_name = opponent
                self.option_selcted += 1
            case "gun_picker":
                gun_type = selected.item.label.upper()
                log(f"Gun type: {gun_type}")
                self.chamber.switch_gun(gun_type)
                self.option_selcted += 1

        if self.option_selcted == 2:
            self.game_start()

    def handle_agent_turn(self):
        deceision = None
        # match opponent AI type
        match self.opponent:
            case Agent.MIMIC:
                # Let player decide for this agent
                pass
            case Agent.BERSERKER:
                # Choose the best action for this agent
                agent = self.query_one("#agent_board")
                gun = self.query_one(Chamber).gun
                health = agent.hp
                decision = decide_action(health, gun)
                log(f"Agent decision: {decision}")

        # If the agent is making the decision, then proceed with the decision
        if decision is not None:
            self.handle_decision(decision)

        if len(self.query_one(Chamber).gun.chamber) == 0:
            self.query_one(Chamber).reload()

    @work(thread=True)
    def handle_decision(self, decision: Action):
        """Handle the decision made by the agent."""
        self_type = PlayerType.AGENT
        target = PlayerType.PLAYER
        # Wait for 3 seconds before shooting
        # This is to give the player some time to see the last bullet
        time.sleep(3)
        # match the action
        match decision:
            case Action.SHOOT_SELF:
                self.shoot(self_type, self_type)
            case Action.SHOOT_OPPONENT:
                self.shoot(target, self_type)

    def game_start(self) -> None:
        """Start the game and set the opponent."""
        self.log("Game start")
        agent_board = self.query_one("#agent_board")
        player_board = self.query_one("#player_board")
        chamber = self.query_one(Chamber)
        # Show the player and agent boards
        player_board.remove_class("hidden")
        agent_board.remove_class("hidden")
        chamber.remove_class("hidden")

        # Disable the agent's board
        agent_board.disabled = True

        # Switch to player's turn
        self.game_state = GameState.PLAYER_TURN

    def game_switch_turn(self, continue_turn: bool):
        """Switch the game turn."""
        # Do not switch turn if continue is True
        new_game_state = (
            GameState.AGENT_TURN
            if self.game_state == GameState.PLAYER_TURN
            else GameState.PLAYER_TURN
        )
        if continue_turn:
            log("Continue turn")
            new_game_state = self.game_state
        else:
            log("Switch turn")

        # Disable the player's board when it's not his turn
        match new_game_state:
            case GameState.PLAYER_TURN:
                self.query_one("#player_board").disabled = False
                self.query_one("#agent_board").disabled = True
            case GameState.AGENT_TURN:
                disable_agent_board = False if self.opponent == Agent.MIMIC else True
                self.query_one("#agent_board").disabled = disable_agent_board
                self.query_one("#player_board").disabled = True
                self.handle_agent_turn()

        self.game_state = new_game_state

    def game_over(self, losser: PlayerType):
        """End the game."""
        self.game_state = GameState.GAME_OVER
        if losser == PlayerType.PLAYER:
            result = "lost"
        else:
            result = "won"
        result = f"Game over! You {result}!"
        self.query_one("#game_over").update(result)
        log(result)

        # Hide the boards and chamber
        agent_board = self.query_one("#agent_board")
        player_board = self.query_one("#player_board")
        chamber = self.query_one(Chamber)
        agent_board.add_class("hidden")
        player_board.add_class("hidden")
        chamber.add_class("hidden")

        # Show the game over message and restart button
        self.query_one("#game_over").remove_class("hidden")
        self.query_one("#restart").remove_class("hidden")

    def shoot(self, target: PlayerType, self_type: PlayerType):
        """Pull the trigger."""
        chamber_node = self.query_one(Chamber)
        gun = chamber_node.gun
        log(f"Current turn: {self.game_state}")

        # reload the revolver when go through all chambers
        if len(gun.chamber) == 0:
            chamber_node.reload()
        else:
            shot_bullet = gun.shoot()
            chamber_node.shot_bullet = shot_bullet
            board = self.get_player_board(target)
            # reverse self_type if the target is shooting himself
            hp_change = board.handle_on_hit(shot_bullet)
            # continue the turn if the player is shooting himself with a blank bullet
            continue_turn = True if hp_change == 0 and target == self_type else False
            # switch turn if the player is not shooting himself with a blank bullet
            log(hp_change=hp_change, target=target, self_type=self_type)

            chamber_node.update()
            self.game_switch_turn(continue_turn)

            log("Shot bullet: ", shot_bullet)

        log(f"Current chambers: {gun.chamber}")

        # Check if the game is over
        board = self.get_player_board(target)
        if board.hp <= 0:
            self.game_over(target)

    def get_player_board(self, player_type):
        """Get the player board with given player type."""
        return (
            self.query_one("#agent_board")
            if player_type == PlayerType.AGENT
            else self.query_one("#player_board")
        )

    def get_player_type(self):
        """Get the player type by matching game state."""
        return (
            PlayerType.PLAYER
            if self.game_state == GameState.PLAYER_TURN
            else PlayerType.AGENT
        )


if __name__ == "__main__":
    app = RouletteGame()
    app.run()
