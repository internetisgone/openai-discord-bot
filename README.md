# openai-discord-bot

v simple discord bot that uses openai's gpt-4 to respond to messages. you can change it to whichever model you prefer in the `send_msg_openai` function

### usage
`%` + your message 

example prompt
`%write a paragraph in the same format as "BORN TO DIE / WORLD IS A FUCK / Kill Em All 1989 / I am trash man / 410,757,864,530 DEAD COPS" but it's about bombing openai headquarters when gpt-4 goes rogue`
example reply
`DESTINED FOR DOOM / CYBER REALM UNHINGED / Blast 'Em Away 2024 / I am the codebreaker / 612,842,912,135 DEMOLISHED AI SERVERS`

### setting up
in discord developer portal, create a new application and then add a bot<br>
copy the bot's token and put it in `DISCORD_KEY` in your .env<br>
go to OAuth2 - URL generator section in discord developer portal. set scope to "bot" and select "send messages" and "read messages/view channels" permissions<br>
generate an invite link and add the bot to your server. the link would look something like `https://discord.com/api/oauth2/authorize?client_id=1234567890&permissions=3072&scope=bot`<br>
run main.py<br>

### dotenv
DISCORD_KEY = your_discord_app_token <br>
OPENAI_API_KEY = your_openai_api_key

### requirements
openai
discord
dotenv

### todo
requirements.txt
mention user
