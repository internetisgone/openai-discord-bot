# openai-discord-bot

simple discord bot that uses openai's chat and completion api to respond to messages. check the
[official doc](https://platform.openai.com/docs/models) for latest changes.

## usage
### slash command
`/kkb [model] [prompt] [image url]`
image url is required for gpt-4-vision-preview only
### shorthand command
`%` + your message 
uses the default model, in this case gpt-4

## setting up
- install the requirements and create a .env file using the template below
- paste your openai api key in .env
- go to discord developer portal, create a new application and add a bot under it
- copy the bot's token and paste it in .env
- generate an invite link. go to OAuth2 - URL generator, set scopes to "bot" and "applications.commands", and select the "send messages", "use slash commands" permission
- invite the bot to your server and run main.py

## .env
```
DISCORD_KEY = "123456"
OPENAI_API_KEY = "654321"
```
