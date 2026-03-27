import discord
from discord.ext import commands
import json
import asyncio
import os
import sys
import aiohttp

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setup_variables import SETUPBOT_TOKEN, GUILD_ID, CONFIG_JSON, TEMPLATE_DIR

# Load config
with open(CONFIG_JSON, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# Load templates
MOD_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'moderation_template.json')
WELCOME_TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'welcome_template.json')

# Bot setup with ALL intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

def get_color(color_name):
    """Convert color name to discord.Color"""
    colors = {
        'red': discord.Color.red(),
        'orange': discord.Color.orange(),
        'yellow': discord.Color.yellow(),
        'green': discord.Color.green(),
        'blue': discord.Color.blue(),
        'purple': discord.Color.purple(),
        'magenta': discord.Color.magenta(),
        'gold': discord.Color.gold(),
        'default': discord.Color.default()
    }
    return colors.get(color_name.lower(), discord.Color.default())

async def get_icon_bytes(icon_path, icon_type):
    """Convert icon to bytes for Discord API"""
    if icon_type == "file":
        with open(icon_path, 'rb') as f:
            return f.read()
    elif icon_type == "url":
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_path) as resp:
                if resp.status == 200:
                    return await resp.read()
    return None

async def create_role_with_permissions(guild, role_data):
    """Create a role with specific permissions if it doesn't already exist"""
    # Check if role already exists
    existing_role = discord.utils.get(guild.roles, name=role_data['name'])
    if existing_role:
        print(f'Role already exists: {existing_role.name}')
        return existing_role

    perms_dict = role_data.get('permissions', {})
    permissions = discord.Permissions(**perms_dict)
    
    color = get_color(role_data.get('color', 'default'))
    hoist = role_data.get('hoist', False)
    
    role = await guild.create_role(
        name=role_data['name'],
        permissions=permissions,
        color=color,
        hoist=hoist
    )
    return role

