import discord
from discord import DMChannel
from discord.ext import commands
from discord.utils import get
import time
import asyncio
import os
from urllib.request import urlopen
from urllib.error import HTTPError
from datetime import datetime
from random import randint

import tokens
import utils
import pesquisa_google
import bot_links as links

msg_cargos_pronomes = 791808051983155200
tempo_inicial = '0'

comandos_errados = [
    '-p', '-n', '-q', '-m', '-r', '!p', '-rm',
    '-rf', '-rr', '-rw', '-ff', 'ar!', '-go',
    '-di'
]


def check_anti_log(mensagem):
    for comando in bot.commands:
        if (str(comando) in mensagem):
            return False
        for alias in comando.aliases:
            if str(alias) in mensagem:
                return False
    for comando in comandos_errados:
        if (str(comando) in utils.normalizar(mensagem)):
            return False
    return True


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='>', case_insensitive=True,
    intents=intents, help_command=None
)


@bot.event
async def on_ready():
    global tempo_inicial
    tempo_inicial = utils.hora_atual()
    utils.clear()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='github.com/Eduardo-Barreto/Marselo-Bot/'
        )
    )
    edu = await bot.fetch_user(tokens.eduardo_id)
    await DMChannel.send(edu, 'estou online!', delete_after=5)
    print(f'estou online, loguei em {bot.user}')


@bot.event
async def on_guild_join(guild):
    canal = guild.system_channel
    await canal.send(
        'Oi, eu sou o Marselo e fui criado para o servidor' +
        ' First Community Brasil! Você pode encontrar' +
        f' mais sobre mim em {links.repositorio}'
    )
    log_deleted = get(guild.text_channels, name='log-deleted')
    if log_deleted is None:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            )
        }
        await guild.create_text_channel('log-deleted', overwrites=overwrites)


@bot.event
async def on_member_join(member):
    print(f'{member} entrou no servidor :)')
    canal = member.guild.system_channel
    await canal.send(
        f'Bem vindo {member.mention}! Se apresenta pra gente,' +
        ' e não esquece de reagir na mensagem dos pronomes' +
        ' (basta subir um pouco ou ir nas mensagens fixadas)' +
        ' pra receber o cargo com os seus :)'
    )


@bot.event
async def on_member_remove(member):
    print(f'{member} saiu do servidor :(')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Por favor passe todos os argumentos requiridos.')
        await ctx.send(f'Você pode verificar os comandos em {links.readme}')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'Perai {ctx.author.mention},' +
            ' você não tem permissão para executar esse comando 🤨'
        )
    if isinstance(error, discord.Forbidden):
        await ctx.send(
            'Oops, não tenho permissão para executar esse comando 😔'
        )

    if isinstance(error, asyncio.TimeoutError):
        utils.clear()

    else:
        print(error)


@bot.event
async def on_raw_reaction_add(payload):

    if payload.message_id != msg_cargos_pronomes:
        return

    if payload.emoji.name == '💙':
        role = discord.utils.get(payload.member.guild.roles, name='a/ela/-a')
    elif payload.emoji.name == '💛':
        role = discord.utils.get(payload.member.guild.roles, name='o/ele/-o')
    elif payload.emoji.name == '🧡':
        role = discord.utils.get(payload.member.guild.roles, name='ê/elu/-e')

    await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(
        lambda m: m.id == payload.user_id,
        guild.members
    )

    if payload.message_id != msg_cargos_pronomes:
        return

    if payload.emoji.name == '💙':
        role = discord.utils.get(guild.roles, name='a/ela/-a')
    elif payload.emoji.name == '💛':
        role = discord.utils.get(guild.roles, name='o/ele/-o')
    elif payload.emoji.name == '🧡':
        role = discord.utils.get(guild.roles, name='ê/elu/-e')

    await member.remove_roles(role)


@bot.event
async def on_message_delete(message):
    global anti_raid
    if(
        (message.channel.name != 'log-deleted')
        and check_anti_log(message.content)
        and message.author.id != 234395307759108106
        and message.author.id != 235088799074484224
    ):
        member = message.author
        canal = message.channel.id
        user = message.author.id
        mensagem = message.content
        for channel in member.guild.channels:
            if channel.name == 'log-deleted':
                await channel.send(
                    f'`{mensagem}` de <@{user}> apagada no canal <#{canal}>'
                )


