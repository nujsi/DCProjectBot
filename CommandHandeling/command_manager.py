from CommandHandeling.CommandTypes.project_command import ProjectCommand


class CommandManager:

    def __init__(self, command_prefix):

        self.command_array = []
        self.command_prefix = command_prefix
        self.add_commands_to_command_array()

    def add_commands_to_command_array(self):

        self.add_command(ProjectCommand(self.command_prefix, "project", "Ermöglich es, einen Projekt-Channel zu erstellen, dessen Name jeder Interessent sich als Rolle hinzufügen kann, um dann innerhalb des Channels mit der Rolle getaggt werden zu können."))

    def add_command(self, command):

        self.command_array.append(command)

    def get_command_array(self):

        return self.command_array

    def get_command_prefix(self):

        return self.command_prefix

    def set_command_prefix(self, command_prefix):

        self.command_prefix = command_prefix

    async def check_message(self, **kwargs):

        """
        Methode durchläuft alle in der Liste vorhandenen Klassen, die von Command erben und somit
        als Command dienen sollen.

        Als Parameter wird ein Dict übergeben, das die Nachricht als Objekt und Details zu dieser beinhaltet.

        check_message soll die Nachricht durchsuchen und gucken, ob diese mit dem festgelegten Prefix anfängt.
        Wenn dies zutrifft, wird überprüft, ob der Command der jeweiligen Klasse aus der Liste, durch die iteriert wird,
        gleich dem command ist, der im Chat geschrieben wurde, also dem Teil nach dem Nachrichten-Prefix: bei !kill, ist
        der Command kill.
        Wenn ja, dann handelt es sich eindeutig um einen Command und für diesen kann die Methode execute() aufgerufen werden,
        in der festgelegt ist, was der Command machen soll.

        Nach erfolgreichem Ausführen des Commands wird dessen Rückgabewert (ein Tupel) genommen, um zu entscheiden,
        ob die Nachricht in den Chat gelangen soll. Wenn dabei der erste Teil des Tupels (send_response_to_chat_bool) True
        ist, wird die Nachricht dem Tupel (response_tuple[1]) entnommen und zurückgegeben.

        -> project_bot.py Falls diese Nachricht kein "" ist, wird sie im Chat erscheinen.

        :param kwargs:
        :return:
        """

        message_obj = kwargs["message_obj"]
        message_content = kwargs["message_content"]
        message_array = message_content.split(" ")

        command_prefix = message_array[0][0]
        command = message_array[0][1:]
        command_details = "".join([i + " " for i in message_array[1:]])

        if self.command_prefix == command_prefix:

            for c in self.get_command_array():

                if command.lower() == c.get_command().lower():

                    response_tuple = await c.execute(message_obj=message_obj, command_details=command_details)

                    if response_tuple:

                        send_response_to_chat_bool = response_tuple[0]

                        if send_response_to_chat_bool:

                            chat_message = response_tuple[1]

                            return chat_message

        return ""
