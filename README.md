# Discord File Browser Bot

A Discord bot that lets you browse and download files directly through Discord commands.

## Features

- Browse remote/local files
- Download files via GoFile links using the GoFile API
- Delete, rename, move, execute, and inject files to users computer
- Simple slash/prefix command interface
- Ability to automatically **hide** file along with **persistance** (run on startup)

## Requirements

- Python 3.4+
- A Discord account and a server where you can add bots
- A [GoFile](https://gofile.io) account (free tier works)

## 1. Setting Up a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application**, give it a name, and click **Create**.
3. In the left sidebar, click **Bot**.
4. Click **Reset Token** (or **Add Bot** if it's your first time), then **Copy** the token.
5. Under the **Bot** tab, enable any **Privileged Gateway Intents** your bot needs (e.g. `Message Content Intent` if you're using prefix commands).
6. Go to **OAuth2 → URL Generator**:
   - Under **Scopes**, check `bot` (and `applications.commands` if you're using slash commands).
   - Under **Bot Permissions**, select at minimum:
     - `Send Messages`
     - `Read Message History`
     - `Attach Files`
     - `Embed Links`
   - Copy the generated URL at the bottom.
7. Paste that URL into your browser, select your server, and click **Authorize** to invite the bot.

## 2. Getting Your GoFile API Key

1. Create a free account at [gofile.io](https://gofile.io) if you don't already have one.
2. Log in, then go to your **Profile** page (click your avatar/username in the top right).
3. Scroll to the section labeled **API Key** (sometimes called "Token").
4. Click **Copy** to copy your API key.
5. Save this key

## 3. Installation
download source zip

Install dependencies:

```bash
pip install -r requirements.txt

```
run Main.py

```bash
python Main.py

```
A Gui window will appear and the guide tab wil ltake you from there.

## License

This project is licensed under the [MIT License](LICENSE).
