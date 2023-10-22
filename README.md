# openai-discord-bot

v simple discord bot that uses openai's gpt-4 api to respond to messages. you can change gpt-4 to whichever model you prefer (see openai api docs for [chat](https://platform.openai.com/docs/api-reference/chat) and [completion](https://platform.openai.com/docs/api-reference/completions) for details).

## usage
`%` + your message 

## setting up
- install the requirements and create a .env file using the template below
- paste your openai key in .env
- go to discord developer portal, create a new application and add a bot under it
- copy the bot's token and paste it in .env
- generate an invite link. go to OAuth2 - URL generator, set scope to "bot", and select the "send messages" and "read messages/view channels" permissions
- invite the bot to your server and run main.py

## .env
```
DISCORD_KEY = "123456"
OPENAI_API_KEY = "654321"
```
