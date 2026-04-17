"""
register8.py — 8-bit CPU register emulator
Supports: load, shift, rotate, carry flag, arithmetic, logic ops
"""


class Register8:
    """
    Emulates an 8-bit CPU register with flags.

    Flags tracked:
        carry (C)    — bit shifted/rotated out, or arithmetic overflow
        zero  (Z)    — result was 0x00
        neg   (N)    — bit 7 of result is set (negative in signed arithmetic)
    """

    def __init__(self, value: int = 0):
        self._val = 0
        self.carry = False
        self.zero = False
        self.neg = False
        self.load(value)

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def _store(self, value: int, carry: bool = False):
        """Mask to 8 bits, update flags, store."""
        self._val = value & 0xFF
        self.carry = carry
        self.zero = (self._val == 0)
        self.neg = bool(self._val & 0x80)
        return self

    @property
    def value(self) -> int:
        return self._val

    @value.setter
    def value(self, v: int):
        self.load(v)

    def load(self, value: int) -> "Register8":
        """Load a value into the register (carry cleared)."""
        return self._store(value & 0xFF, carry=False)

    # ------------------------------------------------------------------
    # Shifts  (bit shifted out goes to carry)
    # ------------------------------------------------------------------

    def shl(self) -> "Register8":
        """Logical shift left. MSB → carry, LSB filled with 0."""
        carry = bool(self._val & 0x80)
        return self._store(self._val << 1, carry=carry)

    def shr(self) -> "Register8":
        """Logical shift right. LSB → carry, MSB filled with 0."""
        carry = bool(self._val & 0x01)
        return self._store(self._val >> 1, carry=carry)

    def asr(self) -> "Register8":
        """Arithmetic shift right. LSB → carry, MSB sign-extended."""
        carry = bool(self._val & 0x01)
        sign = self._val & 0x80          # preserve bit 7
        return self._store((self._val >> 1) | sign, carry=carry)

    # ------------------------------------------------------------------
    # Rotates  (bit rotated out wraps around — optionally through carry)
    # ------------------------------------------------------------------

    def rol(self) -> "Register8":
        """Rotate left. MSB wraps to LSB; carry = old MSB."""
        carry = bool(self._val & 0x80)
        return self._store((self._val << 1) | (self._val >> 7), carry=carry)

    def ror(self) -> "Register8":
        """Rotate right. LSB wraps to MSB; carry = old LSB."""
        carry = bool(self._val & 0x01)
        return self._store((self._val >> 1) | (self._val << 7), carry=carry)

    def rol_carry(self) -> "Register8":
        """Rotate left *through* carry (9-bit rotation, like 6502 ROL).
        old carry → LSB, MSB → new carry."""
        new_carry = bool(self._val & 0x80)
        return self._store((self._val << 1) | int(self.carry), carry=new_carry)

    def ror_carry(self) -> "Register8":
        """Rotate right *through* carry (9-bit rotation, like 6502 ROR).
        old carry → MSB, LSB → new carry."""
        new_carry = bool(self._val & 0x01)
        return self._store((self._val >> 1) | (int(self.carry) << 7), carry=new_carry)

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------

    def add(self, operand: int) -> "Register8":
        """Add with carry-out (like ADC without carry-in)."""
        result = self._val + (operand & 0xFF)
        return self._store(result, carry=result > 0xFF)

    def adc(self, operand: int) -> "Register8":
        """Add with carry-in (6502-style ADC)."""
        result = self._val + (operand & 0xFF) + int(self.carry)
        return self._store(result, carry=result > 0xFF)

    def sub(self, operand: int) -> "Register8":
        """Subtract with borrow-out."""
        result = self._val - (operand & 0xFF)
        return self._store(result, carry=result < 0)   # carry = borrow

    def inc(self) -> "Register8":
        """Increment (carry unaffected, like 6502 INC)."""
        c = self.carry
        self._store(self._val + 1)
        self.carry = c
        return self

    def dec(self) -> "Register8":
        """Decrement (carry unaffected)."""
        c = self.carry
        self._store(self._val - 1)
        self.carry = c
        return self

    # ------------------------------------------------------------------
    # Logic
    # ------------------------------------------------------------------

    def AND(self, operand: int) -> "Register8":
        return self._store(self._val & operand)

    def OR(self, operand: int) -> "Register8":
        return self._store(self._val | operand)

    def XOR(self, operand: int) -> "Register8":
        return self._store(self._val ^ operand)

    def NOT(self) -> "Register8":
        """Bitwise complement."""
        return self._store(~self._val)          # ~x & 0xFF via _store

    def bit(self, n: int) -> bool:
        """Return the value of bit n (0 = LSB, 7 = MSB)."""
        return bool((self._val >> n) & 1)

    def set_bit(self, n: int) -> "Register8":
        """Set bit n."""
        return self._store(self._val | (1 << n), carry=self.carry)

    def clear_bit(self, n: int) -> "Register8":
        """Clear bit n."""
        return self._store(self._val & ~(1 << n), carry=self.carry)

    def toggle_bit(self, n: int) -> "Register8":
        """Toggle bit n."""
        return self._store(self._val ^ (1 << n), carry=self.carry)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        flags = (
            f"C={'1' if self.carry else '0'} "
            f"Z={'1' if self.zero  else '0'} "
            f"N={'1' if self.neg   else '0'}"
        )
        return (
            f"Register8(0b{self._val:08b} | "
            f"0x{self._val:02X} | "
            f"{self._val:3d}) [{flags}]"
        )

    def __int__(self) -> int:
        return self._val

    def __eq__(self, other) -> bool:
        if isinstance(other, Register8):
            return self._val == other._val
        return self._val == other


