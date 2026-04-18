from register8 import Register8
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
    name = "not set"

    # LFSR register
    lfsr = Register8(0x17)

    def __repr__(self) -> str:
        return (
            "Name:\n"
            f"\t{self.name}\n"
            f"\t{self.lfsr}"
        )

    def c64_style_lfsr_right(self):
        # shift right
        self.lfsr.shr()

        # if carry, XOR with magic $1D
        if self.lfsr.carry:
            self.lfsr.XOR(0xB8)

        return self

    def c64_style_lfsr_left(self):
        # shift right
        self.lfsr.shl()

        # if carry, XOR with magic $1D
        if self.lfsr.carry:
            self.lfsr.XOR(0x1D)

        return self
    






if __name__ == "__main__":
    name = ProcgenName().rng_len(3)
    print(name)
    print("right shift:")
    # Example usage
    for _ in range(8):
        print(name.lfsr)
        state = name.c64_style_lfsr_right()

    print("\nright left:\n")
    # Example usage
    for _ in range(8):
        print(name.lfsr)
        state = name.c64_style_lfsr_left()



