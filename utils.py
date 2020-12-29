import discord
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import normalize
import pyshorteners
import os


def normalizar(txt):
    texto = txt.lower()
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def clear():
    os.system('cls' if os.name=='nt' else 'clear')


def dicionario(palavra):

    if palavra == 'marselo':
        url = "https://youtu.be/dQw4w9WgXcQ"
        embed = discord.Embed(title=f'marselo\n', url=url, colour=discord.Colour(0x3498DB))
        embed.add_field(name=f'marselo', value='marselo', inline=False)
        embed.set_footer(text="marselo")
        return embed

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
            url = "https://youtu.be/dQw4w9WgXcQ"
            embed = discord.Embed(title=f'Não consegui encontrar "{palavra}" no dicio :(\n', url=url, colour=discord.Colour(0x3498DB))
            search = palavra.replace('-', '+')
            url = 'https://www.google.com/search?&q='+ search+'&ie=UTF-8&oe=UTF-8'
            shorted = pyshorteners.Shortener()
            url = shorted.tinyurl.short(url)
            embed.add_field(name=f'Mas pesquisei isso no google e esse foi o resultado:', value=url, inline=False)
            embed.set_footer(text="desculpa")
        else:
            embed = discord.Embed(title=f'{palavra.title()}\n', url=url, colour=discord.Colour(0x3498DB))
            embed.set_footer(text="Disponível em: https://www.dicio.com.br.")
            embed.add_field(name=pesquisa[0].title(), value='--'*len(pesquisa[0]), inline=False)
            cont = 0
            for i in range(1, len(pesquisa)):
                if pesquisa[i] and pesquisa[i] != " ":
                    cont+=1
                    embed.add_field(name=f'Significado {cont}: ', value=pesquisa[i], inline=False)
        return embed
    except:
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
                url = "https://youtu.be/dQw4w9WgXcQ"
                embed = discord.Embed(title=f'Não consegui encontrar "{palavra}" no dicio :(\n', url=url, colour=discord.Colour(0x3498DB))
                search = palavra.replace('-', '+')
                url = 'https://www.google.com/search?&q='+ search+'&ie=UTF-8&oe=UTF-8'
                shorted = pyshorteners.Shortener()
                url = shorted.tinyurl.short(url)
                embed.add_field(name=f'Mas pesquisei isso no google e esse foi o resultado:', value=url, inline=False)
                embed.set_footer(text="desculpa")
            else:
                embed = discord.Embed(title=f'{palavra.title()}\n', url=url, colour=discord.Colour(0x3498DB))
                embed.set_footer(text="Disponível em: https://www.dicio.com.br.")
                embed.add_field(name=pesquisa[0].title(), value='--'*len(pesquisa[0]), inline=False)
                cont = 0
                for i in range(1, len(pesquisa)):
                    if pesquisa[i] and pesquisa[i] != " ":
                        cont+=1
                        embed.add_field(name=f'Significado {cont}: ', value=pesquisa[i], inline=False)
            return embed

        except:
            url = "https://youtu.be/dQw4w9WgXcQ"
            palavra = palavra.replace('-', ' ')
            embed = discord.Embed(title=f'Não consegui encontrar "{palavra}" no dicio :(\n', url=url, colour=discord.Colour(0x3498DB))
            search = palavra.replace('-', '+')
            url = 'https://www.google.com/search?&q='+ search+'&ie=UTF-8&oe=UTF-8'
            shorted = pyshorteners.Shortener()
            url = shorted.tinyurl.short(url)
            embed.add_field(name=f'Mas pesquisei isso no google e esse foi o resultado:', value=url, inline=False)
            embed.set_footer(text="desculpa")
            return embed
