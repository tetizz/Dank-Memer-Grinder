import re

from discord.ext import commands

class Autobuy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.price_message = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild and self.bot.state:
            for embed in message.embeds:
                embed = embed.to_dict()

                # Buy lifesavers
                try:
                    if (
                        embed["title"] == "Your lifesaver protected you!"
                        and self.bot.config_dict["autobuy"]["lifesavers"]["state"]
                    ):
                        remaining = int(
                            re.search(
                                r"have (.*?)x Life Saver",
                                message.components[0].children[0].label,
                            ).group(1)
                        )
                        required = int(
                            self.bot.config_dict["autobuy"]["lifesavers"]["amount"]
                        )
                        if remaining < required and self.price_message is not None:
                            price = await self.get_price_from_message(self.price_message)
                            if price is not None:
                                channel = await message.author.create_dm()
                                quantity = required - remaining
                                amount = str(quantity * price)
                                await self.bot.send("withdraw", channel, amount=amount)
                                await self.bot.sub_send(
                                    "shop",
                                    "buy",
                                    channel,
                                    item="Life Saver",
                                    quantity=str(quantity),
                                )
                                self.bot.log(
                                    f"Bought {quantity} Lifesavers",
                                    "yellow",
                                )
                            return
                except KeyError:
                    pass

    async def set_price_message(self, message):
        self.price_message = message

    async def get_price_from_message(self, message):
        content = message.content
        price_match = re.search(r"/shop buy for (\d+)", content)
        if price_match:
            return int(price_match.group(1))
        return None
            # Shovel
            try:
                if (
                    "You don't have a shovel, you need to go buy one."
                    in embed["description"]
                    and self.bot.config_dict["autobuy"]["shovel"]
                ):
                    await self.bot.send("withdraw", amount="35k")
                    await self.bot.sub_send("shop", "buy", item="Shovel", quantity="1")
                    self.bot.log(
                        f"Bought Shovel",
                        "yellow",
                    )
            except KeyError:
                pass

            # Fishing pole
            try:
                if (
                    "You don't have a fishing pole, you need to go buy one"
                    in embed["description"]
                    and self.bot.config_dict["autobuy"]["fishing"]
                ):
                    await self.bot.send("withdraw", amount="35k")
                    await self.bot.sub_send(
                        "shop", "buy", item="Fishing Pole", quantity="1"
                    )
                    self.bot.log(
                        f"Bought Shovel",
                        "yellow",
                    )
            except KeyError:
                pass

            # Hunting rifle
            try:
                if (
                    "You don't have a hunting rifle, you need to go buy one."
                    in embed["description"]
                    and self.bot.config_dict["autobuy"]["rifle"]
                ):
                    await self.bot.send("withdraw", amount="35k")
                    await self.bot.sub_send(
                        "shop", "buy", item="Hunting Rifle", quantity="1"
                    )
                    self.bot.log(
                        f"Bought Shovel",
                        "yellow",
                    )
            except KeyError:
                pass


async def setup(bot):
    await bot.add_cog(Autobuy(bot))
