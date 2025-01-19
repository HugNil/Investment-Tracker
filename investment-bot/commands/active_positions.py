import discord
from discord import app_commands
from db.database import get_active_positions


class ActivePositions(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aktiva",
                          description="Visa alla aktiva positioner.")
    async def aktiva(self, interaction: discord.Interaction):
        positions = get_active_positions()
        if positions:
            # Skapa rubriken med monospace-format
            response = "```"  # Starta kodblock
            response += "Aktiva positioner:\n\n"
            response += f"{'ID':<5} | {'Aktie':<30} | {'GAV':<10} | {'Stop-loss':<10} | {'Risknivå':<10} | {'Köpt':<15}\n"  # noqa: E501
            response += f"{'-'*5} | {'-'*30} | {'-'*10} | {'-'*10} | {'-'*10} | {'-'*15}\n"  # noqa: E501

            for pos in positions:
                response += f"{pos[0]:<5} | {pos[3]:<30} | {pos[4]:<10.2f} | {pos[6] or 'Ej angivet':<10} | {pos[7] or 'Ej angivet':<10} | {pos[1]:<15}\n"  # noqa: E501

            response += "```"  # Avsluta kodblock
            await interaction.response.send_message(response)
        else:
            await interaction.response.send_message(
                "Inga aktiva positioner just nu.")
