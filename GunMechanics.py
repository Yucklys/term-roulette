from enum import *
import random

class ValidMoves(Enum):
    SHOOT_AI = 0
    SHOOT_PLAYER = 1

class PowerUps(Enum):
    DOUBLE_DAMAGE = 3
    HEAL = 4

class GunType(Enum):
    REVOLVER = "Revolver"
    HANDGUN = "Handgun"
    SHOTGUN = "Shoutgun"

class AmmoType(Enum):
    LIVE_ROUND = 1
    BLANK_ROUND = 2


class LoadGun:
    def __init__(self, type: GunType):
        
        if type == GunType.REVOLVER:
            self.weapon_name = GunType.REVOLVER.value
            self.mag_size = 6
            self.chamber = [None] * 6
            self.populate()

        elif type == GunType.HANDGUN:
            self.weapon_name =  GunType.HANDGUN.value
            self.mag_size = 10
            self.chamber = [None] * 10
            self.populate()

        elif type == GunType.SHOTGUN:
            self.weapon_name = GunType.SHOTGUN
            self.mag_size = 2
            self.chamber = [None] * 2
            self.populate()
    
    def populate(self):
        chamber_count = 0
        while chamber_count != (self.mag_size/2):
            n = random.randint(0, (self.mag_size - 1))
            self.chamber[n] = 1
            chamber_count += 1

        for i in range(self.mag_size):
            if self.chamber[i] == None:
                rand_power_up_or_blank = random.randint(2,4)
                self.chamber[i] = rand_power_up_or_blank
        
        
    def get_current_bullet(self):
         val = self.chamber[0]
         if val <= 2 :
             return AmmoType(val)
         else:
             return PowerUps(val)
      
    def shoot(self):
        bullet_being_shot = None
        
        if(self.chamber.len()!= 0):
            bullet_being_shot = self.chamber.pop(0)

        return bullet_being_shot



