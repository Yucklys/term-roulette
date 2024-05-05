"""Russian Roulette Game implementation in TUI."""

from .ui import RouletteGame
from GunMechanics import GunType


def run_game():
    """Run the game in current shell."""
    app = RouletteGame(GunType.REVOLVER)
    app.run()
