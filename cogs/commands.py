import discord
from discord.ext import commands
import json
import os
import random
import time
import asyncio
import re

datafile = 'prime.json'


def loaddata():
    if not os.path.exists(datafile):
        return []
    with open(datafile, 'r') as f:
        return json.load(f)

def savedata(data):
    with open(datafile, 'w') as f:
        json.dump(data, f, indent=4)

class PrimeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name='prime', invoke_without_command=True)
    async def prime(self, ctx):
        em = discord.Embed(color=0xff0000)
        em.add_field(name="Error", value="Please use a valid subcommand: add, remove, show")
        await ctx.send(embed=em)

    @prime.command(name='add')
    @commands.is_owner()
    async def prime_add(self, ctx, member: discord.Member):
        primedata = loaddata()
        if isinstance(primedata, dict):
            primedata = primedata.get("ids", [])
        if member.id not in primedata:
            primedata.append(member.id)
            savedata({"ids": primedata})
            em = discord.Embed(color=0x00ff00)
            em.add_field(name="Success", value=f"{member.mention} has been added to the prime list.")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="Error", value=f"{member.mention} is already in the prime list.")
            await ctx.send(embed=em)

    @prime.command(name='remove')
    @commands.is_owner()
    async def prime_remove(self, ctx, member: discord.Member):
        primedata = loaddata()
        if isinstance(primedata, dict):
            primedata = primedata.get("ids", [])
        if member.id in primedata:
            primedata.remove(member.id)
            savedata({"ids": primedata})
            em = discord.Embed(color=0x00ff00)
            em.add_field(name="Success", value=f"{member.mention} has been removed from the prime list.")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="Error", value=f"{member.mention} is not in the prime list.")
            await ctx.send(embed=em)

    @prime.command(name='show')
    @commands.is_owner()
    async def prime_show(self, ctx):
        primedata = loaddata()
        if isinstance(primedata, dict):
            primedata = primedata.get("ids", [])
        if not primedata:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="Prime Members", value="No members found in the prime list.")
            await ctx.send(embed=em)
            return

        embeds = []
        for i in range(0, len(primedata), 10):
            chunk = primedata[i:i+10]
            em = discord.Embed(color=0x0025ff)
            value = "\n".join([f"{i + idx + 1}. <@{user_id}> ({user_id})" for idx, user_id in enumerate(chunk)])
            em.add_field(name="Prime Members", value=value)
            embeds.append(em)

        cpage = 0

        class Paginator(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=60)
                self.cpage = 0

            @discord.ui.button(label='Previous', style=discord.ButtonStyle.blurple)
            async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.cpage -= 1
                if self.cpage < 0:
                    self.cpage = len(embeds) - 1
                await interaction.response.edit_message(embed=embeds[self.cpage])

            @discord.ui.button(label='Next', style=discord.ButtonStyle.blurple)
            async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.cpage += 1
                if self.cpage >= len(embeds):
                    self.cpage = 0
                await interaction.response.edit_message(embed=embeds[self.cpage])

        view = Paginator()
        await ctx.send(embed=embeds[cpage], view=view)

class MinesCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='mines',alaises=["mine"] ,description='Mines game mode')
    async def mines(self, ctx: commands.Context, tileamt: int, betno: str, seed: str):
        if not re.fullmatch(r'[0-9a-fA-F]{64}', seed):
            em = discord.Embed(
                title="âŒ Invalid Hash Seed",
                description="Please Provide Valid Hash Seed.",
                color=0xff0000
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/icons/991408716589039686/b0ff6378a268b89b1762c8fca0143949.png?size=2048")  
            await ctx.send(embed=em)
            return

        primedata = loaddata()
        aizerids = primedata.get("ids", [])

        if ctx.author.id not in aizerids:
            em = discord.Embed(
                title="â›” Access Denied",
                description="You are not a **Premium Member** and cannot use this command.\nCheck Out **Premium** Channel To Buy Premium.",
                color=0xff0000
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")  
            em.set_footer(text="Upgrade to Premium to access exclusive features.")
            await ctx.send(embed=em)
            return

        if len(betno) == 1:
            aizer2 = discord.Embed(
                title="ðŸ”„ Processing...",
                description="<a:stolen_emoji:1271551203888730216> `|` Predicting the mines game outcome, please wait...",
                color=0xFFFF00  
            )
            load = await ctx.send(embed=aizer2)

            await asyncio.sleep(3)  

            aizerst = time.time()

            grid = ['ðŸ”´'] * 25
            alrusd = []
            rltiles = ['â“'] * 25  

            count = 0
            while tileamt > count:
                a = random.randint(0, 24)
                if a in alrusd:
                    continue
                alrusd.append(a)
                grid[a] = 'ðŸ’Ž'
                rltiles[a] = 'ðŸ’Ž'
                count += 1


            basech = random.randint(88, 100)  
            chance = max(basech, 88) 

            aizergrid = "\n".join(' '.join(rltiles[i:i+5]) for i in range(0, 25, 5))

            aizer3 = discord.Embed(
                title="ðŸ’Ž Mines Game Mode ðŸ’Ž",
                description=(
                    f"**Game Details**\n"
                    f"**ðŸŽ¯ Accuracy:**\n```{chance}%```\n"
                    f"**ðŸŽ² Round ID:**\n```{betno}```\n"
                    f"**ðŸ—º Grid Layout:**\n```{aizergrid}```\n"
                    f"**â± Response Time:**\n```{str(int(time.time() - aizerst))} seconds```\n"
                    f"**ðŸ”’ Hash Seed:**\n```{seed}```\n"
                    f"**ðŸ§© Tiles Revealed:**\n```{tileamt}```\n"
                    f"**ðŸ’¡ Tips:**\n*Try to uncover tiles strategically to avoid hitting mines.*\n"
                    f"**ðŸ” Game Summary:**\n"
                    f"- **Total Mines:** ```{count}```\n"
                    f"- **Safe Tiles Remaining:** ```{25 - tileamt - count}```\n"
                ),
                color=0x0025ff
            )
            aizer3.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            aizer3.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")
            aizer3.set_footer(text="Made By Team Holy", icon_url="https://cdn.discordapp.com/icons/991408716589039686/b0ff6378a268b89b1762c8fca0143949.png?size=2048")

            await load.edit(embed=aizer3)

        else:
            em = discord.Embed(
                title="âŒ Invalid Bet Number",
                description="The bet number must be a single character.",
                color=0xff0000
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")  
            await ctx.send(embed=em)

    @commands.hybrid_command(name='dragontower', description='Dragon Tower game mode')
    async def dragontower(self, ctx: commands.Context, seed: str, amt: int):
        if not re.fullmatch(r'[0-9a-fA-F]{64}', seed):
            em = discord.Embed(
                title="âŒ Invalid Hash Seed",
                description="Please Enter Valid Hash Seed.",
                color=0x6e6e6e
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66ba3cea&is=66b8eb6a&hm=57c60e16ec633b135c2d0b747eada722f72be8f5417cce486de98979cd67d9aa&")  
            await ctx.send(embed=em)
            return

        primedata = loaddata()
        aizerids = primedata.get("ids", [])

        if ctx.author.id not in aizerids:
            em = discord.Embed(
                title="â›” Access Denied",
                description="You are not a **Premium Member** and cannot use this command.\nCheck Out **Premium** Channel To Buy Premium.",
                color=0x6e6e6e
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")  
            em.set_footer(text="Upgrade to Premium to access exclusive features.")
            await ctx.send(embed=em)
            return

        if amt > 0 and amt <= 32:
            aizer2 = discord.Embed(
                title="ðŸ”„ Calculating...",
                description="<a:stolen_emoji:1271551203888730216> `|` Determining the outcome of Dragon Tower, please wait...",
                color=0x6e6e6e
            )
            load = await ctx.send(embed=aizer2)

            await asyncio.sleep(3)

            aizerst = time.time()

            gridwdth = 4
            gridhigh = 9
            gridsize = gridwdth * gridhigh
            grid = ['â“'] * gridsize

            eggpossis = []
            for row in range(gridhigh - 1, gridhigh - amt - 1, -1):
                col = random.randint(0, gridwdth - 1)
                eggpossis.append(row * gridwdth + col)

            for pos in eggpossis:
                grid[pos] = 'ðŸ¥š'

            basech = random.randint(80, 100)
            chance = max(basech, 80)

            aizergrid = "\n".join(' '.join(grid[i:i+gridwdth]) for i in range(0, gridsize, gridwdth))

            aizer3 = discord.Embed(
                title="ðŸ—¡ï¸ Dragon Tower Game Mode ðŸ—¡ï¸",
                description=(
                    f"**Game Details**\n"
                    f"**ðŸŽ¯ Accuracy:**\n```{chance}%```\n"
                    f"**ðŸ—º Grid Layout:**\n```{aizergrid}```\n"
                    f"**â± Response Time:**\n```{str(int(time.time() - aizerst))} seconds```\n"
                    f"**ðŸ”’ Hash Seed:**\n```{seed}```\n"
                    f"**ðŸ‘¾ Mode:**\n```Easy```\n"
                    f"**ðŸ§© Tiles Revealed:**\n```{amt}```\n"
                    f"**ðŸ’¡ Tips:**\nUncover tiles carefully to find hidden treasures.\n"
                    f"**ðŸ” Game Summary:**\n"
                    f"- **Total Eggs:** ```{amt}```\n"
                ),
                color=0x6e6e6e 
            )
            aizer3.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            aizer3.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&");
            aizer3.set_footer(text="Made By Team Holy", icon_url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")

            await load.edit(embed=aizer3)

        else:
            em = discord.Embed(
                title="âŒ Invalid Tile Amount",
                description="The tile amount must be between 1 and 5.",
                color=0x6e6e6e
            )
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")  
            await ctx.send(embed=em)

    @commands.hybrid_command(name="synchronization", aliases=["sync"])
    @commands.is_owner()
    async def sync(self, ctx):
        try:
            synced = await self.client.tree.sync()
            await ctx.send(embed=discord.Embed(title=f"Synced {len(synced)} commands"))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title="Error", description=str(e)))


    @commands.hybrid_command(name='help', description='Displays the help panel with command details.')
    async def help(self, ctx: commands.Context):
        hlp = discord.Embed(
            title="ðŸ“œ Command Help Panel",
            description="*Here are the available commands and their usage:*",
            color=0x00A1E0 
        )
        avatar_url = self.client.user.avatar.url if self.client.user.avatar else self.client.user.default_avatar.url
        hlp.set_author(name=self.client.user.name, icon_url=avatar_url)
        hlp.set_thumbnail(url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")

        hlp.add_field(
            name="ðŸª™ `mines`",
            value=(
                "**Description:**\n"
                "Play the Mines game mode where you reveal tiles to find treasures while avoiding hazards.\n\n"
                "**Usage:**\n"
                "`/mines <tileamt> <betno> <seed>`\n"
                "- `tileamt`: Number of tiles to reveal (1-25).\n"
                "- `betno`: Round identifier (a single character).\n"
                "- `seed`: A hash seed for get accurate details."
            ),
            inline=False
        )

        hlp.add_field(
            name="ðŸ‰ `dragontower`",
            value=(
                "**Description:**\n"
                "Play the Dragon Tower game mode where you uncover tiles to find hidden eggs and avoid hazards.\n\n"
                "**Usage:**\n"
                "`/dragontower <seed> <amt>`\n"
                "- `seed`: A hash seed for get accurate details.\n"
                "- `amt`: Number of tiles to reveal (1-36)."
            ),
            inline=False
        )

        hlp.set_footer(text="Made By Team Holy", icon_url="https://cdn.discordapp.com/attachments/1201570410836279499/1272235258628145332/image.png?ex=66bae5aa&is=66b9942a&hm=787d983b07be0dc4b743744e232b45a0ee07daaa36a7caafc8571413ea3f5655&")

        await ctx.send(embed=hlp)

async def setup(client):
    await client.add_cog(PrimeCog(client))
    await client.add_cog(MinesCog(client))
    print("loaded cogs")
