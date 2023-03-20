import os
import openai 
import discord
from dotenv import load_dotenv
# import random

BOT_COMMAND_PREFIX = "%"
PROXY = "http://127.0.0.1:1087" # set to None if not using a proxy
CHAR_LIMIT_DISCORD = 2000       # max chars in a message

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def send_msg_openai(prompt):
    try: 
        completion = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = [ 
                {"role": "user", "content": prompt} 
            ],
            temperature = 0.9,
        )
        print(completion.choices[0])
        return completion.choices[0].message.content
    except Exception as e:
        print(e)
        return ""

async def send_msg_discord(message, user_message):
    try:
        # try get a response via openai api
        response = await send_msg_openai(user_message)

        ####### test #######
        # send a random msg
        # response = responses_bomb[random.randint(0, len(responses_bomb) - 1)]

        # response = "<@" + str(message.author.id) + ">\n\n" + response # mention author

        if len(response) > CHAR_LIMIT_DISCORD:
            print(f"response exceeded {CHAR_LIMIT_DISCORD} chars")
            parts = [response[i:i+CHAR_LIMIT_DISCORD] for i in range(0, len(response), CHAR_LIMIT_DISCORD)]
            for part in parts:
                await message.reply(part)
        else:
            await message.reply(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = None
    if PROXY != None:
        client = discord.Client(intents = intents, proxy = PROXY)  
    else:
        client = discord.Client(intents = intents)

    @client.event
    async def on_ready():
         print(f"{client.user} is running")

    @client.event
    async def on_message(message):
        # ignore msg sent by the bot itself
        if message.author == client.user:
            return

        user_message = str(message.content)
        if user_message[0]== BOT_COMMAND_PREFIX:
            user_message = user_message[1:]
            # print(message)
            # print(f'sending prompt "{user_message}" from {message.author} in #{message.channel} in {message.guild}')
            print(f'✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆ \n sending prompt "{user_message}" at {message.created_at} UTC \n ✧･ﾟ:✧･ﾟ:* ✧･ﾟ✧*:･ﾟﾐ☆')
            await send_msg_discord(message, user_message)

    client.run(os.getenv("DISCORD_KEY"))

if __name__ == '__main__':
    run_discord_bot()