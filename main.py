import os
import openai 
import discord
from dotenv import load_dotenv
# import random

BOT_COMMAND_PREFIX = "%"

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
        # discord has a char limit of 2000
        if len(response) > 2000:
            print("response exceeded 2000 chars")
            response = response[:1999]

        # send a random msg
        # if user_message[0] == "p":
        #     response = responses_pseud[random.randint(0, len(responses_pseud) - 1)]
        # else:
        #     response = responses_bomb[random.randint(0, len(responses_bomb) - 1)]

        await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents, proxy="http://127.0.0.1:1087")  # proxy is used for bypassing internet censorship. can be ommited if discord isn't banned in your country

    @client.event
    async def on_ready():
         print(f"{client.user} is running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        user_message = str(message.content)

        if user_message[0]== BOT_COMMAND_PREFIX:
            user_message = user_message[1:]
            print(f'sending prompt: "{user_message}" from {message.author} in #({message.channel})')
            await send_msg_discord(message, user_message)

    client.run(os.getenv("DISCORD_KEY"))

if __name__ == '__main__':
    run_discord_bot()
    