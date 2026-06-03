from nxc.helpers.misc import CATEGORY


class NXCModule:
    """Module to get flags for CTF use only."""

    name = "get_flag"
    description = "Get the flag for the given user (Default: current user)"
    supported_protocols = ["smb", "winrm"]
    category = CATEGORY.ENUMERATION

    def options(self, context, module_options):
        """
        PATH: The path from where to grab the flag from
        FLAG_NAME: The name of the file where the flag is stored (Default: user.txt, if Administrator, then Default: root.txt)
        USER: The user's desktop from which we must grab the flag from
        """
        self.flag_name = module_options.get("FLAG_NAME") or None
        self.path = module_options.get("PATH") or ""
        self.user = module_options.get("USER") or None

    def get_flag(self, context, connection):
        if (
            self.flag_name is None
            and self.user is None
            and connection.username.lower() == "administrator"
        ):
            self.flag_name = "root.txt"

        elif self.flag_name is None:
            self.flag_name = "user.txt"

        if self.path == "":
            if self.user is None:
                self.path = (
                    f"C:\\Users\\{connection.username}\\Desktop\\{self.flag_name}"
                )
            else:
                self.path = f"C:\\Users\\{self.user}\\Desktop\\{self.flag_name}"
        context.log.display(f"Trying to get the flag from: {self.path}")
        command = f"type {self.path}"
        p = connection.execute(command, True)
        context.log.highlight(f"{p}")

    def on_login(self, context, connection):
        self.get_flag(context, connection)
