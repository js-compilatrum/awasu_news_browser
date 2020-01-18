import pytest

from core.helpers import print_colored


def test_print_colored(capsys):
    color_text = "Text in color"
    print_colored("INFO", color_text)
    captured = capsys.readouterr()
    assert f"{color_text}" in captured.out


def test_print_colored_without_color(capsys):
    print_colored('NOTEXISTSCOLOR', 'text')
    captured = capsys.readouterr()
    assert f"Unknown color" in captured.out

