import discord
from discord import app_commands


async def aktie_autocomplete(interaction: discord.Interaction, current: str):
    aktier = [
        "Marathon Digital",
        "Tesla",
        "Apple",
        "Microsoft",
        "Cipher Mining"
        ]
    return [app_commands.Choice(name=aktie, value=aktie)
            for aktie in aktier if current.lower() in aktie.lower()]


async def risknivå_autocomplete(interaction: discord.Interaction,
                                current: str):
    nivaer = ["High", "Medium", "Low"]
    return [app_commands.Choice(name=niva, value=niva)
            for niva in nivaer if current.lower() in niva.lower()]
