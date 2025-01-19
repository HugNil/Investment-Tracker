import discord
from discord import app_commands
from db.database import sell_position


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
        try:
            aktie, resultat = sell_position(id, price=pris)
            if aktie:
                await interaction.response.send_message(
                    f"Sålde {aktie} med resultat {resultat:.2f}%.")
            else:
                await interaction.response.send_message(
                    "Ingen aktiv position hittades med det ID:t.",
                    ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"Fel vid säljning: {e}", ephemeral=True)
