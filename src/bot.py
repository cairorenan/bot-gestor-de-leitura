import asyncio
import discord
from discord.ext import commands
import requests
from discord import Option
from livroview.livroview import LivroView
from livroedit.livroedit import LivroEdit

url_cadastrar = "http://localhost:5432/cadastrar"
url_listar = "http://localhost:5432/list"
tokken = ''

permissoes = discord.Intents.default()
permissoes.message_content = True
bot = commands.Bot(".", intents= permissoes)

@bot.event
async def on_ready():
    print("pronto!")

@bot.slash_command(name="cadastrar", description="cadastra um livro no banco de dados")
async def cadastrar(ctx:discord.ApplicationContext, nome: str, autor: str, imagem: str, status: Option = Option(description="Escolha o status de leitura", choices=["PENDENTE", "CONCLUIDO", "PLANEJADO"])):
    data = {
        "nome": nome,
        "autor": autor,
        "imagem": imagem,
        "status": status
    }
    clivro = requests.post(url_cadastrar, json=data)
    if clivro.status_code == 200:        
        await ctx.respond(f"Livro {nome} Cadastrado!")
    else:
        await ctx.respond("algo deu errado!")

@bot.slash_command(name="listar_individualmente", description="lista os livros um por um")
async def listar_individualmente(ctx:discord.ApplicationContext):
    llivro = requests.get(url_listar)
    if llivro.status_code == 200:
        livros = llivro.json()
        if not livros:
            await ctx.respond("Nenhum livro foi cadastrado!")
            return
        view = LivroView(livros)
        embed = view.criar_embed()
        await ctx.respond(embed=embed, view=view)
    else:
        await ctx.respond("algo deu errado!")

@bot.slash_command(name="listar_todos", description="lista os livros em forma de lista")
async def listar_todos(ctx:discord.ApplicationContext):
    llivro = requests.get(url_listar)
    if llivro.status_code == 200:
        livros = llivro.json()
        if not livros:
            await ctx.respond("Nenhum livro foi cadastrado!")
            return
        embed = discord.Embed(title="-----Lista de Livros-----")
        for l in livros:
            nome = l["nome"]
            status = l["status"]
            embed.add_field(name=nome, value=f"Status: {status}",inline=False)
        await ctx.respond(embed = embed)

@bot.slash_command(name="deletar_livro", description="deleta algum livro")
async def deletar_livro(ctx: discord.ApplicationContext, nome: str):
    llivro = requests.get(url_listar)
    if llivro.status_code == 200:
        livros = llivro.json()
        for l in livros:
            if l["nome"] == nome:
                id = l["id"]
                dlivro = requests.delete(f"http://localhost:5432/deletar/{id}")
                if dlivro.status_code == 200:
                    await ctx.respond(f"Livro: {nome} deletado com sucesso!")
                else:
                    await ctx.respond(f"Não foi possível deletar {nome}")
                return
        await ctx.respond("Livro não encontrado.")
    else:
        await ctx.respond("Algo deu errado ao buscar os livros.")

@bot.slash_command(name="buscar_livro", description="busca o livro desejado e edita se desejado")
async def editar_livro(ctx: discord.ApplicationContext, nome: str):
    llivro = requests.get(url_listar)
    if llivro.status_code == 200:
        livros = llivro.json()
        for l in livros:
            if l["nome"] == nome:
                id = l["id"]
                edit = LivroEdit(l)
                embed = edit.criar_embed()
                await ctx.respond(embed=embed, view=edit)
                await edit.wait()
                while edit.escolha is None:
                    await asyncio.sleep(1)
                novo_nome = l["nome"]
                novo_autor = l["autor"]
                nova_imagem = l["imagem"]
                novo_status = l["status"]
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                match edit.escolha:
                    case 1:
                        await ctx.followup.send("Digite o novo nome para o livro: ")
                        try:
                            msg = await bot.wait_for('message', check=check, timeout=25)
                        except asyncio.TimeoutError:
                            await ctx.followup.send("Tempo esgotado")
                            return

                        novo_nome = msg.content

                    case 2:
                        await ctx.followup.send("Digite o novo autor para o livro: ")         
                        try:
                            msg = await bot.wait_for('message', check=check, timeout=25)
                        except asyncio.TimeoutError:
                            await ctx.followup.send("Tempo esgotado")
                            return

                        novo_autor = msg.content

                    case 3:
                        await ctx.followup.send("insira uma nova imagem para o livro:")
                        try:
                            msg = await bot.wait_for('message', check=check, timeout=25)
                        except asyncio.TimeoutError:
                            await ctx.followup.send("Tempo esgotado")
                            return

                        nova_imagem = msg.content
                    
                    case 4:
                        await ctx.followup.send("Digite o novo status para o livro (PENDENTE, CONCLUIDO, PLANEJADO): ")
                        try:
                            msg = await bot.wait_for('message', check=check, timeout=25)
                        except asyncio.TimeoutError:
                            await ctx.followup.send("Tempo esgotado")
                            return

                        novo_status = msg.content
                data = {
                "nome": novo_nome,
                "autor": novo_autor,
                "imagem": nova_imagem,
                "status": novo_status
            }
                elivro = requests.put(f"http://localhost:5432/editar/{id}", json=data)
                if elivro.status_code == 200:
                    await ctx.followup.send("Livro editado com sucesso!")
                else:
                    await ctx.followup.send("Algo deu errado...")

bot.run(tokken)