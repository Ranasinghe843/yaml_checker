import os
import yaml
import re
from commit_hash import is_commit_hash
from github_runners import uses_github_runner
from verified_creators import is_verified_creator

def extract_actions_and_runs_on(workflow_file):
    actions = []
    runs_on = []
    with open(workflow_file, 'r') as file:
        workflow_content = yaml.safe_load(file)
        if 'jobs' in workflow_content:
            for job in workflow_content['jobs'].values():
                if 'steps' in job:
                    for step in job['steps']:
                        if 'uses' in step:
                            actions.append(step['uses'])
                if 'runs-on' in job:
                    runs_on_value = job['runs-on']
                    if isinstance(runs_on_value, str):
                        matrix_var_match = re.search(r'\${{\s*matrix\.([\w-]+)\s*}}', runs_on_value)
                        if matrix_var_match:
                            matrix_var = matrix_var_match.group(1)
                            matrix_value = job.get('strategy', {}).get('matrix', {}).get(matrix_var, '')
                            runs_on.extend(matrix_value)
                        else:
                            runs_on.append(runs_on_value)
                    elif isinstance(runs_on_value, list):
                        for run in runs_on_value:
                            matrix_var_match = re.search(r'\${{\s*matrix\.([\w-]+)\s*}}', run)
                            if matrix_var_match:
                                matrix_var = matrix_var_match.group(1)
                                matrix_value = job.get('strategy', {}).get('matrix', {}).get(matrix_var, '')
                                runs_on.extend(matrix_value)
                            else:
                                runs_on.append(run)
    return actions, runs_on
        
def per_repo(dir):
    os.chdir(dir)
    workflow_files = [file for file in os.listdir('.') if file.endswith('.yml') or file.endswith('.yaml')]
    total_actions = 0
    actions_with_commit_hash = 0
    github_runner_not_used = 0
    unverified_creators = []
    verified_creators = []
    unverified_creator_actions = 0

    for workflow_file in workflow_files:
        actions, runs_on = extract_actions_and_runs_on(workflow_file)
        total_actions += len(actions)
        for action in actions:
            # Split the action reference to extract the ref part
            if is_commit_hash(action):
                actions_with_commit_hash += 1
            
            # Extract the creator of the action
            creator = action.split('/')[0]
            if creator in unverified_creators:
                unverified_creator_actions += 1
            elif creator in verified_creators:
                continue
            else:
                is_verified = is_verified_creator(creator)
                if is_verified == True:
                    verified_creators.append(creator)
                else:
                    unverified_creators.append(creator)
                    unverified_creator_actions += 1
    
        if not uses_github_runner(runs_on):
            github_runner_not_used += 1
            
    print("Total actions:", total_actions)
    print("Actions with commit hash pinning:", actions_with_commit_hash)
    print("Self-hosted runners used:", github_runner_not_used)
    print("Actions used from unverified creators:", unverified_creator_actions)
    print("Verified creators:", verified_creators)
    print("Unverified creators:", unverified_creators)

def main():
    contents = os.listdir('../repos')
    directories = [entry for entry in contents if os.path.isdir(os.path.join('../repos', entry))]
    for direct in directories:
        print(direct + ':')
        per_repo('../repos/' + direct + '/.github/workflows')
        print("")
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    main()
