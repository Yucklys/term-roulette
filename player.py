from enum import Enum


class PlayerType(Enum):
    PLAYER = 1
    AGENT = 2

    def opp(self):
        """Return the opponent of the player type."""
        if self == PlayerType.PLAYER:
            return PlayerType.AGENT
        else:
            return PlayerType.PLAYER


def calculate_reward(self, health, gun):
    bullets_left, blank_count, dd_count, heal_count = gun.bullet_distribution()
    positions_left = len(gun.chamber)
    double_bullet_found = True if dd_count != 0 else False
    heal_chamber_found = True if heal_count != 0 else False

    if double_bullet_found:
        shoot_opponent = 10
        shoot_self = -6
    else:
        shoot_opponent = 5
        shoot_self = -3

    if heal_chamber_found:
        shoot_blank_opponent = -3
        shoot_blank_self = 5
    else:
        shoot_blank_opponent = -1
        shoot_blank_self = 3

    bullet_probability = bullets_left / positions_left

    expected_shoot_opponent = (
        bullet_probability * shoot_opponent
        + (1 - bullet_probability) * shoot_blank_opponent
    )
    expected_shoot_self = (
        bullet_probability * shoot_self + (1 - bullet_probability) * shoot_blank_self
    )

    return expected_shoot_self, expected_shoot_opponent


def decide_action(self, health, player_moves, gun):
    reward_shoot_self, reward_shoot_opponent = self.calculate_reward(health, gun)

    if reward_shoot_self > reward_shoot_opponent:
        return "shoot_self"
    else:
        return "shoot_opponent"
