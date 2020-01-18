from enum import Enum

import arrow
import colorama


class TextColor(Enum):
    """
    Defining colors for text console print
    """
    INFO = colorama.Fore.LIGHTYELLOW_EX
    WARNING = colorama.Fore.RED
    RESET = colorama.Fore.WHITE
    ERROR = colorama.Fore.RED
    PROCESSING = colorama.Fore.LIGHTBLUE_EX


def print_colored(mode: str, text: str) -> None:
    """
    Colored print to console show data and debuging
    :param mode: text category (match color)
    :param text: text to print
    :return: None
    """

    try:
        color = TextColor[mode].value
        print(color,
              f"{arrow.now().format('HH:mm:ss')}> {text}",
              TextColor.RESET.value,
              flush=True)
    except KeyError:
        print("Unknown color to use. Check 'TextColor' to get correct value")