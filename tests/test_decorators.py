
from src.decorators import log


class TestDecorators:
    def test_success_with_filename(self):
        @log("log.txt")
        def add(a, b):
            return a + b

        # Вызываем add только здесь!
        result = add(3, 4)
        assert result == 7

    def test_success_no_filename(self, capsys):
        @log(None)
        def multiply(x, y):
            return x * y

        result = multiply(2, 6)
        assert result == 12
        captured = capsys.readouterr()
        assert "Function multiply OK" in captured.out

    def test_no_args_no_kwargs(self, capsys):
        """Функция без аргументов."""
        @log(None)
        def hello():
            return "Hi!"

        result = hello()
        assert result == "Hi!"

        captured = capsys.readouterr()
        assert "Args: ()" in captured.out
        assert "Kwargs: {}" in captured.out
