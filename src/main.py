#!/bin/env python
# -*- coding: UTF-8 -*-
# twitch-chat-bot
import os
import time
import json
from twitchio.ext import commands
from gtts import gTTS
import asyncio

from config.auth import TOKEN, TELEGRAM_URL, YOUTUBE_URL, INSTAGRAM_URL, ID

# Track the bot's start time for uptime calculations
start_time = time.time()

# Language dictionary for greetings and uptime messages
languages = {
    "en": {
        "hello": "Hello",
        "uptime": "I've been up for {hours} hours, {minutes} minutes, and {seconds:.2f} seconds.",
        "telegram": f"Join our community on Telegram at {TELEGRAM_URL}",
        "youtube": f"Check out my YouTube channel at {YOUTUBE_URL}",
        "instagram": f"Follow me on Instagram at {INSTAGRAM_URL}",
        "help": "**Available commands:**\n"
            "!hello - Greet the bot\n"
            # "!uptime - Get the bot's uptime\n"
            "!lang - See supported languages and set your preference\n"
            "!setlang [en/es] - Set your preferred language\n"
            "!telegram - Get the Telegram channel link\n"
            "!youtube - Get the YouTube channel link\n"
            "!instagram - Get the Instagram profile link\n"
            "!tts [message] - Make the bot speak your message (Optional)\n",
    },
    "es": {
        "hello": "Hola",
        "uptime": "He estado activo durante {hours} horas, {minutes} minutos y {seconds:.2f} segundos.",
        "telegram": f"Únete a nuestra comunidad en Telegram en {TELEGRAM_URL}",
        "youtube": f"Visita mi canal de YouTube en {YOUTUBE_URL}",
        "instagram": f"Sígueme en Instagram en {INSTAGRAM_URL}",
        "help": "**Comandos disponibles:**\n"
            "!hola - Saluda al bot\n"
            # "!uptime - Consulta el tiempo de actividad del bot\n"
            "!lang - Ve los idiomas compatibles y establece tu preferencia\n"
            "!setlang [en/es] - Establece tu idioma preferido\n"
            "!telegram - Obtén el enlace del canal de Telegram\n"
            "!youtube - Obtén el enlace del canal de YouTube\n"
            "!instagram - Obtén el enlace del perfil de Instagram\n"
            "!tts [mensaje] - Haz que el bot hable tu mensaje (Opcional)\n",
    },
}


