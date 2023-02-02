# Importerer bibliotekene vi trenger
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from collections import deque

# Setter opp intents og oppretter en bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

# Når bot-en er klar, skriver vi ut en melding i terminalen
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


# is_vaffel_orakel forteller om vaffelstekingen er i gang eller ikke
is_vaffel_orakel = False

# q er køen
q = deque()


def bruker_er_orakel(ctx):
    """Sjekker om brukeren har rollen 'Orakel'."""

    # Henter rollen 'Orakel' fra serveren
    role = discord.utils.get(ctx.guild.roles, name='Orakel')

    # Sjekker om brukeren har rollen. Returnerer resultatet
    return (role in ctx.author.roles)


""" KOMMANDOER FOR ORAKLER """

@bot.command()
@commands.check(bruker_er_orakel)                 # Sørger for at brukeren har rollen "Orakel"
@commands.check(lambda _: not is_vaffel_orakel)   # Sørger for at vaffelstekingen ikke allerede er i gang
async def vaffelstart(ctx):
    """Åpner for bestilling av vaffler."""

    # Tømmer køen hvis det er noen i den fra forrige gang
    if len(q) > 0:
        q.clear()
        
    # Setter is_vaffel_orakel til True
    global is_vaffel_orakel
    is_vaffel_orakel = True

    await ctx.send(
        "Hei allesammen! Vaffelstekingen er nå satt igang!\n\n"
        "Skriv `$vaffel` for å bestille en vaffel, og `$kø` for å se hvor mange som er i køen."
        "\n\n@here"
    )


@bot.command()
@commands.check(bruker_er_orakel)             # Sørger for at brukeren har rollen "Orakel"
@commands.check(lambda _: is_vaffel_orakel)   # Sørger for at vaffelstekingen er i gang
async def vaffelstopp(ctx):
    """Stenger bestilling av vaffler. Kommandoen 'stekt' kan fortsatt brukes."""
    
    # Skriver ut en melding om det fremdeles er noen i køen
    if (antall := len(q)) > 0:
        await ctx.reply(
            f"Merk: det er fremdeles {antall} {'person' if antall == 1 else 'personer'} i køen. "
            "Du kan fortsatt bruke `$stekt`."
        )

    # Setter is_vaffel_orakel til False
    global is_vaffel_orakel
    is_vaffel_orakel = False

    await ctx.send("Vaffelstekingen er nå stoppet. Takk for i dag!")


@bot.command()
@commands.check(bruker_er_orakel)   # Sørger for at brukeren har rollen "Orakel"
async def stekt(ctx, *, arg = '0'):
    """Brukes når nye vaffler er stekt. Argumentet er antall vaffler som har blitt stekt siden sist."""

    # Sjekker om brukeren har gitt et positivt heltall som argument
    if (not arg.isdecimal()) or (int(arg) < 1):
        await ctx.reply("Bruk et positivt heltall som argument. For eksempel: `$stekt 2`.")
        return

    # Setter antall til det minste av antall vaffler stekt og antall personer i køen
    antall = min(int(arg), len(q))

    # Sender melding til de 'antall' neste personene i køen
    for _ in range(antall):
        # popleft() henter personens Discord ID og fjerner personen fra køen
        await ctx.send(f"<@{q.popleft()}> din vaffel er klar!")

    await ctx.reply(
        f"{antall} {'person' if antall == 1 else 'personer'} har fått melding og er fjernet fra køen. "
        f"Det er nå {len(q)} {'person' if len(q) == 1 else 'personer'} i køen."
    )


""" KOMMANDOER FOR ALLE """

@bot.command()
@commands.check(lambda _: is_vaffel_orakel)   # Sørger for at vaffelstekingen er i gang
async def vaffel(ctx):
    """Bestiller en vaffel."""

    # Sjekker om personen som bestiller allerede er i køen
    if ctx.author.id in q:
        await ctx.reply("Du er allerede i køen.")
        return

    # Legger til personens Discord ID i køen
    q.append(ctx.author.id)

    await ctx.reply(f"Takk for bestillingen! Du er nummer {len(q)} i køen.")


@bot.command()
async def kø(ctx):
    """Viser hvilken plass brukeren har i køen. Viser antall personer som er i køen ellers."""
    
    # Sjekker om personen er i køen
    if ctx.author.id in q:
        # index() finner personens plass i køen
        await ctx.reply(f"Du er nummer {q.index(ctx.author.id) + 1} i køen.")
    else:
        # len() finner antall personer i køen
        antall = len(q)
        await ctx.reply(f"Det er {antall} {'person' if antall == 1 else 'personer'} i køen.")


# Henter token fra .env-filen
load_dotenv()

# Starter bot-en
bot.run(os.environ.get("TOKEN"))
