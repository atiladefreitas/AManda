import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

server_id = discord.Object(id=1011390676409262140)

intents = discord.Intents.default()
intents.members = True


class MeuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, application_id=1015640583747936386)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=server_id)
        await self.tree.sync(guild=server_id)


client = MeuClient(intents=discord.Intents.default())

# bot startup


@client.event
async def on_ready():
    print("O bot está funcionando 🚀")

# mensagem de boas vindas


@client.event
async def on_member_join(member):
    boasvindas = client.get_channel(1011626674611310623)
    regras = client.get_channel(1011612420957020260)

    mensagem = await boasvindas.send(f"Bem vindo {member.mention}! Leia as regras em {regras.mention}")

    await asyncio.sleep(60)

    await mensagem.delete()


@client.event
async def on_member_join(member):
    member.add_roles(1028364839904616468)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
