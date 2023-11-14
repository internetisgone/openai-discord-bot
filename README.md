# openai-discord-bot

simple discord bot that uses openai's api to respond to messages.<br>
currently supports gpt-4, gpt-4-vision-preview, gpt-4-1106-preview, gpt-3.5-turbo, text-davinci-003 (legacy) and text-davinci-002 (legacy).<br>
check the
[api docs](https://platform.openai.com/docs/api-reference) for latest info.

## usage
### slash command
`/kkb [model] [prompt] [temperature] [image url]`<br>
temperature is optional. defaults to 1<br>
image url is required for gpt-4-vision-preview only
### shorthand command
`%[prompt]`<br>
uses the default model gpt-4

## setting up
- install the requirements and create a .env file using the template below
- paste your openai api key in .env
- go to discord developer portal, create a new application and add a bot under it
- copy the bot's token and paste it in .env
- generate an invite link. go to OAuth2 - URL generator, set scopes to "bot" and "applications.commands". select the "send messages" and "use slash commands" permissions
- invite the bot to your server and run main.py

## .env
```
DISCORD_KEY = "123456"
OPENAI_API_KEY = "654321"
```
