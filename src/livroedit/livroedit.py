import discord
from discord.ui import Button, View

class LivroEdit(View):
    def __init__(self, livro):
        super().__init__(timeout=500)
        self.Livro = livro
        self.escolha = None

    def criar_embed(self):
        l = self.Livro
        embed = discord.Embed(title=l["nome"], description=f"Autor: {l['autor']}\nStatus: {l['status']}\n 1 - Editar Nome\n 2 - Editar Autor\n 3 - Editar Imagem\n 4 - Editar Status")
        embed.set_image(url=l["imagem"])
        return embed
    
    @discord.ui.button(emoji="1️⃣", style=discord.ButtonStyle.primary)
    async def editar_nome(self, button: Button, interaction: discord.Interaction):
        self.escolha = 1
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(emoji="2️⃣", style=discord.ButtonStyle.primary)
    async def editar_autor(self, button: Button, interaction: discord.Interaction):
        self.escolha = 2
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(emoji="3️⃣", style=discord.ButtonStyle.primary)
    async def editar_imagem(self, button: Button, interaction: discord.Interaction):
        self.escolha = 3
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(emoji="4️⃣", style=discord.ButtonStyle.primary)
    async def editar_status(self, button: Button, interaction: discord.Interaction):
        self.escolha = 4
        await interaction.response.defer()
        self.stop()
