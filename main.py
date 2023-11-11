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
CHAR_LIMIT_DISCORD = 2000         # max chars in a discord message

models = { 
    "4": "gpt-4",
    "4-vision": "gpt-4-vision-preview",
    "4-turbo": "gpt-4-1106-preview",
    "3.5-turbo": "gpt-3.5-turbo", 
    "davinci-003": "text-davinci-003"
    }

async def get_response_openai(model, prompt):
    try: 
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

async def get_response_openai_vision(prompt, img_url):
    try: 
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
            max_tokens = 300,
        )
        print(response)
        return response.choices[0].message.content
    except Exception as e:
        print(str(e))
        return "612,842,912,135 DEMOLISHED OPENAI SERVERS: " + str(e) 

async def get_response_openai_legacy(model, prompt):
    try: 
        response = openai_client.completions.create(
            model = models[model],
            prompt = prompt
        )
        print(response)
        return response.choices[0].text
    except Exception as e:
        print(str(e))
        return "612,842,912,135 DEMOLISHED OPENAI SERVERS: " + str(e) 

async def send_msg(model, followup, prompt, img_url):
    try:
        # try get a response via openai api
        if model == "4-vision":
            if img_url == None:
                # todo check if url returns valid image
                await followup.send("img url is required to use gpt-4-vision")
                return
            response = await get_response_openai_vision(prompt, img_url)
        elif model == "davinci-003":
            response = await get_response_openai_legacy(model, prompt)
        else:
            response = await get_response_openai(model, prompt)

        if len(response) > CHAR_LIMIT_DISCORD:
            parts = [response[i:i+CHAR_LIMIT_DISCORD] for i in range(0, len(response), CHAR_LIMIT_DISCORD)]
            for part in parts:
                await followup.send(part)
        else:
            await followup.send(response)

    except Exception as e:
        print(str(e))
        return "error: " + str(e)

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
            
    @tree.command(name = "kkb") 
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
        await send_msg(model.name, interaction.followup, prompt, img_url)

    bot.run(os.getenv("DISCORD_KEY"))

if __name__ == '__main__':
    run_discord_bot()