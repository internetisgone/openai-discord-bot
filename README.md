# openai-discord-bot
simple discord bot that responds to messages using openai's chat completions api.<br>
check the
[api docs](https://platform.openai.com/docs/api-reference) for latest info.

## usage
### slash command
`/kkb [model] [prompt] [temperature] [image url]`<br>
temperature is optional. defaults to 1<br>
image url is required for gpt-4-vision-preview only
### shorthand command
`%[prompt]`<br>
use the default model gpt-3.5-turbo

## setup and run
- create a venv and install requirements
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  pip -r install requirements.txt
  ```
- create a .env file using the template below
- paste your openai api key in .env
- go to discord developer portal, create a new application and add a bot under it. copy the bot's token and paste it in .env
- go to OAuth2 - URL generator, set scopes to `bot` and `applications.commands`. select the `send messages` and `use slash commands` permissions
- invite the bot to your server with the link and run main.py

## .env
```
DISCORD_KEY="123456"
OPENAI_API_KEY="654321"
```
