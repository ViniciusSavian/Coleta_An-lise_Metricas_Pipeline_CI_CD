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


# ── Testes parametrizados para aumentar volume ────────────────────────────────


@pytest.mark.parametrize("a,b,expected", [
    (0, 0, 0), (1, 1, 2), (2, 3, 5), (10, 20, 30),
    (100, 200, 300), (-1, 1, 0), (-5, -5, -10),
    (0.5, 0.5, 1.0), (1000, 2000, 3000), (7, 3, 10),
    (15, 15, 30), (99, 1, 100), (50, 50, 100), (3, 7, 10),
])
def test_add_parametrizado(calc, a, b, expected):
    assert calc.add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 2), (10, 4, 6), (0, 0, 0), (100, 1, 99),
    (-1, -1, 0), (7, 7, 0), (1000, 999, 1), (3, 5, -2),
    (20, 10, 10), (0, 5, -5), (8, 4, 4), (15, 7, 8),
])
def test_subtract_parametrizado(calc, a, b, expected):
    assert calc.subtract(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 6), (0, 5, 0), (5, 0, 0), (-2, -3, 6),
    (10, 10, 100), (1, 1, 1), (-1, 1, -1), (7, 7, 49),
    (3, 4, 12), (6, 6, 36), (2, 10, 20), (5, 5, 25),
])
def test_multiply_parametrizado(calc, a, b, expected):
    assert calc.multiply(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5.0), (9, 3, 3.0), (100, 4, 25.0), (7, 7, 1.0),
    (1, 2, 0.5), (3, 6, 0.5), (20, 4, 5.0), (81, 9, 9.0),
    (50, 10, 5.0), (16, 4, 4.0),
])
def test_divide_parametrizado(calc, a, b, expected):
    assert calc.divide(a, b) == expected


# ── Operações avançadas ───────────────────────────────────────────────────────


class TestPower:
    """Testes da operação de potência."""

    def test_power_basico(self, calc):
        assert calc.power(2, 3) == 8

    def test_power_expoente_zero(self, calc):
        assert calc.power(5, 0) == 1

    def test_power_expoente_um(self, calc):
        assert calc.power(7, 1) == 7

    def test_power_base_negativa(self, calc):
        assert calc.power(-2, 3) == -8

    def test_power_fracionado(self, calc):
        assert calc.power(4, 0.5) == 2.0


class TestSqrt:
    """Testes da raiz quadrada."""

    def test_sqrt_perfeito(self, calc):
        assert calc.sqrt(9) == 3.0

    def test_sqrt_zero(self, calc):
        assert calc.sqrt(0) == 0.0

    def test_sqrt_dois(self, calc):
        assert abs(calc.sqrt(2) - 1.41421356) < 1e-6

    def test_sqrt_negativo_levanta_excecao(self, calc):
        with pytest.raises(ValueError, match="negativo"):
            calc.sqrt(-1)


class TestModulo:
    """Testes da operação de módulo."""

    def test_modulo_basico(self, calc):
        assert calc.modulo(10, 3) == 1

    def test_modulo_divisivel(self, calc):
        assert calc.modulo(9, 3) == 0

    def test_modulo_por_zero_levanta_excecao(self, calc):
        with pytest.raises(ValueError, match="zero"):
            calc.modulo(5, 0)

    def test_modulo_negativo(self, calc):
        assert calc.modulo(-7, 3) == 2
