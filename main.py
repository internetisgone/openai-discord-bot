import os
import openai 
import discord
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

bot_command_prefix = "?"

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
        response = await send_msg_openai(user_message)
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

        # print(f'{message.author} said: "{user_message}" in #({message.channel})')
        if user_message[0] == bot_command_prefix:
            user_message = user_message[1]
            await send_msg_discord(message, user_message)

    client.run(os.getenv("DISCORD_KEY"))


if __name__ == '__main__':
    print("running...")
    run_discord_bot()
    # response = send_msg_openai()