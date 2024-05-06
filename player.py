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


class validMoves(Enum):
    SHOOT_OPPONENT = 0
    SHOOT_SELF = 1
    USE_DOUBLE_DAMAGE_BULLET = 2
    USE_HEAL = 3


def decide_action(health, player_moves, game_state):
    # Hypothetical reward calculation using provided game state
    reward_shoot_self = calculate_reward_shoot_self(health, player_moves, game_state)
    reward_shoot_opponent = calculate_reward_shoot_opponent(
        health, player_moves, game_state
    )

    if reward_shoot_self > reward_shoot_opponent:
        return "shoot_self"
    else:
        return "shoot_opponent"


def calculate_reward_shoot_self(health, player_moves, game_state):
    # Placeholder for calculating the reward for shooting oneself
    # Modify this function to use real game state logic
    return 10  # Example static value


def calculate_reward_shoot_opponent(health, player_moves, game_state):
    # Placeholder for calculating the reward for shooting the opponent
    # Modify this function to use real game state logic
    return 20  # Example static value


class Player:
    def __init__(self, health: int, player_moves: list):
        self.health = health
        self.player_moves = player_moves

    def action_Against_Self(self, action, bullet_shot):
        if action == validMoves.SHOOT_SELF and bullet_shot == 2:
            self.player_moves.append(validMoves.SHOOT_SELF)
        elif action == validMoves.SHOOT_SELF and bullet_shot == 1:
            self.player_moves.append(validMoves.SHOOT_SELF)
            self.health -= 1
        elif action == validMoves.SHOOT_SELF and bullet_shot == 3:
            self.player_moves.append(validMoves.SHOOT_SELF)
            self.player_moves.append(validMoves.USE_DOUBLE_DAMAGE_BULLET)
            self.health -= 2
        elif action == validMoves.SHOOT_SELF and bullet_shot == 4:
            self.player_moves.append(validMoves.SHOOT_SELF)
            self.player_moves.append(validMoves.USE_HEAL)
            self.health += 1

    def action_Against_Opp(self, action, bullet_shot):
        damage_to_opponent = 0
        if action == validMoves.SHOOT_OPPONENT and bullet_shot == 2:
            self.player_moves.append(validMoves.SHOOT_OPPONENT)
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 1:
            self.player_moves.append(validMoves.SHOOT_OPPONENT)
            damage_to_opponent += 1
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 3:
            self.player_moves.append(validMoves.SHOOT_OPPONENT)
            self.player_moves.append(validMoves.USE_DOUBLE_DAMAGE_BULLET)
            damage_to_opponent += 2
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 4:
            self.player_moves.append(validMoves.SHOOT_SELF)
            self.player_moves.append(validMoves.USE_HEAL)
            damage_to_opponent -= 1

    def update_health(self, amount):
        self.health += amount


class Ai:
    def __init__(self, health: int, ai_type):
        self.health = health
        self.type = ai_type
        if ai_type == "mimic":
            self.moves = []

    def action_Against_Self(self, action, bullet_shot):
        if action == validMoves.SHOOT_SELF and bullet_shot == 2:
            self.health -= 0
        elif action == validMoves.SHOOT_SELF and bullet_shot == 1:
            self.health -= 1
        elif action == validMoves.SHOOT_SELF and bullet_shot == 3:
            self.health -= 2
        elif action == validMoves.SHOOT_SELF and bullet_shot == 4:
            self.health += 1

    def action_Against_Opp(self, action, bullet_shot):
        damage_to_opponent = 0
        if action == validMoves.SHOOT_OPPONENT and bullet_shot == 2:
            damage_to_opponent += 0
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 1:
            damage_to_opponent += 1
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 3:
            damage_to_opponent += 2
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 4:
            damage_to_opponent -= 1

    def copy(self, moves_to_follow):
        if self.type == "mimic":
            self.moves = moves_to_follow

    def update_health(self, damage_recieved):
        if damage_recieved < 0:
            self.health += 1
        else:
            self.health -= damage_recieved
