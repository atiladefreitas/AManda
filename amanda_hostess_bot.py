import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os

server_id = discord.Object(id=1011390676409262140)

intents = discord.Intents.all()
intents.members = True


class MeuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, application_id=1015640583747936386)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=server_id)
        await self.tree.sync(guild=server_id)


client = MeuClient(intents=discord.Intents.all())

# bot startup


@client.event
async def on_ready():
    print("O bot está funcionando 🚀")

# mensagem de boas vindas


@client.event
async def on_member_join(member):
    boasvindas = client.get_channel(1011626674611310623)
    regras = client.get_channel(1011612420957020260)
    cargo = member.guild.get_role(1028364839904616468)

    mensagem = await boasvindas.send(f"Bem vindo {member.mention}! Leia as regras em {regras.mention}")

    await member.add_roles(cargo)

    await asyncio.sleep(60)

    await mensagem.delete()


@client.tree.command()
@app_commands.default_permissions(kick_members=True)
async def expulsar(interaction: discord.Interaction, usuario: discord.Member, motivo: str = "O usuário foi expulso por fazer spam."):
    try:
        await usuario.kick(reason=motivo)
    except:
        await interaction.response.send_message(f"O usuário {usuario} não pode ser expulso, pois não tenho permissões.")
    else:
        await interaction.response.send_message("O usuário foi expulso com sucesso.")


@client.tree.command()
@app_commands.default_permissions(ban_members=True)
async def banir(interaction: discord.Interaction, usuario: discord.Member, motivo: str = "O usuário foi banido por fazer spam."):
    try:
        await usuario.ban(delete_message_days=7, reason=motivo)
    except:
        await interaction.response.send_message(f"O usuário {usuario} não pode ser banido, pois não tenho permissões.")
    else:
        await interaction.response.send_message("O usuário foi banido com sucesso.")


@client.tree.command()
@app_commands.default_permissions(ban_members=True)
async def desbanir(interaction: discord.Interaction, usuario: discord.Member, motivo: str = "O usuário foi banido por fazer spam."):
    try:
        await usuario.unban(reason=motivo)
    except:
        await interaction.response.send_message(f"O usuário {usuario} não pode ser desbanido, pois não tenho permissões.")
    else:
        await interaction.response.send_message("O usuário foi desbanido com sucesso.")


@client.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def embed_regras(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Fique atento às regras do servidor!",
        description="É um imenso prazer ter você aqui! Para nos mantermos fortes, unidos e organizados, é preciso que algumas regras e recomendações de comportamento sejam definidas (além do bom senso)",
        colour=14707394
    )

    embed.set_author(
        name="AMentoria", icon_url="https://i.imgur.com/9FK4CDT.png")

    embed.set_footer(
        text="As regras estão sujeitas à alteração da moderação")

    embed.set_image(url="https://i.imgur.com/hLstMzb.png")

    embed.add_field(
        name="1️⃣  **Boa Convivência**", value="Desrespeito, palavras de baixo calão em excesso (mesmo que disfarçado), preconceito, extremismo e intolerância é proibido no servidor e nas DMs de nossos membros. Evite brincadeiras de mau gosto com quem você não tem intimidade \n", inline=False)

    embed.add_field(
        name="2️⃣  **Spam**", value="É proibido spam, flood, correntes, ou qualquer tipo de atividade que atrapalhe o fluxo correto dos canais de interação; \n", inline=False)
    embed.add_field(
        name="3️⃣ **É proibida a discussão de assuntos sensíveis**", value="incluindo mas não limitado a: política, religião, orientação sexual, etc.", inline=False)

    await interaction.response.send_message(embed=embed)


@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def limparchat(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)


@client.tree.command()
@commands.has_role(1028373517516931113)
async def pomo_message(interaction: discord.Interaction):
    await interaction.response.send_message("Olá! Neste canal você poderá acompanhar o seu tempo de estudo e de descanso.\nNão se preocupe, você será avisado(a) quando um desses tempos terminar 😄 ")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
