"""Russian Roulette Game implementation in TUI."""

from .ui import RouletteGame


def run_game():
    """Run the game in current shell."""
    app = RouletteGame()
    app.run()
