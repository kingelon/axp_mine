import subprocess
import os

# Set the directory where you want to clone the repositories
target_dir = r"C:\Users\vippa\OneDrive\Documents\git_KE\test_git_clones"

# Path to the repos.txt file
repos_file_path = os.path.join("..", "data", "input", "giturls.txt")

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# Read repos.txt line by line and clone each repo
with open(repos_file_path, "r") as file:
    repos = file.readlines()
    for repo in repos:
        repo = repo.strip()
        if repo:
            # Append .git to the URL if it's not already present
            if not repo.endswith('.git'):
                repo += '.git'

            repo_name = repo.split('/')[-1].replace('.git', '')
            repo_path = os.path.join(target_dir, repo_name)

            print(f"Cloning repository: {repo}")
            subprocess.run(["git", "clone", repo, repo_path])

            # Change directory to the newly cloned repository
            os.chdir(repo_path)

            # Create a new branch 'POMupdates'
            print(f"Creating and checking out branch 'POMupdates' for {repo_name}")
            subprocess.run(["git", "checkout", "-b", "POMupdates"])

            # Optionally, you can push the new branch to the remote
            # subprocess.run(["git", "push", "-u", "origin", "POMupdates"])

            # Change back to the target directory for the next repo
            os.chdir(target_dir)

print("All repositories have been cloned and the 'POMupdates' branch has been created and checked out.")
