from register8 import Register8
from procgen_seed48 import Seed48
import random



class ProcgenName:
    """
    Uses the Elite-style the_one_string with pairs of letters
    that can be used to form syllables in words / name for the procgen world.

    I'm going to borrow the romanization of Hiragana from Japanese to give me Japanese-sounding names.
    And I'm going to bastardize it so I have enough for 128 pairs (max 8bit index 254 for last pair)

    Single chars: like Elite, just ignore space when printing ("A TADA" is "TADA", "BAN KIRU" becomes "BANKIRU")

    Spaces aren't needed because if you want multiple names, you ask for them. 

    """
    # the one magic string!
    # pairs of letters that we'll use to generate all the names for the game
    # Japanese-sounding by basing it on romanticized Hiragana
    # 'Pascal' case so I can see what's going on, C64 will be all caps / single char font
    the_one_string = (
        "A I U E O N "
        "KaKiKuKeKoKy"
        "SaSiSuSeSoSy"
        "TaSiTuTeToTy"
        "NaNiNuNeNoNy"
        "HaHiHuHeHoHy"
        "MaMiMuMeMoMy"
        "YaYiYuYeYoY "
        "RaRiRuReRoRy"
        "WaWiWuWeWoWy"
        "GaGiGuGeGoGy"
        "ZaZiZuZeZoZY"
        "DaDiDuDeDoDY"
        "BaBiBuBeBoBy"
        "PaPiPuPePoPy"
        "JaJiJuJeJoJy"

        "KaKiKuKeKoKy"
        "SaSiSuSeSoSy"
        "TaSiTuTeToTy"
        "NaNiNuNeNoNy"
        "HaHiHuHeHoHy"
        "' - "
    )

    # 128 pairs for 256 len is what we want here
    @classmethod
    def len(cls):
        return len(cls.the_one_string)
    
    # creates name of len pairs from RNG
    def rng_len(self, len: int):
        self.name = ""
        for i in range(len):
            pair_index = random.randint(0, 127) * 2
            self.name = self.name + self.the_one_string[pair_index : pair_index + 2]
            self.name = self.name.replace(" ", "")

        return self
    
    # name
    name = None

    def __repr__(self) -> str:
        return (
            f"{self.name}"
        )

    def single_from_seed(self, seed: Seed48):
        self.name = ""
        return self.add_name()
    
    def multi_from_seed(self, seed: Seed48):
        self.name = ""
        size_list = [1, 2, 2, 2, 2, 3, 3, 4]
        index = seed.w0_hi._val & 0b00000111
        size = size_list[index]
        for i in range(0, size):
            self.add_name(seed)
            self.name = self.name + " "

        return self


    def add_name(self, seed: Seed48):
        size_list = [1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5]
        # how many pairs
        # 0-15 index
        index = seed.w0_lo._val & 0b00001111
        size = size_list[index]

        # get name from that many pairs
        for i in range(0, size):
            pair_index = (seed.w2_lo._val & 0b01111111) * 2
            self.name = self.name + self.the_one_string[pair_index : pair_index + 2].replace(" ", "")
            seed.next_seed()

        return self



if __name__ == "__main__":
    seed = Seed48()
    name = "Bob 0"
    print(name)
    seed.set_from_name(name)
    name = ProcgenName().multi_from_seed(seed)
    print(name)
    name = "Bob 1"
    print(name)
    seed.set_from_name(name)
    name = ProcgenName().multi_from_seed(seed)
    print(name)
    name = "Bob 2"
    print(name)
    seed.set_from_name(name)
    name = ProcgenName().multi_from_seed(seed)
    print(name)
    name = "Bob 3"
    print(name)
    seed.set_from_name(name)
    name = ProcgenName().multi_from_seed(seed)
    print(name)



