from register8 import Register8



class Seed48:
    """
    Elite's 48bit seed: 3 16bit registers: w0, w1, w2

    With algo to move to next state.

    And generate seed from name

    """

    w0_lo = None
    w0_hi = None

    w1_lo = None
    w1_hi = None

    w2_lo = None
    w2_hi = None

    def __init__(self):
        self.reset()

    def reset(self):
        self.w0_lo = Register8(0x17)
        self.w0_hi = Register8(0x23)

        self.w1_lo = Register8(0x5E)
        self.w1_hi = Register8(0xE5)

        self.w2_lo = Register8(0x84)
        self.w2_hi = Register8(0x19)

    def __repr__(self) -> str:
        w0 = (self.w0_hi._val << 8) | self.w0_lo._val
        w1 = (self.w1_hi._val << 8) | self.w1_lo._val
        w2 = (self.w2_hi._val << 8) | self.w2_lo._val


        return (
            f"w0 = 0x{w0:04X}\t"
            f"w1 = 0x{w1:04X}\t"
            f"w2 = 0x{w2:04X}\t"
        )

    def verbose(self) -> str:
        return (
            f"{self.w0_lo}\t"
            f"{self.w0_hi}\t"
            f"{self.w1_lo}\tn"
            f"{self.w1_hi}\t"
            f"{self.w2_lo}\t"
            f"{self.w2_hi}\t"
        )

    # takes the name of a system/npc/object and turns into a 48bit seed
    # uses the Elite step to randomize between each letter for lots of randomness
    # once you have that seed, you then advance to next state and grab your byte from the 48 for procgen
    # (and lol, this ": str" is just documentation, it's not even checked at runtime! :table_flip:)
    def set_from_name(self, name: str):
        self.reset()

        # add char valus to one of w1's bytes
        # w1 used in all the sums (w0+w1, w1+w2, w0+w1+w2)
        # advance seed each time to scramble in
        for char in name:
            self.w1_lo.add(ord(char))
            self.next_seed()
            self.next_seed()
            self.next_seed()
            self.next_seed()
            self.next_seed()

        # 5 times so any small change has mixed up all seeds
        self.next_seed()
        self.next_seed()
        self.next_seed()
        self.next_seed()
        self.next_seed()

        return self


    # next seed Elite algo - but algo from LLMs is dodgy 
    #   they disagree even with themselves on the exact details...
    # To move from one to next:
    #     w0 = w0 + w1                          # some LLMs say this is just w0 = w1, just shifting, but add does the shift anyway: w0=0, w1=3, new w0=3 - shifted
    #     w1 = w1 + w2                          # same as above, add not shift
    #     w2 = old_w0 + old_w1 + w2             # but new w0 is already old w0 + old w1 so...
    #     w2 = w0 + w2                          # w0 is already w0 + w1, so we're just adding w2
    # But we're doing it with Register8s        - so we'll see the ADC carries within the 16bit seeds
    def next_seed(self):
        # w0 = w0 + w1
        self.w0_lo.add(self.w1_lo._val)         # just add lows without carry
        self.w0_hi.carry = self.w0_lo.carry     # carry the carry :)
        self.w0_hi.adc(self.w1_hi._val)         # add hights with the lo's carry

        # w1 = w1 + w2
        self.w1_lo.add(self.w2_lo._val)         # just add lows without carry
        self.w1_hi.carry = self.w1_lo.carry     # carry the carry :)
        self.w1_hi.adc(self.w2_hi._val)         # add hights with the lo's carry

        # w2 = w0 + w2
        self.w2_lo.add(self.w0_lo._val)         # just add lows without carry
        self.w2_hi.carry = self.w2_lo.carry     # carry the carry :)
        self.w2_hi.adc(self.w0_hi._val)         # add hights with the lo's carry


if __name__ == "__main__":
    seed = Seed48()
    seed.set_from_name("MAWF")
    print(seed)
    seed.next_seed()
    print(seed)
    seed.next_seed()
    print(seed)
    seed.next_seed()
    print(seed)
    seed.next_seed()
    print(seed)
    seed.next_seed()
    print(seed)


