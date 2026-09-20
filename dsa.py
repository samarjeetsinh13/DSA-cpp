from pathlib import Path
import subprocess


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).parent.resolve()


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
# FILE FUNCTIONS
# ============================================================

def create_problem_folder(
    platform,
    difficulty,
    title,
    topic,
    problem_number,
    solution
):
    folder_name = title.lower().replace(" ", "-")

    if problem_number:
        try:
            folder_name = f"{int(problem_number):04d}-{folder_name}"
        except ValueError:
            folder_name = f"{problem_number}-{folder_name}"

    problem_dir = (
        BASE_DIR
        / platform
        / difficulty
        / folder_name
    )

    # Safety: never overwrite an existing problem
    if problem_dir.exists():
        print("\n⚠ Problem already exists!")
        print(f"Location: {problem_dir}")
        print("Nothing was changed.")
        return None

    problem_dir.mkdir(parents=True)

    # Create solution.cpp
    solution_file = problem_dir / "solution.cpp"
    solution_file.write_text(
        solution,
        encoding="utf-8"
    )

    # Create README.md
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
# VS CODE FUNCTION
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
        print("You can open solution.cpp manually in VS Code.")


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

        # Remove everything from staging area
        run_git_command([
            "git",
            "reset"
        ])

        raise RuntimeError(
            "Unexpected files were staged. "
            "Nothing was committed or pushed."
        )

    print("✓ Safety check passed.")
    print("✓ Only the current problem files are staged.")


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
# WAIT FOR PUSH COMMAND
# ============================================================

def wait_for_push(problem_dir, platform, difficulty, title):
    print("\n" + "=" * 55)
    print("          EDIT YOUR SOLUTION NOW")
    print("=" * 55)

    print("\nYour files are located at:")
    print(problem_dir)

    print("\nYou can now:")
    print("1. Open/edit solution.cpp")
    print("2. Fix your code")
    print("3. Test your solution")
    print("4. Save the file with Ctrl + S")

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

    # --------------------------------------------------------
    # Git automation
    # --------------------------------------------------------

    try:
        print("\n" + "=" * 55)
        print("          PREPARING GITHUB PUSH")
        print("=" * 55)

        git_path = git_add_problem(problem_dir)

        verify_staged_files(git_path)

        commit_message = (
            f"Solve {platform} - {title} [{difficulty}]"
        )

        git_commit(commit_message)

        git_push()

        print("\n" + "=" * 55)
        print("          ✓ GITHUB PUSH SUCCESSFUL")
        print("=" * 55)

        print(f"\nProblem : {title}")
        print(f"Platform: {platform}")
        print(f"Level   : {difficulty}")

        print("\n✓ Files committed")
        print("✓ GitHub updated")

    except RuntimeError as error:
        print("\n" + "=" * 55)
        print("          ❌ GIT AUTOMATION FAILED")
        print("=" * 55)

        print(f"\n{error}")

        print("\nYour problem files are still safe locally.")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 55)
    print("             DSA SOLUTION MANAGER V4")
    print("=" * 55)

    # --------------------------------------------------------
    # Get problem information
    # --------------------------------------------------------

    platform = get_platform()

    difficulty = get_difficulty()

    title, topic, problem_number = get_problem_info()

    # --------------------------------------------------------
    # Get solution
    # --------------------------------------------------------

    solution = get_solution()

    if not solution.strip():
        print("\n⚠ No solution entered.")
        print("Nothing was created.")
        return

    # --------------------------------------------------------
    # Create files
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Show success
    # --------------------------------------------------------

    print("\n" + "-" * 55)
    print("✓ PROBLEM CREATED SUCCESSFULLY")
    print("-" * 55)

    print(f"Platform   : {platform}")
    print(f"Difficulty : {difficulty}")
    print(f"Problem    : {title}")
    print(f"Topic      : {topic}")
    print(f"Location   : {problem_dir}")

    print("\nFiles created:")
    print("✓ solution.cpp")
    print("✓ README.md")

    # --------------------------------------------------------
    # Open solution in VS Code
    # --------------------------------------------------------

    solution_file = problem_dir / "solution.cpp"

    open_in_vscode(solution_file)

    # --------------------------------------------------------
    # Wait for user to edit and push
    # --------------------------------------------------------

    wait_for_push(
        problem_dir,
        platform,
        difficulty,
        title
    )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()