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
    
    # 3 pair test
    @classmethod
    def fpt(cls):
        pairIndex = random.randint(0, 127) * 2
        name = cls.the_one_string[pairIndex : pairIndex + 2]
        pairIndex = random.randint(0, 127) * 2
        name = name + cls.the_one_string[pairIndex : pairIndex + 2]
        pairIndex = random.randint(0, 127) * 2
        name = name + cls.the_one_string[pairIndex : pairIndex + 2]

        return name
    
if __name__ == "__main__":
    print(ProcgenName.fpt())

