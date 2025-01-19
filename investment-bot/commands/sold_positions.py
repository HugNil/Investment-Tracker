import discord
from discord import app_commands
from db.database import get_sold_positions


class SoldPositions(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avslutade",
                          description="Visa alla avslutade positioner.")
    async def avslutade(self, interaction: discord.Interaction):
        positions = get_sold_positions()
        if positions:
            total_result = 0  # Variabel för att summera resultatet

            # Skapa rubriken
            response = "Avslutade positioner:\n\n"
            response += f"{'ID':<5} | {'Aktie':<30} | {'GAV':<10} | {'Såld':<10} | {'Resultat':<10} | {'Köpt':<15} | {'Såld':<15}\n"  # noqa: E501
            response += f"{'-'*5} | {'-'*30} | {'-'*10} | {'-'*10} | {'-'*10} | {'-'*15} | {'-'*15}\n"  # noqa: E501

            for pos in positions:
                total_result += pos[9]
                response += f"{pos[0]:<5} | {pos[3]:<30} | {pos[4]:<10.2f} | {pos[5]:<10.2f} | {pos[9]:<9.2f}% | {pos[1]:<15} | {pos[2]:<15}\n"  # noqa: E501

            # Lägg till totalen i meddelandet
            response += f"\nTotalt resultat: {total_result:.2f}%"
            await interaction.response.send_message(f"```{response}```")
        else:
            await interaction.response.send_message(
                "Inga avslutade positioner hittades.")
