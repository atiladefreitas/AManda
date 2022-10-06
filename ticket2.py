import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

id_do_servidor = 1011390676409262140
id_cargo_atendente = 1011436517790580777


class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="ajuda", label="Ajuda", emoji="👋"),
            discord.SelectOption(value="atendimento",
                                 label="Atendimento", emoji="📨"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "ajuda":
            await interaction.response.send_message("bla bla bla", ephemeral=True)
        elif self.values[0] == "atendimento":
            await interaction.response.send_message("Clique abaixo para criar um ticket", ephemeral=True, view=CreateTicket())


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Dropdown())


class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value = None

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.blurple, emoji="➕")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True, content=f"Você já tem um atendimento em andamento!")
                    return

        if ticket != None:
            await ticket.unarchive()
            # ,invitable=False) Exclusivo para Thread Privada
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080)
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080, type=discord.ChannelType.public_thread)
            # await ticket.edit(invitable=False) Exclusivo para Thread Privada

        await interaction.response.send_message(ephemeral=True, content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"📩  **|** {interaction.user.mention} ticket criado! Envie todas as informações possíveis sobre seu caso e aguarde até que um atendente responda.\n\nApós a sua questão ser sanada, você pode usar `/fecharticket` para encerrar o atendimento!")

#####################


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        # Nós usamos isso para o bot não sincronizar os comandos mais de uma vez
        self.synced = False

    async def setup_hook(self) -> None:
        self.add_view(DropdownView())

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Checar se os comandos slash foram sincronizados
            # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            await tree.sync(guild=discord.Object(id=id_do_servidor))
            self.synced = True
        print(f"Entramos como {self.user}.")


aclient = client()

tree = app_commands.CommandTree(aclient)


@tree.command(guild=discord.Object(id=id_do_servidor), name='setup', description='Setup')
@commands.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("Painel criado", ephemeral=True)

    embed = discord.Embed(
        colour=discord.Color.blurple(),
        title="Centra de Ajuda do Servidor",
        description="Nessa seção, você pode tirar suas dúvidas ou entrar em contato com a nossa equipe AMentoria. \n \n Para evitar problemas, leia as opções com atenção e lembre-se de tentar pedir ajuda nos suportes comunitários mais acima nessa categoria."
    )
    embed.set_image(url="https://i.imgur.com/wvW5pQp.png")

    await interaction.channel.send(embed=embed, view=DropdownView())


@tree.command(guild=discord.Object(id=id_do_servidor), name="fecharticket", description='Feche um atendimento atual.')
async def _fecharticket(interaction: discord.Interaction):
    mod = interaction.guild.get_role(1025556740365885521)
    if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
        await interaction.response.send_message(f"O ticket foi arquivado por {interaction.user.mention}, obrigado por entrar em contato!")
        await interaction.channel.edit(archived=True)
    else:
        await interaction.response.send_message("Isso não pode ser feito aqui...")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
aclient.run(TOKEN)
