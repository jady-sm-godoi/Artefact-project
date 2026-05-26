from unittest import mock


class TestFactualQASession:
    def test_full_q_and_a_session(self):
        from io import StringIO

        from src.cli import main

        inputs = "What is the capital of France?\nexit\n"
        with (
            mock.patch("sys.stdin", StringIO(inputs)),
            mock.patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            main(argv=[])

        output = stdout.getvalue()
        assert "Paris" in output
        assert "Processing..." in output


class TestCalculationQueryFlow:
    def test_arithmetic_via_route_query(self):
        from io import StringIO

        from src.cli import main

        inputs = "128 * 46\nexit\n"
        with (
            mock.patch("sys.stdin", StringIO(inputs)),
            mock.patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            main(argv=[])

        output = stdout.getvalue()
        assert "5888" in output
        assert "Processing..." in output

    def test_symbolic_via_route_query(self):
        from io import StringIO

        from src.cli import main

        inputs = "factor(x**2 - 4)\nexit\n"
        with (
            mock.patch("sys.stdin", StringIO(inputs)),
            mock.patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            main(argv=[])

        output = stdout.getvalue()
        assert "(x - 2)*(x + 2)" in output
        assert "Processing..." in output

    def test_invalid_expression_via_cli(self):
        from io import StringIO

        from src.cli import main

        inputs = "2 +++ * 3\nexit\n"
        with (
            mock.patch("sys.stdin", StringIO(inputs)),
            mock.patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            main(argv=[])

        output = stdout.getvalue()
        assert "Error" in output


class TestFollowUpFlow:
    def test_context_followup(self):
        from io import StringIO

        from src.cli import main

        inputs = (
            "My favorite number is 42.\nWhat is my favorite number?\nexit\n"
        )
        with (
            mock.patch("sys.stdin", StringIO(inputs)),
            mock.patch("sys.stdout", new_callable=StringIO) as stdout,
        ):
            main(argv=[])

        output = stdout.getvalue()
        assert "42" in output
        assert "Processing..." in output
