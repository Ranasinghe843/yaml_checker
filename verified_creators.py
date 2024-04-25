import requests

def get_verified_creators():
    with open('../../../../yaml_checker/verified_creators.txt', 'r') as f:
        verified_creators = [line.rstrip('\n') for line in f]
    return verified_creators

def get_unverified_creators():
    with open('../../../../yaml_checker/unverified_creators.txt', 'r') as f:
        unverified_creators = [line.rstrip('\n') for line in f]
    return unverified_creators

def add_verified_creator(username):
    with open('../../../../yaml_checker/verified_creators.txt', 'a') as f:
        f.write(username + '\n')

def add_unverified_creator(username):
    with open('../../../../yaml_checker/unverified_creators.txt', 'a') as f:
        f.write(username + '\n')

def is_verified_creator(username):
    verified_creators = get_verified_creators()
    if username in verified_creators:
        return True
    
    unverified_creators = get_unverified_creators()
    if username in unverified_creators:
        return False
    
    print("Making API call ...")

    access_token = ""
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'Bearer ' + access_token}
    query = """
    query {
      organization(login: "%s") {
        login
        isVerified
      }
    }
    """ % username

    response = requests.post(url, json={'query': query}, headers=headers)
    data = response.json()

    if 'errors' in data:
        add_unverified_creator(username)
        return False
    else:
        organization = data['data']['organization']
        if organization:
            if organization['isVerified']:
                add_verified_creator(username)
                return True
            else:
                add_unverified_creator(username)
                return False
        else:
            add_unverified_creator(username)
            return False