@bot.event
async def on_invite_create(invite: discord.Invite):
    usuario = invite.inviter
    print(f'{usuario.name} criou um convite')
    await invite.delete()
    await DMChannel.send(
        usuario,
        'Oi, vi aqui que você criou um convite pro servidor!' +
        ' Muito legal convidar pessoas, mas nós temos um convite global' +
        ' para isso, por favor use ele pra nos ajudar :)' +
        '\nhttps://discord.gg/8JWEN4F'
    )


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    comando = utils.normalizar(message.content)
    ctx = message.channel

    if message.author == bot.user:
        return

    if ((comando[0:2] in comandos_errados)
       or (comando[0:3] in comandos_errados)):

        if not str(ctx.name).startswith('comando'):
            try:
                await message.delete()
            except discord.Forbidden:
                await ctx.send(
                    'você enviou um comando para um outro bot,' +
                    ' mas foi no canal errado...'
                )
                await ctx.send(
                    'normalmente eu só apago' +
                    ' mas aparentemente não tenho essa permissão aqui.'
                )
        return

    if 'google pesquisar' in comando:
        print(
            f'{utils.hora_atual()}: {message.author.name} pediu pesquisa' +
            f' no server {message.guild}, no canal {message.channel}'
        )
        await ctx.send(
            'Pode deixar que eu pesquiso pra você!'
        )
        url = pesquisa_google.get_link(comando.replace('google pesquisar', ''))
        pesquisa_google.get_screenshot(url)
        embed = discord.Embed(
            title='Clique aqui para ser redirecionado',
            description='cada coisa q vcs pesquisam...',
            colour=discord.Colour(0x349cff),
            url=url,
        )
        embed.set_footer(text='desculpa a demora me barraram na entrada')
        imagem = discord.File('screenshot.jpg', filename='screenshot.jpg')
        embed.set_image(url='attachment://screenshot.jpg')
        await ctx.send(
            content=f'Aqui está a sua pesquisa, <@{message.author.id}>',
            file=imagem,
            embed=embed
        )


@bot.command(aliases=['ajuda'])
async def help(ctx, *, argumento=''):
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >help' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    if len(argumento) > 0:
        url = f'{links.readme}#{argumento}'
        await ctx.send(f'Ajuda para o comando {argumento}: {url}')
    else:
        await ctx.send(
            'Você pode encontrar todos os comandos em:' +
            f' {links.readme}'
        )


@bot.command(aliases=['dicionario', 'dc', 'dict'])
async def dicio(ctx, *, palavra):
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >dicio' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    await ctx.send('Opa, é pra já! Saindo no capricho')
    await utils.dicionario(ctx, palavra.lower())


@bot.command(aliases=['wikipedia'])
async def wiki(ctx, *, topico):
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >wiki' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    await utils.wikipedia(ctx, topico)


@bot.command()
async def ping(ctx):
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >ping' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )

    def pingar_dicio(palavra):
        init_time = int(round(time.time() * 1000))
        url = f'https://s.dicio.com.br/{palavra}.jpg'
        try:
            ping_dicio = urlopen(url)
            ping_dicio = int(round(time.time() * 1000)) - init_time

        except HTTPError:
            ping_dicio = 'Fora do ar'

        return ping_dicio

    pong = await ctx.send('pong?')
    init_time = int(round(time.time() * 1000))
    await pong.edit(content='Calculando o ping...')
    ping_marselo = int(round(time.time() * 1000)) - init_time

    ping_dicio = pingar_dicio('livro')

    init_time = int(round(time.time() * 1000))
    url = pesquisa_google.get_link('livro')
    pesquisa_google.get_screenshot(url)
    ping_google = int(round(time.time() * 1000)) - init_time

    embed = discord.Embed(
        title='Ping do marselo e suas dependências',
        colour=discord.Colour(0x349cff),
        url=links.rickrolling,
        description='Valores listados em milissegundos' +
                    ' e provavelmente imprecisos'
    )
    embed.set_footer(text='nossa mas esse do google é demorado né...')
    embed.add_field(
        name='Ping Marselo:',
        value=f'{ping_marselo}ms',
        inline=False
    )
    if type(ping_dicio) == str:
        embed.add_field(
            name='Ping Dicio:',
            value=f'{ping_dicio}',
            inline=False
        )
    else:
        embed.add_field(
            name='Ping Dicio:',
            value=f'{ping_dicio}ms',
            inline=False
        )
    embed.add_field(
        name='Ping Google:',
        value=f'{ping_google}ms',
        inline=False
    )
    await pong.edit(content='Pong!', embed=embed)


