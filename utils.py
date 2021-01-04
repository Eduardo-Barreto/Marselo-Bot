import discord
from urllib.request import urlopen
from urllib.error import HTTPError
from unicodedata import normalize
import os
from datetime import datetime
import wikipedia as wiki

import pesquisa_google


def normalizar(txt):
    texto = txt.lower()
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def hora_atual():
    return (datetime.now()).strftime("%H:%M:%S")


async def dicionario(ctx, palavra):

    palavra = normalizar(palavra)

    if palavra == 'marselo':
        url = "https://youtu.be/dQw4w9WgXcQ"
        embed = discord.Embed(
            title='marselo\n', url=url, colour=discord.Colour(0x349cff)
        )
        embed.add_field(name='marselo', value='marselo', inline=False)
        embed.set_footer(text="marselo")
        await ctx.send(embed=embed)
        return

    try:
        url = f'https://s.dicio.com.br/{palavra}.jpg'
        urlopen(url)
        await ctx.send(url)
        return

    except HTTPError:
        try:
            palavra = palavra.replace(' ', '-')
            url = f'https://s.dicio.com.br/{palavra}.jpg'
            urlopen(url)
            await ctx.send(url)
            return

        except HTTPError:
            url = pesquisa_google.get_link(palavra)
            pesquisa_google.get_screenshot(url)
            embed = discord.Embed(
                title=f'Não consegui encontrar "{palavra}" no dicio :(',
                description='Mas pesquisei no google e encontrei isso:',
                colour=discord.Colour(0x349cff),
                url=url,
            )
            embed.set_footer(
                text='Você pode clicar no texto em azul para abrir'
            )
            imagem = discord.File(
                'screenshot.jpg',
                filename='screenshot.jpg'
            )
            embed.set_image(url='attachment://screenshot.jpg')
            palavra = palavra.replace('-', ' ')
            await ctx.send(file=imagem, embed=embed)


async def wikipedia(ctx, topico):
    try:
        topico = topico.title()
        wiki.set_lang("pt")
        texto = wiki.summary(topico, sentences=3)
        pagina = wiki.page(topico)
        topico_url = topico.replace(' ', '_')
        url = f'https://pt.wikipedia.org/wiki/{topico_url}'
        embed = discord.Embed(
            title=topico,
            colour=discord.Colour(0x349cff),
            url=url,
        )
        imagem1 = pagina.images[0]
        imagem2 = pagina.images[1]
        embed.set_image(url=imagem1)
        embed.set_thumbnail(url=imagem2)
        embed.add_field(
            name='Resumo:',
            value=texto,
            inline=False
        )
        embed.set_footer(
            text=f'Disponível em {url}'
        )
        await ctx.send(embed=embed)

    except wiki.exceptions.PageError:
        url = pesquisa_google.get_link(topico)
        pesquisa_google.get_screenshot(url)
        embed = discord.Embed(
            title=f'Não consegui encontrar "{topico}" na wiki :(',
            description='Mas pesquisei no google e encontrei isso:',
            colour=discord.Colour(0x349cff),
            url=url,
        )
        embed.set_footer(
            text='Você pode clicar no texto em azul para abrir'
        )
        imagem = discord.File(
            'screenshot.jpg',
            filename='screenshot.jpg'
        )
        embed.set_image(url='attachment://screenshot.jpg')
        topico = topico.replace('-', ' ')
        await ctx.send(file=imagem, embed=embed)
