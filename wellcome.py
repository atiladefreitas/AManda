import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=">",
                      case_insensitive=True, intents=intents)


@client.event
async def on_member_join(member):
    boasvindas = client.get_channel(1011626674611310623)
    regras = client.get_channel(1011612420957020260)

    mensagem = await boasvindas.send(f"Bem vindo {member.mention}! Leia as regras em {regras.mention}")
    print("AAAAAAAAAAAAAAAA")


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