@bot.command(aliases=['lembrar', 'lembre'])
async def reminder(ctx, *, lembrar):
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >reminder' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    membro = ctx.author.id

    if 'em' in lembrar:
        base = lembrar.split(' em ')
    else:
        await ctx.send(
            'Oops, você digitou algo inválido, lembre-se:' +
            'a sintaxe do comando é `>lembrar {sobre} em {tempo}' +
            ' {unidade(segundos/minutos/horas)}`'
        )
        return
    sobre = base[0]
    base_tempo = str(base[1]).split(' ')
    try:
        tempo = float(base_tempo[0])
    except ValueError:
        await ctx.send(
            'Oops, você digitou algo inválido, lembre-se:' +
            'a sintaxe do comando é `>lembrar {sobre} em {tempo}' +
            ' {unidade(segundos/minutos/horas)}`'
        )
        return

    unidade = base_tempo[1]
    await ctx.send(f'Ok <@{membro}>, vou te lembrar sobre {lembrar}!')
    if unidade.startswith('segundo'):
        await asyncio.sleep(tempo)
        await ctx.send(f'Oi <@{membro}>, vim te lembrar sobre {sobre}!')
    elif unidade.startswith('minuto'):
        tempo = tempo*60
        await asyncio.sleep(tempo)
        await ctx.send(f'Oi <@{membro}>, vim te lembrar sobre {sobre}!')
    elif unidade.startswith('hora'):
        tempo = tempo*3600
        await asyncio.sleep(tempo)
        await ctx.send(f'Oi <@{membro}>, vim te lembrar sobre {sobre}!')
    else:
        await ctx.send(
            'Oops, você digitou algo inválido, lembre-se:' +
            'a sintaxe do comando é `>lembrar {sobre} em {tempo}' +
            ' {unidade(segundos/minutos/horas)}`'
        )


@bot.command()
async def uptime(ctx):
    global tempo_inicial
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >uptime' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    tempo_atual = utils.hora_atual()
    formato = '%H:%M:%S'

    uptime = (
        datetime.strptime(tempo_atual, formato) -
        datetime.strptime(tempo_inicial, formato)
    )

    if uptime.days < 0:
        uptime = datetime.timedelta(
            days=0,
            seconds=uptime.seconds,
            microseconds=uptime.microseconds
        )

    await ctx.send(f'estou online há {uptime}!')


@bot.command(aliases=['dado', 'rolar', 'dice'])
async def roll(ctx, valor):
    dado = valor.lower()
    dado = dado.replace('d', '')
    numero = randint(0, int(dado))
    await ctx.send(
        f':game_die: <@{ctx.author.id}> rolou um `d{dado}`' +
        f' e conseguiu um `{numero}`! :game_die:'
    )


@bot.command(
    aliases=[
        'xorx', 'sortear', 'sorteio',
        'escolher', 'choose', 'pick',
    ]
)
async def sort(ctx, *, lista):
    escolher = lista.split(',')

    escolhido = randint(0, (len(escolher) - 1))

    escolhido_final = escolher[escolhido]
    await ctx.send(
        f'<@{ctx.author.id}> eu escolho... `{escolhido_final.strip()}`!'
    )


@bot.command(aliases=['jp'])
async def jokenpo(ctx, *, elemento):
    elementos = ['pedra', 'papel', 'tesoura']

    counter = 0
    for item in elementos:
        if item in elemento:
            counter += 1

    if counter != 1:
        await ctx.send('por favor use um elemento valido :pensive:')
        return

    minha_escolha = elementos[randint(0, 2)]

    if elemento.startswith(minha_escolha):
        await ctx.send(f'escolhi `{minha_escolha}` e deu empate :handshake:')
        return

    elif minha_escolha == 'papel' and elemento.startswith('pedra'):
        await ctx.send(f'escolhi `{minha_escolha}` e ganhei :sunglasses:')
        return

    elif minha_escolha == 'pedra' and elemento.startswith('tesoura'):
        await ctx.send(f'escolhi `{minha_escolha}` e ganhei :sunglasses:')
        return

    elif minha_escolha == 'tesoura' and elemento.startswith('papel'):
        await ctx.send(f'escolhi `{minha_escolha}` e ganhei :sunglasses:')
        return

    elif(
        not elemento.startswith('pedra') and
        not elemento.startswith('papel') and
        not elemento.startswith('tesoura')
    ):
        await ctx.send(
            'ah :pensive: o elemento deve estar depois do comando' +
            ', tipo `>jokenpo pedra`'
        )
        return

    else:
        await ctx.send(f'escolhi `{minha_escolha}` e perdi :pensive:')
        return


