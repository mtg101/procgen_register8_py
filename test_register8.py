"""
test_register8.py — pytest unit tests for Register8
Run with: pytest test_register8.py -v
"""

import pytest
from register8 import Register8


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def r():
    """Fresh register loaded with 0x00."""
    return Register8()


# ======================================================================
# Load & init
# ======================================================================

class TestLoad:
    def test_default_value_is_zero(self):
        r = Register8()
        assert r.value == 0x00

    def test_load_value(self):
        r = Register8(0xAB)
        assert r.value == 0xAB

    def test_load_masks_to_8bit(self):
        r = Register8(0x1FF)        # 9-bit value
        assert r.value == 0xFF

    def test_load_clears_carry(self):
        r = Register8(0xFF)
        r.add(0x01)                 # sets carry
        r.load(0x42)
        assert r.carry is False

    def test_load_sets_zero_flag(self):
        r = Register8(0x42)
        r.load(0x00)
        assert r.zero is True

    def test_load_sets_neg_flag(self):
        r = Register8(0x80)
        assert r.neg is True

    def test_load_clears_neg_flag(self):
        r = Register8(0x7F)
        assert r.neg is False

    def test_value_setter(self):
        r = Register8()
        r.value = 0x55
        assert r.value == 0x55


# ======================================================================
# Shifts
# ======================================================================

class TestShifts:
    def test_shl_basic(self):
        r = Register8(0b00000001)
        r.shl()
        assert r.value == 0b00000010

    def test_shl_msb_to_carry(self):
        r = Register8(0b10000000)
        r.shl()
        assert r.value == 0x00
        assert r.carry is True

    def test_shl_no_carry(self):
        r = Register8(0b00000001)
        r.shl()
        assert r.carry is False

    def test_shl_sets_zero_flag(self):
        r = Register8(0b10000000)
        r.shl()
        assert r.zero is True

    def test_shr_basic(self):
        r = Register8(0b10000000)
        r.shr()
        assert r.value == 0b01000000

    def test_shr_lsb_to_carry(self):
        r = Register8(0b00000001)
        r.shr()
        assert r.value == 0x00
        assert r.carry is True

    def test_shr_no_carry(self):
        r = Register8(0b00000010)
        r.shr()
        assert r.carry is False

    def test_shr_msb_filled_with_zero(self):
        r = Register8(0xFF)
        r.shr()
        assert r.value == 0x7F      # MSB is 0, not 1

    def test_asr_preserves_sign_bit(self):
        r = Register8(0b10000000)
        r.asr()
        assert r.value == 0b11000000    # sign extended

    def test_asr_positive_same_as_shr(self):
        r = Register8(0b01000000)
        r.asr()
        assert r.value == 0b00100000

    def test_asr_lsb_to_carry(self):
        r = Register8(0b10000001)
        r.asr()
        assert r.carry is True


# ======================================================================
# Rotates
# ======================================================================

class TestRotates:
    def test_rol_basic(self):
        r = Register8(0b00000001)
        r.rol()
        assert r.value == 0b00000010

    def test_rol_msb_wraps_to_lsb(self):
        r = Register8(0b10000000)
        r.rol()
        assert r.value == 0b00000001
        assert r.carry is True

    def test_rol_all_ones_unchanged(self):
        r = Register8(0xFF)
        r.rol()
        assert r.value == 0xFF
        assert r.carry is True

    def test_ror_basic(self):
        r = Register8(0b10000000)
        r.ror()
        assert r.value == 0b01000000

    def test_ror_lsb_wraps_to_msb(self):
        r = Register8(0b00000001)
        r.ror()
        assert r.value == 0b10000000
        assert r.carry is True

    def test_rol_carry_uses_carry_as_lsb(self):
        r = Register8(0b00000000)
        r.carry = True
        r.rol_carry()
        assert r.value == 0b00000001    # carry fed into LSB
        assert r.carry is False

    def test_rol_carry_msb_to_carry(self):
        r = Register8(0b10000000)
        r.carry = False
        r.rol_carry()
        assert r.value == 0b00000000
        assert r.carry is True

    def test_ror_carry_uses_carry_as_msb(self):
        r = Register8(0b00000000)
        r.carry = True
        r.ror_carry()
        assert r.value == 0b10000000    # carry fed into MSB
        assert r.carry is False

    def test_ror_carry_lsb_to_carry(self):
        r = Register8(0b00000001)
        r.carry = False
        r.ror_carry()
        assert r.value == 0b00000000
        assert r.carry is True

    def test_rol_carry_full_cycle_9_steps(self):
        """After 9 rol_carry steps the value should be restored."""
        r = Register8(0b10110011)
        r.carry = False
        original = r.value
        for _ in range(9):
            r.rol_carry()
        assert r.value == original


# ======================================================================
# Arithmetic
# ======================================================================

