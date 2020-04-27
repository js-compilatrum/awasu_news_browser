import PySimpleGUI as sg
from pathlib import Path

WORKDIR = Path.cwd()
SETUP_DIR_PATH = WORKDIR / "core" / "settings"

create_message = f"""No config file! 
Use {WORKDIR / "awasu" / "config.py"} example, choose you option and save under 
{SETUP_DIR_PATH} 
"""


def config_window_file():
    print(Path.cwd())
    sg.theme('BluePurple')
    awasu_examples_dir = WORKDIR / "awasu"
    cfg_example = Path(awasu_examples_dir /  "config.py").read_text()
    sg.popup('Create config first!', f"Go to: {awasu_examples_dir}\n\n{create_message}\n\n{cfg_example}")


def is_config():
    try:
        import core.settings.config
    except ImportError:
        config_window_file()
        raise FileExistsError("No config.py file under core / settings / config.py. "
                              "Use example from awasu / config.py folder and create one!")


def runchecks():
    """
    Check that all option all available to run

    :return: None
    """
    is_config()
