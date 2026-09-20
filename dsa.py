from pathlib import Path
import subprocess


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).parent.resolve()


# ============================================================
# MAIN MENU
# ============================================================

def show_main_menu():

    print("\n" + "=" * 60)
    print("             DSA SOLUTION MANAGER V5")
    print("=" * 60)

    print("\n1. Create New Code")
    print("2. Push Existing")
    print("3. Exit")

    while True:

        choice = input("\nChoose an option: ").strip()

        if choice in {"1", "2", "3"}:
            return choice

        print("Invalid choice. Please enter 1, 2, or 3.")


# ============================================================
# INPUT FUNCTIONS
# ============================================================

def get_platform():

    print("\nPlatform")
    print("1. LeetCode")
    print("2. HackerRank")

    while True:

        choice = input("Choose platform: ").strip()

        if choice == "1":
            return "LeetCode"

        if choice == "2":
            return "HackerRank"

        print("Invalid choice. Please enter 1 or 2.")


def get_difficulty():

    print("\nDifficulty")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    difficulties = {
        "1": "Easy",
        "2": "Medium",
        "3": "Hard"
    }

    while True:

        choice = input("Choose difficulty: ").strip()

        if choice in difficulties:
            return difficulties[choice]

        print("Invalid choice. Please enter 1, 2, or 3.")


def get_problem_info():

    title = input("\nProblem title: ").strip()

    topic = input("Topic: ").strip()

    problem_number = input(
        "Problem number (press Enter if not applicable): "
    ).strip()

    return title, topic, problem_number


def get_solution():

    print("\nPaste your C++ solution below.")
    print("When finished, type END on a new line.")
    print("-" * 50)

    lines = []

    while True:

        line = input()

        if line == "END":
            break

        lines.append(line)

    return "\n".join(lines)


# ============================================================
# FOLDER NAME
# ============================================================

def create_folder_name(title, problem_number):

    folder_name = title.lower().replace(" ", "-")

    if problem_number:

        try:
            folder_name = f"{int(problem_number):04d}-{folder_name}"

        except ValueError:
            folder_name = f"{problem_number}-{folder_name}"

    return folder_name


# ============================================================
# CREATE PROBLEM
# ============================================================

def create_problem_folder(
    platform,
    difficulty,
    title,
    topic,
    problem_number,
    solution
):

    folder_name = create_folder_name(
        title,
        problem_number
    )

    problem_dir = (
        BASE_DIR
        / platform
        / difficulty
        / folder_name
    )

    # Never overwrite
    if problem_dir.exists():

        print("\n⚠ Problem already exists!")
        print(f"Location: {problem_dir}")
        print("Nothing was changed.")

        return None

    problem_dir.mkdir(parents=True)

    # solution.cpp
    solution_file = problem_dir / "solution.cpp"

    solution_file.write_text(
        solution,
        encoding="utf-8"
    )

    # README.md
    readme_file = problem_dir / "README.md"

    readme_content = f"""# {title}

- Platform: {platform}
- Difficulty: {difficulty}
- Topic: {topic}
"""

    readme_file.write_text(
        readme_content,
        encoding="utf-8"
    )

    return problem_dir


# ============================================================
# VS CODE
# ============================================================

