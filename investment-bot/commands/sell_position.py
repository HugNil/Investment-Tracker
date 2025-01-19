import discord
from discord import app_commands
from db.database import sell_position
import os


AUTHORIZED_CHANNEL_ID = int(os.getenv("AUTHORIZED_CHANNEL_ID", 0))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ACTIVE_POS", 0))


class SellPosition(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sälj",
                          description="Markera en position som såld.")
    @app_commands.describe(
        id="ID för positionen som ska säljas",
        pris="Säljpriset"
    )
    async def sälj(self, interaction: discord.Interaction,
                   id: int, pris: float):
        # Kontrollera om kommandot körs i den auktoriserade kanalen
        if interaction.channel_id != AUTHORIZED_CHANNEL_ID:
            await interaction.response.send_message(
                "Detta kommando kan endast användas i den auktoriserade kanalen.",  # noqa: E501
                ephemeral=True
            )
            return
        try:
            aktie, resultat = sell_position(id, price=pris)
            if aktie:
                # Skicka bekräftelse till användaren
                await interaction.response.send_message("Sälj-signalen registrerad")  # noqa: E501

                # Skicka resultatet till målkanalen
                target_channel = interaction.client.get_channel(TARGET_CHANNEL_ID)  # noqa: E501
                if target_channel:
                    await target_channel.send(
                        f"Position såld:\n"
                        f"- **Aktie:** {aktie}\n"
                        f"- **Resultat:** {resultat:.2f}%\n"
                        f"- **Säljpris:** {pris:.2f}"
                    )
                else:
                    # Om målkanalen inte hittas
                    await interaction.followup.send(
                        "Sälj-signalen registrerad, men målkanalen kunde inte hittas.",  # noqa: E501
                        ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    "Ingen aktiv position hittades med det ID:t.",
                    ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Fel vid säljning: {e}", ephemeral=True)
