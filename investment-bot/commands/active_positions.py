import discord
from discord import app_commands
from db.database import get_active_positions
from dotenv import load_dotenv
import os

load_dotenv()
AUTHORIZED_CHANNEL_ID = int(os.getenv("AUTHORIZED_CHANNEL_ID", 0))
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ACTIVE_POS", 0))


class ActivePositions(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aktiva",
                          description="Visa alla aktiva positioner.")
    async def aktiva(self, interaction: discord.Interaction):
        # Kontrollera om kommandot körs i den auktoriserade kanalen
        if interaction.channel_id != AUTHORIZED_CHANNEL_ID:
            await interaction.response.send_message(
                "Detta kommando kan endast användas i den auktoriserade kanalen.",  # noqa: E501
                ephemeral=True
            )
            return

        # Hämta aktiva positioner
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

            # Skicka resultatet till målkanalen
            target_channel = interaction.client.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(response)
                # Bekräfta för användaren att resultatet skickades
                await interaction.response.send_message(
                    "Aktiva positioner skickades till målkanalen.",
                    ephemeral=True
                )
            else:
                # Om målkanalen inte hittas
                await interaction.response.send_message(
                    "Målkanalen kunde inte hittas. Kontrollera kanalinställningarna.",  # noqa: E501
                    ephemeral=True
                )
        else:
            # Om inga positioner finns
            await interaction.response.send_message(
                "Inga aktiva positioner just nu.",
                ephemeral=True
            )
