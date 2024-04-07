import pathlib
import sys

current_path = pathlib.Path(__file__).parent.absolute()
current_project_main_path = current_path.parent.parent
src_path = current_project_main_path.joinpath("src")
sys.path.append(str(src_path))
