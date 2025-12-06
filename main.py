from flask import Flask, request
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

url = os.getenv("URL")
channel_id = os.getenv("CHANNELID")

def discord_webhook(url: str, data: dict) -> None:
    print(data)
    repo: dict = data["repository"]
    repo_fullname: str = repo["full_name"]
    repo_name: str = repo["name"]
    commits: dict = data["commits"]
    locked: bool = repo["private"]

    sender: str = data["sender"]
    sender_name: str = sender["login"]
    sender_url: str = sender["html_url"]
    
    fromcommit: str = data["before"][0:5]
    tocommit: str = data["after"][0:5]
    
    res: str = ""

    locked_emoji: str = ""
    if locked:
        locked_emoji = "🔒"

    for commit in commits:
        message: str = commit["message"]
        res += message + "\n"
    
    requests.post(url, {
        "username": "github",
        "content": f"{res}\n-# {fromcommit}->{tocommit}\n-# [{sender_name}](<{sender_url}>) в [{repo_name}{locked_emoji}](<https://github.com/{repo_fullname}>)"
        }
    )

@app.route("/git", methods=["POST"])
def git() -> int:
    data = request.get_json()
    discord_webhook(url, data)
    return 200

if __name__ == "__main__":
    app.run(os.getenv("HOST"), os.getenv("PORTs"), True)