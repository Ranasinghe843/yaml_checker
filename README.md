# GitHub Actions Analyzer

This Python script analyzes GitHub workflow files to gather metrics such as the total number of actions, the number of actions with commit hash pinning, the number of times Self-hosted runners are used and whether the action is from a verified creator or not.

## How to Use

1. **Clone the Repository:** Clone this repository to your local machine.

2. **Install Dependencies:** Make sure you have Python installed on your system. Install the required dependencies using the following command:
```
pip install -r requirements.txt
```

3. **Add Access Token:** Add you github access token to the ```access_token.txt``` file

4. **Run the scripts:** The scripts need the downloaded repos in a folder outside the repository. To run the scripts then, run:
```
python yaml_checker.py {foldername}
```
5. **Output:** The output will be in the ```data.json``` file