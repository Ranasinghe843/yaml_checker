def is_commit_hash(action):
    return len(action.split('@')[-1]) == 40