@bot.command()
async def marselo(ctx):
    url = "https://youtu.be/dQw4w9WgXcQ"
    embed = discord.Embed(
        title='Verdade linda\n', url=url, colour=discord.Colour(0x349cff)
    )
    embed.add_field(name='Concordo', value='MUUUIIITOOO', inline=False)
    embed.set_footer(text="com o que disse")
    await ctx.send(embed=embed)


@bot.command(aliases=['clean', 'limpar', 'apagar'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade=1):
    print(
        f'{utils.hora_atual()}: {ctx.author.name} pediu >clear {quantidade}' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    if quantidade > 1000:
        quantidade = 1000
    elif quantidade < 0:
        quantidade = 1
    await ctx.channel.purge(
        limit=(quantidade+1),
        check=lambda msg: not msg.pinned
    )


@commands.has_permissions(kick_members=True)
@bot.command(aliases=['mutar', 'silenciar'])
async def mute(ctx, membro: discord.Member):
    for role in membro.roles:
        if role.name != '@everyone':
            try:
                await membro.remove_roles(role)
            except discord.Forbidden:
                await ctx.send(
                    f'{membro.name} não pode ser silenciado por ter um' +
                    ' cargo acima do meu.'
                )
                return

    silenciado = discord.utils.get(ctx.guild.roles, name='silenciado')
    await membro.add_roles(silenciado)
    await ctx.send(f'<@{membro.id}> foi silenciado.')
    print(f'{utils.hora_atual()}: {ctx.author.name} mutou {membro.name}')


@bot.command(aliases=['expulsar'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo=None):
    await membro.kick(reason=motivo)
    await ctx.send(f'{membro.mention} foi expulso do servidor.')
    print(f'{utils.hora_atual()}: {ctx.author.name} expulsou {membro.name}')


@bot.command(aliases=['banir'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo=None):
    await membro.ban(reason=motivo)
    await ctx.send(f'{membro.mention} foi banido do servidor.')
    await ctx.send(links.banido)
    print(f'{utils.hora_atual()}: {ctx.author.name} baniu {membro.name}')


@bot.command(aliases=['desbanir'])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, membro):
    lista_banidos = await ctx.guild.bans()
    nome, tag = membro.split('#')

    for banido in lista_banidos:
        usuario = banido.user
        if (usuario.name, usuario.discriminator) == (nome, tag):
            await ctx.guild.unban(usuario)
            await ctx.send(f'{usuario.mention} desbanido')
            await ctx.send(links.desbanido)
            print(
                f'{utils.hora_atual()}: {ctx.author.name}' +
                f' desbaniu {usuario.name}'
            )
            return


@bot.command()
async def cls(ctx):
    if ctx.author.id == tokens.eduardo_id:
        utils.clear()
        await ctx.message.delete()


@bot.command()
async def status(ctx, *, status):

    if ctx.author.id == tokens.eduardo_id:

        if status.startswith('padrao'):
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name='github.com/Eduardo-Barreto/Marselo-Bot/'
                )
            )

        if status.startswith('jogando'):
            name = status.replace('jogando ', '')
            await bot.change_presence(activity=discord.Game(name=name))

        if status.startswith('ouvindo'):
            name = status.replace('ouvindo ', '')
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=name
                )
            )

        if status.startswith('assistindo'):
            name = status.replace('assistindo ', '')
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=name
                )
            )

        utils.clear()
        print(f'Status alterado para "{status}"')
        await ctx.message.delete()


@bot.command()
async def atualizar(ctx):
    if ctx.author.id == tokens.eduardo_id:
        await ctx.message.delete()
        os.chdir('..')
        os.system('sudo rm -R Marselo-Bot')
        os.system(
            'git clone https://github.com/Eduardo-Barreto/Marselo-Bot.git'
        )
        os.system(
            'cp /home/pi/Desktop/tokens.py /home/pi/Desktop/Marselo-Bot'
        )
        os.chdir('Marselo-Bot')
        os.system('clear')
        os.system('python3 bot.py')
        quit()


bot.run(tokens.discord)
