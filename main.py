import os
import logging 
import discord
from discord import app_commands
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

SLASH_COMMAND_NAME = "kkb"
SHORTHAND_COMMAND_PREFIX = "%"
DEFAULT_MODEL = "4o"
CHAR_LIMIT_DISCORD = 2000         # max chars in a discord message

# for production 
PROXY = None
DISCORD_KEY = os.getenv("DISCORD_KEY")

# for dev 
# PROXY = "http://127.0.0.1:1087"
# DISCORD_KEY = os.getenv("DISCORD_KEY_TEST")

logging.basicConfig(level = logging.INFO, format = "%(asctime)s %(levelname)s %(process)d %(message)s")

models = { 
    "4o": "gpt-4o",
    "4": "gpt-4",
    "4-turbo": "gpt-4-turbo",
    "3.5-turbo": "gpt-3.5-turbo", 
    "davinci-002": "davinci-002"
    }

async def get_response_openai(model, prompt, temperature, img_url):
    try:         
        # legacy completion model
        if model == "davinci-002":
            response = openai_client.completions.create(
                model = models[model],
                prompt = prompt,
                temperature = temperature,
                max_tokens = 1000
            )
            return response.choices[0].text
                    
        # current models
        else:
            response = None

            if img_url == None:
                response = openai_client.chat.completions.create(
                model = models[model],
                messages = [
                    {
                        "role": "user",
                        "content": 
                        [
                            { "type": "text", "text": prompt },
                        ],
                    }
                ],
                max_tokens = 1000,
                temperature = temperature,
            )
            else:
                response = openai_client.chat.completions.create(
                model = models[model],
                messages = [
                    {
                        "role": "user",
                        "content": 
                        [
                            { "type": "text", "text": prompt },
                            {
                                "type": "image_url",
                                "image_url": { "url": img_url },
                            },
                        ],
                    }
                ],
                max_tokens = 1000,
                temperature = temperature,
            )
           
        return response.choices[0].message.content
    
    except Exception as e:
        logging.error(str(e))
        return "612,842,912,135 DEMOLISHED OPENAI SERVERS: " + str(e) 

async def send_msg(model, followup, prompt, temperature, img_url, is_shorthand = False):
    try:
        response = await get_response_openai(model, prompt, temperature, img_url)    

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
        logging.error(str(e))
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
        try:
            synced = await tree.sync()
            logging.info(f"synced {len(synced)} commands")
        except Exception as e:
            logging.error(f"failed to sync command tree: {str(e)}")

    # slash command  
    @tree.command(name = SLASH_COMMAND_NAME) 
    @app_commands.choices(model = [
        app_commands.Choice(name = "4o", value = 0),
        app_commands.Choice(name = "4", value = 1),
        app_commands.Choice(name = "4-turbo", value = 2),
        app_commands.Choice(name = "3.5-turbo", value = 3),
        app_commands.Choice(name = "davinci-002", value = 4)
    ])
    async def on_command(
        interaction: discord.Interaction,
        model: app_commands.Choice[int],
        prompt: str,
        temperature: float = 1.0,
        img_url: str = None,
        # img_base64: str
        ):

        # temperature should be between 0 and 2
        temperature = max(min(temperature, 2), 0)

        if img_url == None:
            await interaction.response.send_message(f"retard really said \"{prompt}\" at temperature {temperature} to {models[model.name]} ")
        else:
            await interaction.response.send_message(f"retard really said \"{prompt}\" and sent this image {img_url} at temperature {temperature} to {models[model.name]}")

        # print(f'\n✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆ \n sending prompt "{prompt}" and image {img_url} to model {model.name} at temperature {temperature} \n ✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆')
        await send_msg(model.name, interaction.followup, prompt, temperature, img_url, False)

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
        # print(f'\n✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆ \n sending prompt "{usr_msg}" to default model {DEFAULT_MODEL} \n ✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆')
        await send_msg(DEFAULT_MODEL, msg, usr_msg, 1.0, None, True)

    bot.run(DISCORD_KEY)

if __name__ == '__main__':
    run_discord_bot()