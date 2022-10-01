import discord
from discord import app_commands
import json
from dotenv import load_dotenv
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

    mensagem = await boasvindas.send(f"Bem vindo {member.mention}! Leia as regras em {regras.mention}")

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
async def embed_regras(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Fique atento às regras do servidor!",
        description="É um imenso prazer ter você aqui! Para nos mantermos fortes, unidos e organizados, é preciso que algumas regras e recomendações de comportamento sejam definidas (além do bom senso)",
        colour=14707394
    )

    embed.set_author(
        name="AMentoria", icon_url="https://i.imgur.com/9FK4CDT.png")

    embed.set_footer(text="Agora é só aproveitar 😄")

    embed.set_image(url="https://i.imgur.com/hLstMzb.png")

    embed.add_field(
        name="1️⃣  **Boa Convivência**", value="Desrespeito, palavras de baixo calão em excesso (mesmo que disfarçado), preconceito, extremismo e intolerância é proibido no servidor e nas DMs de nossos membros. Evite brincadeiras de mau gosto com quem você não tem intimidade \n", inline=False)

    embed.add_field(
        name="2️⃣  **Spam**", value="É proibido spam, flood, correntes, ou qualquer tipo de atividade que atrapalhe o fluxo correto dos canais de interação; \n", inline=False)
    embed.add_field(
        name="Regra 3", value="Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been", inline=False)

    await interaction.response.send_message(embed=embed)


@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def limparchat(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)

# Reclame aqui
# Criar ticket


@client.tree.command()
async def criarticket(interaction: discord.Interaction):
    suporte = interaction.guild.get_role(1011436517790580777)
    categoria = interaction.guild.get_channel(1015067862500655217)

    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
        suporte: discord.PermissionOverwrite(read_messages=True),
        interaction.user: discord.PermissionOverwrite(read_messages=True)
    }

    canal = await interaction.guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, category=categoria)
    await interaction.response.send_message(f"O atendimento foi criado em {canal.mention}", ephemeral=True)
    await canal.send(f"olá, {interaction.user.mention} você abriu um atendimento! Em breve você será atendido")

# Apagar ticket


@client.tree.command()
async def apagarticket(interaction: discord.Interaction):
    await interaction.channel.delete()


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
