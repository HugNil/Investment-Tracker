import discord
from discord import app_commands
import os

# Hämta auktoriserade kanal-ID från miljövariabler
AUTHORIZED_CHANNEL_ID = int(os.getenv("AUTHORIZED_CHANNEL_ID", 0))


async def aktie_autocomplete(interaction: discord.Interaction, current: str):
    # Kontrollera om kommandot används i den auktoriserade kanalen
    if interaction.channel_id != AUTHORIZED_CHANNEL_ID:
        return []  # Returnera en tom lista för att stänga av autocomplete

    # Lista över tillgängliga aktier
    aktier = ["Marathon Digital", "Cleanspark", "Bitfarms", "Riot Platforms", "Cipher Mining", "Ethereum", "Solana", "XRP", "Arbitrum"]  # noqa: E501
    return [
        app_commands.Choice(name=aktie, value=aktie)
        for aktie in aktier if current.lower() in aktie.lower()
    ]


async def risknivå_autocomplete(interaction: discord.Interaction, current: str):  # noqa: E501
    # Kontrollera om kommandot används i den auktoriserade kanalen
    if interaction.channel_id != AUTHORIZED_CHANNEL_ID:
        return []  # Returnera en tom lista för att stänga av autocomplete

    # Lista över tillgängliga risknivåer
    nivaer = ["High", "Medium", "Low"]
    return [
        app_commands.Choice(name=niva, value=niva)
        for niva in nivaer if current.lower() in niva.lower()
    ]
