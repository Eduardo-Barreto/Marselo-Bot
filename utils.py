import pesquisa_google
import discord
from urllib.request import urlopen
from urllib.error import HTTPError
from unicodedata import normalize
import os
from datetime import datetime
import wikipedia as wiki

from tokens import conexao_username, conexao_password, conexao_token
from bot_links import conexao_digital
from ics import Calendar
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def normalizar(txt):
    texto = txt.lower()
    return normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def hora_atual():
    return (datetime.now()).strftime("%H:%M:%S")


def processar(texto):
    to_replace = [
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+',
        '=', '"', ',', '?', '.', ':', '~', '>', '<', '{', '}', ';'
    ]
    for item in to_replace:
        texto = texto.replace(item, '')
    texto = texto.strip()

    for numero in range(10):
        texto = texto.replace(str(numero), '')
    texto = texto.strip()

    return texto


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
                url=url
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


async def pegar_trabalhos(ctx):

    logged_session = requests.Session()

    url = 'https://conexaodigital2em.sesisp.org.br/login/index.php'
    data = {'username': conexao_username, 'password': conexao_password}

    response_login = logged_session.post(url, data=data, verify=False)

    if response_login.status_code == 200:
        print('Login realizado com sucesso')

    url = (
        'https://conexaodigital2em.sesisp.org.br/calendar/' +
        f'export_execute.php?userid=2012&authtoken={conexao_token}' +
        'preset_what=courses&preset_time=weeknow'
    )

    response_calendar = logged_session.get(
        url, verify=False, allow_redirects=True)

    if response_calendar.status_code == 200:
        print('Calendário acessado com sucesso')

    c = Calendar(response_calendar.text)

    eventos = {}

    for event in c.events:
        materia = str(event.categories)
        materia = materia[2:materia.find(' -')]
        tempo = str(event.begin.humanize())
        tempo = tempo.replace('a day', 'um dia')
        tempo = tempo.replace('in', 'em')
        tempo = tempo.replace('days', 'dias')
        tempo = tempo.replace('ago', 'atrás')
        # TODO: traduzir dias restantes
        nome = event.name
        nome = nome[:nome.find('está marcado(a)')]
        eventos.update({tempo: [materia, nome]})

    embed = discord.Embed(
        title='Lições dessa semana!',
        description='2º Ano do Ensino médio - SESI CE 402',
        colour=discord.Colour(0x349cff),
        url=conexao_digital
    )
    embed.set_footer(
        text='Conexão Digital SESI-SP | Marselo'
    )

    for item in sorted(eventos):
        embed.add_field(
            name=eventos.get(item)[0],
            value=f'{eventos.get(item)[1]}\n**({item})**',
            inline=False
        )

    await ctx.send('Aqui está! :)', embed=embed)
