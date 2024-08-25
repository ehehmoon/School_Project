from openai import OpenAI
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
from pytz import timezone

client = OpenAI(api_key = 'ur api')

class GPT(commands.Cog):
    """GPT commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gpt')
    async def gpt(self, ctx, *, prompt):
        embed = discord.Embed(title='GPT Result <a:spinner:1140592462902079498>', description='waiting...', color=0x0067ff)
        msg = await ctx.send(embed=embed, reference=ctx.message)
        
        try:
            response = await send_gpt(prompt)
            if response:
                embed = discord.Embed(title='GPT Result <a:verify_eh:948526125448065075>', description=response, color=0x0067ff)
            else:
                embed = discord.Embed(title='ERROR 404', description='<a:no:948526289407602701> 지금 gpt api가 먹통인거 같아요. 나중에 다시 시도해주세요.', color=0xff0000)
        except Exception as e:
            print(f"Error: {e}")
            embed = discord.Embed(title='ERROR 404', description='<a:no:948526289407602701> 지금 gpt api가 먹통인거 같아요. 나중에 다시 시도해주세요.', color=0xff0000)
        File = open('존재했던과거를보아라.txt', 'w')
        File.truncate(0)
        File.write(f'저는 이전에 "{prompt}"라 명령 받아서 저는 "{response}"라 대답했습니다.')
        File = open("log.txt", "a")
        File.write(f'{ctx.author.name}({ctx.author.id}) - {prompt} / GPT - {response} : {datetime.now(timezone("Asia/Seoul")).strftime("%F %H시 %M분")}\n')
        File.close()
        await msg.edit(embed=embed)


async def send_gpt(prompt):
    File = open('past.txt', 'r')
    File = File.read()
    response = client.chat.completions.create(
        model = 'gpt-4o',
        response_format = {'type' : 'text'},
        messages= [
            {'role' : 'user', 'content' : prompt},
            {'role' : 'system', 'content' : File},
            {'role' : 'assistant', 'content' : '사용자의 언어에 맞춰서 대답하시오. you may use english.'},
        ]
    )
    response = response.choices[0].message.content
    return response

def setup(bot):
    bot.add_cog(GPT(bot))
