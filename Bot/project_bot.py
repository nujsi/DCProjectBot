from discord import Client
from CommandHandeling.command_manager import CommandManager


class ProjectBot(Client):

    def __init__(self, command_prefix, **options):

        super().__init__(**options)
        COMMAND_PREFIX = command_prefix
        self.cm_manager = CommandManager(COMMAND_PREFIX)

    async def on_ready(self):

        bot_name = self.user.name
        print(f"Eingeloggt als {bot_name}!")

    async def on_message(self, message):

        """
        on_message-Event von discord.Client.event

        Wird aufgerufen, wenn eine Nachricht in einem Channel o. Ä. geschrieben wird.

        Methode check_message des CM wird aufgerufen und überprüft, ob es sich um einen
        validen Command handelt. Die Methode gibt entweder einen "" zurück, wenn keine
        Nachricht in den Chat gesendet werden soll, oder die Nachricht selbst, die
        dann in den entsprechenden Channel gesendet wird: await message.channel.send()

        :param: message-Objekt, das jegliche Infos zur Nachricht enthält (z. B. Autor)
        """

        message_content = message.content

        if not message.author.bot:

            response_msg = await self.cm_manager.check_message(message_obj=message, message_content=message_content)

            if response_msg:
                await message.channel.send(response_msg)


if __name__ == '__main__':

    token = "haha, hast du wohl gedacht.. :§"

    bot = ProjectBot("!")
    bot.run(token)
