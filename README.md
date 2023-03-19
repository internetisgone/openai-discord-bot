# openai-discord-bot

v simple discord bot that uses openai's gpt-4 api to respond to messages. you can change gpt-4 to whichever model you prefer (see openai api docs for [chat](https://platform.openai.com/docs/api-reference/chat) and [completion](https://platform.openai.com/docs/api-reference/completions) for details).

## usage
`%` + your message 

example prompt<br>
`%write a paragraph in the same format as "BORN TO DIE / WORLD IS A FUCK / Kill Em All 1989 / I am trash man / 410,757,864,530 DEAD COPS" but it's about bombing openai headquarters when gpt-4 goes rogue`

## setting up
- go to discord developer portal, create a new application and add a bot under it<br>
- copy the bot's token and paste it in `DISCORD_KEY` field in your .env file<br>
- generate an invite link. go to OAuth2 - URL generator section, set scope to "bot", and select the "send messages" and "read messages/view channels" permissions<br>
- invite the bot to your server and run main.py<br>

## .env
```
DISCORD_KEY = "123456"
OPENAI_API_KEY = "654321"
```

## requirements
openai<br>
discord<br>
dotenv

## todo
requirements.txt<br>
mention user<br>
server whitelist
