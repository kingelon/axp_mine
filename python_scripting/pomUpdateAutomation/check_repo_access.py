import subprocess
import os

# Path to the repos.txt file
repos_file_path = os.path.join("..", "data", "input", "repos.txt")

# Output file to store access results
output_file_path = os.path.join("..", "data", "output", "repo_access.txt")


# Function to check if you have access to the repo
def check_repo_access(repo_url):
    try:
        # Attempt to list remote branches to verify access
        result = subprocess.run(
            ["git", "ls-remote", repo_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # If the command succeeded, return True
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False


# Open the output file
with open(output_file_path, "w") as output_file:
    # Read repos.txt line by line
    with open(repos_file_path, "r") as file:
        repos = file.readlines()
        for repo in repos:
            repo = repo.strip()
            if repo:
                # Append .git if it's not already present
                if not repo.endswith('.git'):
                    repo += '.git'

                # Extract the repo name from the URL
                repo_name = repo.split('/')[-1].replace('.git', '')

                print(f"Checking access for {repo_name}...")

                # Check if you have access to the repo
                if check_repo_access(repo):
                    output_file.write(f"{repo_name}: green (access)\n")
                else:
                    output_file.write(f"{repo_name}: red (no access)\n")

print("Repository access check complete. Results have been written to repo_access.txt.")
