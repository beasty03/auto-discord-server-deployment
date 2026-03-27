import sqlite3
import json
from typing import Tuple, Dict, Any
import discord
from discord import app_commands
from discord.ext import commands
from setup_variables import DB_FILE, TEMPLATE_DIR
import os

SYNC_CHANNEL_NAME = "texting"
TEMPLATE_FILE = os.path.join(TEMPLATE_DIR, 'user_database_template.json')

def _load_template() -> Dict[str, Any]:
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def _ensure_table(conn: sqlite3.Connection):
    template = _load_template()
    user_fields = template.get("user", {})
    
    # Build column definitions dynamically from template
    columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
    
    for field_name, default_value in user_fields.items():
        if field_name == "user_id":
            columns.append("user_id TEXT UNIQUE")
        elif isinstance(default_value, list):
            columns.append(f"{field_name} TEXT")  # Store arrays as JSON strings
        else:
            columns.append(f"{field_name} TEXT")
    
    create_sql = f"CREATE TABLE IF NOT EXISTS users ({', '.join(columns)})"
    
    cur = conn.cursor()
    cur.execute(create_sql)
    conn.commit()
    print(f"[DEBUG] Table structure: {columns}")

def _roles_list(member: discord.Member):
    return [r.name for r in member.roles if r.name != "@everyone"]

def _build_user_data(member: discord.Member, template: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamically build user data based on template fields"""
    user_fields = template.get("user", {})
    data = {}
    
    for field_name in user_fields.keys():
        if field_name == "user_id":
            data[field_name] = str(member.id)
        elif field_name == "username":
            data[field_name] = member.name
        elif field_name == "join_date":
            data[field_name] = member.joined_at.isoformat() if member.joined_at else None
        elif field_name == "roles":
            data[field_name] = json.dumps(_roles_list(member), ensure_ascii=False)
        else:
            # Unknown field, set to null
            data[field_name] = None
    
    return data

class SyncUsersCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _sync_blocking(self, guild: discord.Guild) -> Tuple[int, int]:
        print(f"[DEBUG] Starting sync for guild: {guild.name}")
        print(f"[DEBUG] Member count: {len(guild.members)}")
        
        template = _load_template()
        user_fields = list(template.get("user", {}).keys())
        
        conn = sqlite3.connect(DB_FILE)
        try:
            _ensure_table(conn)
            cur = conn.cursor()
            inserted = updated = 0
            
            for member in guild.members:
                user_data = _build_user_data(member, template)
                uid = user_data["user_id"]
                
                cur.execute('SELECT id FROM users WHERE user_id = ?', (uid,))
                if cur.fetchone():
                    # Build UPDATE query dynamically
                    set_clause = ", ".join([f"{field}=?" for field in user_fields if field != "user_id"])
                    values = [user_data[field] for field in user_fields if field != "user_id"]
                    values.append(uid)  # WHERE user_id = ?
                    
                    cur.execute(f"UPDATE users SET {set_clause} WHERE user_id=?", values)
                    updated += 1
                else:
                    # Build INSERT query dynamically
                    fields_str = ", ".join(user_fields)
                    placeholders = ", ".join(["?" for _ in user_fields])
                    values = [user_data[field] for field in user_fields]
                    
                    cur.execute(f"INSERT INTO users ({fields_str}) VALUES ({placeholders})", values)
                    inserted += 1
                    
            conn.commit()
            print(f"[DEBUG] Sync complete: {inserted} inserted, {updated} updated")
            return inserted, updated
        except Exception as e:
            print(f"[DEBUG] Error during sync: {e}")
            raise
        finally:
            conn.close()

    def _is_texting_channel(self, channel) -> bool:
        return getattr(channel, "name", None) == SYNC_CHANNEL_NAME

    @app_commands.command(name="sync_users", description="Sync guild members to the DB")
    @app_commands.guilds(1486699680531218485)
    async def sync_users(self, interaction: discord.Interaction):
        print(f"[DEBUG] Command called by {interaction.user}")
        
        perms = interaction.user.guild_permissions if interaction.guild else None
        if not (perms and perms.manage_guild):
            print("[DEBUG] Permission denied")
            await interaction.response.send_message("You need Manage Guild permission.", ephemeral=True)
            return

        if interaction.guild is None or not self._is_texting_channel(interaction.channel):
            print(f"[DEBUG] Wrong channel: {interaction.channel.name if interaction.channel else 'None'}")
            await interaction.response.send_message(f"Use this command only in #{SYNC_CHANNEL_NAME}.", ephemeral=True)
            return

        print("[DEBUG] Deferring response...")
        await interaction.response.defer(thinking=True)
        
        print("[DEBUG] Starting executor...")
        loop = self.bot.loop
        inserted, updated = await loop.run_in_executor(None, self._sync_blocking, interaction.guild)
        
        print("[DEBUG] Sending followup...")
        await interaction.followup.send(f"Sync complete: {inserted} inserted, {updated} updated.", ephemeral=True)
        print("[DEBUG] Done!")

async def setup(bot: commands.Bot):
    await bot.add_cog(SyncUsersCog(bot))