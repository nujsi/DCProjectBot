from DCProjectBot.CommandHandeling.command import Command
from discord import utils, Member, Embed


class ProjectCommand(Command):

    async def execute(self, **kwargs):

        send_msg_to_chat = True

        message_obj = kwargs["message_obj"]
        command_details = kwargs["command_details"]
        command_details_array = command_details.split(" ")

        ADD_STRINGS = "add", "a"
        DEL_STRINGS = "del", "d"
        JOIN_STRINGS = "join", "j"
        LEAVE_STRINGS = "leave", "l"
        PROJECT_CHANNEL_NAME = "".join(command_details_array[1:])
        PROJECT_CREATOR_STRING = "-creator"
        PROJECT_ROLE_NAME = PROJECT_CHANNEL_NAME
        PROJECT_OWNER_ROLE_NAME = PROJECT_ROLE_NAME + PROJECT_CREATOR_STRING

        member = message_obj.author
        member_name = member.name
        self.guild = message_obj.guild
        self.guild_name = message_obj.guild.name

        chat_message = ""
        chat_member_mention = f"{member.mention}"

        if command_details[0].lower() in ADD_STRINGS:

            if not self.is_channel_existing(channel_name=PROJECT_CHANNEL_NAME):

                await self.create_new_text_channel(channel_name=PROJECT_CHANNEL_NAME)

                if not self.is_role_existing(role_name=PROJECT_ROLE_NAME):

                    await self.create_role(role_name=PROJECT_ROLE_NAME)
                    await self.create_role(role_name=PROJECT_OWNER_ROLE_NAME)
                    project_role = utils.get(self.guild.roles, name=PROJECT_ROLE_NAME)
                    project_owner_role = utils.get(self.guild.roles, name=PROJECT_OWNER_ROLE_NAME)

                    if project_role and project_owner_role:

                        await self.add_role_to_member(member, project_role)
                        await self.add_role_to_member(member, project_owner_role)

                        chat_message = f"{chat_member_mention} Text-Channel und Rolle {PROJECT_CHANNEL_NAME} wurden erstellt und {member_name} hinzugefügt."

                    else:

                        print(project_role, project_owner_role)
            else:

                chat_message = f"Channel {PROJECT_CHANNEL_NAME} existiert bereits."

        elif command_details[0].lower() in DEL_STRINGS:

            if self.is_channel_existing(channel_name=PROJECT_CHANNEL_NAME):

                if self.is_member_permitted_to_del_channel(member=member, project_owner_role_name=PROJECT_OWNER_ROLE_NAME):

                    project_channel = utils.get(self.guild.channels, name=PROJECT_CHANNEL_NAME)
                    project_role = utils.get(self.guild.roles, name=PROJECT_ROLE_NAME)
                    project_owner_role = utils.get(self.guild.roles, name=PROJECT_OWNER_ROLE_NAME)

                    await self.delete_channel(project_channel)

                    if project_role:

                        await self.remove_role_from_every_member(role=project_role)
                        await self.delete_role(project_role)

                    if project_owner_role:

                        await self.remove_role_from_every_member(role=project_owner_role)
                        await self.delete_role(project_owner_role)

                    chat_message = f"{chat_member_mention} Channel {PROJECT_CHANNEL_NAME} und Rolle {PROJECT_ROLE_NAME} wurden gelöscht."

                else:

                    chat_message = f"{chat_member_mention} Du besitzt keine Berechtigung, um {PROJECT_CHANNEL_NAME} zu löschen."

            else:

                chat_message = f"{chat_member_mention} Channel {PROJECT_CHANNEL_NAME} existiert nicht."

        elif command_details[0].lower() in JOIN_STRINGS:

            if self.is_channel_existing(PROJECT_CHANNEL_NAME):

                if self.is_role_existing(PROJECT_ROLE_NAME):

                    project_role = utils.get(self.guild.roles, name=PROJECT_ROLE_NAME)

                    await self.add_role_to_member(member, project_role)

                    chat_message = f"{chat_member_mention} Rolle {PROJECT_ROLE_NAME} wurde {member_name} hinzugefügt."

            else:

                chat_message = f"{chat_member_mention} Channel {PROJECT_CHANNEL_NAME} existiert nicht."

        elif command_details[0].lower() in LEAVE_STRINGS:

            if self.is_channel_existing(PROJECT_CHANNEL_NAME):

                if self.is_role_existing(PROJECT_ROLE_NAME):

                    if self.is_role_existing(PROJECT_OWNER_ROLE_NAME):

                        project_owner_role = utils.get(self.guild.roles, name=PROJECT_OWNER_ROLE_NAME)

                        await self.remove_role_from_member(member, project_owner_role)

                    project_role = utils.get(self.guild.roles, name=PROJECT_ROLE_NAME)

                    await self.remove_role_from_member(member, project_role)

                    chat_message = f"{chat_member_mention} Rolle {PROJECT_ROLE_NAME} wurde {member_name} entzogen."

            else:

                chat_message = f"{chat_member_mention} Channel {PROJECT_CHANNEL_NAME} existiert nicht."

        return send_msg_to_chat, chat_message


    def is_channel_existing(self, channel_name):

        return utils.get(self.guild.channels, name=channel_name)

    async def create_new_text_channel(self, channel_name):

        await self.guild.create_text_channel(name=channel_name)

    def is_role_existing(self, role_name):

        return utils.get(self.guild.roles, name=role_name)

    async def create_role(self, role_name):

        await self.guild.create_role(name=role_name)

    async def add_role_to_member(self, member, role):

        await Member.add_roles(member, role)

    async def remove_role_from_every_member(self, role):

        role_name = role.name

        for member in self.guild.members:

            has_role = utils.get(member.roles, name=role_name)

            if has_role:

                await member.remove_roles(role)

    def is_member_permitted_to_del_channel(self, member, project_owner_role_name):

        has_channel_manage_permissions, has_project_owner_role = member.guild_permissions.manage_channels, utils.get(member.roles, name=project_owner_role_name)
        return True if has_channel_manage_permissions or has_project_owner_role else False

    async def delete_channel(self, channel):

        await channel.delete()

    async def remove_role_from_member(self, member, role):

        await member.remove_roles(role)

    async def delete_role(self, role):

        await role.delete()