import discord
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
from unicodedata import normalize
import os
from datetime import datetime

import pesquisa_google


def normalizar(txt):
    texto = txt.lower()
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


async def dicionario(ctx, palavra):

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
        url = f'https://www.dicio.com.br/{palavra}/'
        response = urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find('p')

        def remove_html_tags(text):
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)

        pesquisa = []

        for txt in text:
            pesquisa.append(remove_html_tags(str(txt)))

        if pesquisa[0].startswith('Ainda não temos'):
            print('Ainda não tem a palavra no dicio')
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
            return
        else:
            embed = discord.Embed(
                title=f'{palavra.title()}\n',
                url=url,
                colour=discord.Colour(0x349cff)
            )
            embed.set_footer(text="Disponível em: https://www.dicio.com.br.")
            embed.add_field(
                name=pesquisa[0].title(),
                value='--'*len(pesquisa[0]),
                inline=False
            )
            cont = 0
            for i in range(1, len(pesquisa)):
                if pesquisa[i] and pesquisa[i] != " ":
                    cont += 1
                    embed.add_field(
                        name=f'Significado {cont}: ',
                        value=pesquisa[i],
                        inline=False
                    )
        await ctx.send(embed=embed)
        return
    except HTTPError:
        print('http error no dicio, tentando com traços')
        try:
            palavra = palavra.replace(' ', '-')
            url = f'https://www.dicio.com.br/{palavra}/'
            response = urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.find('p')

            def remove_html_tags(text):
                clean = re.compile('<.*?>')
                return re.sub(clean, '', text)

            pesquisa = []

            for txt in text:
                pesquisa.append(remove_html_tags(str(txt)))

            if pesquisa[0].startswith('Ainda não temos'):
                print('Ainda não tem a palavra no dicio')
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
            else:
                embed = discord.Embed(
                    title=f'{palavra.title()}\n',
                    url=url,
                    colour=discord.Colour(0x349cff)
                )
                embed.set_footer(
                    text="Disponível em: https://www.dicio.com.br."
                )
                embed.add_field(
                    name=pesquisa[0].title(),
                    value='--'*len(pesquisa[0]),
                    inline=False
                )
                cont = 0
                for i in range(1, len(pesquisa)):
                    if pesquisa[i] and pesquisa[i] != " ":
                        cont += 1
                        embed.add_field(
                            name=f'Significado {cont}: ',
                            value=pesquisa[i],
                            inline=False
                        )
            await ctx.send(embed=embed)
            return

        except HTTPError:
            print('http error total no dicio')
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


def hora_atual():
    return (datetime.now()).strftime("%H:%M:%S")
