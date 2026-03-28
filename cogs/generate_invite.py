import webbrowser
import os 
import sys 

# Add parent directory to path FIRST
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# THEN import
CLIENT_ID = 1486718913273135124
from discord.ext import commands

def generate_invite_link(client_id, permissions=8):
    """
    Generate Discord bot invite link
    
    Permissions:
    8 = Administrator (all permissions)
    """
    invite_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"
    return invite_url

async def setup(bot: commands.Bot):
    pass  # This cog doesn't add any commands, just provides utility function

if __name__ == "__main__":
    print("=== Discord Bot Invite Link Generator ===\n")
    invite_link = generate_invite_link(CLIENT_ID)
    print(f"Invite Link:\n{invite_link}\n")
    
    print("Opening invite link in browser...")
    webbrowser.open(invite_link)
    
    print("\nSteps:")
    print("1. Select your server in the browser window")
    print("2. Click 'Authorize'")
    print("3. Enable Developer Mode: Discord Settings → Advanced → Developer Mode")
    print("4. Right-click your server → Copy Server ID")
    print("5. Add the Guild ID to setup_variables.py")
    print("\nThen run: python setup_server.py")
