# Fetch Stargazers

Simple CLI tool to info about the stargazers of a GitHub repository.

## Quick Start


1. Set up a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate       # on macOS/Linux
# OR
.\.venv\Scripts\Activate.ps1    # on Windows (PowerShell)
```

2. Install the required packages:

```
pip install -r requirements.txt
```

3. Make it executable:

```
chmod +x gaze.py
```

4. Profit

```
$ .venv/bin/python stargazers_to_csv.py instantdb instant stargazers.csv --token $GITHUB_TOKEN
```

You can now open the `stargazers.csv` file in your favorite spreadsheet
application.

## Notes

This script was made via
[o3](https://chatgpt.com/share/682bbae6-2ad0-8013-91c2-1fde0e9c7c10) 

Beware of rate limits. From ChatGPT:

> Auth & rate limits: unauthenticated calls hit the 60-requests/hour ceiling. Pass a personal-access token (repo scope is fine) to jump to 5k/hour.
