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


class Agent(Enum):
    MIMIC = "Mimic"
    BERSERKER = "Berserker"


class Action(Enum):
    SHOOT_SELF = "shoot_self"
    SHOOT_OPPONENT = "shoot_opponent"


def calculate_reward(health, gun):
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

    # If there are no bullets left, return 0, 0 to avoid division by zero
    if positions_left == 0:
        return 0, 0

    bullet_probability = bullets_left / positions_left

    expected_shoot_opponent = (
        bullet_probability * shoot_opponent
        + (1 - bullet_probability) * shoot_blank_opponent
    )
    expected_shoot_self = (
        bullet_probability * shoot_self + (1 - bullet_probability) * shoot_blank_self
    )

    return expected_shoot_self, expected_shoot_opponent


def decide_action(health, gun):
    reward_shoot_self, reward_shoot_opponent = calculate_reward(health, gun)

    if reward_shoot_self > reward_shoot_opponent:
        return Action.SHOOT_SELF
    else:
        return Action.SHOOT_OPPONENT
