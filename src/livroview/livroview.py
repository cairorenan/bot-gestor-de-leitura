import discord
from discord.ui import Button, View

class LivroView(View):
    def __init__(self, livros):
        super().__init__(timeout=None)
        self.Livros = livros
        self.index = 0

    def criar_embed(self):
        l = self.Livros[self.index]
        embed = discord.Embed(title=l["nome"], description=f"Autor: {l['autor']}\nStatus: {l['status']}")
        embed.set_image(url=l["imagem"])
        embed.set_footer(text=f"{self.index+1} de {len(self.Livros)}")
        return embed

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.primary)
    async def anterior(self, button: Button, interaction: discord.Interaction):
        if self.index > 0:
            self.index -= 1
            await interaction.response.edit_message(embed=self.criar_embed(), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.primary)
    async def proximo(self, button: Button, interaction: discord.Interaction):
        if self.index < len(self.Livros) - 1:
            self.index += 1
            await interaction.response.edit_message(embed=self.criar_embed(), view=self)
        else:
            await interaction.response.defer()
