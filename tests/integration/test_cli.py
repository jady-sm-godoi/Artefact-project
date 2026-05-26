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
