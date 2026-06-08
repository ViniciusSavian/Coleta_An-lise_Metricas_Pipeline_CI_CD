"""Calculadora simples com operações aritméticas básicas."""


class Calculator:
    """Calculadora com operações aritméticas básicas."""

    def add(self, a, b):
        """Soma dois números."""
        return a + b

    def subtract(self, a, b):
        """Subtrai b de a."""
        return a - b

    def multiply(self, a, b):
        """Multiplica dois números."""
        return a * b

    def divide(self, a, b):
        """Divide a por b.

        Raises:
            ValueError: Se b for zero.
        """
        if b == 0:
            raise ValueError("Divisão por zero não é permitida.")
        return a / b
