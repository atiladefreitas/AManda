import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import json

server_id = discord.Object(id=1011390676409262140)


class MeuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, application_id=1015640583747936386)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(View())
        self.tree.copy_global_to(guild=server_id)
        await self.tree.sync(guild=server_id)


client = MeuClient(intents=discord.Intents.default())


@client.event
async def on_ready():
    print("O bot está funcionando 🚀")


@client.tree.command()
async def ola(interaction: discord.Interaction):
    await interaction.response.send_message("de nada! careca")


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
@app_commands.default_permissions(manage_messages=True)
async def limparchat(interaction: discord.Interaction, quantidade: int):
    await interaction.channel.purge(limit=quantidade)
    await interaction.response.send_message("🧹 O chat foi apagado com sucesso")

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

# Definindo a função de visualizar carteira


async def mostrar_carteira():
    with open("carteira.json", "r") as f:
        saldos = json.load(f)

    return saldos

# Definindo a função para abrir uma conta caso usuário não tenha


async def abrir_conta(user):
    saldos = await mostrar_carteira()
    if str(user.id) in saldos:
        return False
    else:
        saldos[str(user.id)] = {}
        saldos[str(user.id)]["saldo"] = 0
    with open("carteira.json", "w") as f:
        json.dump(saldos, f)
    return True


async def adicionar_saldo(user, valor):
    await abrir_conta(user)
    saldos = await mostrar_carteira()
    saldos[str(user.id)]["saldo"] += int(valor)

    with open("carteira.json", "w") as f:
        json.dump(saldos, f)

    return saldos[str(user.id)]["saldo"]


@client.tree.command()
async def saldo(interaction: discord.Interaction, membro: discord.Member = None):
    if membro == None:
        membro = interaction.user

    await abrir_conta(membro)
    saldos = await mostrar_carteira()
    dinheiro = saldos[str(membro.id)]["saldo"]

    await interaction.response.send_message(f"O usuário tem {dinheiro} de dinheiro", ephemeral=True)


@client.tree.command()
async def adicionarsaldo(interaction: discord.Interaction, quantidade: int, membro: discord.Member = None):
    if membro == None:
        membro = interaction.user

    valor_final = await adicionar_saldo(membro, quantidade)
    await interaction.response.send_message(f"O usuário recebeu {quantidade} de moedas e agora tem {valor_final}.", ephemeral=True)


class View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

        botao = discord.ui.Button(
            label="Botão de Link", url="https://www.youtube.com/c/AMentoriaENEMEstrat%C3%A9giaEmAprova%C3%A7%C3%A3o/featured")
        self.add_item(botao)
        self.add_item(Menu())

    @discord.ui.button(label="Botão Normal", style=discord.ButtonStyle.blurple, emoji="🚀", disabled=False, custom_id="persistent_view:botao")
    async def botao1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Botão clicado.", ephemeral=True)


class Menu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="value1", label="Opção 1", emoji="🚀"),
            discord.SelectOption(value="value2", label="Opção 2", emoji="🎉"),
            discord.SelectOption(value="value3", label="Opção 3", emoji="👍"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=3,
            options=options,
            custom_id="persistent_view:menu"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.values, ephemeral=True)


@client.tree.command()
async def teste(interaction: discord.Interaction):
    await interaction.response.send_message("Mensagem", view=View())


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
