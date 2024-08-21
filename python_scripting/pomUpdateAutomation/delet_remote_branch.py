import subprocess
import os

# Set the directory where your repositories are cloned
target_dir = "C:/Users/vippa/OneDrive/Documents/git_KE/test_git_clones"

# Path to the repos.txt file
repos_file_path = os.path.join("..", "data", "input", "repos.txt")


# Function to check if a remote branch exists
def remote_branch_exists(branch_name):
    result = subprocess.run(["git", "ls-remote", "--heads", "origin", branch_name], stdout=subprocess.PIPE, text=True)
    return branch_name in result.stdout


# Read repos.txt line by line and delete the remote branch 'POMupdates'
with open(repos_file_path, "r") as file:
    repos = file.readlines()
    for repo in repos:
        repo = repo.strip()
        if repo:
            repo_name = repo.split('/')[-1].replace('.git', '')
            repo_path = os.path.join(target_dir, repo_name)

            # Check if the repository directory exists
            if os.path.isdir(repo_path):
                print(f"Switching to 'main' and checking branch 'POMupdates' for {repo_name}")

                # Change directory to the cloned repository
                os.chdir(repo_path)

                # Checkout the 'main' branch (or 'master' if that's the default branch)
                subprocess.run(["git", "checkout", "main"], check=True)

                # Check if the remote branch exists before trying to delete it
                if remote_branch_exists("POMupdates"):
                    print(f"Deleting remote branch 'POMupdates' for {repo_name}")
                    subprocess.run(["git", "push", "origin", "--delete", "POMupdates"], check=True)
                else:
                    print(f"Remote branch 'POMupdates' does not exist for {repo_name}")

                # Delete the local branch 'POMupdates' if it exists
                subprocess.run(["git", "branch", "-d", "POMupdates"], check=False)

                # Change back to the target directory for the next repo
                os.chdir(target_dir)
            else:
                print(f"Repository directory {repo_path} does not exist.")

print("Branch check and deletion process complete.")
