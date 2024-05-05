from enum import *
import random


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


class Gun:
    def __init__(self, type: GunType):
        if type == GunType.REVOLVER:
            self.weapon_name = GunType.REVOLVER.value
            self.mag_size = 6
            self.chamber = [None] * 6

        elif type == GunType.HANDGUN:
            self.weapon_name = GunType.HANDGUN.value
            self.mag_size = 10
            self.chamber = [None] * 10

        elif type == GunType.SHOTGUN:
            self.weapon_name = GunType.SHOTGUN
            self.mag_size = 2
            self.chamber = [None] * 2

    def reload(self):
        self.chamber = [None] * self.mag_size

        chamber_count = 0
        while chamber_count != (self.mag_size / 2):
            n = random.randint(0, (self.mag_size - 1))
            self.chamber[n] = 1
            chamber_count += 1

        for i in range(self.mag_size):
            if self.chamber[i] == None:
                rand_power_up_or_blank = random.randint(2, 4)
                self.chamber[i] = rand_power_up_or_blank

    def bullet_distribution(self):
        blank_count = live_count = powerUp_count = 0

        for i in range(len(self.chamber)):
            if self.chamber[i] == 1:
                live_count += 1
            elif self.chamber[i] == 2:
                blank_count += 1
            else:
                powerUp_count += 1

        return blank_count, live_count, powerUp_count

    def get_current_bullet(self):
        val = self.chamber[0]
        if val <= 2:
            return AmmoType(val)
        else:
            return PowerUps(val)

    def shoot(self):
        bullet_being_shot = None

        if len(self.chamber) != 0:
            bullet_being_shot = self.chamber.pop(0)

        return bullet_being_shot
