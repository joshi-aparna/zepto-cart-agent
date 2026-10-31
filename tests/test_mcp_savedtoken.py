import asyncio
from pathlib import Path

from fastmcp import Client
from fastmcp.client.auth import OAuth
from key_value.aio.stores.filetree import FileTreeStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet
from langchain.mcp import MCPAdapter

async def main():
    encryption_key_path = Path.home() / ".zepto-agent-key"

    if encryption_key_path.exists():
        encryption_key = encryption_key_path.read_bytes()
    else:
        encryption_key = Fernet.generate_key()
        encryption_key_path.write_bytes(encryption_key)
        encryption_key_path.chmod(0o600)

    token_dir = Path.home() / ".zepto-agent-tokens"

    for collection in ("mcp-oauth-client-info", "mcp-oauth-token", "mcp-oauth-token-expiry"):
        (
            token_dir / collection / "https:" / "mcp.zepto.co.in" / "mcp"
        ).mkdir(parents=True, exist_ok=True)

    store = FileTreeStore(data_directory=token_dir)

    encrypted_store = FernetEncryptionWrapper(
        key_value=store,
        fernet=Fernet(encryption_key),
    )

    auth = OAuth(
        token_storage=encrypted_store,
        callback_host="localhost"
    )
    
    client = Client(
        "https://mcp.zepto.co.in/mcp",
        auth=auth,
    )

    async with MCPAdapter(client) as adapter:
        tools = await adapter.list_tools()
        print([tool.name for tool in tools])

if __name__ == "__main__":
    asyncio.run(main())