class TestArithmetic:
    def test_add_basic(self):
        r = Register8(0x10)
        r.add(0x20)
        assert r.value == 0x30
        assert r.carry is False

    def test_add_overflow_sets_carry(self):
        r = Register8(0xFF)
        r.add(0x01)
        assert r.value == 0x00
        assert r.carry is True
        assert r.zero is True

    def test_add_does_not_use_carry_in(self):
        r = Register8(0x01)
        r.carry = True
        r.add(0x01)                 # carry-in ignored by add()
        assert r.value == 0x02

    def test_adc_includes_carry(self):
        r = Register8(0x01)
        r.carry = True
        r.adc(0x01)
        assert r.value == 0x03      # 1 + 1 + carry(1) = 3

    def test_adc_no_carry(self):
        r = Register8(0x01)
        r.carry = False
        r.adc(0x01)
        assert r.value == 0x02

    def test_adc_16bit_addition(self):
        """0x01FF + 0x0001 = 0x0200 via two 8-bit adc steps."""
        lo = Register8(0xFF); lo.add(0x01)
        hi = Register8(0x01); hi.carry = lo.carry; hi.adc(0x00)
        assert hi.value == 0x02
        assert lo.value == 0x00

    def test_sub_basic(self):
        r = Register8(0x10)
        r.sub(0x05)
        assert r.value == 0x0B
        assert r.carry is False

    def test_sub_borrow_sets_carry(self):
        r = Register8(0x00)
        r.sub(0x01)
        assert r.value == 0xFF      # wraps around
        assert r.carry is True

    def test_inc_basic(self):
        r = Register8(0x41)
        r.inc()
        assert r.value == 0x42

    def test_inc_wraps(self):
        r = Register8(0xFF)
        r.inc()
        assert r.value == 0x00
        assert r.zero is True

    def test_inc_does_not_affect_carry(self):
        r = Register8(0xFF)
        r.carry = True
        r.inc()
        assert r.carry is True      # carry preserved

    def test_dec_basic(self):
        r = Register8(0x42)
        r.dec()
        assert r.value == 0x41

    def test_dec_wraps(self):
        r = Register8(0x00)
        r.dec()
        assert r.value == 0xFF

    def test_dec_does_not_affect_carry(self):
        r = Register8(0x01)
        r.carry = False
        r.dec()
        assert r.carry is False


# ======================================================================
# Logic
# ======================================================================

class TestLogic:
    def test_and(self):
        r = Register8(0b11001100)
        r.AND(0b10101010)
        assert r.value == 0b10001000

    def test_and_zero_result(self):
        r = Register8(0b11110000)
        r.AND(0b00001111)
        assert r.value == 0x00
        assert r.zero is True

    def test_or(self):
        r = Register8(0b10100000)
        r.OR(0b00001010)
        assert r.value == 0b10101010

    def test_xor(self):
        r = Register8(0b11001100)
        r.XOR(0b10101010)
        assert r.value == 0b01100110

    def test_xor_self_is_zero(self):
        r = Register8(0xAB)
        r.XOR(0xAB)
        assert r.value == 0x00
        assert r.zero is True

    def test_not(self):
        r = Register8(0b10110011)
        r.NOT()
        assert r.value == 0b01001100

    def test_not_zero_becomes_ff(self):
        r = Register8(0x00)
        r.NOT()
        assert r.value == 0xFF

    def test_not_ff_becomes_zero(self):
        r = Register8(0xFF)
        r.NOT()
        assert r.value == 0x00
        assert r.zero is True


# ======================================================================
# Bit operations
# ======================================================================

class TestBitOps:
    def test_bit_read_lsb(self):
        r = Register8(0b00000001)
        assert r.bit(0) is True

    def test_bit_read_msb(self):
        r = Register8(0b10000000)
        assert r.bit(7) is True

    def test_bit_read_clear(self):
        r = Register8(0b10000000)
        assert r.bit(0) is False

    def test_set_bit(self):
        r = Register8(0x00)
        r.set_bit(3)
        assert r.value == 0b00001000

    def test_set_bit_idempotent(self):
        r = Register8(0b00001000)
        r.set_bit(3)
        assert r.value == 0b00001000    # no change

    def test_clear_bit(self):
        r = Register8(0xFF)
        r.clear_bit(3)
        assert r.value == 0b11110111

    def test_clear_bit_idempotent(self):
        r = Register8(0b11110111)
        r.clear_bit(3)
        assert r.value == 0b11110111

    def test_toggle_bit_on(self):
        r = Register8(0x00)
        r.toggle_bit(5)
        assert r.value == 0b00100000

    def test_toggle_bit_off(self):
        r = Register8(0xFF)
        r.toggle_bit(5)
        assert r.value == 0b11011111

    def test_set_clear_bit_preserves_carry(self):
        r = Register8(0x00)
        r.carry = True
        r.set_bit(0)
        assert r.carry is True
        r.clear_bit(0)
        assert r.carry is True


# ======================================================================
# Flags
# ======================================================================

class TestFlags:
    def test_zero_flag_set_when_zero(self):
        r = Register8(0x01)
        r.sub(0x01)
        assert r.zero is True

    def test_zero_flag_cleared_when_nonzero(self):
        r = Register8(0x00)
        r.inc()
        assert r.zero is False

    def test_neg_flag_set_when_bit7(self):
        r = Register8(0x7F)
        r.inc()
        assert r.neg is True        # 0x80 has bit 7 set

    def test_neg_flag_cleared_below_0x80(self):
        r = Register8(0x7F)
        assert r.neg is False


# ======================================================================
# Chaining
# ======================================================================

class TestChaining:
    def test_chain_shl(self):
        r = Register8(0x01)
        r.shl().shl().shl()
        assert r.value == 0x08

    def test_chain_mixed(self):
        r = Register8(0x00)
        r.set_bit(0).shl().shl()
        assert r.value == 0x04

    def test_chain_returns_self(self):
        r = Register8(0x01)
        result = r.shl()
        assert result is r


# ======================================================================
# Equality & repr
# ======================================================================

class TestHelpers:
    def test_eq_int(self):
        r = Register8(0x42)
        assert r == 0x42

    def test_eq_register(self):
        assert Register8(0x42) == Register8(0x42)

    def test_neq(self):
        assert Register8(0x42) != Register8(0x43)

    def test_int_cast(self):
        r = Register8(0xAB)
        assert int(r) == 0xAB

    def test_repr_contains_hex(self):
        r = Register8(0xAB)
        assert "0xAB" in repr(r)

    def test_repr_contains_binary(self):
        r = Register8(0xAB)
        assert "10101011" in repr(r)
