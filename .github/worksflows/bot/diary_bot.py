import os
import datetime
import discord
from github import Github

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = "calmkamille/diary" 

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

def post_diary(content: str):
    """GitHub に日記を作成または更新する関数"""
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    path = f"diary/{day}.txt"

    try:
        existing_file = repo.get_contents(path)
        repo.update_file(
            path=path,
            message=f"Update diary {day}",
            content=content,
            sha=existing_file.sha
        )
        print(f"✅ Updated diary: {path}")

    except Exception as e:
        repo.create_file(
            path=path,
            message=f"Add diary {day}",
            content=content
        )
        print(f"✅ Created new diary: {path}")

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    try:
        post_diary(message.content)
        await message.channel.send("日記を GitHub に保存しました！")
    except Exception as e:
        print(f"❌ Error: {e}")
        await message.channel.send("日記の保存に失敗しました。")

client.run(DISCORD_TOKEN)
