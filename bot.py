import discord
from discord.ext import commands
from discord.utils import get
import time
import asyncio

import tokens
import utils
import bot_links as links

last_ping = 200
msg_cargos_pronomes = 791808051983155200


def check_anti_log(mensagem):
    for comando in bot.commands:
        if str(comando) in mensagem:
            return False
        for alias in comando.aliases:
            if str(alias) in mensagem:
                return False
    return True


intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix='>', case_insensitive=True,
    intents=intents, help_command=None
)


@bot.event
async def on_ready():
    utils.clear()
    print(f'estou online, loguei em {bot.user}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='github.com/Eduardo-Barreto/Marselo-Bot/'
        )
    )


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


@bot.command(aliases=['ajuda'])
async def help(ctx, *, argumento=''):
    if len(argumento) > 0:
        url = f'{links.readme}#{argumento}'
        await ctx.send(f'Ajuda para o comando {argumento}: {url}')
    else:
        await ctx.send(
            'Você pode encontrar todos os comandos em:' +
            f' {links.readme}'
        )


@bot.command(aliases=['dicionario', 'dc', 'dict'])
async def dicio(ctx, palavra):
    print(
        f'{ctx.author.name} pediu >ping' +
        f' no server {ctx.guild}, no canal {ctx.channel}'
    )
    await ctx.send('Opa, é pra já! Saindo no capricho')
    await ctx.send(embed=utils.dicionario(palavra.lower()))


@bot.command()
async def ping(ctx):
    print(f'{ctx.author.name} pediu >ping' +
          f' no server {ctx.guild}, no canal {ctx.channel}')
    global last_ping
    pong = await ctx.send('pong?')
    init_time = int(round(time.time() * 1000))
    await pong.edit(content='Pong!')
    ping = int(round(time.time() * 1000)) - init_time

    if ping < last_ping:
        await ctx.send(f'demorei {ping}ms, mais rapido que da ultima vez :)')
    elif ping > last_ping:
        await ctx.send(f'demorei {ping}ms, mais lento que da ultima vez :/')
    else:
        await ctx.send(f'demorei {ping}ms, o mesmo que da ultima vez!')
    last_ping = ping
    return


@bot.command(aliases=['lembrar', 'lembre'])
async def reminder(ctx, *, lembrar):
    print(
        f'{ctx.author.name} pediu >lembrar' +
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


@bot.command(aliases=['limpar', 'apagar'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade=1):
    print(
        f'{ctx.author.name} pediu >clear {quantidade+1}' +
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


@bot.command(aliases=['expulsar'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo=None):
    await membro.kick(reason=motivo)
    await ctx.send(f'{membro.mention} foi expulso do servidor.')
    print(f'{ctx.author.name} expulsou {membro.name}')


@bot.command(aliases=['banir'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo=None):
    await membro.ban(reason=motivo)
    await ctx.send(f'{membro.mention} foi banido do servidor.')
    await ctx.send(links.banido)
    print(f'{ctx.author.name} baniu {membro.name}')


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
            print(f'{ctx.author.name} desbaniu {usuario.name}')
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
async def teste(ctx):
    log_deleted = get(ctx.guild.text_channels, name='log-deleted')
    if log_deleted is None:
        print('canal nao encontrado')


bot.run(tokens.discord)
