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

class Player():
    def __init__(self, health: int, player_moves: list):
        self.health = health
        self.player_moves = player_moves
        
    def calculate_reward(self, health, gun):

        bullets_left, blank_count, dd_count, heal_count = gun.bullet_distribution()
        positions_left = bullets_left + blank_count
        double_bullet_found = True if dd_count == 0 else False
        heal_chamber_found = True if heal_count == 0 else False

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

        bullet_probability = bullets_left/positions_left

        expected_shoot_opponent = bullet_probability*shoot_opponent + (1-bullet_probability)*shoot_blank_opponent
        expected_shoot_self = bullet_probability*shoot_self + (1-bullet_probability)*shoot_blank_self

        return expected_shoot_self, expected_shoot_opponent
    
    def decide_action(self, health, player_moves, gun):
        reward_shoot_self, reward_shoot_opponent = self.calculate_reward(health, player_moves, gun)

        if reward_shoot_self > reward_shoot_opponent:
            return 'shoot_self'
        else:
            return 'shoot_opponent'
    
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
            damage_to_opponent +=2
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 4:
            self.player_moves.append(validMoves.SHOOT_SELF)
            self.player_moves.append(validMoves.USE_HEAL)
            damage_to_opponent -= 1

    def update_health(self, amount):
        self.health += amount
    



class Ai():
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
            damage_to_opponent +=2
        elif action == validMoves.SHOOT_OPPONENT and bullet_shot == 4:
            damage_to_opponent -= 1


    def copy(self, moves_to_follow):
        if self.type == "mimic":
            self.moves = moves_to_follow


    def update_health(self, damage_recieved):
        if damage_recieved < 0 :
            self.health += 1
        else :
            self.health -= damage_recieved



    

  
        
    
    

