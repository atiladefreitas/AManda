import discord
from discord import app_commands

server_id = discord.Object(id=1011390676409262140)


class MeuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents, application_id=1015640583747936386)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.add_view(View())
        self.tree.copy_global_to(guild=server_id)
        await self.tree.sync(guild=server_id)


class View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

        botao = discord.ui.Button(
            label="Botão de Link", url="https://www.youtube.com/dunegg")
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


client = MeuClient(intents=discord.Intents.default())


@client.event
async def on_ready():
    print("o bot está funcionando 🚀")


@client.tree.command()
async def ola(interaction: discord.Interaction):
    await interaction.response.send_message("Olá, tudo bem?")

""" load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
 """

client.run(
    'MTAxNTY0MDU4Mzc0NzkzNjM4Ng.GHUbSg.LA_6Ip69-KXM_fLdwsmI47itVsYhXjGVLH9w9E')