# ======================================================================
# Demo
# ======================================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  8-bit Register Demo")
    print("=" * 55)

    r = Register8(0b10110011)
    print(f"\nLoaded:      {r}")

    print(f"\n-- Shifts --")
    r.load(0b10110011)
    print(f"SHL:         {r.shl()}")
    r.load(0b10110011)
    print(f"SHR:         {r.shr()}")
    r.load(0b10110011)
    print(f"ASR:         {r.asr()}")

    print(f"\n-- Rotates --")
    r.load(0b10110011)
    print(f"ROL:         {r.rol()}")
    r.load(0b10110011)
    print(f"ROR:         {r.ror()}")

    print(f"\n-- Rotate through carry --")
    r.load(0b10110011); r.carry = True
    print(f"ROL_C (C=1): {r.rol_carry()}")
    r.load(0b10110011); r.carry = False
    print(f"ROR_C (C=0): {r.ror_carry()}")

    print(f"\n-- Arithmetic --")
    r.load(0xFE)
    print(f"ADD 0x03:    {r.add(0x03)}")   # overflow → carry
    r.load(0x42)
    print(f"SUB 0x10:    {r.sub(0x10)}")
    r.load(0xFF)
    print(f"INC:         {r.inc()}")        # wraps to 0x00, zero flag set

    print(f"\n-- Logic --")
    r.load(0b10101010)
    print(f"AND 0x0F:    {r.AND(0x0F)}")
    r.load(0b10100000)
    print(f"OR  0x0F:    {r.OR(0x0F)}")
    r.load(0b11001100)
    print(f"XOR 0xFF:    {r.XOR(0xFF)}")
    r.load(0b10110011)
    print(f"NOT:         {r.NOT()}")

    print(f"\n-- Bit ops --")
    r.load(0b00000000)
    r.set_bit(3); r.set_bit(7)
    print(f"Set b3,b7:   {r}")
    r.clear_bit(7)
    print(f"Clear b7:    {r}")
    print(f"Bit 3 = {r.bit(3)}, Bit 7 = {r.bit(7)}")

    print(f"\n-- Chaining --")
    r.load(0x01).shl().shl().shl()
    print(f"0x01 << 3:   {r}")

    print()
