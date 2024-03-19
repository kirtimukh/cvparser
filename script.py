import os, asyncio
import dotenv
import datetime

from utils.ai_utils import analyze_text_with_openai
from utils.file_utils import read_and_extract_text_from_file, store_results
from utils.validation_utils import validate_env_vars, validate_source_dir

from settings import SUPPORTED_FILE_TYPES, MAX_ASYNC_TASKS, CSV_HEADERS

dotenv.load_dotenv()

SOURCE_DIR = os.getenv("CV_FILES", None)


def get_relevant_files(source_dir, skipdirs=[]):
    relevant_files = []

    no_perm_dirs = []
    no_perm_files = []

    for root, dirs, file_names in os.walk(source_dir):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.access(dir_path, os.R_OK):
                print("Permission denied:", dir_path)
                print("Exiting...")
                exit()

        for file_name in file_names:
            file_path = os.path.join(root, file_name)

            if not os.access(file_path, os.R_OK):
                print("Permission denied:", dir_path)
                print("Exiting...")
                exit()

            file_extension = file_name.split(".")[-1]
            if file_extension not in SUPPORTED_FILE_TYPES:
                continue

            relevant_files.append(file_path)

    if no_perm_dirs or no_perm_files:
        print("Read permission denied for the following:")
        for dir_path in no_perm_dirs:
            print(dir_path)
        for file_path in no_perm_files:
            print(file_path)

    print(f"Found {len(relevant_files)} files.", end="")
    return relevant_files


async def runner(task_group, count, total_files, infiles=[]):
    start_num = str(count - MAX_ASYNC_TASKS + 1) if count >= MAX_ASYNC_TASKS else "1"
    end_num = str(count)
    print(f"\nEvaluating {start_num}-{end_num} of {total_files} files", end="")
    results = await asyncio.gather(*task_group)
    store_results(results, csv_headers=CSV_HEADERS)


async def runalysis(relevant_files):
    total_files = len(relevant_files)
    count = 0
    task_group = []
    path_list = []
    for filepath in relevant_files:
        relative_path = os.path.relpath(filepath, SOURCE_DIR)
        file_text = read_and_extract_text_from_file(filepath)
        count += 1
        task = asyncio.create_task(analyze_text_with_openai(file_text, relative_path))
        task_group.append(task)
        path_list.append(relative_path)

        if count % MAX_ASYNC_TASKS == 0:
            await runner(task_group, count, total_files, infiles=path_list)

            task_group = []
            path_list = []
    await runner(task_group, count, total_files)


def main():
    validate_env_vars()
    validate_source_dir(SOURCE_DIR)
    relevant_files = get_relevant_files(SOURCE_DIR)
    asyncio.run(runalysis(relevant_files))


# Run the main function
if __name__ == "__main__":
    t1 = datetime.datetime.now()
    main()
    t2 = datetime.datetime.now()
    print(f"\nTime taken to complete:", t2 - t1)
