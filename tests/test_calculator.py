"""Testes automatizados da calculadora."""
import pytest
from calculator.calculator import Calculator


@pytest.fixture
def calc():
    """Fixture que retorna uma instância de Calculator."""
    return Calculator()


class TestAdd:
    """Testes da operação de soma."""

    def test_add_dois_positivos(self, calc):
        assert calc.add(2, 3) == 5

    def test_add_dois_negativos(self, calc):
        assert calc.add(-1, -2) == -3

    def test_add_positivo_negativo(self, calc):
        assert calc.add(10, -4) == 6

    def test_add_com_zero(self, calc):
        assert calc.add(0, 5) == 5

    def test_add_zero_com_zero(self, calc):
        assert calc.add(0, 0) == 0

    def test_add_floats(self, calc):
        assert calc.add(1.5, 2.5) == 4.0

    def test_add_grande(self, calc):
        assert calc.add(1_000_000, 2_000_000) == 3_000_000


class TestSubtract:
    """Testes da operação de subtração."""

    def test_subtract_positivos(self, calc):
        assert calc.subtract(5, 3) == 2

    def test_subtract_resultado_negativo(self, calc):
        assert calc.subtract(3, 5) == -2

    def test_subtract_com_zero(self, calc):
        assert calc.subtract(5, 0) == 5

    def test_subtract_zero_de_zero(self, calc):
        assert calc.subtract(0, 0) == 0

    def test_subtract_negativos(self, calc):
        assert calc.subtract(-3, -5) == 2

    def test_subtract_floats(self, calc):
        assert abs(calc.subtract(5.5, 2.2) - 3.3) < 1e-9


class TestMultiply:
    """Testes da operação de multiplicação."""

    def test_multiply_positivos(self, calc):
        assert calc.multiply(3, 4) == 12

    def test_multiply_com_negativo(self, calc):
        assert calc.multiply(-2, 3) == -6

    def test_multiply_dois_negativos(self, calc):
        assert calc.multiply(-2, -3) == 6

    def test_multiply_por_zero(self, calc):
        assert calc.multiply(5, 0) == 0

    def test_multiply_por_um(self, calc):
        assert calc.multiply(7, 1) == 7

    def test_multiply_floats(self, calc):
        assert calc.multiply(2.5, 4.0) == 10.0


class TestDivide:
    """Testes da operação de divisão."""

    def test_divide_basico(self, calc):
        assert calc.divide(10, 2) == 5.0

    def test_divide_resultado_float(self, calc):
        assert calc.divide(7, 2) == 3.5

    def test_divide_por_zero_levanta_excecao(self, calc):
        with pytest.raises(ValueError, match="Divisão por zero"):
            calc.divide(5, 0)

    def test_divide_negativos(self, calc):
        assert calc.divide(-6, 2) == -3.0

    def test_divide_fracao(self, calc):
        assert calc.divide(1, 4) == 0.25

    def test_divide_por_si_mesmo(self, calc):
        assert calc.divide(7, 7) == 1.0
