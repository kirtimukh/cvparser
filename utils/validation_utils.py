import os
import dotenv

dotenv.load_dotenv()


def exit_with_message(message):
    print("\n" + message, end="")
    exit()


def validate_env_vars():
    if not os.getenv("OPENAI_API_KEY", None):
        exit_with_message("OPENAI_API_KEY environment variable not set.")
    if not os.getenv("CV_FILES", None):
        exit_with_message("CV_FILES environment variable not set.")


def validate_source_dir(dir_path):
    if not os.path.isdir(dir_path):
        exit_with_message(f"{dir_path} is not a directory.")
    if not os.access(dir_path, os.R_OK):
        exit_with_message(f"Permission to read `{dir_path}` has been denied.")
