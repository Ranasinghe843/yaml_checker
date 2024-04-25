def get_github_runners():
    with open('../../../../yaml_checker/github_runners.txt', 'r') as f:
        github_runners = [line.rstrip('\n') for line in f]
    return github_runners

def uses_github_runner(runs_on):
    github_runners = get_github_runners()
    return all(run in github_runners for run in runs_on)

def main():
    github_runners = get_github_runners()
    print(github_runners)

if __name__ == '__main__':
    main()