class Bot(commands.Bot):
    bot_start_time = time.time()

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix='!',
            initial_channels=['jarwarez'])

        self.user_languages = {}  # Diccionario para almacenar idiomas de usuarios
        try:
            with open('user_languages.json', 'r') as f:
                self.user_languages = json.load(f)
        except FileNotFoundError:
            pass
        self.current_language = "es"  # Default language

    async def event_ready(self):
        # Informative message upon successful login
        print(f'Logged in as | {self.nick} (User id is | {self.user_id})')

    @commands.command()
    async def lang(self, ctx: commands.Context):
        """Displays the currently supported languages for the bot."""
        supported_languages = ", ".join(languages.keys())
        await ctx.send(f"The bot currently supports the following languages: {supported_languages}")

    @commands.command()
    async def setlang(self, ctx: commands.Context, language: str):
        if language.lower() not in languages:
            await ctx.send(f"Invalid language. Choose 'en' or 'es'.")
            return
        self.current_language = language.lower()
        await ctx.send(f"{ctx.author.name} set language to {language.upper()}.")
        self.user_languages[ctx.author.id] = language.lower()
        with open('user_languages.json', 'w') as f:
            json.dump(self.user_languages, f)

    @commands.command()
    async def setlangbot(self, ctx: commands.Context, language: str):
        """Sets the language for the bot (en or es)."""
        if language.lower() not in languages:
            await ctx.send(f"Invalid language. Choose 'en' or 'es'.")
            return
        self.current_language = language.lower()
        await ctx.send(f"Language set to {language.upper()}.")

    @commands.command()
    async def help(self, ctx: commands.Context):
        """Displays a list of available commands and their descriptions."""
        user_lang = self.user_languages.get(ctx.author.id, self.current_language)
        await ctx.send(languages[user_lang]["help"])

    @commands.command()
    async def me(self, ctx: commands.Context):
        """Greets the user who invoked the command."""
        user_lang = self.user_languages.get(ctx.author.id, self.current_language)
        await ctx.send(ctx.author.name)
        # await ctx.send(f"Hello, {ctx.author.name}! ")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """Greets the user who invoked the command."""
        user_lang = self.user_languages.get(ctx.author.id, self.current_language)
        await ctx.send(languages[user_lang]["hello"] + ", " + ctx.author.name + "!")
        # await ctx.send(f"Hello, {ctx.author.name}! ")

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """Displays the bot's uptime."""
        if ctx.author.id == ID:
            now = time.time()
            uptime = now - start_time
            hours, remainder = divmod(int(uptime), 3600)
            minutes, seconds = divmod(remainder, 60)
            message = languages[self.current_language]["uptime"].format(
                hours=hours, minutes=minutes, seconds=seconds
            )
            await ctx.send(message)
            # await ctx.send(f"I've been up for {hours} hours, {minutes} minutes, and {seconds:.2f} seconds.")
        else:
           await ctx.send("This command is only accessible to the streamer.")

    @commands.command()
    async def secret_command(self, ctx: commands.Context):
        if ctx.author.id == ID:
            await ctx.send("This is a secret command, only for admins.")
        else:
            await ctx.send("This command is only accessible to the streamer.")

    @commands.command()
    async def telegram(self, ctx: commands.Context):
        """Provides (placeholder) information or link to your Telegram channel."""
        user_lang = self.user_languages.get(ctx.author.id, self.current_language)
        await ctx.send(languages[user_lang]["telegram"])
        # await ctx.send(f"{ctx.author.name}, you can find me on Telegram at (your Telegram channel link here).")

    @commands.command()
    async def youtube(self, ctx: commands.Context):
        """Provides (placeholder) information or link to your YouTube channel."""
        user_lang = self.user_languages.get(ctx.author.id, self.current_language)
        await ctx.send(languages[user_lang]["youtube"])
        # await ctx.send(f"{ctx.author.name}, check out my YouTube channel at (your YouTube channel link here).")

    @commands.command()
    async def instagram(self, ctx: commands.Context):
        """Provides (placeholder) information or link to your Instagram profile."""
        user_lang = self.user_languages.get(ctx.author.id, self.current_language)
        await ctx.send(languages[user_lang]["instagram"])
        # await ctx.send(f"{ctx.author.name}, follow me on Instagram at (your Instagram profile link here).")

    async def speak(self, ctx: commands.Context, message: str):
        """Speaks the provided message using Google Text-to-Speech (optional)."""
        if gTTS is None:
            await ctx.send("Text-to-speech functionality is not available.")
            return

        try:
            # Customize language and voice settings as needed
            tts = gTTS(text=message, lang="en", slow=False)
            tts.save("message.mp3")
            await ctx.voice.play("message.mp3")  # Assuming your bot has joined a voice channel
            await asyncio.sleep(tts.duration())  # Wait for audio to finish playing
        except Exception as e:
            print(f"Error during text-to-speech: {e}")
            await ctx.send("An error occurred while speaking the message.")
        finally:
            # Clean up audio file (optional)
            os.remove("message.mp3")

    @commands.command()
    async def tts(self, ctx: commands.Context, *, message):
        """Speaks the user's name and message using Google Text-to-Speech (optional)."""
        full_message = f"{ctx.author.name}, {message}"
        await self.speak(ctx, full_message)

    # @bot.event
    async def event_command_error(self, ctx, error):
        """Handles errors related to unmatched commands."""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command '{ctx.invoked_with}' not found. Try '!help' for a list of commands.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