def open_in_vscode(file_path):

    print("\nOpening solution.cpp in VS Code...")

    try:

        subprocess.Popen(
            ["code", str(file_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print("✓ solution.cpp opened in VS Code.")

    except FileNotFoundError:

        print("\n⚠ VS Code command 'code' was not found.")
        print("Open solution.cpp manually in VS Code.")


# ============================================================
# GIT FUNCTIONS
# ============================================================

def run_git_command(command):

    print(f"\n$ {' '.join(map(str, command))}")

    result = subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print(result.stderr.strip())

    if result.returncode != 0:

        raise RuntimeError(
            f"Git command failed: {' '.join(map(str, command))}"
        )

    return result


def git_add_problem(problem_dir):

    relative_path = problem_dir.relative_to(BASE_DIR)

    git_path = relative_path.as_posix()

    run_git_command([
        "git",
        "add",
        "--",
        git_path
    ])

    return git_path


# ============================================================
# SAFETY CHECK
# ============================================================

def verify_staged_files(git_path):

    result = run_git_command([
        "git",
        "diff",
        "--cached",
        "--name-only"
    ])

    staged_files = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    expected_files = {
        f"{git_path}/solution.cpp",
        f"{git_path}/README.md"
    }

    actual_files = set(staged_files)

    print("\nChecking staged files...")

    if actual_files != expected_files:

        print("\n❌ SAFETY CHECK FAILED")

        print("\nExpected:")

        for file in sorted(expected_files):
            print(f"  {file}")

        print("\nActually staged:")

        for file in sorted(actual_files):
            print(f"  {file}")

        print("\nResetting staging area...")

        run_git_command([
            "git",
            "reset"
        ])

        raise RuntimeError(
            "Unexpected files were staged. "
            "Nothing was committed or pushed."
        )

    print("✓ Safety check passed.")
    print("✓ Only the selected problem files are staged.")


# ============================================================
# COMMIT / PUSH
# ============================================================

def git_commit(commit_message):

    run_git_command([
        "git",
        "commit",
        "-m",
        commit_message
    ])


def git_push():

    run_git_command([
        "git",
        "push"
    ])


# ============================================================
# PUSH ONE PROBLEM
# ============================================================

def push_problem(
    problem_dir,
    platform,
    difficulty,
    title
):

    try:

        print("\n" + "=" * 60)
        print("             PREPARING GITHUB PUSH")
        print("=" * 60)

        # Stage only selected problem
        git_path = git_add_problem(problem_dir)

        # Safety check
        verify_staged_files(git_path)

        commit_message = (
            f"Solve {platform} - {title} [{difficulty}]"
        )

        # Commit
        git_commit(commit_message)

        # Push
        git_push()

        print("\n" + "=" * 60)
        print("             ✓ GITHUB PUSH SUCCESSFUL")
        print("=" * 60)

        print(f"\nProblem : {title}")
        print(f"Platform: {platform}")
        print(f"Level   : {difficulty}")

        print("\n✓ Files committed")
        print("✓ GitHub updated")

        return True

    except RuntimeError as error:

        print("\n" + "=" * 60)
        print("             ❌ GIT AUTOMATION FAILED")
        print("=" * 60)

        print(f"\n{error}")

        print("\nYour problem files are still safe locally.")

        return False


# ============================================================
# CREATE NEW CODE
# ============================================================

def create_new_code():

    print("\n" + "=" * 60)
    print("                 CREATE NEW CODE")
    print("=" * 60)

    platform = get_platform()

    difficulty = get_difficulty()

    title, topic, problem_number = get_problem_info()

    solution = get_solution()

    if not solution.strip():

        print("\n⚠ No solution entered.")
        print("Nothing was created.")

        return

    problem_dir = create_problem_folder(
        platform,
        difficulty,
        title,
        topic,
        problem_number,
        solution
    )

    if problem_dir is None:
        return

    print("\n" + "-" * 60)
    print("✓ PROBLEM CREATED SUCCESSFULLY")
    print("-" * 60)

    print(f"Platform   : {platform}")
    print(f"Difficulty : {difficulty}")
    print(f"Problem    : {title}")
    print(f"Topic      : {topic}")
    print(f"Location   : {problem_dir}")

    print("\nFiles created:")
    print("✓ solution.cpp")
    print("✓ README.md")

    solution_file = problem_dir / "solution.cpp"

    open_in_vscode(solution_file)

    print("\n" + "=" * 60)
    print("             EDIT YOUR SOLUTION NOW")
    print("=" * 60)

    print("\nWhen everything is ready, type:")
    print("push")

    print("\nType 'cancel' if you don't want to push.")

    while True:

        command = input("\nCommand: ").strip().lower()

        if command == "cancel":

            print("\nPush cancelled.")
            print("Your files are still saved locally.")

            return

        if command == "push":
            break

        print("Unknown command.")
        print("Please type 'push' or 'cancel'.")

    push_problem(
        problem_dir,
        platform,
        difficulty,
        title
    )


# ============================================================
# FIND ALL EXISTING PROBLEMS
# ============================================================

def get_all_existing_problems():

    problems = []

    platforms = [
        "LeetCode",
        "HackerRank"
    ]

    difficulties = [
        "Easy",
        "Medium",
        "Hard"
    ]

    for platform in platforms:

        for difficulty in difficulties:

            difficulty_dir = (
                BASE_DIR
                / platform
                / difficulty
            )

            if not difficulty_dir.exists():
                continue

            for folder in sorted(difficulty_dir.iterdir()):

                if not folder.is_dir():
                    continue

                solution_file = folder / "solution.cpp"
                readme_file = folder / "README.md"

                # A valid DSA problem must contain both files
                if (
                    solution_file.exists()
                    and readme_file.exists()
                ):

                    problems.append({
                        "path": folder,
                        "platform": platform,
                        "difficulty": difficulty,
                        "name": folder.name
                    })

    return problems


# ============================================================
# DISPLAY EXISTING PROBLEMS
# ============================================================

def show_existing_problems(problems):

    print("\n" + "=" * 60)
    print("                  EXISTING PROBLEMS")
    print("=" * 60)

    if not problems:

        print("\n✓ No existing problems remaining.")

        return

    for index, problem in enumerate(
        problems,
        start=1
    ):

        print(
            f"{index}. "
            f"{problem['platform']}/"
            f"{problem['difficulty']}/"
            f"{problem['name']}"
        )

    print("\n" + "-" * 60)
    print("Options:")
    print("  push all  -> Push every listed problem")
    print("  number    -> Push selected problem")
    print("  path      -> Manually enter problem folder path")
    print("  exit      -> Return to main menu")
    print("-" * 60)


# ============================================================
# MANUAL PATH
# ============================================================

def get_manual_problem_path():

    print("\nPaste the problem folder path.")

    print("Example:")
    print(
        r"C:\Users\samar\OneDrive\DSA"
        r"\LeetCode\Easy\0001-two-sum"
    )

    raw_path = input("\nPath: ").strip()

    if not raw_path:
        print("\n⚠ No path entered.")

        return None

    path = Path(raw_path.strip('"'))

    # Convert relative path to BASE_DIR relative path
    if not path.is_absolute():

        path = (
            BASE_DIR / path
        ).resolve()

    else:

        path = path.resolve()

    if not path.exists():

        print("\n❌ Path does not exist.")
        print(path)

        return None

    if not path.is_dir():

        print("\n❌ The path must be a problem folder.")

        return None

    solution_file = path / "solution.cpp"
    readme_file = path / "README.md"

    if not solution_file.exists():

        print("\n❌ solution.cpp not found.")

        return None

    if not readme_file.exists():

        print("\n❌ README.md not found.")

        return None

    # Make sure the selected folder is inside BASE_DIR
    try:

        relative_path = path.relative_to(BASE_DIR)

    except ValueError:

        print("\n❌ Safety restriction:")
        print("The problem folder must be inside the DSA repository.")

        return None

    parts = relative_path.parts

    if len(parts) < 3:

        print("\n❌ Invalid DSA problem path.")

        return None

    platform = parts[0]
    difficulty = parts[1]

    if platform not in {
        "LeetCode",
        "HackerRank"
    }:

        print("\n❌ Invalid platform.")

        return None

    if difficulty not in {
        "Easy",
        "Medium",
        "Hard"
    }:

        print("\n❌ Invalid difficulty.")

        return None

    return {
        "path": path,
        "platform": platform,
        "difficulty": difficulty,
        "name": path.name
    }


# ============================================================
# PUSH EXISTING
# ============================================================

def push_existing():

    print("\n" + "=" * 60)
    print("                  PUSH EXISTING")
    print("=" * 60)

    while True:

        # ----------------------------------------------------
        # Refresh the list EVERY TIME
        # ----------------------------------------------------

        problems = get_all_existing_problems()

        # ----------------------------------------------------
        # ZERO PROBLEMS
        # ----------------------------------------------------

        if not problems:

            print("\n" + "=" * 60)
            print("          ✓ ALL EXISTING PROBLEMS ARE DONE")
            print("=" * 60)

            print("\nReturning to main menu...")

            return

        # ----------------------------------------------------
        # SHOW CURRENT LIST
        # ----------------------------------------------------

        show_existing_problems(problems)

        # ----------------------------------------------------
        # GET COMMAND
        # ----------------------------------------------------

        command = input(
            "\nCommand: "
        ).strip()

        if not command:

            print("\n⚠ Please enter an option.")

            continue

        command_lower = command.lower()

        # ====================================================
        # EXIT
        # ====================================================

        if command_lower == "exit":

            print("\nReturning to main menu...")

            return

        # ====================================================
        # PUSH ALL
        # ====================================================

        if command_lower == "push all":

            print("\n" + "=" * 60)
            print("                  PUSH ALL")
            print("=" * 60)

            print(
                f"\n{len(problems)} problem(s) "
                "will be processed."
            )

            confirm = input(
                "\nType 'push all' again to confirm: "
            ).strip().lower()

            if confirm != "push all":

                print("\nPush all cancelled.")

                continue

            # Process a snapshot.
            # The list is refreshed after every push.
            for problem in problems:

                print("\n" + "-" * 60)

                print(
                    f"Processing: "
                    f"{problem['platform']}/"
                    f"{problem['difficulty']}/"
                    f"{problem['name']}"
                )

                success = push_problem(
                    problem["path"],
                    problem["platform"],
                    problem["difficulty"],
                    problem["name"]
                )

                if not success:

                    print(
                        "\n⚠ Push failed."
                    )

                    print(
                        "Stopping Push All so you can "
                        "fix the problem."
                    )

                    break

            # Go back to the top.
            # Remaining problems will be displayed.
            continue

        # ====================================================
        # MANUAL PATH
        # ====================================================

        if command_lower == "path":

            manual_problem = get_manual_problem_path()

            if manual_problem is None:
                continue

            print("\nSelected:")
            print(
                f"{manual_problem['platform']}/"
                f"{manual_problem['difficulty']}/"
                f"{manual_problem['name']}"
            )

            confirm = input(
                "\nType 'push' to continue or "
                "'cancel' to stop: "
            ).strip().lower()

            if confirm != "push":

                print("\nPush cancelled.")

                continue

            push_problem(
                manual_problem["path"],
                manual_problem["platform"],
                manual_problem["difficulty"],
                manual_problem["name"]
            )

            # Refresh list
            continue

        # ====================================================
        # NUMBER
        # ====================================================

        if command.isdigit():

            number = int(command)

            if not (
                1 <= number <= len(problems)
            ):

                print(
                    "\n❌ Invalid problem number."
                )

                continue

            selected = problems[number - 1]

            print("\nSelected:")
            print(
                f"{selected['platform']}/"
                f"{selected['difficulty']}/"
                f"{selected['name']}"
            )

            confirm = input(
                "\nType 'push' to continue or "
                "'cancel' to stop: "
            ).strip().lower()

            if confirm != "push":

                print("\nPush cancelled.")

                continue

            push_problem(
                selected["path"],
                selected["platform"],
                selected["difficulty"],
                selected["name"]
            )

            # Refresh list
            continue

        # ====================================================
        # INVALID COMMAND
        # ====================================================

        print("\n❌ Unknown command.")

        print(
            "Use: push all, a number, path, or exit."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    while True:

        choice = show_main_menu()

        # ----------------------------------------------------
        # CREATE NEW
        # ----------------------------------------------------

        if choice == "1":

            create_new_code()

        # ----------------------------------------------------
        # PUSH EXISTING
        # ----------------------------------------------------

        elif choice == "2":

            push_existing()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "3":

            print("\n" + "=" * 60)
            print("              EXITING DSA MANAGER")
            print("=" * 60)

            print("\nGoodbye! 👋")

            break


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()