async def set_channel_permissions(channel, permissions_data, role_map):
    """Set channel permissions based on template"""
    overwrites = {}
    
    # Deny @everyone by default if specified
    if '@everyone' in permissions_data.get('deny', []):
        overwrites[channel.guild.default_role] = discord.PermissionOverwrite(view_channel=False)
    
    # Allow specific roles to view
    for role_name in permissions_data.get('view', []):
        if role_name in role_map:
            overwrites[role_map[role_name]] = discord.PermissionOverwrite(view_channel=True)

    # Explicitly deny specific roles
    for role_name in permissions_data.get('deny', []):
        if role_name in role_map and role_name != '@everyone':
            overwrites[role_map[role_name]] = discord.PermissionOverwrite(view_channel=False)
    
    await channel.edit(overwrites=overwrites)

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')
    
    guild = bot.get_guild(int(GUILD_ID))
    if not guild:
        print(f'Error: Could not find guild with ID {GUILD_ID}')
        await bot.close()
        return
    
    print(f'Found guild: {guild.name}')
    
    try:
        # Change server name and icon
        new_server_name = config["server"]["name"]
        icon_path = config["server"].get("icon")
        icon_type = config["server"].get("icon_type", "none")
        
        print(f'Updating server settings...')
        
        # Prepare icon
        icon_bytes = None
        if icon_path and icon_type != "none":
            try:
                icon_bytes = await get_icon_bytes(icon_path, icon_type)
            except Exception as e:
                print(f'Could not load icon: {e}')
        
        # Update server
        if guild.name != new_server_name or icon_bytes:
            await guild.edit(name=new_server_name, icon=icon_bytes)
            print(f'Server name updated to: {new_server_name}')
        
        # Clean up existing channels and categories
        print('Cleaning server...')
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f'Deleted: {channel.name}')
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f'Could not delete {channel.name}: {e}')
        
        print('Server cleaned!\n')
        
        # Load moderation template
        print('Loading Moderation Template...')
        mod_template = None
        if os.path.exists(MOD_TEMPLATE_PATH):
            with open(MOD_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
                mod_template = json.load(f)

        # Load welcome template if specified
        welcome_template = None
        if config.get("use_welcome_template", False) and os.path.exists(WELCOME_TEMPLATE_PATH):
            with open(WELCOME_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
                welcome_template = json.load(f)
        
        # Create roles
        print('Creating Roles...')
        role_map = {}
        
        # Create moderation roles first (Admin, Moderator)
        if mod_template and 'roles' in mod_template:
            for role_data in mod_template['roles']:
                role = await create_role_with_permissions(guild, role_data)
                role_map[role.name] = role
                print(f'Created role: {role.name}')
        
        # Create custom roles from config
        if 'custom_roles' in config and config['custom_roles']:
            for role_name in config['custom_roles']:
                role_data = {'name': role_name}
                role = await create_role_with_permissions(guild, role_data)
                role_map[role_name] = role
                print(f'Created custom role: {role_name}')

        # Create welcome roles if specified
        if welcome_template and 'roles' in welcome_template:
            for role_data in welcome_template['roles']:
                role = await create_role_with_permissions(guild, role_data)
                role_map[role.name] = role
                print(f'Created welcome role: {role.name}')

        # Create categories and channels
        print('Creating Categories and Channels...')
        
        # Create moderation categories and channels
        if mod_template and 'categories' in mod_template:
            for category_data in mod_template['categories']:
                category_name = category_data['name']
                category = await guild.create_category(category_name)
                print(f'Created category: {category_name}')
                
                # Create text channels
                for channel_data in category_data.get('text_channels', []):
                    channel_name = channel_data['name'] if isinstance(channel_data, dict) else channel_data
                    channel = await guild.create_text_channel(channel_name, category=category)
                    print(f'Created text channel: {channel_name}')
                    
                    # Set permissions if specified
                    if isinstance(channel_data, dict) and 'permissions' in channel_data:
                        await set_channel_permissions(channel, channel_data['permissions'], role_map)

                # Create voice channels
                for channel_data in category_data.get('voice_channels', []):
                    channel_name = channel_data['name'] if isinstance(channel_data, dict) else channel_data
                    channel = await guild.create_voice_channel(channel_name, category=category)
                    print(f'Created voice channel: {channel_name}')

        # Create welcome category and channels if specified
        if welcome_template:
            print('Creating Welcome Channels...')
            for channel_data in welcome_template.get('text_channels', []):
                channel_name = channel_data['name']
                channel = await guild.create_text_channel(channel_name)
                print(f'Created welcome text channel: {channel_name}')
                
                # Set permissions if specified
                if 'permissions' in channel_data:
                    await set_channel_permissions(channel, channel_data['permissions'], role_map)

        # Create custom categories and channels from config
        print('Creating Custom Categories...')
        if 'custom_categories' in config and config['custom_categories']:
            for category_data in config['custom_categories']:
                category_name = category_data['name']
                category = await guild.create_category(category_name)
                print(f'Created category: {category_name}')
                
                # Create text channels
                for channel_data in category_data.get('text_channels', []):
                    channel_name = channel_data['name'] if isinstance(channel_data, dict) else channel_data
                    channel = await guild.create_text_channel(channel_name, category=category)
                    print(f'Created text channel: {channel_name}')

                # Create voice channels
                for channel_data in category_data.get('voice_channels', []):
                    channel_name = channel_data['name'] if isinstance(channel_data, dict) else channel_data
                    channel = await guild.create_voice_channel(channel_name, category=category)
                    print(f'Created voice channel: {channel_name}')
        
        print('✅ Server setup complete!')
        
    except discord.Forbidden:
        print('❌ Error: Bot does not have permission to manage server')
    except Exception as e:
        print(f'❌ Error during setup: {e}')
    
    await bot.close()

# Run bot
bot.run(SETUPBOT_TOKEN)