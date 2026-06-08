"""Calculadora com operações aritméticas básicas e avançadas."""
import math


class Calculator:
    """Calculadora com operações aritméticas básicas e avançadas."""

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

    def power(self, base, exponent):
        """Eleva base ao expoente."""
        return base ** exponent

    def sqrt(self, a):
        """Calcula a raiz quadrada de a.

        Raises:
            ValueError: Se a for negativo.
        """
        if a < 0:
            raise ValueError("Raiz quadrada de número negativo não é real.")
        return math.sqrt(a)

    def modulo(self, a, b):
        """Retorna o resto da divisão de a por b.

        Raises:
            ValueError: Se b for zero.
        """
        if b == 0:
            raise ValueError("Módulo por zero não é permitido.")
        return a % b
