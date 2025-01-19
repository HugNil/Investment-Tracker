import discord
from discord import app_commands
from db.database import get_sold_positions
import os

AUTHORIZED_CHANNEL_ID = int(os.getenv("AUTHORIZED_CHANNEL_ID", 0))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ACTIVE_POS", 0))


class SoldPositions(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avslutade",
                          description="Visa alla avslutade positioner.")
    async def avslutade(self, interaction: discord.Interaction):
        # Kontrollera om kommandot körs i den auktoriserade kanalen
        if interaction.channel_id != AUTHORIZED_CHANNEL_ID:
            await interaction.response.send_message(
                "Detta kommando kan endast användas i den auktoriserade kanalen.",  # noqa: E501
                ephemeral=True
            )
            return

        # Hämta avslutade positioner
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
            response = f"```{response}```"

            # Skicka resultatet till målkanalen
            target_channel = interaction.client.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(response)
                # Bekräfta för användaren att resultatet skickades
                await interaction.response.send_message(
                    "Avslutade positioner skickades till målkanalen.",
                    ephemeral=True
                )
            else:
                # Om målkanalen inte hittas
                await interaction.response.send_message(
                    "Målkanalen kunde inte hittas. Kontrollera kanalinställningarna.",  # noqa: E501
                    ephemeral=True
                )
        else:
            # Om inga avslutade positioner finns
            await interaction.response.send_message(
                "Inga avslutade positioner hittades.",
                ephemeral=True
            )
