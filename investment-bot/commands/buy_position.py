import discord
from discord import app_commands
from db.database import add_position
from commands.autocomplete import aktie_autocomplete, risknivå_autocomplete
import os


AUTHORIZED_CHANNEL_ID = int(os.getenv("AUTHORIZED_CHANNEL_ID", 0))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ACTIVE_POS", 0))


class BuyPosition(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="köp", description="Registrera en köp-signal.")
    @app_commands.describe(
        aktie="Namnet på aktien",
        gav="Genomsnittligt anskaffningsvärde",
        stoploss="Stop-loss-värde (valfritt)",
        risknivå="Risknivå (valfritt)"
    )
    @app_commands.autocomplete(aktie=aktie_autocomplete,
                               risknivå=risknivå_autocomplete)
    async def köp(
        self,
        interaction: discord.Interaction,
        aktie: str,
        gav: float,
        stoploss: float = None,
        risknivå: str = None,
    ):
        # Kontrollera om kommandot körs i den auktoriserade kanalen
        if interaction.channel_id != AUTHORIZED_CHANNEL_ID:
            await interaction.response.send_message(
                "Detta kommando kan endast användas i den auktoriserade kanalen.",  # noqa: E501
                ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)

        try:
            # Registrera positionen i databasen
            add_position(aktie, gav, stoploss, risknivå)

            # Skicka meddelande till målkanalen
            target_channel = interaction.client.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(
                    f"**Köper**:\n"
                    f"- **Aktie:** {aktie}\n"
                    f"- **GAV:** {gav:.2f}\n"
                    f"- **Stop-loss:** {stoploss or 'Ej angivet'}\n"
                    f"- **Risknivå:** {risknivå or 'Ej angivet'}"
                )

            # Avsluta kommandot utan synligt svar
            await interaction.followup.send(
                "Köp-signalen har registrerats.",
                ephemeral=True,
            )
        except Exception as e:
            # Hantera fel och meddela endast användaren
            await interaction.followup.send(f"Fel vid registrering: {e}",
                                            ephemeral=True)
