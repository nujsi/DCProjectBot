from abc import ABC, abstractmethod


class Command(ABC):
    """
    Klasse Command ist eine abstrakte Klasse, die Funktionen für alle Klassen, die
    von Commman erben, vorgibt. Somit kann eine neue Klasse, die von Command
    erbt, genutzt werden, um mit den definierten Parametern zu arbeiten.

    Beispielsweise kann durch eine Instanz der erbenden Klasse auf den Command an sich zugegriffen werden
    oder die Funktion execute ausführen, in der dann für den bestimmten Command genauer festgelegt ist, was der Command
    tun soll.

    Bsp: Instanz des CommandManagers, der alle Commands im Konstruktor (__init__) addet.

        cmd_manager = CommandManager(command_prefix)

        Wenn man nun durch alle Commands (alle Klassen, die von Command erben) iteriert, dann kann man für
        jede Klasse die Funktionen ausführen, weil diese von Command vorgegeben sind.

        for i in cmd_manager.get_command_array():

            i.execute()

    """

    def __init__(self, command_alias, command, command_description):

        self.command_alias = command_alias
        self.command = command
        self.command_description = command_description

    def get_command_alias(self):
        return self.command_alias

    def get_command(self):
        return self.command

    def get_command_description(self):
        return self.command_description

    def execute(self):
        pass
