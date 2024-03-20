from github import Github
import gitlab
import os

# Configutarion
github_token = 'xxx'
gitlab_url = 'xxx'
gitlab_token = 'xxx'
gitlab_group_id = xxx
github_org = 'xxx'
local_repo_path = "/projects" # you may change this path


# Library instance
gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)
g = Github(github_token)
 
# Get All Repository URL in Github Org.
def get_git_org_projects():
    org = g.get_organization(github_org)
    return [repo.clone_url for repo in org.get_repos()]

# Clone Repo To local and change remote to gitlab
def clone_to_gitlab(git_repo_url):
    repo_name = git_repo_url.split('/')[-1].split('.')[0]  # get name fron url
    os.chdir(local_repo_path)

    # Clone Repository
    print(f"Cloning {git_repo_url} to local...")
    os.system(f"git clone {git_repo_url}")
    
    project = gl.projects.create({'name': repo_name, 'namespace_id': gitlab_group_id})
    print(f"project {project.ssh_url_to_repo}")


    # Change remote
    os.chdir(f"{local_repo_path}/{repo_name}")
    os.system(f'git remote set-url origin {project.ssh_url_to_repo}')
    os.system("git push")
    print(f"{git_repo_url} successfully cloned to GitLab group.")


# Main function
def main():
    git_projects = get_git_org_projects()
    
    if git_projects:
        for git_repo_url in git_projects:
            clone_to_gitlab(git_repo_url)
    else:
        print("No projects found.")

if __name__ == "__main__":
    main()
