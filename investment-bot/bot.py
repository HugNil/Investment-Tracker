import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Ladda miljövariabler från .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


class InvestmentBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Lägg till alla kommandon från separata filer
        from commands.sold_positions import SoldPositions
        from commands.active_positions import ActivePositions
        from commands.buy_position import BuyPosition
        from commands.sell_position import SellPosition

        await self.add_cog(SoldPositions(self))
        await self.add_cog(ActivePositions(self))
        await self.add_cog(BuyPosition(self))
        await self.add_cog(SellPosition(self))
        await self.tree.sync()


# Starta boten
if __name__ == "__main__":
    bot = InvestmentBot()
    bot.run(TOKEN)
