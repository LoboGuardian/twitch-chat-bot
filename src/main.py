# twhitch-chat-bot
import time
from twitchio.ext import commands

from config.auth import TOKEN

# Track the bot's start time for uptime calculations
start_time = time.time()


class Bot(commands.Bot):
    bot_start_time = time.time()

    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix='!',
            initial_channels=['jarwarez'])

    async def event_ready(self):
        # Informative message upon successful login
        print(f'Logged in as | {self.nick} (User id is | {self.user_id})')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        """Greets the user who invoked the command."""
        await ctx.send(f"Hello, {ctx.author.name}! ")

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """Displays the bot's uptime."""
        now = time.time()
        uptime = now - start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"I've been up for {hours} hours, {minutes} minutes, and {seconds:.2f} seconds.")


if __name__ == "__main__":
    bot = Bot()
    # bot.add_error_handler(handle_errors)
    bot.run()
