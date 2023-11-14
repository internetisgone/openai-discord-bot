import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()
openai_client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

PROXY = None
# PROXY = "http://127.0.0.1:1087"
SLASH_COMMAND_NAME = "kkb"
SHORTHAND_COMMAND_PREFIX = "%"
DEFAULT_MODEL = "4"
CHAR_LIMIT_DISCORD = 2000         # max chars in a discord message

models = { 
    "4": "gpt-4",
    "4-vision": "gpt-4-vision-preview",
    "4-turbo": "gpt-4-1106-preview",
    "3.5-turbo": "gpt-3.5-turbo", 
    "davinci-003": "text-davinci-003"
    }

async def get_response_openai(model, prompt, img_url):
    try: 
        # vision model
        if model == "4-vision":
            if img_url == None:
                return "img url is required to use gpt-4-vision"
            
            response = openai_client.chat.completions.create(
                model = models["4-vision"],
                messages = [ 
                    {
                        "role": "user", 
                        "content": 
                        [
                            { "type": "text", "text": prompt },
                            { "type": "image_url", "image_url": img_url}
                        ]
                    } 
                ],
                max_tokens = 600,
            )
            print(response)
            return response.choices[0].message.content
    
        # legacy completion models 
        elif model == "davinci-003":
            response = openai_client.completions.create(
                model = models[model],
                prompt = prompt,
                temperature = 0.9,
                max_tokens = 2000
            )
            print(response)
            return response.choices[0].text

        # current models (4 and 3.5)
        else:
            response = openai_client.chat.completions.create(
                model = models[model],
                messages = [ 
                    {
                        "role": "user", 
                        "content": 
                        [
                            { "type": "text", "text": prompt },
                        ]
                    } 
                ],
            )
            print(response)
            return response.choices[0].message.content
    
    except Exception as e:
        print(str(e))
        return "612,842,912,135 DEMOLISHED OPENAI SERVERS: " + str(e) 

async def send_msg(model, followup, prompt, img_url, is_shorthand = False):
    try:
        response = await get_response_openai(model, prompt, img_url)    

        if len(response) > CHAR_LIMIT_DISCORD:
            parts = [response[i:i+CHAR_LIMIT_DISCORD] for i in range(0, len(response), CHAR_LIMIT_DISCORD)]
            for part in parts:
                if is_shorthand == True:
                    await followup.reply(part)
                else:
                    await followup.send(part)
        else:
            if is_shorthand == True:
                await followup.reply(response)
            else:
                await followup.send(response)

    except Exception as e:
        print(str(e))
        if is_shorthand == True:
            await followup.reply(str(e))
        else:
            await followup.send(str(e))

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = discord.Client(intents = intents, proxy = PROXY) 
    tree = app_commands.CommandTree(bot)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is running")
        #  for guild_id in SERVER_WHITELIST:
        try:
            synced = await tree.sync()
            print(f"synced commands {synced}")
        except Exception as e:
            print(f"failed to sync command tree: {str(e)}")

    # slash command  
    @tree.command(name = SLASH_COMMAND_NAME) 
    @app_commands.choices(model = [
        app_commands.Choice(name = "4", value = 0),
        app_commands.Choice(name = "4-vision", value = 1),
        app_commands.Choice(name = "4-turbo", value = 2),
        app_commands.Choice(name = "3.5-turbo", value = 3),
        app_commands.Choice(name = "davinci-003", value = 4),
    ])
    async def on_command(
        interaction: discord.Interaction,
        model: app_commands.Choice[int],
        prompt: str,
        img_url: str = None,
        # img_base64: str
        ):
        if img_url == None:
            await interaction.response.send_message(f"retard really said \"{prompt}\" to {models[model.name]}")
        else:
            await interaction.response.send_message(f"retard really said \"{prompt}\" and sent this image {img_url} to {models[model.name]}")

        print(f'✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆ \n sending prompt "{prompt}" and image {img_url} to model {model.name} at {interaction.created_at} UTC \n ✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆')
        await send_msg(model.name, interaction.followup, prompt, img_url, False)

    # shorthand command for the default model
    @bot.event
    async def on_message(msg):
        # ignore dms and msg sent by the bot itself
        if msg.channel.type == "private" or msg.author == bot.user:
            return

        # ignore msg not starting with the command prefix
        if msg.content == None or len(msg.content) < 1 or msg.content[0] != SHORTHAND_COMMAND_PREFIX:
            return
        
        usr_msg = msg.content[1:]
        print(f'✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆ \n sending prompt "{usr_msg}" at {msg.created_at} UTC to default model {DEFAULT_MODEL} \n ✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆')
        await send_msg(DEFAULT_MODEL, msg, usr_msg, None, True)

    bot.run(os.getenv("DISCORD_KEY"))

if __name__ == '__main__':
    run_discord_bot()