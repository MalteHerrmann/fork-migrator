"""
This tool is used to compare the contents of an Evmos or Ethermint fork
with the original repository and will output the percentage of overlap
between the two.
"""

import difflib
import os
import sys


def get_file_contents(file_path):
    """Returns the file contents, while ignoring comments."""

    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.readlines()

    idx = 0
    for line in contents:
        if line.strip().startswith("//"):
            idx += 1
        else:
            break

    return contents[idx:]


def calculate_overlap_percentage(content1, content2):
    """Calculates the overlap percentage between two strings."""

    matcher = difflib.SequenceMatcher(None, content1, content2)
    return matcher.ratio() * 100


def compare_repositories(path1, path2):
    """Compares the contents of two repositories and returns the overlap percentage."""

    print(f"Comparing {path1} and {path2}")
    overlap_percentages = []

    if not os.path.exists(path1):
        raise FileNotFoundError("Repo 1 doesn't exist")

    if not os.path.exists(path2):
        raise FileNotFoundError("Repo 2 doesn't exist")

    for root1, _, files1 in os.walk(path1):
        print("root: ", root1)
        if ".git" in root1 or "client/docs" in root1:
            continue

        relative_root1 = root1[len(path1) + 1 :]
        for file1 in files1:
            print(f"Checking {file1}")
            file1_path = os.path.join(root1, file1)
            file2_path = os.path.join(path2, relative_root1, file1)

            if os.path.exists(file2_path) and os.path.isfile(file2_path):
                try:
                    content1 = get_file_contents(file1_path)
                    content2 = get_file_contents(file2_path)

                    overlap_percentage = calculate_overlap_percentage(
                        content1, content2
                    )
                    overlap_percentages.append(
                        (file1_path, file2_path, overlap_percentage)
                    )
                except UnicodeDecodeError:
                    print(
                        f"Could not compare {file1_path} and "
                        + f"{file2_path} due to encoding error",
                    )
                except Exception as e: # pylint: disable=broad-except # want to log all exceptions here
                    print(
                        f"Could not compare {file1_path} and "
                        + f"{file2_path} due to error: {e}",
                    )
                break

    return overlap_percentages


def check_fork(path1, path2):
    """
    The main function of this tool.
    Checks the overlap between the repostories at the given paths.
    """

    overlap_percentages = compare_repositories(path1, path2)

    with open("overlap_percentages.csv", "w", encoding="utf-8") as file:
        for file1_path, file2_path, overlap_percentage in overlap_percentages:
            print(
                f"Files: {file1_path} and {file2_path} - "
                + f"Overlap Percentage: {overlap_percentage}%"
            )
            file.write(f"{file1_path},{file2_path},{overlap_percentage}\n")


if __name__ == "__main__":
    # TODO: This should rather let the user toggle between Ethermint or Evmos
    # and then provide the version + path to compare to
    if len(sys.argv) != 3:
        print("Please provide the paths to the repositories to compare")
        print("It's required to pass in two paths to compare the repositories")

    repo1_path = sys.argv[1]
    repo2_path = sys.argv[2]

    check_fork(repo1_path, repo2_path)
