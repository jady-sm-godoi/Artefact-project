class TestArithmetic:
    def test_addition(self):
        from src.tools.calculator import evaluate

        assert evaluate("2 + 3") == "5"

    def test_subtraction(self):
        from src.tools.calculator import evaluate

        assert evaluate("10 - 4") == "6"

    def test_multiplication(self):
        from src.tools.calculator import evaluate

        assert evaluate("128 * 46") == "5888"

    def test_division(self):
        from src.tools.calculator import evaluate

        assert evaluate("15 / 4") == "15/4"

    def test_power(self):
        from src.tools.calculator import evaluate

        assert evaluate("2 ** 10") == "1024"

    def test_integer_division(self):
        from src.tools.calculator import evaluate

        assert evaluate("17 // 5") == "3"

    def test_modulo(self):
        from src.tools.calculator import evaluate

        assert evaluate("17 % 5") == "2"


class TestSymbolicMath:
    def test_simplify(self):
        from src.tools.calculator import evaluate

        result = evaluate("simplify(x**2 + 2*x + 1)")
        assert "x**2" in result or "(x + 1)**2" in result

    def test_factor(self):
        from src.tools.calculator import evaluate

        assert evaluate("factor(x**2 - 4)") == "(x - 2)*(x + 2)"

    def test_diff(self):
        from src.tools.calculator import evaluate

        assert evaluate("diff(x**3, x)") == "3*x**2"

    def test_integrate(self):
        from src.tools.calculator import evaluate

        assert evaluate("integrate(2*x, x)") == "x**2"

    def test_trig(self):
        from src.tools.calculator import evaluate

        assert evaluate("sin(pi/2)") == "1"

    def test_constants(self):
        from src.tools.calculator import evaluate

        assert evaluate("E") == "E"
        assert evaluate("pi").startswith("pi")


class TestErrorHandling:
    def test_invalid_syntax(self):
        from src.tools.calculator import evaluate

        result = evaluate("2 +++ * 3")
        assert "Error" in result
        assert "invalid expression" in result.lower()

    def test_empty_string(self):
        from src.tools.calculator import evaluate

        result = evaluate("")
        assert "Error" in result

    def test_invalid_syntax_symbols(self):
        from src.tools.calculator import evaluate

        result = evaluate("@")
        assert "Error" in result

    def test_unmatched_parentheses(self):
        from src.tools.calculator import evaluate

        result = evaluate("(2 + 3")
        assert "Error" in result
