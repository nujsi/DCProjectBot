from DCProjectBot.CommandHandeling.CommandTypes.ProjectCommand import ProjectCommand


class CommandManager():

    def __init__(self, command_prefix):

        self.command_array = []
        self.command_prefix = command_prefix
        self.add_commands_to_command_array()

    def add_commands_to_command_array(self):

        self.add_command(ProjectCommand(self.command_prefix, "project", "Ermöglich es, einen Projekt-Channel zu erstellen, für die jede Miglieder und Interessenten Rollen erhalten können."))

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
        Die Funnktion wird aufgerufen, wenn im Chat eine neue Nachricht aufkommt, die noch nicht geprüft wurde.
        Als Parameter wird ein Dict übergeben, das die Nachricht und Details zu dieser beinhaltet

        Sie soll die Nachricht durchsuchen und gucken, ob diese mit dem festgelegten Alias anfängt.
        Wenn dies zutrifft, werden der Command und die Command-Details in einer Var gespeichert.

        Nun kann das Array aller von Command erbenden Klassen durchlaufen werden und für jedn Durchlauf
        die Funktion execute() aufgerufen werden, nachdem siichergestellt wurde, dass der Command exiistiert.

        Nach erfolgreichem Ausführen des Commands wird dessen Rückgabewert (ein Tupel) genommen, um zu entscheiden,
        ob die Nachricht in den DCChat gelangen soll. Wenn dabei der erste Teil des Tupels True ist, wird die
        Nachricht der Rückgabewert der Methode, die diese Methode aufgerufen hat, sein.

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
