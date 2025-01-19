import discord
from discord import app_commands
from db.database import add_position
from commands.autocomplete import aktie_autocomplete, risknivå_autocomplete


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
    async def köp(self, interaction: discord.Interaction,
                  aktie: str, gav: float,
                  stoploss: float = None, risknivå: str = None):
        try:
            add_position(aktie, gav, stoploss, risknivå)
            await interaction.response.send_message(
                f"Köp registrerat för '{aktie}' med GAV {gav}, stop-loss \
                    {stoploss or 'Ej angivet'}, risknivå \
                        {risknivå or 'Ej angivet'}."
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Fel vid registrering: {e}", ephemeral=True)
