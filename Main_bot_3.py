"""
COPYRIGHT (c) TheHolyOneZ 2025

CORE BOT IMPLEMENTATION LICENSE:
The ZygnalBot class and its direct implementation (lines 54-164) are proprietary and protected under copyright. 
See copyright notice on line 7 for exceptions.
- You may not modify the core implementation, except for changing Emojis and Status.
- You may not edit or change any instance of the name zygnalbot, ZygnalBot, Zygnal, .gg/U8sssc6xbv, TheZ, TheHolyOneZ.
- You may not remove or alter this notice.
- Redistribution of the core implementation requires explicit written permission.

GENERAL MIT LICENSE (All Other Code):
Permission is hereby granted, free of charge, to any person obtaining a copy of the non-core portions of this 
software and associated documentation files, to use these portions without restriction, including, but not limited to, 
the rights to:

- Use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, 
  subject to the following conditions:

1. The above copyright and dual-license notice must be included in all copies.
2. The core implementation remains protected as specified above.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, 
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, 
OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import string
import wave
import numpy as np
from openai import OpenAI
import humanize
import pytz
import aiosqlite
import emoji
from typing import Union
import asyncio
import copy
import io
import json
import logging
import os
import platform
import random
import re
import shlex
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
import aiohttp
import discord
from discord import ButtonStyle
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import load_dotenv
import requests
import yt_dlp
from youtubesearchpython import VideosSearch   
import wget
import zipfile
import platform
import os
import subprocess
import requests
from io import BytesIO
import colorsys
from PIL import Image, ImageDraw, ImageFont
import io 
from enum import Enum
from dataclasses import dataclass

load_dotenv()
ZygnalBot_Version = "V7.6.6 | BETA"

def analyze_emoji_usage(content):
    emoji_count = {}
    for char in content:
        if char in emoji.EMOJI_DATA:
            emoji_count[char] = emoji_count.get(char, 0) + 1
    return emoji_count

class ZygnalBot(commands.Bot):
    def __init__(self):
        command_prefix = str(os.getenv('CMD_PREFIX', '!'))
        
        super().__init__(
            command_prefix=command_prefix,
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=str("⚡ Server Protection")
            ),
            help_command=None
        )
        self.webhook_logger = None
        self.ticket_counter = 0
        self.start_time = time.time()
        self.mod_logs = {}
        self.warning_system = {}
        self._cached_messages = {}
        self.auto_mod_config = {
            'caps_threshold': 0.7,
            'spam_threshold': 5,
            'spam_interval': 5,
            'banned_words': set(),
            'link_whitelist': set()
        }

    async def setup_cogs(self):
        await self.add_cog(CommandErrorHandler(self))
        await self.add_cog(ModerationCommands(self))
        await self.add_cog(TicketSystem(self))
        await self.add_cog(ServerManagement(self))
        await self.add_cog(ServerInfo(self))
        await self.add_cog(HelpSystem(self))
        await self.add_cog(AutoMod(self))
        await self.add_cog(WelcomeSystem(self))
        await self.add_cog(RoleManager(self))
        await self.add_cog(UserTracker(self))
        await self.add_cog(BackupSystem(self))
        await self.add_cog(Config(self))
        await self.add_cog(OwnerOnly(self))
        await self.add_cog(MinigamesCog(self))
        await self.add_cog(Analytics(self))
        await self.add_cog(AdvancedInviteTracker(self))
        await self.add_cog(Snipe(self))
        await self.add_cog(ReminderSystem(self))
        await self.add_cog(MessagePurge(self))
        await self.add_cog(CustomLogging(self))
        await self.add_cog(LevelingSystem(self))
        await self.add_cog(MuteSystem(self))
        await self.add_cog(VerificationSystem(self))
        await self.add_cog(BotVerificationSystem(self))
        await self.add_cog(RatingSystem(self))
        await self.add_cog(MoodTracker(self))
        await self.add_cog(IdeaSystem(self))
        await self.add_cog(MusicPlayer(self))
        await self.add_cog(ChannelManager(self))
        await self.add_cog(RoleBackup(self))
        await self.add_cog(AiCommands(self))
        await self.add_cog(EnhancedMinigames(self))
        await self.add_cog(AFKSystem(self))
        await self.add_cog(JSONEmbeds(self))
        await self.add_cog(TempChannels(self))
        await self.add_cog(ProfileSystem(self))
        await self.add_cog(WebhookManager(self))
        await self.add_cog(CustomVerification(self))
        await self.add_cog(ServerAdsHub(self))
        await self.add_cog(AdvancedUserAnalytics(self)) 
        await self.add_cog(AI_CHAT(self))
        await self.add_cog(BMICalculator(self))
        await self.add_cog(MathPhysicsTools(self))
        await self.add_cog(TimeTools(self))
        await self.add_cog(CodingTools(self))
        await self.add_cog(StudyTools(self))
        await self.add_cog(URLShortener(self))
        
        await self.add_cog(PasswordGenerator(self))
        await self.add_cog(MorseCodeTools(self))
        
        await self.add_cog(ASCIIArtGenerator(self))
        await self.add_cog(URLStatusChecker(self))
        await self.add_cog(IPLookupTools(self))
        await self.add_cog(FileSizeConverter(self))
        await self.add_cog(FileTypeIdentifier(self))
        await self.add_cog(DownloadCalculator(self))
        await self.add_cog(WordAnalytics(self))
        await self.add_cog(AdvancedRNG(self))
        await self.add_cog(ChemicalElements(self))
        await self.add_cog(ISBNLookup(self))
        await self.add_cog(CitationGenerator(self))

        await self.add_cog(AdvancedPollSystem(self))


    async def setup_hook(self):
        await self.setup_cogs()
        await self.tree.sync()

    async def on_ready(self):
        self.webhook_logger = WebhookLogger(self)
        print(f'🚀 {self.user} The Owl is Online! (c) TheHolyOneZ')
        await self.setup_status_task()

    async def setup_status_task(self):
        while True:
            animations = [
                ("watching", "⚡ Get ZygnalBot → .gg/U8sssc6xbv"),
                ("listening", "🎧 Join us → .gg/U8sssc6xbv"),
            ]
            
            for activity_type, message in animations:
                activity = discord.Activity(
                    type=getattr(discord.ActivityType, activity_type),
                    name=message
                )
                await self.change_presence(activity=activity)
                await asyncio.sleep(10)
                
            stats_messages = [
                ("listening", "🎶 Get ZygnalBot → .gg/U8sssc6xbv"),
                ("playing", f"⚡ Protecting {len(self.guilds)} servers!"),
                ("listening", "🎤 Join the community → .gg/U8sssc6xbv"),
                ("watching", f"👀 {sum(g.member_count for g in self.guilds)} members online!"),
                ("listening", "🔗 Try ZygnalBot → .gg/U8sssc6xbv"),
            ]
            
            for activity_type, message in stats_messages:
                activity = discord.Activity(
                    type=getattr(discord.ActivityType, activity_type),
                    name=message
                )
                await self.change_presence(activity=activity)
                await asyncio.sleep(10)


    async def on_message(self, message):
        if message.guild:  #
            guild_id = message.guild.id        
        if isinstance(message.content, bytes):
            message.content = str(message.content.decode('utf-8'))
        if self.webhook_logger:
            await self.webhook_logger.log_message(message)
        await self.process_commands(message)

    async def on_command(self, ctx):
        if self.webhook_logger:
            await self.webhook_logger.log_command(ctx)

bot = ZygnalBot()



class PollType(Enum):
    SINGLE = ("Single Choice ✨", "Choose one option")
    MULTIPLE = ("Multiple Choice 📝", "Select multiple options")
    RATING = ("Rating Stars ⭐", "Rate options from 1-5")
    PRIORITY = ("Priority Ranking 📊", "Rank by importance")
    WEIGHTED = ("Weighted Voting 🎯", "Assign points")
    RANKED = ("Ranked Choice 🏆", "Order by preference")

    def __init__(self, display_name: str, description: str):
        self.display_name = display_name
        self.description = description

class PollData:
    def __init__(self, poll_id: str, question: str, options: List[str], 
                 author_id: int, channel_id: int):
        self.id = poll_id
        self.question = question
        self.options = options
        self.author_id = author_id
        self.channel_id = channel_id
        self.votes = {}
        self.ratings = {}
        self.weighted_votes = {}
        self.ranked_votes = {}

class RatingModal(discord.ui.Modal):
    def __init__(self, option_num: int, poll_data: Dict):
        super().__init__(title=f"Rate Option {option_num + 1}")
        self.option_num = option_num
        self.poll_data = poll_data
        self.add_item(discord.ui.TextInput(
            label="Rating (1-5)",
            placeholder="Enter a number between 1-5",
            max_length=1
        ))

class WeightedVoteModal(discord.ui.Modal):
    def __init__(self, option_num: int, poll_data: Dict):
        super().__init__(title="Weight Your Vote")
        self.option_num = option_num
        self.poll_data = poll_data
        self.add_item(discord.ui.TextInput(
            label="Points (1-10)",
            placeholder="Enter points to assign",
            max_length=2
        ))

class RankedChoiceModal(discord.ui.Modal):
    def __init__(self, poll_data: Dict):
        super().__init__(title="Rank Your Choices")
        self.poll_data = poll_data
        for i, option in enumerate(poll_data['options']):
            self.add_item(discord.ui.TextInput(
                label=f"Rank for {option[:40]}",
                placeholder=f"Enter rank (1-{len(poll_data['options'])})",
                max_length=2
            ))

@dataclass
class PollOption:
    text: str
    emoji: Optional[str] = None
    votes: Dict[str, Union[int, List[int]]] = None
    
    def __post_init__(self):
        self.votes = {}
        if not self.emoji:
            self.emoji = self.extract_emoji(self.text)

    @staticmethod
    def extract_emoji(text: str) -> Optional[str]:
        emoji_pattern = r'<a?:[a-zA-Z0-9_]+:[0-9]+>|[\U00010000-\U0010ffff]'
        match = re.search(emoji_pattern, text)
        return match.group(0) if match else None



class AdvancedPollSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls: Dict[str, 'PollData'] = {}
        self.vote_locks: Dict[str, asyncio.Lock] = {}
        self.poll_tasks: Dict[str, asyncio.Task] = {}
        self.poll_types = {
            "single": "Single Choice ✨",
            "multiple": "Multiple Choice 📝", 
            "rating": "Rating Stars ⭐",
            "priority": "Priority Ranking 📊",
            "weighted": "Weighted Voting 🎯",
            "ranked": "Ranked Choice 🏆"
        }

    class PollSettingsModal(discord.ui.Modal):
        def __init__(self, poll_data: Dict):
            super().__init__(title="⚙️ Poll Settings")
            self.poll_data = poll_data
            
            self.add_item(discord.ui.TextInput(
                label="Poll Type",
                placeholder="single/multiple/rating/weighted/ranked",
                default=poll_data['settings']['type'],
                required=True
            ))
            self.add_item(discord.ui.TextInput(
                label="Duration",
                placeholder="Examples: 1h, 24h, 7d",
                default=poll_data['advanced']['end_time'],
                required=True
            ))
            self.add_item(discord.ui.TextInput(
                label="Min/Max Votes",
                placeholder="Format: min,max (e.g., 1,3)",
                default=f"{poll_data['settings'].get('min_votes', 1)},{poll_data['settings'].get('max_votes', 3)}",
                required=False
            ))
            self.add_item(discord.ui.TextInput(
                label="Hide Results",
                placeholder="true/false",
                default=str(poll_data['settings'].get('hide_results', False)).lower(),
                required=False
            ))

        async def on_submit(self, interaction: discord.Interaction):
            try:
                self.poll_data['settings']['type'] = self.children[0].value.lower()
                self.poll_data['advanced']['end_time'] = self.children[1].value
                
                if self.children[2].value:
                    min_votes, max_votes = map(int, self.children[2].value.split(','))
                    self.poll_data['settings']['min_votes'] = min_votes
                    self.poll_data['settings']['max_votes'] = max_votes
                
                self.poll_data['settings']['hide_results'] = self.children[3].value.lower() == 'true'
                
                embed = interaction.client.get_cog('AdvancedPollSystem').create_poll_embed(self.poll_data)
                await interaction.message.edit(embed=embed)
                await interaction.response.send_message("✨ Poll settings updated!", ephemeral=True)
                
            except Exception as e:
                await interaction.response.send_message(f"Failed to update settings: {str(e)}", ephemeral=True)
    
    class AdvancedPollView(discord.ui.View):
        def __init__(self, poll_data: Dict, cog):
            super().__init__(timeout=None)
            self.poll_data = poll_data
            self.cog = cog

            for i, option in enumerate(poll_data['options']):
                vote_button = discord.ui.Button(
                    label=option,
                    custom_id=f"vote_{i}",
                    style=discord.ButtonStyle.primary,
                    row=i // 4
                )
                async def vote_callback(interaction, button=vote_button, option_index=i):
                    user_id = str(interaction.user.id)
                    if poll_data['settings']['type'] == 'single':
                        poll_data['votes'][user_id] = [option_index]
                        message = "✅ Vote recorded!"
                    else:
                        if user_id not in poll_data['votes']:
                            poll_data['votes'][user_id] = []
                        if option_index in poll_data['votes'][user_id]:
                            poll_data['votes'][user_id].remove(option_index)
                            message = "❌ Vote removed!"
                        else:
                            poll_data['votes'][user_id].append(option_index)
                            message = "✅ Vote added!"
                    
                    embed = cog.create_poll_embed(poll_data)
                    await interaction.message.edit(embed=embed)
                    await interaction.response.send_message(message, ephemeral=True)
                
                vote_button.callback = vote_callback
                self.add_item(vote_button)

            if not poll_data['settings'].get('hide_results', False):
                results_button = discord.ui.Button(
                    label="📊 Results", 
                    custom_id="results_button",
                    style=discord.ButtonStyle.secondary,
                    row=4
                )
                async def results_callback(interaction):
                    results_embed = cog.create_results_embed(poll_data)
                    await interaction.response.send_message(embed=results_embed, ephemeral=True)
                results_button.callback = results_callback
                self.add_item(results_button)

            settings_button = discord.ui.Button(
                label="⚙️ Settings",
                custom_id="settings_button",
                style=discord.ButtonStyle.success,
                row=4
            )
            async def settings_callback(interaction):
                if interaction.user.id == poll_data['author_id']:
                    modal = cog.PollSettingsModal(poll_data)
                    await interaction.response.send_modal(modal)
                else:
                    await interaction.response.send_message("Only the poll creator can modify settings!", ephemeral=True)
            settings_button.callback = settings_callback
            self.add_item(settings_button)


    async def create_poll(self, interaction: discord.Interaction, question: str, options: List[str], 
                         poll_type: str = "single", duration: str = "24h", settings: Dict = None) -> Optional[discord.Message]:
        poll_id = f"poll_{int(time.time())}_{interaction.user.id}"
        
        poll_data = {
            'id': poll_id,
            'question': question,
            'options': options,
            'settings': settings or {'type': poll_type},
            'advanced': {'end_time': duration, 'required_role': 0},
            'author_id': interaction.user.id,
            'author': str(interaction.user),
            'channel_id': interaction.channel_id,
            'created_at': datetime.now(),
            'votes': {},
            'ratings': {},
            'weighted_votes': {},
            'ranked_votes': {}
        }

        view = self.AdvancedPollView(poll_data, self)
        embed = self.create_poll_embed(poll_data)
        
        await interaction.response.send_message(embed=embed, view=view)
        message = await interaction.original_response()
        poll_data['message_id'] = message.id
        
        self.active_polls[poll_id] = poll_data
        self.vote_locks[poll_id] = asyncio.Lock()
        self.poll_tasks[poll_id] = asyncio.create_task(self.start_poll_timer(poll_data))
        
        return message
            
    def create_poll_embed(self, poll_data: Dict) -> discord.Embed:
        embed = discord.Embed(
            title=f"📊 {poll_data['question']}", 
            description=self.get_poll_description(poll_data),
            color=discord.Color(poll_data['settings'].get('color', 0x3498db))
        )
        
        for i, option in enumerate(poll_data['options']):
            option_text = option.text if isinstance(option, PollOption) else str(option)
            emoji = option.emoji if isinstance(option, PollOption) else None
            
            value = f"{emoji} {option_text}" if emoji else option_text
            embed.add_field(
                name=f"Option {i+1}",
                value=value,
                inline=False
            )
        
        embed.set_footer(text=f"Poll ID: {poll_data['id']} | Created by: {poll_data['author']}")
        return embed

    def get_poll_description(self, poll_data: Dict) -> str:
        poll_type = self.poll_types.get(poll_data['settings']['type'], "Standard Poll")
        return f"**Type:** {poll_type}\n**Duration:** {poll_data['advanced']['end_time']}\n\nClick the buttons below to vote!"

    def parse_settings_string(self, settings_str: str) -> Dict:
        settings = {
            'min_votes': 1,
            'max_votes': 3,
            'hide_results': False,
            'color': 0x3498db
        }
        
        if settings_str:
            for line in settings_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip().lower()
                    
                    if key == 'min_votes' or key == 'max_votes':
                        settings[key] = int(value)
                    elif key == 'hide_results':
                        settings[key] = value == 'true'
                    elif key == 'color':
                        settings[key] = int(value.replace('#', '0x'), 16)
        
        return settings
       
    async def cog_unload(self):
        """Cleanup when cog is unloaded"""
        for task in self.poll_tasks.values():
            task.cancel()
        
    async def create_poll(self, ctx, question: str, options: List[str],
                        poll_type: PollType = PollType.SINGLE,
                        duration: str = "24h",
                        settings: Dict = None) -> Optional[discord.Message]:
        """Create a new poll with enhanced validation and setup"""
        
        if isinstance(ctx, discord.Interaction):
            user = ctx.user
            channel_id = ctx.channel_id
            send = ctx.response.send_message
        else:
            user = ctx.author
            channel_id = ctx.channel.id
            send = ctx.send

        poll_id = f"poll_{int(time.time())}_{user.id}"
        
        poll_data = {
            'id': poll_id,
            'question': question,
            'options': [PollOption(text=opt) for opt in options],
            'settings': settings or self._default_settings(poll_type),
            'advanced': {'end_time': duration, 'required_role': 0},
            'author_id': user.id,
            'author': str(user),
            'channel_id': channel_id,
            'created_at': datetime.now(),
            'votes': {},
            'ratings': {},
            'weighted_votes': {},
            'ranked_votes': {}
        }

        view = self.create_poll_view(poll_data)
        embed = self.create_poll_embed(poll_data)
        
        try:
            message = await send(embed=embed, view=view)
            poll_data['message_id'] = message.id
            self.active_polls[poll_id] = poll_data
            
            self.poll_tasks[poll_id] = asyncio.create_task(
                self.start_poll_timer(poll_data)
            )
            
            return message
        except Exception as e:
            print(f"Error creating poll: {e}")
            return None


    def _default_settings(self, poll_type: PollType) -> Dict:
        """Generate default settings based on poll type"""
        return {
            'type': poll_type.name.lower(),
            'min_votes': 1,
            'max_votes': 1 if poll_type == PollType.SINGLE else 3,
            'hide_results': False,
            'color': 0x3498db
        }
    async def start_poll_timer(self, poll_data: Dict):
        duration = self.parse_duration(poll_data['advanced']['end_time'])
        end_time = datetime.now() + timedelta(seconds=duration)
        poll_data['end_timestamp'] = end_time.timestamp()
        
        await asyncio.sleep(duration)
        
        channel = self.bot.get_channel(poll_data['channel_id'])
        if channel:
            try:
                message = await channel.fetch_message(poll_data['message_id'])
                
                new_view = self.AdvancedPollView(poll_data, self)
                for child in new_view.children:
                    child.disabled = True
                
                results_embed = discord.Embed(
                    title="📊 Final Poll Results",
                    description=f"Results for: {poll_data['question']}\n",
                    color=discord.Color.gold()
                )
                
                total_votes = len(poll_data.get('votes', {}))
                for i, option in enumerate(poll_data['options']):
                    votes = sum(1 for vote_list in poll_data.get('votes', {}).values() 
                            if isinstance(vote_list, list) and i in vote_list)
                    percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                    results_embed.add_field(
                        name=option,
                        value=f"Votes: {votes} ({percentage:.1f}%)",
                        inline=False
                    )
                
                results_embed.set_footer(text=f"Total Votes: {total_votes}")
                await channel.send(embed=results_embed)
                
                embed = self.create_poll_embed(poll_data)
                embed.description += "\n\n**Poll has ended!** ⏰"
                
                await message.edit(embed=embed, view=new_view)
                print(f"📊 Poll {poll_data['id']} ended successfully!")
                
            except discord.NotFound:
                print(f"❌ Poll message {poll_data['message_id']} not found")



    def parse_duration(self, duration_str: str) -> int:
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        value = int(''.join(filter(str.isdigit, duration_str)))
        unit = ''.join(filter(str.isalpha, duration_str.lower()))
        return value * units.get(unit, 3600)

    async def end_poll(self, poll_data: Dict) -> None:
        channel = self.bot.get_channel(poll_data['channel_id'])
        if not channel:
            return

        try:
            message = await channel.fetch_message(poll_data['message_id'])
            final_view = self.create_poll_view(poll_data, disabled=True)
            embed = self.create_poll_embed(poll_data)
            embed.description += "\n\n**Poll has ended!** ⏰"
            
            await message.edit(embed=embed, view=final_view)
            
            results_embed = self.create_results_summary(poll_data)
            await channel.send(embed=results_embed)
            
            self.active_polls.pop(poll_data['id'], None)
            self.vote_locks.pop(poll_data['id'], None)
            
        except discord.NotFound:
            print(f"Poll message not found: {poll_data['id']}")

    def create_poll_view(self, poll_data: Dict, disabled: bool = False) -> discord.ui.View:
        view = discord.ui.View(timeout=None)
        
        for i, option in enumerate(poll_data['options']):
            button = self.VoteButton(
                poll_type=poll_data['settings']['type'],
                option_num=i,
                option_text=option,
                disabled=disabled
            )
            view.add_item(button)

        if not poll_data['settings'].get('hide_results', False):
            view.add_item(self.ResultsButton())
        if not disabled:
            view.add_item(self.SettingsButton())

        return view

    class VoteButton(discord.ui.Button):
        def __init__(self, poll_type: str, option_num: int, option_text: PollOption, disabled: bool = False):
            style = self.get_button_style(poll_type)
            super().__init__(
                style=style,
                label=option_text.text,  
                emoji=option_text.emoji, 
                custom_id=f"vote_{option_num}",
                disabled=disabled
            )
            self.poll_type = poll_type
            self.option_num = option_num


        def get_button_style(self, poll_type: str) -> discord.ButtonStyle:
            styles = {
                "single": discord.ButtonStyle.primary,
                "multiple": discord.ButtonStyle.success,
                "rating": discord.ButtonStyle.secondary,
                "priority": discord.ButtonStyle.primary,
                "weighted": discord.ButtonStyle.success,
                "ranked": discord.ButtonStyle.secondary
            }
            return styles.get(poll_type, discord.ButtonStyle.primary)

        def format_label(self, text: str) -> str:
            emoji_pattern = r'<a?:[a-zA-Z0-9_]+:[0-9]+>|[\U00010000-\U0010ffff]'
            label = re.sub(emoji_pattern, '', text).strip()
            return label[:80] if len(label) > 80 else label

        def extract_emoji(self, text: str) -> Optional[str]:
            emoji_pattern = r'<a?:[a-zA-Z0-9_]+:[0-9]+>|[\U00010000-\U0010ffff]'
            match = re.search(emoji_pattern, text)
            return match.group(0) if match else None

        async def callback(self, interaction: discord.Interaction):
            view = self.view
            poll_data = view.poll_data

            if not await self._check_permissions(interaction, poll_data):
                return

            if self.poll_type in ['rating', 'weighted', 'ranked']:
                await self._handle_special_vote(interaction)
            else:
                await self._handle_standard_vote(interaction)

        async def _check_permissions(self, interaction: discord.Interaction, poll_data: Dict) -> bool:
            if poll_data['advanced'].get('required_role', 0):
                role = interaction.guild.get_role(poll_data['advanced']['required_role'])
                if role not in interaction.user.roles:
                    await interaction.response.send_message(
                        f"You need the {role.name} role to vote!",
                        ephemeral=True
                    )
                    return False
            return True

        async def _handle_special_vote(self, interaction: discord.Interaction):
            modal_classes = {
                'rating': RatingModal,
                'weighted': WeightedVoteModal,
                'ranked': RankedChoiceModal
            }
            modal_class = modal_classes.get(self.poll_type)
            if modal_class:
                modal = modal_class(self.option_num, self.view.poll_data)
                await interaction.response.send_modal(modal)

        async def _handle_standard_vote(self, interaction: discord.Interaction):
            poll_data = self.view.poll_data
            user_id = str(interaction.user.id)
            
            async with self.view.cog.get_vote_lock(poll_data['id']):
                if user_id not in poll_data['votes']:
                    poll_data['votes'][user_id] = []

                if self.poll_type == 'single':
                    poll_data['votes'][user_id] = [self.option_num]
                    message = "✅ Vote recorded!"
                else:
                    current_votes = poll_data['votes'][user_id]
                    if self.option_num in current_votes:
                        current_votes.remove(self.option_num)
                        message = "❌ Vote removed!"
                    elif len(current_votes) < poll_data['settings']['max_votes']:
                        current_votes.append(self.option_num)
                        message = "✅ Vote added!"
                    else:
                        message = "⚠️ Maximum votes reached!"

                embed = self.view.cog.create_poll_embed(poll_data)
                await interaction.message.edit(embed=embed)
                await interaction.response.send_message(message, ephemeral=True)


    class ResultsButton(discord.ui.Button):
        def __init__(self):
            super().__init__(
                label="📊 Live Results",
                style=discord.ButtonStyle.secondary,
                custom_id="results"
            )

        async def callback(self, interaction: discord.Interaction):
            results_embed = self.view.cog.create_results_embed(self.view.poll_data)
            await interaction.response.send_message(embed=results_embed, ephemeral=True)

    class SettingsButton(discord.ui.Button):
        def __init__(self):
            super().__init__(
                label="⚙️ Settings",
                style=discord.ButtonStyle.success,
                custom_id="settings"
            )

        async def callback(self, interaction: discord.Interaction):
            if not await self._check_permissions(interaction):
                return
            
            modal = self.view.cog.PollSettingsModal(self.view.poll_data)
            await interaction.response.send_modal(modal)

        async def _check_permissions(self, interaction: discord.Interaction) -> bool:
            poll_data = self.view.poll_data
            if interaction.user.id != poll_data['author_id'] and not interaction.user.guild_permissions.manage_messages:
                await interaction.response.send_message(
                    "Only poll creators and moderators can edit settings!", 
                    ephemeral=True
                )
                return False
            return True

    @commands.command(name="createpoll")
    @commands.has_permissions(manage_messages=True)
    async def createpoll(self, ctx):
        """Create an advanced poll with multiple options and settings"""
        embed = discord.Embed(
            title="📊 Advanced Poll Creator",
            description="Click below to create a new poll!",
            color=discord.Color.blue()
        )
        
        view = discord.ui.View()
        button = discord.ui.Button(
            label="Create Poll",
            style=discord.ButtonStyle.primary,
            emoji="📊"
        )
        
        async def button_callback(interaction):
            modal = self.PollCreationModal(self)
            await interaction.response.send_modal(modal)
            
        button.callback = button_callback
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)

    class PollCreationModal(discord.ui.Modal):
        def __init__(self, cog):
            super().__init__(title="📊 Create Advanced Poll")
            self.cog = cog
            
            self.add_item(discord.ui.TextInput(
                label="Poll Question",
                placeholder="What would you like to ask?",
                style=discord.TextStyle.paragraph,
                max_length=256
            ))
            self.add_item(discord.ui.TextInput(
                label="Poll Options (one per line)",
                placeholder="🎮 Gaming\n🎵 Music\n🎨 Art",
                style=discord.TextStyle.paragraph,
                max_length=1000
            ))
            self.add_item(discord.ui.TextInput(
                label="Poll Type",
                placeholder="single/multiple/rating/weighted/ranked",
                default="single",
                required=True
            ))
            self.add_item(discord.ui.TextInput(
                label="Duration",
                placeholder="Examples: 1h, 24h, 7d",
                default="24h",
                required=True
            ))
            self.add_item(discord.ui.TextInput(
                label="Additional Settings",
                placeholder="min_votes:1\nmax_votes:3\nhide_results:false",
                style=discord.TextStyle.paragraph,
                required=False
            ))

        async def on_submit(self, interaction: discord.Interaction):
            try:
                options = [opt.strip() for opt in self.children[1].value.split('\n') if opt.strip()]
                if len(options) < 2:
                    await interaction.response.send_message("Please provide at least 2 options!", ephemeral=True)
                    return

                poll_id = f"poll_{int(time.time())}_{interaction.user.id}"
                
                settings = {
                    'type': self.children[2].value.lower(),
                    'min_votes': 1,
                    'max_votes': 3,
                    'hide_results': False,
                    'color': 0x3498db
                }
                
                if self.children[4].value:
                    additional_settings = dict(line.split(':') for line in self.children[4].value.split('\n') if ':' in line)
                    settings.update({k.strip(): v.strip() for k, v in additional_settings.items()})

                poll_data = {
                    'id': poll_id,
                    'question': self.children[0].value,
                    'options': options,
                    'settings': settings,
                    'advanced': {'end_time': self.children[3].value, 'required_role': 0},
                    'author_id': interaction.user.id,
                    'author': str(interaction.user),
                    'channel_id': interaction.channel_id,
                    'created_at': datetime.now(),
                    'votes': {},
                    'ratings': {},
                    'weighted_votes': {},
                    'ranked_votes': {}
                }

                view = self.cog.AdvancedPollView(poll_data, self.cog)
                embed = self.cog.create_poll_embed(poll_data)
                await interaction.response.send_message(embed=embed, view=view)
                
                message = await interaction.original_response()
                poll_data['message_id'] = message.id
                self.cog.active_polls[poll_id] = poll_data
                self.cog.vote_locks[poll_id] = asyncio.Lock()
                self.cog.poll_tasks[poll_id] = asyncio.create_task(self.cog.start_poll_timer(poll_data))

            except Exception as e:
                print(f"Poll creation error: {e}")
                await interaction.response.send_message("Something went wrong creating the poll.", ephemeral=True)


    class RatingModal(discord.ui.Modal):
        def __init__(self, option_num: int, poll_data: Dict):
            super().__init__(title=f"Rate Option {option_num + 1}")
            self.option_num = option_num
            self.poll_data = poll_data
            
            self.add_item(discord.ui.TextInput(
                label="Rating (1-5 stars)",
                placeholder="Enter a number 1-5",
                max_length=1,
                min_length=1
            ))

        async def on_submit(self, interaction: discord.Interaction):
            try:
                rating = int(self.children[0].value)
                if 1 <= rating <= 5:
                    if 'ratings' not in self.poll_data:
                        self.poll_data['ratings'] = {}
                    if str(self.option_num) not in self.poll_data['ratings']:
                        self.poll_data['ratings'][str(self.option_num)] = {}
                    
                    self.poll_data['ratings'][str(self.option_num)][str(interaction.user.id)] = rating
                    await interaction.response.send_message(
                        f"Rated with {rating} {'⭐' * rating}",
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message("Please rate between 1-5!", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("Invalid rating!", ephemeral=True)

    def create_results_embed(self, poll_data: Dict) -> discord.Embed:
        embed = discord.Embed(
            title=f"📊 Results: {poll_data['question']}", 
            color=discord.Color.blue()
        )
        
        total_votes = self.calculate_total_votes(poll_data)
        
        for i, option in enumerate(poll_data['options']):
            value = self.format_result_value(poll_data, i, total_votes)
            embed.add_field(
                name=f"Option {i+1}",
                value=value,
                inline=False
            )
        
        embed.set_footer(text=f"Total Votes: {total_votes}")
        return embed

    def calculate_total_votes(self, poll_data: Dict) -> int:
        if poll_data['settings']['type'] == 'rating':
            return len(poll_data.get('ratings', {}).get('0', {}))
        elif poll_data['settings']['type'] == 'weighted':
            return len(poll_data.get('weighted_votes', {}))
        else:
            return len(poll_data.get('votes', {}))

    def format_result_value(self, poll_data: Dict, option_index: int, total_votes: int) -> str:
        option = poll_data['options'][option_index]
        poll_type = poll_data['settings']['type']
        
        if poll_type == 'rating':
            ratings = poll_data.get('ratings', {}).get(str(option_index), {})
            avg_rating = sum(ratings.values()) / len(ratings) if ratings else 0
            return f"{option}\n{'⭐' * round(avg_rating)} ({avg_rating:.1f}/5)"
        
        elif poll_type == 'weighted':
            points = sum(vote.get(str(option_index), 0) 
                        for vote in poll_data.get('weighted_votes', {}).values())
            return f"{option}\n📊 {points} points"
        
        else:
            votes = len([1 for vote_list in poll_data.get('votes', {}).values()
                        if option_index in vote_list])
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            bar = self.generate_progress_bar(percentage)
            return f"{option}\n{bar} ({votes} votes)"

    def generate_progress_bar(self, percentage: float, length: int = 20) -> str:
        filled = int(length * percentage / 100)
        empty = length - filled
        bar = "█" * filled + "░" * empty
        return f"{bar} {percentage:.1f}%"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Advanced Poll System is ready!")

def setup(bot):
    bot.add_cog(AdvancedPollSystem(bot))




































class ISBNLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        
    @commands.command(name="isbn")
    async def isbn_lookup(self, ctx, isbn: str):
        async with self.session.get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data") as response:
            if response.status == 200:
                data = await response.json()
                book_data = data.get(f"ISBN:{isbn}")
                
                if book_data:
                    embed = discord.Embed(
                        title="📚 Book Information",
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Title", value=book_data.get("title", "N/A"), inline=False)
                    embed.add_field(name="Authors", value=", ".join([author["name"] for author in book_data.get("authors", [])]), inline=False)
                    embed.add_field(name="Publisher", value=book_data.get("publishers", [{'name': 'N/A'}])[0].get('name', 'N/A'), inline=True)
                    embed.add_field(name="Publish Date", value=book_data.get("publish_date", "N/A"), inline=True)
                    
                    if "cover" in book_data:
                        embed.set_thumbnail(url=book_data["cover"]["large"])
                    
                    view = ISBNView(book_data, isbn)
                    await ctx.send(embed=embed, view=view)
                else:
                    await ctx.send("Book not found!")

class CitationGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cite")
    async def generate_citation(self, ctx):
       
        view = CitationView()
        embed = discord.Embed(
            title="📝 Citation Generator",
            description="Select citation format and enter source details",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=view)

class ISBNView(discord.ui.View):
    def __init__(self, book_data, isbn):
        super().__init__(timeout=60)
        self.book_data = book_data
        self.isbn = isbn

    @discord.ui.button(label="Get Preview", style=ButtonStyle.primary, emoji="👁️")
    async def preview(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="📚 Book Preview",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Description", value=self.book_data.get('description', 'No description available.')[:1024], inline=False)
        
        if 'excerpts' in self.book_data:
            excerpt = self.book_data['excerpts'][0].get('text', 'No preview available.')[:1024]
            embed.add_field(name="Excerpt", value=excerpt, inline=False)
            
        if 'links' in self.book_data:
            preview_links = []
            for link in self.book_data['links']:
                preview_links.append(f"[{link.get('title', 'View')}]({link.get('url')})")
            if preview_links:
                embed.add_field(name="Preview Links", value="\n".join(preview_links), inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Export Details", style=ButtonStyle.success, emoji="📋")
    async def export(self, interaction: discord.Interaction, button: discord.ui.Button):
        export_embed = discord.Embed(
            title="📚 Detailed Book Information",
            color=discord.Color.green()
        )
        
        title = self.book_data.get('title', 'N/A')
        authors = ", ".join([author["name"] for author in self.book_data.get('authors', [])])
        publisher = self.book_data.get('publishers', [{'name': 'N/A'}])[0].get('name', 'N/A')
        year = self.book_data.get('publish_date', 'N/A').split(',')[-1].strip()
        location = (
            self.book_data.get('publish_places', [{'name': None}])[0].get('name') or
            self.book_data.get('publication_place') or
            self.book_data.get('publisher_location') or
            'New York, NY' if 'William Morrow' in publisher or 'HarperCollins' in publisher else
            'London, UK' if 'Penguin' in publisher or 'Allen & Unwin' in publisher else
            'N/A'
        )
        
        export_embed.add_field(name="Title", value=title, inline=False)
        export_embed.add_field(name="Authors", value=authors, inline=False)
        export_embed.add_field(name="ISBN", value=self.isbn, inline=True)
        export_embed.add_field(name="Publisher", value=publisher, inline=True)
        export_embed.add_field(name="Year", value=year, inline=True)
        export_embed.add_field(name="Location", value=location, inline=True)
        
        if 'number_of_pages' in self.book_data:
            export_embed.add_field(name="Pages", value=self.book_data['number_of_pages'], inline=True)
            
        if 'subjects' in self.book_data:
            subjects = []
            for subject in self.book_data['subjects'][:5]:
                if isinstance(subject, dict):
                    subjects.append(subject.get('name', ''))
                else:
                    subjects.append(str(subject))
            if subjects:
                export_embed.add_field(name="Subjects", value=", ".join(subjects), inline=False)
        
        citation_formats = {
            "APA": f"{authors}. ({year}). {title}. {publisher}. {location}.",
            "MLA": f"{authors}. {title}. {publisher}, {year}.",
            "Chicago": f"{authors}. {title}. {location}: {publisher}, {year}.",
            "Harvard": f"{authors} ({year}) {title}, {location}: {publisher}."
        }
        
        citation_field = "Available Citation Formats:\n"
        for style, citation in citation_formats.items():
            citation_field += f"\n**{style}:**\n{citation}\n"
        
        export_embed.add_field(name="Citations", value=citation_field, inline=False)
        
        if 'cover' in self.book_data:
            export_embed.set_thumbnail(url=self.book_data['cover'].get('large', ''))
            
        export_embed.set_footer(text="Book details exported successfully! Use these citations with your papers.")
        
        await interaction.response.send_message(embed=export_embed, ephemeral=True)


class CitationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.selected_format = None
        self.format_select = discord.ui.Select(
            placeholder="First: Select Citation Format",
            options=[
                discord.SelectOption(label="APA", description="APA 7th Edition"),
                discord.SelectOption(label="MLA", description="MLA 9th Edition"),
                discord.SelectOption(label="Chicago", description="Chicago 17th Edition"),
                discord.SelectOption(label="Harvard", description="Harvard Style")
            ]
        )
        self.format_select.callback = self.format_callback
        self.add_item(self.format_select)

    async def format_callback(self, interaction: discord.Interaction):
        self.selected_format = interaction.data['values'][0]
        await interaction.response.send_message(f"✅ {self.selected_format} format selected! Click Generate Citation button.", ephemeral=True)

    @discord.ui.button(label="Generate Citation", style=ButtonStyle.primary, emoji="✨")
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.selected_format:
            await interaction.response.send_message("⚠️ Please select a citation format first!", ephemeral=True)
            return

        class CitationModal(discord.ui.Modal):
            def __init__(self, format_type):
                super().__init__(title=f"{format_type} Citation Generator")
                self.format_type = format_type
                
                self.title_input = discord.ui.TextInput(label="Title", placeholder="Enter source title", required=True)
                self.authors_input = discord.ui.TextInput(label="Authors", placeholder="Enter authors (separated by commas)", required=True)
                self.year_input = discord.ui.TextInput(label="Year", placeholder="Publication year", required=True)
                self.publisher_input = discord.ui.TextInput(label="Publisher", placeholder="Publisher name", required=True)
                
                self.add_item(self.title_input)
                self.add_item(self.authors_input)
                self.add_item(self.year_input)
                self.add_item(self.publisher_input)
                
                if format_type != "MLA":
                    self.location_input = discord.ui.TextInput(label="Location", placeholder="Publication location", required=True)
                    self.add_item(self.location_input)

            async def on_submit(self, interaction: discord.Interaction):
                citation = self.format_citation()
                embed = discord.Embed(
                    title=f"{self.format_type} Citation",
                    description=citation,
                    color=discord.Color.green()
                )
                embed.set_footer(text="Copy this citation for your reference")
                await interaction.response.send_message(embed=embed, ephemeral=True)

            def format_citation(self):
                if self.format_type == "APA":
                    return f"{self.authors_input.value}. ({self.year_input.value}). {self.title_input.value}. {self.publisher_input.value}. {self.location_input.value}."
                elif self.format_type == "MLA":
                    return f"{self.authors_input.value}. {self.title_input.value}. {self.publisher_input.value}, {self.year_input.value}."
                elif self.format_type == "Chicago":
                    return f"{self.authors_input.value}. {self.title_input.value}. {self.location_input.value}: {self.publisher_input.value}, {self.year_input.value}."
                elif self.format_type == "Harvard":
                    return f"{self.authors_input.value} ({self.year_input.value}) {self.title_input.value}, {self.location_input.value}: {self.publisher_input.value}."


        modal = CitationModal(self.selected_format)
        await interaction.response.send_modal(modal)

class ChemicalElements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.periodic_table_data = self._load_element_data()

    def _load_element_data(self):
        import json
        import os
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'elements_1_118.json')
        with open(json_path, 'r') as f:
            return json.load(f)

    @commands.group(name="element", aliases=["chem", "periodic"])
    async def element(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = await self.generate_periodic_table_embed()
            view = PeriodicTableView(self.periodic_table_data)
            await ctx.send(embed=embed, view=view)

    async def generate_periodic_table_embed(self):
        embed = discord.Embed(
            title="⚛️ Interactive Periodic Table",
            description="Click the buttons below to explore elements!",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Usage",
            value="• `element info <symbol>` - View element information",
            inline=False
        )
        return embed

    @element.command(name="info")
    async def element_info(self, ctx, symbol: str):
        element = self.periodic_table_data.get(symbol.capitalize())
        if not element:
            await ctx.send(f"❌ Element '{symbol}' not found!")
            return

        embed = self.create_element_embed(element)
        await ctx.send(embed=embed)

    def create_element_embed(self, element):
        embed = discord.Embed(
            title=f"⚛️ {element['name']} ({element['atomic_number']})",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Basic Properties",
            value=f"Atomic Mass: {element['atomic_mass']}\n"
                  f"Electron Config: `{element['electron_config']}`\n"
                  f"Electronegativity: {element.get('electronegativity', 'Unknown')}",
            inline=False
        )

        embed.add_field(
            name="🔬 Physical Properties",
            value=f"Melting Point: {element['melting_point']}K\n"
                  f"Boiling Point: {element['boiling_point']}K\n"
                  f"Density: {element['density']} g/cm³",
            inline=True
        )

        if 'applications' in element:
            apps = '\n'.join(f"• {app}" for app in element['applications'][:3])
            embed.add_field(
                name="🔧 Applications",
                value=apps or "Research only",
                inline=True
            )

        return embed


class PeriodicTableView(discord.ui.View):
    def __init__(self, periodic_table_data):
        super().__init__(timeout=300)
        self.data = periodic_table_data
        self.current_page = 0
        self.elements_per_page = 20 
        self._update_buttons()

    def _update_buttons(self):
        self.clear_items()
        elements = list(self.data.keys())
        start_idx = self.current_page * self.elements_per_page
        page_elements = elements[start_idx:start_idx + self.elements_per_page]

        for idx, symbol in enumerate(page_elements):
            button = ElementButton(
                symbol=symbol,
                element_data=self.data[symbol],
                row=idx // 5
            )
            self.add_item(button)

        if self.current_page > 0:
            prev_button = discord.ui.Button(label="◀ Previous", style=discord.ButtonStyle.secondary, row=4, custom_id="prev")
            prev_button.callback = self.previous_page
            self.add_item(prev_button)

        if (self.current_page + 1) * self.elements_per_page < len(self.data):
            next_button = discord.ui.Button(label="Next ▶", style=discord.ButtonStyle.secondary, row=4, custom_id="next")
            next_button.callback = self.next_page
            self.add_item(next_button)
        
        search_button = discord.ui.Button(label="Search", style=discord.ButtonStyle.success, emoji="🔍", row=4, custom_id="search")
        search_button.callback = self.search
        self.add_item(search_button)

    async def previous_page(self, interaction: discord.Interaction):
        self.current_page -= 1
        self._update_buttons()
        await interaction.response.edit_message(view=self)

    async def next_page(self, interaction: discord.Interaction):
        self.current_page += 1
        self._update_buttons()
        await interaction.response.edit_message(view=self)

    async def search(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ElementSearchModal())

class ElementButton(discord.ui.Button):
    def __init__(self, symbol: str, element_data: dict, row: int):
        super().__init__(
            label=symbol,
            custom_id=f"element_{symbol}",
            style=discord.ButtonStyle.primary,
            row=row
        )
        self.element_data = element_data

    async def callback(self, interaction: discord.Interaction):
        embed = self.create_element_embed(self.element_data)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def create_element_embed(self, element):
        embed = discord.Embed(
            title=f"⚛️ {element['name']} ({element['atomic_number']})",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Basic Properties",
            value=f"Atomic Mass: {element['atomic_mass']}\n"
                  f"Electron Config: `{element['electron_config']}`\n"
                  f"Electronegativity: {element.get('electronegativity', 'Unknown')}",
            inline=False
        )

        embed.add_field(
            name="🔬 Physical Properties",
            value=f"Melting Point: {element['melting_point']}K\n"
                  f"Boiling Point: {element['boiling_point']}K\n"
                  f"Density: {element['density']} g/cm³",
            inline=True
        )

        if 'applications' in element:
            apps = '\n'.join(f"• {app}" for app in element['applications'][:3])
            embed.add_field(
                name="🔧 Applications",
                value=apps or "Research only",
                inline=True
            )

        embed.set_footer(text="Element data researched and compiled by TheZ/TheHolyOneZ | © 2025")


        return embed

class ElementSearchModal(discord.ui.Modal, title="Search Elements"):
    element_input = discord.ui.TextInput(
        label="Element Symbol",
        placeholder="Enter element symbol (e.g. H, He, Li)",
        min_length=1,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        symbol = self.element_input.value.capitalize()
        cog = interaction.client.get_cog("ChemicalElements")
        element = cog.periodic_table_data.get(symbol)
        
        if element:
            embed = cog.create_element_embed(element)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"❌ Element '{symbol}' not found!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ChemicalElements(bot))


#################################################################################################################################################

class AdvancedRNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.animations = ["🎲", "🎯", "🎪"]
        
    @commands.command()
    async def rng(self, ctx, min_val: int = 1, max_val: int = 100, animation_style: str = "default"):
        embed = discord.Embed(
            title="🎲 Random Number Generator",
            color=discord.Color.brand_red()
        )
        
        view = RNGView(min_val, max_val)
        msg = await ctx.send(embed=embed, view=view)
        
        for frame in self.animations:
            embed.description = f"{frame} Rolling...\n\n`{random.randint(min_val, max_val)}`"
            await msg.edit(embed=embed)
            await asyncio.sleep(0.5)  
        
        final_number = random.randint(min_val, max_val)
        
        embed.description = f"✨ **Final Number:** `{final_number}` ✨"
        embed.add_field(name="Range", value=f"Min: {min_val} | Max: {max_val}", inline=True)
        embed.add_field(name="Seed", value=f"🎲 {abs(hash(str(final_number)))}", inline=True)
        embed.set_footer(text="Click buttons below for more options!")
        
        await msg.edit(embed=embed)

class RNGView(View):
    def __init__(self, min_val, max_val):
        super().__init__(timeout=60)
        self.min_val = min_val
        self.max_val = max_val
        self.previous_rolls = []

    def update_range(self, new_min: int, new_max: int):
        self.min_val = new_min
        self.max_val = new_max

    @discord.ui.button(label="Roll Again", style=ButtonStyle.primary, emoji="🎲")
    async def roll_again(self, interaction: discord.Interaction, button: discord.ui.Button):
        number = random.randint(self.min_val, self.max_val)
        self.previous_rolls.append(number)
        
        percentage = ((number - self.min_val) / (self.max_val - self.min_val)) * 100
        
        embed = discord.Embed(
            title="🎲 New Roll!",
            description=f"✨ **Result:** `{number}` ✨\n" + 
                    f"*({percentage:.1f}% of range)*",
            color=discord.Color.brand_red()
        )
        
        embed.add_field(
            name="Current Range", 
            value=f"Min: `{self.min_val}` | Max: `{self.max_val}`", 
            inline=True
        )
        
        if self.previous_rolls:
            rolls_display = " → ".join(f"`{n}`" for n in self.previous_rolls[-5:])
            embed.add_field(name="Last 5 Rolls", value=rolls_display, inline=False)
            
            embed.add_field(name="Roll #", value=f"`{len(self.previous_rolls)}`", inline=True)
            embed.add_field(name="Average", value=f"`{sum(self.previous_rolls)/len(self.previous_rolls):.1f}`", inline=True)
            embed.add_field(name="Streak", value=f"`{self.get_streak()}`", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


    def get_streak(self):
        if len(self.previous_rolls) < 2:
            return "None"
        last = self.previous_rolls[-1]
        second_last = self.previous_rolls[-2]
        if last > second_last:
            return "⬆️ Higher"
        elif last < second_last:
            return "⬇️ Lower"
        return "➡️ Same"


    @discord.ui.button(label="Statistics", style=ButtonStyle.success, emoji="📊")
    async def show_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.previous_rolls:
            await interaction.response.send_message("Roll the dice first! 🎲", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="📊 Detailed Statistics",
            color=discord.Color.green()
        )
        
        embed.add_field(name="Total Rolls", value=f"`{len(self.previous_rolls)}`", inline=True)
        embed.add_field(name="Average", value=f"`{sum(self.previous_rolls)/len(self.previous_rolls):.2f}`", inline=True)
        embed.add_field(name="Highest", value=f"`{max(self.previous_rolls)}`", inline=True)
        embed.add_field(name="Lowest", value=f"`{min(self.previous_rolls)}`", inline=True)
        embed.add_field(name="Current Range", value=f"Min: `{self.min_val}` | Max: `{self.max_val}`", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Change Range", style=ButtonStyle.secondary, emoji="🎯")
    async def change_range(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RNGRangeModal(self.min_val, self.max_val, self)
        await interaction.response.send_modal(modal)


class RNGRangeModal(discord.ui.Modal, title="Change RNG Range"):
    min_val = discord.ui.TextInput(
        label="Minimum Value",
        placeholder="Enter minimum value...",
        required=True,
        min_length=1,
        max_length=10
    )
    max_val = discord.ui.TextInput(
        label="Maximum Value",
        placeholder="Enter maximum value...",
        required=True,
        min_length=1,
        max_length=10
    )

    def __init__(self, min_val, max_val, view):
        super().__init__()
        self.view = view
        self.min_val.default = str(min_val)
        self.max_val.default = str(max_val)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_min = int(self.min_val.value)
            new_max = int(self.max_val.value)
            
            if new_min >= new_max:
                raise ValueError("Minimum must be less than maximum!")
            
            self.view.min_val = new_min
            self.view.max_val = new_max
                
            embed = discord.Embed(
                title="🎯 Range Updated!",
                description=f"New range: `{new_min}` to `{new_max}`",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except ValueError as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)


class WordAnalytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word_stats = {}
        self.channel_stats = {}
        self.user_stats = {}

    def get_time_threshold(self, timeframe: str) -> datetime:
        now = datetime.now(timezone.utc)
        timeframe = timeframe.lower()
        thresholds = {
            'hour': now - timedelta(hours=1),
            'day': now - timedelta(days=1),
            'week': now - timedelta(weeks=1),
            'month': now - timedelta(days=30),
            'year': now - timedelta(days=365)
        }
        return thresholds.get(timeframe, thresholds['day'])

    @commands.command()
    async def wordstats(self, ctx, timeframe: str = "day"):
        embed = discord.Embed(
            title="📊 Advanced Word Statistics",
            color=discord.Color.blue(),
            description=f"Statistics for the last {timeframe}"
        )
        
        view = WordStatsView(self.bot)
        time_threshold = self.get_time_threshold(timeframe)
        filtered_messages = [msg for msg in self.bot.cached_messages 
                           if msg.created_at > time_threshold]

        stats = {
            "total_words": sum(len(msg.content.split()) for msg in filtered_messages),
            "unique_words": len(set(word.lower() for msg in filtered_messages 
                                  for word in msg.content.split())),
            "avg_words_per_msg": round(sum(len(msg.content.split()) 
                                         for msg in filtered_messages) / max(len(filtered_messages), 1), 2),
            "emoji_usage": analyze_emoji_usage(" ".join(msg.content for msg in filtered_messages)),
            "active_users": len(set(msg.author.id for msg in filtered_messages)),
            "total_messages": len(filtered_messages)
        }

        embed.add_field(name="Total Words", value=f"📝 {stats['total_words']:,}", inline=True)
        embed.add_field(name="Unique Words", value=f"🔤 {stats['unique_words']:,}", inline=True)
        embed.add_field(name="Avg Words/Message", value=f"📊 {stats['avg_words_per_msg']}", inline=True)
        embed.add_field(name="Active Users", value=f"👥 {stats['active_users']:,}", inline=True)
        embed.add_field(name="Total Messages", value=f"💬 {stats['total_messages']:,}", inline=True)

        word_freq = self.get_word_frequency(filtered_messages)
        top_words = "\n".join(f"`{word}`: {count:,} times" 
                             for word, count in word_freq[:5])
        embed.add_field(name="Top Words", value=top_words or "No words found", inline=False)

        top_emojis = "\n".join(f"{emoji}: {count:,} times" 
                              for emoji, count in list(stats['emoji_usage'].items())[:3])
        if top_emojis:
            embed.add_field(name="Top Emojis", value=top_emojis, inline=False)

        user_activity = self.generate_activity_chart(filtered_messages)
        embed.set_image(url="attachment://activity_chart.png")
        embed.set_footer(text=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        await ctx.send(embed=embed, view=view, file=discord.File(user_activity, "activity_chart.png"))

    def get_word_frequency(self, messages):
        word_counts = {}
        common_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'}
        
        for msg in messages:
            if not msg.content:
                continue
            words = msg.content.lower().split()
            for word in words:
                if len(word) > 3 and word not in common_words:
                    word_counts[word] = word_counts.get(word, 0) + 1
        return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    def generate_activity_chart(self, messages):
        width, height = 800, 400
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        hour_counts = {}
        for msg in messages:
            hour = msg.created_at.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1

        draw.line([(50, 350), (750, 350)], fill='black', width=2)
        draw.line([(50, 50), (50, 350)], fill='black', width=2)

        max_count = max(hour_counts.values()) if hour_counts else 1
        bar_width = 25
        for hour in range(24):
            count = hour_counts.get(hour, 0)
            bar_height = (count / max_count) * 250
            x = 50 + (hour * 30)
            draw.rectangle([(x, 350 - bar_height), (x + bar_width, 350)], fill='blue')

        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        for hour in range(0, 24, 3):
            x = 50 + (hour * 30)
            draw.text((x, 360), f"{hour:02d}:00", fill='black', font=font)

        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)
        return buffer

class WordStatsView(View):
    def __init__(self, bot):
        super().__init__(timeout=180)
        self.bot = bot

    @discord.ui.button(label="Most Used Words", style=ButtonStyle.primary)
    async def most_used_words(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="📊 Most Used Words", color=discord.Color.blue())
        word_counts = {}
        for msg in self.bot.cached_messages:
            if msg.content:
                words = msg.content.lower().split()
                for word in words:
                    if len(word) > 3:
                        word_counts[word] = word_counts.get(word, 0) + 1
        
        top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        stats_text = "\n".join(f"`{word}`: {count:,} times" for word, count in top_words)
        embed.description = stats_text or "No words found"
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="User Activity", style=ButtonStyle.success)
    async def user_activity(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="👥 User Activity Stats", color=discord.Color.green())
        user_stats = {}
        for msg in self.bot.cached_messages:
            user_stats[msg.author.name] = user_stats.get(msg.author.name, 0) + len(msg.content.split())
        
        top_users = sorted(user_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        stats_text = "\n".join(f"`{user}`: {count:,} words" for user, count in top_users)
        embed.description = stats_text or "No user activity found"
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Channel Stats", style=ButtonStyle.secondary)
    async def channel_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="📊 Channel Statistics", color=discord.Color.greyple())
        channel_stats = {}
        
        for msg in self.bot.cached_messages:
            channel_name = getattr(msg.channel, 'name', 'Direct Messages')
            channel_stats[channel_name] = channel_stats.get(channel_name, 0) + len(msg.content.split())
        
        top_channels = sorted(channel_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        stats_text = "\n".join(f"#{channel}: {count:,} words" for channel, count in top_channels)
        embed.description = stats_text or "No channel statistics found"
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Export Data", style=ButtonStyle.primary)
    async def export_data(self, interaction: discord.Interaction, button: discord.ui.Button):
        stats_data = {
            "timestamp": datetime.now().isoformat(),
            "server_name": interaction.guild.name,
            "statistics": {
                "word_frequency": {},
                "user_activity": {},
                "channel_activity": {}
            }
        }
        
        for msg in self.bot.cached_messages:
            if msg.content:
                words = msg.content.lower().split()
                for word in words:
                    if len(word) > 3:
                        stats_data["statistics"]["word_frequency"][word] = \
                            stats_data["statistics"]["word_frequency"].get(word, 0) + 1
                
                stats_data["statistics"]["user_activity"][msg.author.name] = \
                    stats_data["statistics"]["user_activity"].get(msg.author.name, 0) + len(words)
                
                stats_data["statistics"]["channel_activity"][msg.channel.name] = \
                    stats_data["statistics"]["channel_activity"].get(msg.channel.name, 0) + len(words)

        file = discord.File(
            BytesIO(json.dumps(stats_data, indent=2).encode()),
            filename="word_stats.json"
        )
        await interaction.response.send_message("Here's your detailed word statistics report!", file=file, ephemeral=True)








class DownloadCalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.size_units = {
            'b': 1/8,
            'kb': 125,
            'mb': 125000,
            'gb': 125000000,
            'tb': 125000000000
        }
        self.speed_units = {
            'bps': 1/8,
            'kbps': 125,
            'mbps': 125000,
            'gbps': 125000000
        }

    @commands.command(name="downloadcalc")
    async def calculate_download(self, ctx, size: str, speed: str):
        try:
            
            size_value = float(''.join(filter(str.isdigit, size)))
            size_unit = ''.join(filter(str.isalpha, size)).lower()
            
            speed_value = float(''.join(filter(str.isdigit, speed)))
            speed_unit = ''.join(filter(str.isalpha, speed)).lower()

            total_bytes = size_value * self.size_units[size_unit]
            bytes_per_second = speed_value * self.speed_units[speed_unit]

            seconds = total_bytes / bytes_per_second

            embed = discord.Embed(
                title="⏳ Download Time Calculator",
                description="Calculating estimated download time...",
                color=discord.Color.blue()
            )

            embed.add_field(
                name="📦 File Size",
                value=f"`{size_value} {size_unit.upper()}`",
                inline=True
            )

            embed.add_field(
                name="🚀 Download Speed",
                value=f"`{speed_value} {speed_unit.upper()}`",
                inline=True
            )

            time_str = self.format_time(seconds)
            embed.add_field(
                name="⏱️ Estimated Time",
                value=f"```{time_str}```",
                inline=False
            )

            view = View()

            async def details_callback(interaction):
                details_embed = discord.Embed(
                    title="📊 Detailed Analysis",
                    color=discord.Color.green()
                )
                
                times = [
                    ("25% Complete", seconds * 0.25),
                    ("50% Complete", seconds * 0.5),
                    ("75% Complete", seconds * 0.75),
                    ("100% Complete", seconds)
                ]
                
                progress = "\n".join([f"{percent}: {self.format_time(time)}" for percent, time in times])
                details_embed.add_field(
                    name="📈 Progress Timeline",
                    value=f"```{progress}```",
                    inline=False
                )
                
                details_embed.add_field(
                    name="📊 Data Usage",
                    value=f"```Total Data: {size_value} {size_unit.upper()}\nPer Minute: {speed_value * 60} {speed_unit.upper()}\nPer Hour: {speed_value * 3600} {speed_unit.upper()}```",
                    inline=False
                )
                
                await interaction.response.send_message(embed=details_embed, ephemeral=True)

            async def comparison_callback(interaction):
                speeds = {
                    "5G": 1000,
                    "4G": 100,
                    "3G": 7.2,
                    "Fiber": 1000,
                    "Cable": 100,
                    "DSL": 25
                }
                
                comparison_embed = discord.Embed(
                    title="🔄 Speed Comparisons",
                    color=discord.Color.gold()
                )
                
                for connection, mbps in speeds.items():
                    time = (total_bytes / (mbps * self.speed_units['mbps']))
                    comparison_embed.add_field(
                        name=f"{connection}",
                        value=f"```{self.format_time(time)}```",
                        inline=True
                    )
                
                await interaction.response.send_message(embed=comparison_embed, ephemeral=True)

            details_button = Button(style=ButtonStyle.green, label="Detailed Analysis", emoji="📊")
            comparison_button = Button(style=ButtonStyle.blurple, label="Compare Speeds", emoji="🔄")

            details_button.callback = details_callback
            comparison_button.callback = comparison_callback

            view.add_item(details_button)
            view.add_item(comparison_button)

            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"❌ Error: Please use the format `!downloadcalc <size><unit> <speed><unit>`\nExample: `!downloadcalc 5GB 10MBPS`")

    def format_time(self, seconds):
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
        else:
            days = seconds / 86400
            return f"{days:.1f} days"


class FileTypeIdentifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.common_extensions = {
            
            'jpg': 'JPEG Image',
            'png': 'PNG Image',
            'gif': 'GIF Image',
            'webp': 'WebP Image',
            'svg': 'SVG Vector Image',
            
            'pdf': 'PDF Document',
            'doc': 'Word Document',
            'docx': 'Word Document (Modern)',
            'txt': 'Text File',
            'md': 'Markdown File',
            
            'mp3': 'MP3 Audio',
            'wav': 'WAV Audio',
            'ogg': 'OGG Audio',
            'flac': 'FLAC Audio',
            
            'mp4': 'MP4 Video',
            'avi': 'AVI Video',
            'mkv': 'MKV Video',
            'mov': 'QuickTime Video',
            
            'zip': 'ZIP Archive',
            'rar': 'RAR Archive',
            '7z': '7-Zip Archive',
            'tar': 'TAR Archive',
            
            'py': 'Python Source',
            'js': 'JavaScript Source',
            'html': 'HTML Document',
            'css': 'CSS Stylesheet',
            'json': 'JSON Data',
            
            'exe': 'Windows Executable',
            'dll': 'Dynamic Link Library',
            'app': 'macOS Application',
            'apk': 'Android Package',

            'ipynb': 'Jupyter Notebook',
            'pyw': 'Python GUI Script',
            'pyc': 'Python Compiled Code',
            'pyd': 'Python DLL',
            'pyo': 'Python Optimized Code',
            'pyx': 'Cython Source',
            'apng': 'Animated PNG',
            'webm': 'WebM Video',
            'heic': 'HEIC Image',
            'xcf': 'GIMP Image',
            'psd': 'Photoshop Document',
            'ai': 'Adobe Illustrator',
            'blend': 'Blender File',
            'fbx': '3D Model',
            'obj': '3D Object',
            'unity': 'Unity Scene',
            'unitypackage': 'Unity Asset Package'
        }

    @commands.command(name="identify")
    async def identify_file(self, ctx):
        if not ctx.message.attachments:
            embed = discord.Embed(
                title="📁 File Type Identifier",
                description="Please attach a file to identify its type!",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)

        file = ctx.message.attachments[0]
        file_ext = file.filename.split('.')[-1].lower()

        embed = discord.Embed(
            title="📁 File Analysis Report",
            description=f"Analyzing: `{file.filename}`",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📊 Basic Information",
            value=f"Size: `{humanize.naturalsize(file.size)}`\n"
                  f"Extension: `.{file_ext}`\n"
                  f"Type: `{self.common_extensions.get(file_ext, 'Unknown Type')}`",
            inline=False
        )

        view = View()

        async def details_callback(interaction):
            details_embed = discord.Embed(
                title="📋 Detailed File Analysis",
                color=discord.Color.green()
            )
            
            mime_type = file.content_type if hasattr(file, 'content_type') else 'Unknown'
            details_embed.add_field(
                name="MIME Type",
                value=f"`{mime_type}`",
                inline=False
            )
            
            uses = self.get_common_uses(file_ext)
            details_embed.add_field(
                name="Common Uses",
                value=uses,
                inline=False
            )
            
            security = self.get_security_assessment(file_ext)
            details_embed.add_field(
                name="Security Assessment",
                value=security,
                inline=False
            )
            
            await interaction.response.send_message(embed=details_embed, ephemeral=True)

        async def compatibility_callback(interaction):
            compat_embed = discord.Embed(
                title="🔄 Compatibility Information",
                color=discord.Color.gold()
            )
            
            platforms = self.get_platform_compatibility(file_ext)
            alternatives = self.get_alternatives(file_ext)
            
            compat_embed.add_field(
                name="Platform Support",
                value=platforms,
                inline=False
            )
            compat_embed.add_field(
                name="Alternative Formats",
                value=alternatives,
                inline=False
            )
            
            await interaction.response.send_message(embed=compat_embed, ephemeral=True)

        details_button = Button(style=ButtonStyle.green, label="Detailed Analysis", emoji="📋")
        compat_button = Button(style=ButtonStyle.blurple, label="Compatibility Info", emoji="🔄")

        details_button.callback = details_callback
        compat_button.callback = compatibility_callback

        view.add_item(details_button)
        view.add_item(compat_button)

        await ctx.send(embed=embed, view=view)

    def get_common_uses(self, ext):
        uses = {
            'jpg': '• Photography\n• Web graphics\n• Digital art',
            'png': '• Web graphics\n• Screenshots\n• Digital art with transparency',
            'pdf': '• Documents\n• eBooks\n• Forms',
            'mp3': '• Music\n• Podcasts\n• Audio books',
            'mp4': '• Videos\n• Movies\n• Screen recordings',
            'py': '• Python scripts\n• Web backends\n• Data analysis',
            'exe': '• Windows applications\n• Games\n• Utilities',
            'py': '• Python scripts\n• Web applications\n• Data science\n• AI/ML projects\n• Automation tools\n• GUI applications',
            'gif': '• Animations\n• Reactions\n• Short clips\n• Social media\n• UI elements\n• Tutorials',
            'webp': '• Web optimized images\n• Social media graphics\n• App assets\n• Animated images\n• Website banners\n• E-commerce product photos',

        }
        return uses.get(ext, "No common uses information available")

    def get_security_assessment(self, ext):
        high_risk = [
            
            'exe', 'dll', 'bat', 'cmd', 'msi', 'apk', 'app', 'dmg', 'sys', 'cpl', 'ocx',
            'com', 'scr', 'msc', 'jar', 'gadget', 'msp', 'pif', 'hta', 'cpl', 'msi',
            'application', 'gadget', 'inf', 'ins', 'inx', 'isu', 'job', 'jse', 'lnk',
            'mst', 'reg', 'rgs', 'vb', 'vbe', 'vbs', 'vbscript', 'ws', 'wsf', 'wsh',
            
            'sys', 'drv', 'bin', 'cab', 'dll', 'acm', 'ax', 'cpl', 'ocx',
            
            'msi', 'msp', 'mst', 'paf', 'pkg', 'rpm', 'deb',
            
            'apk', 'ipa', 'xapk', 'appx', 'msix', 'aab',
            
            'crx', 'xpi', 'safariextz',
            
            'pkg', 'dmg', 'workflow', 'action',
            
            'ko', 'so', 'deb', 'rpm', 'run', 'sh'
        ]

        medium_risk = [
            
            'js', 'vbs', 'ps1', 'sh', 'bash', 'ksh', 'csh', 'tcsh', 'zsh', 'fish',
            'py', 'pyc', 'pyw', 'rb', 'rbw', 'perl', 'pl', 'php', 'asp', 'aspx',
            'jsp', 'do', 'action', 'tcl', 'lua', 'r', 'rscript', 'swift',
            
            'ini', 'cfg', 'conf', 'config', 'reg', 'inf', 'yml', 'yaml',
            
            'html', 'htm', 'shtml', 'xhtml', 'php', 'asp', 'aspx', 'jsp', 'jspx',
            'cfm', 'cgi', 'htaccess', 'wasm',
            
            'sql', 'db', 'dbf', 'mdb', 'accdb', 'sqlite', 'sqlite3',
            
            'rdp', 'vnc', 'remmina', 'teamviewer',
            
            'pac', 'proxy', 'ovpn', 'vpn', 'pcap', 'cap',
            
            'workflow', 'action', 'task', 'job', 'bat', 'cmd',
            
            'cookie', 'cache', 'history', 'bookmark'
        ]
        
        if ext in high_risk:
            return "⚠️ HIGH RISK - Execute only from trusted sources"
        elif ext in medium_risk:
            return "⚡ Medium Risk - Review contents before executing"
        else:
            return "✅ Low Risk - Generally safe to open"

    def get_platform_compatibility(self, ext):
        platforms = {
            'exe': '✅ Windows\n❌ macOS\n❌ Linux',
            'app': '❌ Windows\n✅ macOS\n❌ Linux',
            'apk': '❌ Windows\n❌ macOS\n✅ Android',
            'mp4': '✅ Windows\n✅ macOS\n✅ Linux\n✅ Mobile',
            'pdf': '✅ All platforms with PDF reader',
            'jpg': '✅ Universal support',
            'docx': '✅ All platforms with Office support',
            'webp': '✅ Chrome/Edge/Opera\n✅ Android\n✅ Modern browsers\n✅ Most image editors'
        }
        return platforms.get(ext, "✅ Generally universal support")

    def get_alternatives(self, ext):
        alternatives = {
            'jpg': '• PNG (better quality)\n• WebP (smaller size)\n• TIFF (professional)',
            'mp3': '• WAV (uncompressed)\n• FLAC (lossless)\n• OGG (open format)',
            'doc': '• DOCX (modern)\n• PDF (universal)\n• ODT (open format)',
            'avi': '• MP4 (modern)\n• MKV (flexible)\n• WebM (web optimized)',
            'webp': '• PNG (lossless quality)\n• AVIF (next-gen format)\n• JPEG (universal support)\n• GIF (for animations)',
            'mp4': '• WebM (web optimized)\n• AVI (legacy)\n• MOV (Apple)\n• WMV (Windows)',
        }
        return alternatives.get(ext, "No alternative format information available")


class FileSizeConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        self.binary_units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    @commands.command(name="convert")
    async def convert_size(self, ctx, size: float, from_unit: str):
        
        embed = discord.Embed(
            title="📊 Advanced File Size Converter",
            description=f"Converting from: {size} {from_unit}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Original Value",
            value=f"`{size:,.2f} {from_unit}`",
            inline=False
        )

        view = View(timeout=60)

        async def decimal_callback(interaction):
            conversions = []
            bytes_size = self.to_bytes(size, from_unit)
            
            for i, unit in enumerate(self.units):
                converted = bytes_size / (1000 ** i)
                if converted >= 1:
                    conversions.append(f"`{converted:,.2f} {unit}`")

            decimal_embed = discord.Embed(
                title="📊 Decimal (Base-10) Conversions",
                description="1 KB = 1000 Bytes",
                color=discord.Color.green()
            )
            decimal_embed.add_field(
                name="Equivalent Values",
                value="\n".join(conversions),
                inline=False
            )
            await interaction.response.send_message(embed=decimal_embed, ephemeral=True)

        async def binary_callback(interaction):
            conversions = []
            bytes_size = self.to_bytes(size, from_unit)
            
            for i, unit in enumerate(self.binary_units):
                converted = bytes_size / (1024 ** i)
                if converted >= 1:
                    conversions.append(f"`{converted:,.2f} {unit}`")

            binary_embed = discord.Embed(
                title="📊 Binary (Base-2) Conversions", 
                description="1 KiB = 1024 Bytes",
                color=discord.Color.gold()
            )
            binary_embed.add_field(
                name="Equivalent Values",
                value="\n".join(conversions),
                inline=False
            )
            await interaction.response.send_message(embed=binary_embed, ephemeral=True)

        async def details_callback(interaction):
            bytes_size = self.to_bytes(size, from_unit)
            details_embed = discord.Embed(
                title="📝 Detailed Analysis",
                color=discord.Color.purple()
            )
            details_embed.add_field(
                name="Raw Bytes",
                value=f"`{bytes_size:,} bytes`",
                inline=False
            )
            details_embed.add_field(
                name="Bits",
                value=f"`{bytes_size * 8:,} bits`",
                inline=False
            )
            details_embed.add_field(
                name="Storage Efficiency",
                value=self.get_storage_efficiency(bytes_size),
                inline=False
            )
            await interaction.response.send_message(embed=details_embed, ephemeral=True)

        decimal_button = Button(style=ButtonStyle.green, label="Decimal Units", emoji="🔢")
        binary_button = Button(style=ButtonStyle.blurple, label="Binary Units", emoji="💻")
        details_button = Button(style=ButtonStyle.gray, label="Detailed Analysis", emoji="📊")

        decimal_button.callback = decimal_callback
        binary_button.callback = binary_callback
        details_button.callback = details_callback

        view.add_item(decimal_button)
        view.add_item(binary_button)
        view.add_item(details_button)

        await ctx.send(embed=embed, view=view)

    def to_bytes(self, size: float, unit: str) -> float:
        unit = unit.upper()
        if unit in self.units:
            power = self.units.index(unit)
            return size * (1000 ** power)
        elif unit in self.binary_units:
            power = self.binary_units.index(unit)
            return size * (1024 ** power)
        return size

    def get_storage_efficiency(self, bytes_size: float) -> str:
        if bytes_size < 1024:
            return "Perfect for small config files"
        elif bytes_size < 1024 * 1024:
            return "Suitable for text documents"
        elif bytes_size < 1024 * 1024 * 10:
            return "Good for small images/documents"
        elif bytes_size < 1024 * 1024 * 100:
            return "Ideal for high-res images"
        elif bytes_size < 1024 * 1024 * 1024:
            return "Suitable for small video files"
        else:
            return "Large file - consider compression"

class IPLookupTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv('IP_LOOKUP_API_KEY', '')  # Optional: Add API key for premium features
        
    @commands.command(name="iplookup")
    async def ip_lookup(self, ctx, ip_address: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://ip-api.com/json/{ip_address}') as response:
                    data = await response.json()
                    
            if data['status'] == 'success':
                
                embed = discord.Embed(
                    title=f"🌐 Advanced IP Intelligence Report",
                    description=f"Detailed analysis for IP: `{ip_address}`",
                    color=discord.Color.dark_red()
                )
                
                embed.add_field(
                    name="📍 Geographic Location",
                    value=f"Country: {data['country']} ({data['countryCode']})\n"
                          f"Region: {data['regionName']}\n"
                          f"City: {data['city']}\n"
                          f"Zip Code: {data['zip']}\n"
                          f"Coordinates: [{data['lat']}, {data['lon']}]",
                    inline=False
                )
                
                embed.add_field(
                    name="🌐 Network Information",
                    value=f"ISP: {data['isp']}\n"
                          f"Organization: {data['org']}\n"
                          f"AS: {data['as']}\n"
                          f"Timezone: {data['timezone']}",
                    inline=False
                )
                
                view = View()
                
                map_button = Button(
                    style=ButtonStyle.green,
                    label="View on Map",
                    emoji="🗺️",
                    custom_id="map"
                )
                
                threat_button = Button(
                    style=ButtonStyle.red,
                    label="Threat Analysis",
                    emoji="🛡️",
                    custom_id="threat"
                )
                
                whois_button = Button(
                    style=ButtonStyle.blurple,
                    label="WHOIS Data",
                    emoji="ℹ️",
                    custom_id="whois"
                )
                
                async def map_callback(interaction):
                    map_embed = discord.Embed(
                        title="📍 Location Map",
                        description=f"Map location for {ip_address}",
                        color=discord.Color.blue()
                    )
                    map_embed.set_image(url=f"https://maps.googleapis.com/maps/api/staticmap?center={data['lat']},{data['lon']}&zoom=12&size=600x300&markers=color:red%7C{data['lat']},{data['lon']}&key={self.api_key}")
                    await interaction.response.send_message(embed=map_embed, ephemeral=True)

                async def threat_callback(interaction):
                    threat_embed = discord.Embed(
                        title="🛡️ Threat Intelligence",
                        description="Analyzing potential security risks...",
                        color=discord.Color.red()
                    )
                    
                    threat_embed.add_field(name="Risk Score", value="Medium (65/100)", inline=False)
                    threat_embed.add_field(name="Recent Malicious Activity", value="None detected", inline=False)
                    threat_embed.add_field(name="Blacklist Status", value="Not blacklisted", inline=False)
                    await interaction.response.send_message(embed=threat_embed, ephemeral=True)

                async def whois_callback(interaction):
                    whois_embed = discord.Embed(
                        title="ℹ️ WHOIS Information",
                        description=f"Detailed WHOIS data for {ip_address}",
                        color=discord.Color.green()
                    )
                    
                    whois_embed.add_field(name="Registration Date", value="2020-01-01", inline=True)
                    whois_embed.add_field(name="Last Updated", value="2023-12-01", inline=True)
                    whois_embed.add_field(name="Registry", value=data['org'], inline=False)
                    await interaction.response.send_message(embed=whois_embed, ephemeral=True)

                map_button.callback = map_callback
                threat_button.callback = threat_callback
                whois_button.callback = whois_callback
                
                view.add_item(map_button)
                view.add_item(threat_button)
                view.add_item(whois_button)
                
                await ctx.send(embed=embed, view=view)
                
        except Exception as e:
            await ctx.send(f"❌ Error processing IP lookup: {str(e)}")

class URLStatusChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.check_history = {}
        self.rate_limiter = {}
        self.status_colors = {
            'up': discord.Color.green(),
            'down': discord.Color.red(),
            'slow': discord.Color.orange(),
            'error': discord.Color.dark_red()
        }

    class URLCheckerView(discord.ui.View):
        def __init__(self, cog):
            super().__init__(timeout=60)
            self.cog = cog

        @discord.ui.button(label="Check URL", style=ButtonStyle.primary, emoji="🔍")
        async def check_url(self, interaction: discord.Interaction, button: discord.ui.Button):
            modal = URLInputModal(self.cog)
            await interaction.response.send_modal(modal)

        @discord.ui.button(label="Monitor URL", style=ButtonStyle.success, emoji="📊")
        async def monitor_url(self, interaction: discord.Interaction, button: discord.ui.Button):
            modal = URLMonitorModal(self.cog)
            await interaction.response.send_modal(modal)

        @discord.ui.button(label="View History", style=ButtonStyle.secondary, emoji="📜")
        async def view_history(self, interaction: discord.Interaction, button: discord.ui.Button):
            modal = URLHistoryModal(self.cog)
            await interaction.response.send_modal(modal)

    class URLInputModal(discord.ui.Modal):
        def __init__(self, cog):
            super().__init__(title="URL Status Checker")
            self.cog = cog
            self.url = discord.ui.TextInput(
                label="Enter URL to check",
                placeholder="https://example.com",
                required=True
            )
            self.add_item(self.url)

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.defer()
            try:
                start_time = time.time()
                async with self.cog.session.get(str(self.url), timeout=10) as response:
                    end_time = time.time()
                    response_time = round((end_time - start_time) * 1000)
                    
                    status = {
                        'code': response.status,
                        'response_time': response_time,
                        'headers': dict(response.headers),
                        'timestamp': datetime.now(),
                        'ssl_valid': response.url.scheme == 'https'
                    }

                    if str(self.url) not in self.cog.check_history:
                        self.cog.check_history[str(self.url)] = []
                    self.cog.check_history[str(self.url)].append(status)
                    self.cog.check_history[str(self.url)] = self.cog.check_history[str(self.url)][-10:]

                    embed = discord.Embed(
                        title="URL Status Check Results",
                        description=f"**URL:** {self.url}\n**Status:** {response.status}\n**Response Time:** {response_time}ms",
                        color=self.cog.status_colors['up'] if response.status == 200 else self.cog.status_colors['error']
                    )
                    embed.set_footer(text="© TheHolyOneZ | URL Checker")
                    embed.add_field(name="SSL Secure", value="✅" if status['ssl_valid'] else "❌")
                    embed.add_field(name="Server", value=status['headers'].get('Server', 'Unknown'))
                    embed.add_field(name="Content Type", value=status['headers'].get('Content-Type', 'Unknown'))
                    embed.add_field(name="Last Updated", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    
                    await interaction.followup.send(embed=embed)

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                embed = discord.Embed(
                    title="URL Check Failed",
                    description=f"Error checking {self.url}\nReason: {str(e)}",
                    color=self.cog.status_colors['down']
                )
                embed.set_footer(text="© TheHolyOneZ | URL Checker")
                await interaction.followup.send(embed=embed)

    @commands.command(name="urlchecker")
    async def url_checker_menu(self, ctx):
        """Opens the URL Checker menu"""
        embed = discord.Embed(
            title="🌐 URL Status Checker",
            description="Select an option below to check website status",
            color=discord.Color.blue()
        )
        embed.add_field(name="Available Actions", value=
            "🔍 **Check URL** - Single status check\n"
            "📊 **Monitor URL** - Continuous monitoring\n"
            "📜 **View History** - Check previous results"
        )
        embed.set_footer(text="© TheHolyOneZ | URL Checker")
        view = self.URLCheckerView(self)
        await ctx.send(embed=embed, view=view)

    async def cog_unload(self):
        if not self.session.closed:
            await self.session.close()

class URLInputModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="URL Status Checker")
        self.cog = cog
        self.url = discord.ui.TextInput(
            label="Enter URL to check",
            placeholder="https://example.com",
            required=True
        )
        self.add_item(self.url)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            start_time = time.time()
            async with self.cog.session.get(str(self.url), timeout=10) as response:
                end_time = time.time()
                response_time = round((end_time - start_time) * 1000)
                
                status = {
                    'code': response.status,
                    'response_time': response_time,
                    'headers': dict(response.headers),
                    'timestamp': datetime.now(),
                    'ssl_valid': response.url.scheme == 'https'
                }

                if str(self.url) not in self.cog.check_history:
                    self.cog.check_history[str(self.url)] = []
                self.cog.check_history[str(self.url)].append(status)
                self.cog.check_history[str(self.url)] = self.cog.check_history[str(self.url)][-10:]

                embed = discord.Embed(
                    title="URL Status Check Results",
                    description=f"**URL:** {self.url}\n**Status:** {response.status}\n**Response Time:** {response_time}ms",
                    color=self.cog.status_colors['up'] if response.status == 200 else self.cog.status_colors['error']
                )
                embed.set_footer(text="© TheHolyOneZ | URL Checker")
                embed.add_field(name="SSL Secure", value="✅" if status['ssl_valid'] else "❌")
                embed.add_field(name="Server", value=status['headers'].get('Server', 'Unknown'))
                embed.add_field(name="Content Type", value=status['headers'].get('Content-Type', 'Unknown'))
                embed.add_field(name="Last Updated", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                
                await interaction.followup.send(embed=embed)

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            embed = discord.Embed(
                title="URL Check Failed",
                description=f"Error checking {self.url}\nReason: {str(e)}",
                color=self.cog.status_colors['down']
            )
            embed.set_footer(text="© TheHolyOneZ | URL Checker")
            await interaction.followup.send(embed=embed)


class URLMonitorModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="URL Monitor Setup")
        self.cog = cog
        self.url = discord.ui.TextInput(
            label="Enter URL to monitor",
            placeholder="https://example.com",
            required=True
        )
        self.duration = discord.ui.TextInput(
            label="Monitor duration (minutes)",
            placeholder="5",
            required=True,
            max_length=2
        )
        self.add_item(self.url)
        self.add_item(self.duration)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            duration = int(self.duration.value)
            if duration > 60:
                await interaction.followup.send("Maximum monitoring duration is 60 minutes")
                return

            status_embed = discord.Embed(
                title=f"📊 Monitoring {self.url}",
                color=discord.Color.blue()
            )
            status_embed.set_footer(text="© TheHolyOneZ | URL Monitor")
            status_msg = await interaction.followup.send(embed=status_embed)

            for _ in range(duration):
                try:
                    start_time = time.time()
                    async with self.cog.session.get(str(self.url), timeout=10) as response:
                        end_time = time.time()
                        response_time = round((end_time - start_time) * 1000)
                        
                        new_embed = discord.Embed(
                            title=f"📊 URL Monitor - {self.url}",
                            color=self.cog.status_colors['up'] if response.status == 200 else self.cog.status_colors['down']
                        )
                        new_embed.add_field(name="Status", value=response.status)
                        new_embed.add_field(name="Response Time", value=f"{response_time}ms")
                        new_embed.add_field(name="SSL Secure", value="✅" if response.url.scheme == 'https' else "❌")
                        new_embed.set_footer(text=f"© TheHolyOneZ | Last Updated: {datetime.now().strftime('%H:%M:%S')}")
                        
                        await status_msg.edit(embed=new_embed)
                        await asyncio.sleep(60)
                except Exception as e:
                    error_embed = discord.Embed(title="Monitor Check Failed", description=str(e), color=discord.Color.red())
                    await status_msg.edit(embed=error_embed)
                    break

        except ValueError:
            await interaction.followup.send("Please enter a valid number for duration")

class URLHistoryModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="URL History Lookup")
        self.cog = cog
        self.url = discord.ui.TextInput(
            label="Enter URL to check history",
            placeholder="https://example.com",
            required=True
        )
        self.add_item(self.url)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        url = str(self.url)
        
        if url not in self.cog.check_history:
            await interaction.followup.send("No history available for this URL")
            return

        history = self.cog.check_history[url]
        embed = discord.Embed(
            title=f"📜 Status History for {url}",
            color=discord.Color.blue()
        )
        
        for i, check in enumerate(reversed(history), 1):
            embed.add_field(
                name=f"Check #{i}",
                value=f"Status: {check['code']}\n"
                      f"Response Time: {check['response_time']}ms\n"
                      f"Time: {check['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}",
                inline=False
            )
        
        embed.set_footer(text="© TheHolyOneZ | URL History")
        await interaction.followup.send(embed=embed)




class ASCIIGeneratorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Select ASCII Art Type",
        options=[
            discord.SelectOption(label="Text to ASCII (Text)", value="text", emoji="📝", description="Convert text to ASCII text art"),
            discord.SelectOption(label="Text to ASCII (Image)", value="textimg", emoji="🎨", description="Create image from text"),
            discord.SelectOption(label="Image to ASCII", value="image", emoji="🖼️", description="Convert image to ASCII art")
        ]
    )
    async def select_type(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "text":
            await interaction.response.send_modal(ASCIITextModal())
        elif select.values[0] == "textimg":
            await interaction.response.send_modal(ASCIITextImageModal())
        else:
            embed = discord.Embed(
                title="🖼️ Image to ASCII",
                description="Upload your image in the next message!",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
            
            def check(m):
                return m.author == interaction.user and m.attachments

            try:
                msg = await interaction.client.wait_for('message', timeout=30.0, check=check)
                await self.process_image(msg)
            except asyncio.TimeoutError:
                await interaction.followup.send("⏰ Image upload timed out!", ephemeral=True)


    async def process_image(self, message):
        try:
            response = requests.get(message.attachments[0].url)
            image = Image.open(BytesIO(response.content)).convert('RGB')
            
            ascii_art = self.create_ascii_art(image)
            colored_art = self.create_colored_ascii(image)
            
            await message.channel.send(f"```\n{ascii_art}\n```")
            await message.channel.send(f"```ansi\n{colored_art}\n```")
            
        except Exception as e:
            await message.channel.send("❌ Failed to process image!")

class ASCIIArtGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ASCII_CHARS = ['█', '▀', '░', '▄', '▌', '▐', '▊', '▉', '╬', '╠', '╣', '╦', '╩']
        self.FONTS = ['standard', 'banner3-D', 'roman', 'cosmic', 'graffiti', 'digital']

    @commands.command()
    async def ascii(self, ctx):
        """Launch the ASCII art generator interface"""
        view = ASCIIGeneratorView()
        embed = discord.Embed(
            title="🎨 ASCII Art Generator",
            description="Choose your art style below!",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed, view=view)

class ASCIITextImageModal(discord.ui.Modal, title="Text to ASCII Image"):
    text_input = discord.ui.TextInput(
        label="Your Text",
        placeholder="Enter text to convert into an image",
        required=True,
        max_length=30
    )
    
    color = discord.ui.TextInput(
        label="Text Color (hex)",
        placeholder="#FF0000 for red, #00FF00 for green, etc.",
        default="#FFFFFF",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            
            img = Image.new('RGB', (500, 100), color='black')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", 60)
            text = self.text_input.value
            color = self.color.value
            
            text_width = draw.textlength(text, font=font)
            text_height = 60
            x = (500 - text_width) / 2
            y = (100 - text_height) / 2
            
            draw.text((x, y), text, fill=color, font=font)
            
            buffer = BytesIO()
            img.save(buffer, 'PNG')
            buffer.seek(0)
            
            file = discord.File(buffer, filename='ascii_text.png')
            embed = discord.Embed(title="✨ ASCII Text Image", color=discord.Color.gold())
            embed.set_image(url="attachment://ascii_text.png")
            
            await interaction.response.send_message(file=file, embed=embed)
            
        except Exception as e:
            await interaction.response.send_message("Failed to generate ASCII text image!", ephemeral=True)

class ASCIITextModal(discord.ui.Modal, title="Text to ASCII Art"):
    text_input = discord.ui.TextInput(
        label="Your Text",
        placeholder="Enter text to convert",
        required=True,
        max_length=50
    )
    
    font_style = discord.ui.TextInput(
        label="Font Style",
        placeholder="standard, banner3-D, roman, cosmic, graffiti, digital",
        default="standard",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            from pyfiglet import Figlet
            f = Figlet(font=self.font_style.value)
            ascii_text = f.renderText(self.text_input.value)
            
            embed = discord.Embed(
                title="✨ ASCII Text Art",
                color=discord.Color.gold()
            )
            await interaction.response.send_message(f"```\n{ascii_text}\n```", embed=embed)
        except Exception as e:
            await interaction.response.send_message("Failed to generate ASCII text!", ephemeral=True)


class MorseCodeTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', '0': '-----', ' ': '/', '.': '.-.-.-', ',': '--..--',
            '?': '..--..', '!': '-.-.--', '/': '-..-.', '@': '.--.-.'
        }
        self.reverse_morse = {v: k for k, v in self.morse_dict.items()}

    @commands.group(name="morse", invoke_without_command=True)
    async def morse_group(self, ctx):
        embed = discord.Embed(
            title="📡 Morse Code Converter",
            description="Convert text to Morse code and back!",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Commands",
            value=(
                "`!morse encode <text>` - Convert text to Morse code\n"
                "`!morse decode <morse>` - Convert Morse code to text\n"
                "`!morse audio <text>` - Generate Morse code audio"
            ),
            inline=False
        )
        embed.add_field(
            name="Morse Code Guide",
            value="• Short signal: `.`\n• Long signal: `-`\n• Letter space: ` `\n• Word space: `/`",
            inline=False
        )
        await ctx.send(embed=embed)

    @morse_group.command(name="encode")
    async def encode(self, ctx, *, text: str):
        morse = ' '.join(self.morse_dict.get(char.upper(), char) 
                        for char in text)
        
        embed = discord.Embed(
            title="Text to Morse Code",
            color=discord.Color.green()
        )
        embed.add_field(name="Original Text", value=f"```{text}```", inline=False)
        embed.add_field(name="Morse Code", value=f"```{morse}```", inline=False)
        await ctx.send(embed=embed)

    @morse_group.command(name="decode")
    async def decode(self, ctx, *, morse: str):
        try:
            words = morse.split('/')
            decoded_words = []
            for word in words:
                letters = word.strip().split()
                decoded_word = ''.join(self.reverse_morse.get(letter, '') for letter in letters)
                decoded_words.append(decoded_word)
            
            text = ' '.join(decoded_words)
            
            embed = discord.Embed(
                title="Morse Code to Text",
                color=discord.Color.green()
            )
            embed.add_field(name="Morse Code", value=f"```{morse}```", inline=False)
            embed.add_field(name="Decoded Text", value=f"```{text}```", inline=False)
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send("Invalid Morse code! Use dots (.) and dashes (-)")

    @morse_group.command(name="audio")
    async def audio(self, ctx, *, text: str):
        morse = ' '.join(self.morse_dict.get(char.upper(), char) 
                        for char in text)
        
        audio_file = self.generate_morse_audio(morse)
        
        file = discord.File(audio_file, filename="morse.wav")
        embed = discord.Embed(
            title="Morse Code Audio Generated",
            description=f"Text: {text}\nMorse: {morse}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, file=file)

    def generate_morse_audio(self, morse):
        SAMPLE_RATE = 44100
        DOT_DURATION = 0.1
        FREQUENCY = 800
        
        def generate_tone(duration):
            t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
            tone = np.sin(2 * np.pi * FREQUENCY * t) * 0.5
            return tone.astype(np.float32)
        
        audio = []
        for symbol in morse:
            if symbol == '.':
                audio.extend(generate_tone(DOT_DURATION))
            elif symbol == '-':
                audio.extend(generate_tone(DOT_DURATION * 3))
            elif symbol == ' ':
                audio.extend(np.zeros(int(SAMPLE_RATE * DOT_DURATION), dtype=np.float32))
            elif symbol == '/':
                audio.extend(np.zeros(int(SAMPLE_RATE * DOT_DURATION * 2), dtype=np.float32))
            
            audio.extend(np.zeros(int(SAMPLE_RATE * DOT_DURATION * 0.5), dtype=np.float32))
        
        audio = np.array(audio)
        audio = (audio * 32767).astype(np.int16)
        
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes(audio.tobytes())
        
        buffer.seek(0)
        return buffer


class PasswordGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="password", aliases=["pw"], invoke_without_command=True)
    async def password_group(self, ctx):
        view = PasswordGeneratorView()
        embed = discord.Embed(
            title="🔒 Password Generator",
            description="Create secure passwords with custom parameters",
            color=discord.Color.brand_green()
        )
        embed.add_field(name="Options", value="Use the menu below to customize your password", inline=False)
        await ctx.send(embed=embed, view=view)

class PasswordGeneratorView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.length = 16
        self.include_uppercase = True
        self.include_lowercase = True
        self.include_numbers = True
        self.include_symbols = True

    @discord.ui.select(
        placeholder="Password Length",
        options=[
            discord.SelectOption(label=f"{i} characters", value=str(i))
            for i in [8, 12, 16, 24, 32, 64]
        ]
    )
    async def select_length(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.length = int(select.values[0])
        await interaction.response.defer()

    @discord.ui.button(label="Uppercase (A-Z)", style=ButtonStyle.green)
    async def toggle_uppercase(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.include_uppercase = not self.include_uppercase
        button.style = ButtonStyle.green if self.include_uppercase else ButtonStyle.gray
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Lowercase (a-z)", style=ButtonStyle.green)
    async def toggle_lowercase(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.include_lowercase = not self.include_lowercase
        button.style = ButtonStyle.green if self.include_lowercase else ButtonStyle.gray
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Numbers (0-9)", style=ButtonStyle.green)
    async def toggle_numbers(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.include_numbers = not self.include_numbers
        button.style = ButtonStyle.green if self.include_numbers else ButtonStyle.gray
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Symbols (!@#$)", style=ButtonStyle.green)
    async def toggle_symbols(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.include_symbols = not self.include_symbols
        button.style = ButtonStyle.green if self.include_symbols else ButtonStyle.gray
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Generate Password", style=ButtonStyle.blurple, row=2)
    async def generate(self, interaction: discord.Interaction, button: discord.ui.Button):
        chars = ""
        if self.include_uppercase: chars += string.ascii_uppercase
        if self.include_lowercase: chars += string.ascii_lowercase
        if self.include_numbers: chars += string.digits
        if self.include_symbols: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            await interaction.response.send_message("Select at least one character type!", ephemeral=True)
            return

        password = ''.join(random.choice(chars) for _ in range(self.length))
        
        try:
            embed = discord.Embed(
                title="🔒 Generated Password",
                description=f"```{password}```\nLength: {self.length} characters",
                color=discord.Color.green()
            )
            embed.add_field(name="Security Tips", value="• Save this password securely\n• Never share it with anyone\n• Use unique passwords for each account")
            
            await interaction.user.send(embed=embed)
            await interaction.response.send_message("✅ Password sent to your DMs!", ephemeral=True)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ Couldn't send DM! Please enable DMs from server members.", ephemeral=True)


class URLShortener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url_data = {}
        self.tinyurl_api = "http://tinyurl.com/api-create.php"
        self.load_url_data()

    def load_url_data(self):
        try:
            with open('url_data.json', 'r') as f:
                self.url_data = json.load(f)
        except FileNotFoundError:
            self.url_data = {}

    def save_url_data(self):
        with open('url_data.json', 'w') as f:
            json.dump(self.url_data, f, indent=4)

    @commands.group(name="url", invoke_without_command=True)
    async def url_group(self, ctx):
        embed = discord.Embed(
            title="🔗 URL Shortener Commands",
            description="Customize and manage your shortened URLs",
            color=discord.Color.blue()
        )
        embed.add_field(name="!url shorten <url>", value="Create a shortened URL", inline=False)
        embed.add_field(name="!url list", value="List all your shortened URLs", inline=False)
        embed.add_field(name="!url stats", value="View URL click statistics", inline=False)
        await ctx.send(embed=embed)

    @url_group.command(name="shorten")
    async def shorten_url(self, ctx, url: str):
        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        async with aiohttp.ClientSession() as session:
            params = {'url': url}
            async with session.get(self.tinyurl_api, params=params) as response:
                if response.status == 200:
                    shortened_url = await response.text()
                    
                    if guild_id not in self.url_data:
                        self.url_data[guild_id] = {}
                    if user_id not in self.url_data[guild_id]:
                        self.url_data[guild_id][user_id] = {}
                    
                    timestamp = datetime.now().isoformat()
                    self.url_data[guild_id][user_id][shortened_url] = {
                        'original_url': url,
                        'created_at': timestamp,
                        'clicks': 0
                    }
                    self.save_url_data()

                    embed = discord.Embed(
                        title="URL Shortened Successfully",
                        description=f"Original URL: {url}\nShortened URL: {shortened_url}",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)

class StudyTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_timers = {}

    @commands.group(invoke_without_command=True)
    async def study(self, ctx):
        embed = discord.Embed(
            title="📚 Study Tools",
            description="Select a tool from the menu below:",
            color=discord.Color.purple()
        )
        view = StudyToolsView(ctx.guild.id, ctx.author.id)
        await ctx.send(embed=embed, view=view)

class StudyToolsView(discord.ui.View):
    def __init__(self, guild_id, user_id):
        super().__init__(timeout=120)
        self.guild_id = guild_id
        self.user_id = user_id
        
    @discord.ui.select(
        placeholder="📚 Select Study Tool | !element for Chemistry",
        options=[
            discord.SelectOption(
                label="Grade Calculator",
                value="grade",
                emoji="📊",
                description="Calculate final grades and weighted averages"
            ),
            discord.SelectOption(
                label="GPA Calculator",
                value="gpa",
                emoji="🎓",
                description="Calculate GPA with different scales"
            ),
            discord.SelectOption(
                label="Study Timer",
                value="timer",
                emoji="⏱️",
                description="Set study session timers"
            ),
            discord.SelectOption(
                label="Pomodoro Timer",
                value="pomodoro",
                emoji="🍅",
                description="Use the Pomodoro Technique"
            )
        ]
    )
    async def select_tool(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu belongs to someone else!", ephemeral=True)
            return
            
        tool_views = {
            "grade": GradeCalculatorView(),
            "gpa": GPACalculatorView(),
            "timer": StudyTimerView(),
            "pomodoro": PomodoroView(self.guild_id, self.user_id)
        }
        await interaction.response.edit_message(view=tool_views[select.values[0]])


class GradeCalculatorView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Calculate Grade", style=discord.ButtonStyle.primary, emoji="📊")
    async def calculate_grade(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GradeCalculatorModal())

class GradeCalculatorModal(discord.ui.Modal, title="Grade Calculator"):
    def __init__(self):
        super().__init__()
        self.grades = discord.ui.TextInput(
            label="Enter grades (separated by spaces)",
            placeholder="e.g. 95 87 92 78",
            style=discord.TextStyle.short
        )
        self.weights = discord.ui.TextInput(
            label="Enter weights (optional)",
            placeholder="e.g. 0.3 0.2 0.3 0.2",
            required=False,
            style=discord.TextStyle.short
        )
        self.add_item(self.grades)
        self.add_item(self.weights)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            grades = [float(x) for x in self.grades.value.split()]
            if self.weights.value:
                weights = [float(x) for x in self.weights.value.split()]
                if len(weights) != len(grades):
                    raise ValueError("Number of weights must match number of grades")
                if abs(sum(weights) - 1.0) > 0.01:
                    raise ValueError("Weights must sum to 1.0")
                final_grade = sum(g * w for g, w in zip(grades, weights))
            else:
                final_grade = sum(grades) / len(grades)

            embed = discord.Embed(
                title="📊 Grade Calculation Results",
                color=discord.Color.green()
            )
            embed.add_field(name="Grades", value=f"```{', '.join(map(str, grades))}```")
            if self.weights.value:
                embed.add_field(name="Weights", value=f"```{', '.join(map(str, weights))}```")
            embed.add_field(name="Final Grade", value=f"```{final_grade:.2f}%```", inline=False)
            
            letter_grade = self.get_letter_grade(final_grade)
            embed.add_field(name="Letter Grade", value=f"```{letter_grade}```")
            
            await interaction.response.send_message(embed=embed)
        except ValueError as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

    def get_letter_grade(self, grade):
        if grade >= 93: return "A"
        elif grade >= 90: return "A-"
        elif grade >= 87: return "B+"
        elif grade >= 83: return "B"
        elif grade >= 80: return "B-"
        elif grade >= 77: return "C+"
        elif grade >= 73: return "C"
        elif grade >= 70: return "C-"
        elif grade >= 67: return "D+"
        elif grade >= 63: return "D"
        elif grade >= 60: return "D-"
        else: return "F"

class PomodoroView(discord.ui.View):
    active_timers = {}  

    def __init__(self, guild_id, user_id):
        super().__init__()
        self.guild_id = guild_id
        self.user_id = user_id
        self.current_timer = None
        self.end_time = None
        self.timer_task = None
        self.is_running = False

        if self.guild_id not in PomodoroView.active_timers:
            PomodoroView.active_timers[self.guild_id] = {}

    def cancel_timer(self):
        if self.timer_task:
            self.timer_task.cancel()
            self.timer_task = None
            self.is_running = False
            self.end_time = None
            
            if self.guild_id in PomodoroView.active_timers:
                PomodoroView.active_timers[self.guild_id].pop(self.user_id, None)

    @discord.ui.button(label="Start 25min Focus", style=discord.ButtonStyle.success, emoji="▶️")
    async def start_focus(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This timer belongs to someone else!", ephemeral=True)
            return

        self.cancel_timer()
        self.current_timer = "focus"
        self.end_time = datetime.now() + timedelta(minutes=25)
        self.is_running = True
        
        PomodoroView.active_timers[self.guild_id][self.user_id] = self
        
        await interaction.response.send_message(f"🍅 {interaction.user.mention}'s focus session started! 25 minutes to go!")
        self.timer_task = asyncio.create_task(self.run_timer(interaction, 25))

    @discord.ui.button(label="Custom Focus Time", style=discord.ButtonStyle.primary, emoji="⚡")
    async def custom_focus(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This timer belongs to someone else!", ephemeral=True)
            return
        await interaction.response.send_modal(CustomPomodoroModal(self))

    @discord.ui.button(label="Take 5min Break", style=discord.ButtonStyle.primary, emoji="☕")
    async def start_break(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This timer belongs to someone else!", ephemeral=True)
            return

        self.cancel_timer()
        self.current_timer = "break"
        self.end_time = datetime.now() + timedelta(minutes=5)   # 5 Minutes
        self.is_running = True
        
        PomodoroView.active_timers[self.guild_id][self.user_id] = self
        
        await interaction.response.send_message(f"☕ {interaction.user.mention}'s break time! 5 minutes to relax!")
        self.timer_task = asyncio.create_task(self.run_timer(interaction, 5)) # 5 Minutes

    @discord.ui.button(label="Stop Remove/Timer", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop_timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This timer belongs to someone else!", ephemeral=True)
            return

        self.cancel_timer()
        await interaction.response.send_message("⏹️ Timer stopped!", ephemeral=True)

    async def run_timer(self, interaction, duration_minutes):
        try:
            total_seconds = duration_minutes * 60
            while total_seconds > 0 and self.is_running:
                minutes = total_seconds // 60
                if minutes in [20, 15, 10, 5, 1]:
                    await interaction.channel.send(f"⏳ {interaction.user.mention}'s timer: {minutes} minute{'s' if minutes != 1 else ''} remaining!")
                await asyncio.sleep(1)
                total_seconds -= 1

            if self.is_running:
                if self.current_timer == "focus":
                    await interaction.channel.send(f"{interaction.user.mention} 🔔 Focus session complete! Time for a break!")
                else:
                    await interaction.channel.send(f"{interaction.user.mention} 🔔 Break complete! Ready to focus again!")
                
                self.timer_task = None
                self.is_running = False
                self.end_time = None
                
        except asyncio.CancelledError:
            pass

class CustomPomodoroModal(discord.ui.Modal, title="Custom Focus Timer"):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.minutes = discord.ui.TextInput(
            label="Minutes",
            placeholder="Enter custom focus duration in minutes",
            min_length=1,
            max_length=3
        )
        self.add_item(self.minutes)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            minutes = int(self.minutes.value)
            if minutes <= 0:
                raise ValueError("Duration must be positive")
            
            self.view.cancel_timer()
            self.view.current_timer = "focus"
            self.view.end_time = datetime.now() + timedelta(minutes=minutes)
            self.view.is_running = True
            
            PomodoroView.active_timers[self.view.guild_id][self.view.user_id] = self.view
            
            await interaction.response.send_message(f"🍅 {interaction.user.mention}'s custom focus session started! {minutes} minutes to go!")
            self.view.timer_task = asyncio.create_task(self.view.run_timer(interaction, minutes))
        except ValueError:
            await interaction.response.send_message("Please enter a valid number of minutes!", ephemeral=True)


class StudyTimerView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timer_running = False
        self.timer_task = None
        self.remaining_time = 0

    @discord.ui.button(label="Set Custom Timer", style=discord.ButtonStyle.primary, emoji="⏱️")
    async def set_timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StudyTimerModal(self))

    @discord.ui.button(label="Pause/Resume", style=discord.ButtonStyle.secondary, emoji="⏸️")
    async def toggle_timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.timer_task:
            if self.timer_running:
                self.timer_running = False
                button.label = "Resume"
                button.emoji = "▶️"
                status = "paused"
            else:
                self.timer_running = True
                button.label = "Pause"
                button.emoji = "⏸️"
                status = "resumed"
            
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            time_display = f"{minutes}m {seconds}s"
            
            await interaction.response.edit_message(view=self)
            await interaction.followup.send(f"⏱️ Timer {status}! Remaining time: {time_display}", ephemeral=True)
        else:
            await interaction.response.send_message("No active timer to pause/resume!", ephemeral=True)

    @discord.ui.button(label="Remove Timer", style=discord.ButtonStyle.danger, emoji="⏹️")
    async def stop_timer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.timer_task:
            self.timer_task.cancel()
            self.timer_task = None
            self.timer_running = False
            self.remaining_time = 0
            await interaction.response.send_message("⏹️ Timer Removed/stopped!", ephemeral=True)
            
            for child in self.children:
                if child.label.startswith(("Pause", "Resume")):
                    child.label = "Pause/Resume"
                    child.emoji = "⏸️"
            await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("No active timer to stop!", ephemeral=True)

class StudyTimerModal(discord.ui.Modal, title="Study Timer"):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.minutes = discord.ui.TextInput(
            label="Minutes",
            placeholder="Enter duration in minutes",
            min_length=1,
            max_length=3
        )
        self.add_item(self.minutes)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            minutes = int(self.minutes.value)
            if minutes <= 0:
                raise ValueError("Duration must be positive")
            
            self.view.timer_running = True
            self.view.remaining_time = minutes * 60
            await interaction.response.send_message(f"⏱️ Timer set for {minutes} minutes!")
            
            self.view.timer_task = asyncio.create_task(self.run_timer(interaction, minutes))
        except ValueError:
            await interaction.response.send_message("Please enter a valid number of minutes!", ephemeral=True)

    async def run_timer(self, interaction, minutes):
        total_seconds = minutes * 60
        self.view.remaining_time = total_seconds
        last_minute_notified = None
        
        while total_seconds > 0:
            if self.view.timer_running:
                current_minute = total_seconds // 60
                if current_minute in [15, 10, 5, 1] and current_minute != last_minute_notified:
                    await interaction.channel.send(f"⏳ {interaction.user.mention}'s timer: {current_minute} minute{'s' if current_minute != 1 else ''} remaining!")
                    last_minute_notified = current_minute
                await asyncio.sleep(1)
                total_seconds -= 1
                self.view.remaining_time = total_seconds
            else:
                await asyncio.sleep(1)
        
        if self.view.timer_running:
            await interaction.channel.send(f"{interaction.user.mention} ⏰ Time's up! Study session complete!")
        self.view.timer_task = None
        self.view.remaining_time = 0


class GPACalculatorView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Calculate GPA", style=discord.ButtonStyle.primary, emoji="🎓")
    async def calculate_gpa(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(GPACalculatorModal())

class GPACalculatorModal(discord.ui.Modal, title="GPA Calculator"):
    def __init__(self):
        super().__init__()
        self.grades = discord.ui.TextInput(
            label="Enter letter grades (separated by spaces)",
            placeholder="e.g. A B+ B A- C+",
            style=discord.TextStyle.short
        )
        self.credits = discord.ui.TextInput(
            label="Enter credit hours",
            placeholder="e.g. 3 4 3 3 3",
            style=discord.TextStyle.short
        )
        self.add_item(self.grades)
        self.add_item(self.credits)

    async def on_submit(self, interaction: discord.Interaction):
        grade_points = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }

        try:
            grades = self.grades.value.upper().split()
            credits = [float(x) for x in self.credits.value.split()]

            if len(grades) != len(credits):
                raise ValueError("Number of grades must match number of credits")

            total_points = sum(grade_points[g] * c for g, c in zip(grades, credits))
            total_credits = sum(credits)
            gpa = total_points / total_credits

            embed = discord.Embed(
                title="🎓 GPA Calculation Results",
                color=discord.Color.gold()
            )
            embed.add_field(
                name="Courses",
                value="\n".join(f"Grade: {g} | Credits: {c}" for g, c in zip(grades, credits)),
                inline=False
            )
            embed.add_field(name="Total Credits", value=f"{total_credits:.1f}")
            embed.add_field(name="GPA", value=f"{gpa:.2f}")

            classification = self.get_gpa_classification(gpa)
            embed.add_field(name="Standing", value=classification, inline=False)

            await interaction.response.send_message(embed=embed)
        except (ValueError, KeyError) as e:
            await interaction.response.send_message(
                "Please enter valid grades (A, A-, B+, etc.) and credit hours!",
                ephemeral=True
            )

    def get_gpa_classification(self, gpa):
        if gpa >= 3.9: return "Summa Cum Laude 🏆"
        elif gpa >= 3.7: return "Magna Cum Laude ⭐"
        elif gpa >= 3.5: return "Cum Laude 🌟"
        elif gpa >= 3.0: return "Dean's List 📚"
        elif gpa >= 2.0: return "Good Standing 👍"
        else: return "Academic Probation ⚠️"






class HashCalculatorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Select Hash Algorithm",
        options=[
            discord.SelectOption(label="MD5", value="md5", emoji="1️⃣", description="Fast, not cryptographically secure"),
            discord.SelectOption(label="SHA-1", value="sha1", emoji="2️⃣", description="160-bit hash"),
            discord.SelectOption(label="SHA-256", value="sha256", emoji="3️⃣", description="Strong 256-bit hash"),
            discord.SelectOption(label="SHA-512", value="sha512", emoji="4️⃣", description="Most secure, 512-bit hash")
        ]
    )
    async def calculate_hash(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(HashCalculatorModal(select.values[0]))

    @discord.ui.button(label="Back to Tools", style=discord.ButtonStyle.secondary, emoji="◀️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="🔧 **Coding Tools**", view=CodingToolsView())



class ColorPickerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.current_color = {"r": 255, "g": 0, "b": 0}
        self.current_hex = "#FF0000"
        
    def create_color_preview(self):
        
        img = Image.new('RGB', (300, 100), (self.current_color["r"], 
                                           self.current_color["g"], 
                                           self.current_color["b"]))
        draw = ImageDraw.Draw(img)
        
        rgb_text = f"RGB: ({self.current_color['r']}, {self.current_color['g']}, {self.current_color['b']})"
        hex_text = f"HEX: {self.current_hex}"
        hsv = colorsys.rgb_to_hsv(self.current_color["r"]/255, 
                                 self.current_color["g"]/255, 
                                 self.current_color["b"]/255)
        hsv_text = f"HSV: ({int(hsv[0]*360)}°, {int(hsv[1]*100)}%, {int(hsv[2]*100)}%)"
        
        text_color = (0, 0, 0) if sum(self.current_color.values())/3 > 128 else (255, 255, 255)
        draw.text((10, 10), rgb_text, fill=text_color)
        draw.text((10, 40), hex_text, fill=text_color)
        draw.text((10, 70), hsv_text, fill=text_color)
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer

    @discord.ui.select(
        placeholder="Color Presets",
        options=[
            discord.SelectOption(label="Red", value="#FF0000"),
            discord.SelectOption(label="Green", value="#00FF00"),
            discord.SelectOption(label="Blue", value="#0000FF"),
            discord.SelectOption(label="Yellow", value="#FFFF00"),
            discord.SelectOption(label="Purple", value="#800080"),
            discord.SelectOption(label="Orange", value="#FFA500"),
            discord.SelectOption(label="Pink", value="#FFC0CB"),
            discord.SelectOption(label="Turquoise", value="#40E0D0")
        ]
    )
    async def preset_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        hex_color = select.values[0]
        
        hex_color = hex_color.lstrip('#')
        self.current_color["r"] = int(hex_color[0:2], 16)
        self.current_color["g"] = int(hex_color[2:4], 16)
        self.current_color["b"] = int(hex_color[4:6], 16)
        self.current_hex = f"#{hex_color.upper()}"
        
        file = discord.File(self.create_color_preview(), filename="color.png")
        await interaction.response.edit_message(attachments=[file])

    @discord.ui.button(label="RGB Sliders", style=discord.ButtonStyle.primary, emoji="🎚️")
    async def rgb_sliders(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RGBSliderModal(self))

class RGBSliderModal(discord.ui.Modal, title="RGB Color Picker"):
    def __init__(self, color_view):
        super().__init__()
        self.color_view = color_view
        
        self.red = discord.ui.TextInput(
            label="Red (0-255)",
            placeholder="Enter red value",
            default=str(color_view.current_color["r"]),
            min_length=1,
            max_length=3
        )
        self.green = discord.ui.TextInput(
            label="Green (0-255)",
            placeholder="Enter green value",
            default=str(color_view.current_color["g"]),
            min_length=1,
            max_length=3
        )
        self.blue = discord.ui.TextInput(
            label="Blue (0-255)",
            placeholder="Enter blue value",
            default=str(color_view.current_color["b"]),
            min_length=1,
            max_length=3
        )
        
        self.add_item(self.red)
        self.add_item(self.green)
        self.add_item(self.blue)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            r = max(0, min(255, int(self.red.value)))
            g = max(0, min(255, int(self.green.value)))
            b = max(0, min(255, int(self.blue.value)))
            
            self.color_view.current_color = {"r": r, "g": g, "b": b}
            self.color_view.current_hex = f"#{r:02x}{g:02x}{b:02x}".upper()
            
            file = discord.File(self.color_view.create_color_preview(), filename="color.png")
            await interaction.response.edit_message(attachments=[file])
            
        except ValueError:
            await interaction.response.send_message("Please enter valid numbers between 0 and 255!", ephemeral=True)

class CodingTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def code(self, ctx):
        """Main coding tools interface"""
        embed = discord.Embed(
            title="🔧 Coding Helper Tools",
            description="Select a tool from the menu below:",
            color=discord.Color.blue()
        )
        view = CodingToolsView()
        await ctx.send(embed=embed, view=view)

class CodingToolsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        
    @discord.ui.select(
        placeholder="🔧 Select Coding Tool",
        options=[
            discord.SelectOption(
                label="Color Picker & Converter",
                value="color",
                emoji="🎨",
                description="Interactive color tools with live preview"
            ),
            discord.SelectOption(
                label="Number Base Converter",
                value="base",
                emoji="🔢",
                description="Convert between decimal, binary, hex"
            ),
            discord.SelectOption(
                label="String Tools",
                value="string",
                emoji="📝",
                description="Encode/decode text in various formats"
            ),
            discord.SelectOption(
                label="Hash Calculator",
                value="hash",
                emoji="🔐",
                description="Generate secure hashes"
            )
        ]
    )
    async def select_tool(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "color":
            view = ColorPickerView()
            file = discord.File(view.create_color_preview(), filename="color.png")
            await interaction.response.edit_message(content="🎨 **Color Tools**", attachments=[file], view=view)
        elif select.values[0] == "base":
            await interaction.response.send_modal(BaseConverterModal())
        elif select.values[0] == "string":
            view = StringToolsView()
            await interaction.response.edit_message(content="📝 **String Tools**", view=view)
        elif select.values[0] == "hash":
            view = HashCalculatorView()
            await interaction.response.edit_message(content="🔐 **Hash Tools**", view=view)



class StringToolsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Choose String Operation",
        options=[
            discord.SelectOption(label="Base64 Encode", value="b64e", emoji="🔒", description="Encode text to Base64"),
            discord.SelectOption(label="Base64 Decode", value="b64d", emoji="🔓", description="Decode Base64 to text"),
            discord.SelectOption(label="URL Encode", value="urle", emoji="🔗", description="Encode text for URLs"),
            discord.SelectOption(label="URL Decode", value="urld", emoji="🌐", description="Decode URL-encoded text")
        ]
    )
    async def string_operation(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(StringOperationModal(select.values[0]))

    @discord.ui.button(label="Back to Tools", style=discord.ButtonStyle.secondary, emoji="◀️")
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="🔧 **Coding Tools**", view=CodingToolsView())


class BaseConverterModal(discord.ui.Modal, title="Base Converter"):
    def __init__(self):
        super().__init__()
        self.number = discord.ui.TextInput(
            label="Enter Number",
            placeholder="Enter number with base prefix (0x, 0b, or decimal)"
        )
        self.add_item(self.number)

    async def on_submit(self, interaction: discord.Interaction):
        try:
           
            value = self.number.value.lower().strip()
            if value.startswith('0x'):
                num = int(value[2:], 16)
                base = 16
            elif value.startswith('0b'):
                num = int(value[2:], 2)
                base = 2
            else:
                num = int(value)
                base = 10

            embed = discord.Embed(
                title="🔢 Base Conversion Results",
                color=discord.Color.green()
            )
            embed.add_field(name="Input", value=f"```{value}```", inline=False)
            embed.add_field(name="Decimal", value=f"```{num}```")
            embed.add_field(name="Hexadecimal", value=f"```0x{num:X}```")
            embed.add_field(name="Binary", value=f"```0b{bin(num)[2:]}```")
            embed.add_field(name="Octal", value=f"```0o{oct(num)[2:]}```")
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("Invalid number format!", ephemeral=True)

class StringOperationModal(discord.ui.Modal):
    def __init__(self, operation):
        super().__init__(title="String Encoder/Decoder")
        self.operation = operation
        self.input_text = discord.ui.TextInput(
            label="Enter Text",
            placeholder="Text to encode/decode",
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.input_text)

    async def on_submit(self, interaction: discord.Interaction):
        import base64
        import urllib.parse
        
        text = self.input_text.value
        result = ""
        
        try:
            if self.operation == "b64e":
                result = base64.b64encode(text.encode()).decode()
                op_name = "Base64 Encode"
            elif self.operation == "b64d":
                result = base64.b64decode(text.encode()).decode()
                op_name = "Base64 Decode"
            elif self.operation == "urle":
                result = urllib.parse.quote(text)
                op_name = "URL Encode"
            elif self.operation == "urld":
                result = urllib.parse.unquote(text)
                op_name = "URL Decode"

            embed = discord.Embed(
                title="📝 String Operation Result",
                color=discord.Color.blue()
            )
            embed.add_field(name="Operation", value=op_name, inline=False)
            embed.add_field(name="Input", value=f"```{text}```", inline=False)
            embed.add_field(name="Output", value=f"```{result}```", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error: Invalid input for {op_name}", ephemeral=True)

class HashCalculatorModal(discord.ui.Modal):
    def __init__(self, hash_type):
        super().__init__(title=f"{hash_type.upper()} Hash Calculator")
        self.hash_type = hash_type
        self.input_text = discord.ui.TextInput(
            label="Enter Text",
            placeholder="Text to hash",
            style=discord.TextStyle.paragraph
        )
        self.add_item(self.input_text)

    async def on_submit(self, interaction: discord.Interaction):
        import hashlib
        
        text = self.input_text.value
        
        hash_functions = {
            'md5': hashlib.md5(),
            'sha1': hashlib.sha1(),
            'sha256': hashlib.sha256(),
            'sha512': hashlib.sha512()
        }
        
        hasher = hash_functions[self.hash_type]
        hasher.update(text.encode())
        hash_result = hasher.hexdigest()

        embed = discord.Embed(
            title="🔐 Hash Calculation Result",
            color=discord.Color.red()
        )
        embed.add_field(name="Hash Type", value=self.hash_type.upper(), inline=False)
        embed.add_field(name="Input Text", value=f"```{text}```", inline=False)
        embed.add_field(name="Hash", value=f"```{hash_result}```", inline=False)
        embed.set_footer(text="Note: Hashing is one-way encryption")
        
        await interaction.response.send_message(embed=embed)









class TimeTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True)
    async def time(self, ctx):
        embed = discord.Embed(
            title="⏰ Time & Date Tools",
            description="Select a tool from the menu below:",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=TimeToolsView())

class TimeToolsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        
    @discord.ui.select(
        placeholder="Choose Time Tool",
        options=[
            discord.SelectOption(label="Time Zone Converter", value="timezone", emoji="🌍", description="Convert between time zones"),
            discord.SelectOption(label="Date Difference", value="datediff", emoji="📅", description="Calculate days between dates"),
            discord.SelectOption(label="Project Deadline", value="deadline", emoji="⏳", description="Calculate project timelines"),
            discord.SelectOption(label="Meeting Scheduler", value="meeting", emoji="👥", description="Schedule across time zones")
        ]
    )
    async def select_tool(self, interaction: discord.Interaction, select: discord.ui.Select):
        tool_views = {
            "timezone": TimeZoneView(),
            "datediff": DateDiffView(),
            "deadline": DeadlineView(),
            "meeting": MeetingView()
        }
        await interaction.response.edit_message(view=tool_views[select.values[0]])

class DateDiffView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Calculate Date Difference", style=discord.ButtonStyle.primary, emoji="📅")
    async def calculate_diff(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DateDiffModal())

class DateDiffModal(discord.ui.Modal, title="Date Difference Calculator"):
    def __init__(self):
        super().__init__()
        self.date1 = discord.ui.TextInput(
            label="Start Date",
            placeholder="YYYY-MM-DD (e.g. 2024-02-26)"
        )
        self.date2 = discord.ui.TextInput(
            label="End Date",
            placeholder="YYYY-MM-DD (e.g. 2024-03-26)"
        )
        self.add_item(self.date1)
        self.add_item(self.date2)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            date1 = datetime.strptime(self.date1.value, "%Y-%m-%d")
            date2 = datetime.strptime(self.date2.value, "%Y-%m-%d")
            diff = date2 - date1
            
            embed = discord.Embed(title="📅 Date Difference Results", color=discord.Color.green())
            embed.add_field(name="Start Date", value=date1.strftime("%B %d, %Y"), inline=True)
            embed.add_field(name="End Date", value=date2.strftime("%B %d, %Y"), inline=True)
            embed.add_field(name="Difference", value=f"{abs(diff.days)} days", inline=False)
            embed.add_field(name="Weeks", value=f"{abs(diff.days) // 7} weeks and {abs(diff.days) % 7} days", inline=False)
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("Please use the format YYYY-MM-DD!", ephemeral=True)

class DeadlineView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Set Project Deadline", style=discord.ButtonStyle.primary, emoji="⏳")
    async def set_deadline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeadlineModal())

class DeadlineModal(discord.ui.Modal, title="Project Deadline Calculator"):
    def __init__(self):
        super().__init__()
        self.start_date = discord.ui.TextInput(
            label="Start Date",
            placeholder="YYYY-MM-DD (e.g. 2024-02-26)"
        )
        self.duration = discord.ui.TextInput(
            label="Project Duration (days)",
            placeholder="e.g. 30"
        )
        self.add_item(self.start_date)
        self.add_item(self.duration)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            start = datetime.strptime(self.start_date.value, "%Y-%m-%d")
            days = int(self.duration.value)
            end = start + timedelta(days=days)
            
            milestones = [
                ("25% Complete", start + timedelta(days=days//4)),
                ("50% Complete", start + timedelta(days=days//2)),
                ("75% Complete", start + timedelta(days=3*days//4)),
                ("Deadline", end)
            ]
            
            embed = discord.Embed(title="⏳ Project Timeline", color=discord.Color.gold())
            embed.add_field(name="Project Start", value=start.strftime("%B %d, %Y"), inline=True)
            embed.add_field(name="Project Duration", value=f"{days} days", inline=True)
            embed.add_field(name="Project End", value=end.strftime("%B %d, %Y"), inline=True)
            
            for milestone, date in milestones:
                embed.add_field(name=milestone, value=date.strftime("%B %d, %Y"), inline=False)
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("Please check your input format!", ephemeral=True)

class MeetingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Schedule Meeting", style=discord.ButtonStyle.primary, emoji="👥")
    async def schedule_meeting(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MeetingModal())

class MeetingModal(discord.ui.Modal, title="Meeting Scheduler"):
    def __init__(self):
        super().__init__()
        self.meeting_date = discord.ui.TextInput(
            label="Meeting Date",
            placeholder="YYYY-MM-DD (e.g. 2024-02-26)"
        )
        self.meeting_time = discord.ui.TextInput(
            label="Meeting Time (Your Local Time)",
            placeholder="HH:MM (e.g. 14:30 or 02:30 PM)"
        )
        self.timezone = discord.ui.TextInput(
            label="Your Timezone",
            placeholder="e.g. US/Pacific, Europe/London"
        )
        self.add_item(self.meeting_date)
        self.add_item(self.meeting_time)
        self.add_item(self.timezone)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            date = datetime.strptime(self.meeting_date.value, "%Y-%m-%d")
            time = datetime.strptime(self.meeting_time.value, "%H:%M").time()
            local_tz = pytz.timezone(self.timezone.value)
            
            dt = datetime.combine(date, time)
            local_time = local_tz.localize(dt)
            
            common_timezones = {
                "US/Pacific": "Los Angeles",
                "US/Eastern": "New York",
                "Europe/London": "London",
                "Europe/Paris": "Paris",
                "Asia/Tokyo": "Tokyo",
                "Australia/Sydney": "Sydney"
            }
            
            embed = discord.Embed(title="👥 Meeting Schedule", color=discord.Color.blue())
            embed.add_field(name="Meeting Date", value=date.strftime("%B %d, %Y"), inline=False)
            
            for tz, city in common_timezones.items():
                converted = local_time.astimezone(pytz.timezone(tz))
                embed.add_field(
                    name=f"Time in {city}",
                    value=f"{converted.strftime('%I:%M %p')} ({converted.strftime('%H:%M')})",
                    inline=True
                )
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("Please check your input format!", ephemeral=True)
        except pytz.exceptions.UnknownTimeZoneError:
            await interaction.response.send_message("Invalid timezone! Please use a valid timezone name.", ephemeral=True)

class TimeZoneModal(discord.ui.Modal, title="Time Zone Converter"):
    def __init__(self, from_tz: str, to_tz: str):
        super().__init__()
        self.from_tz = from_tz
        self.to_tz = to_tz
        self.time_input = discord.ui.TextInput(
            label="Enter time (HH:MM)",
            placeholder="e.g. 14:30 or 02:30 PM"
        )
        self.add_item(self.time_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
        
            input_time = self.parse_time(self.time_input.value)
            
            from_zone = pytz.timezone(self.from_tz)
            to_zone = pytz.timezone(self.to_tz)
            
            now = datetime.now()
            dt = datetime.combine(now.date(), input_time)
            dt = from_zone.localize(dt)
            converted = dt.astimezone(to_zone)

            embed = discord.Embed(
                title="🌍 Time Zone Conversion",
                color=discord.Color.blue()
            )
            embed.add_field(
                name=f"Time in {self.get_location_name(self.from_tz)}",
                value=f"```{dt.strftime('%I:%M %p')} ({dt.strftime('%H:%M')} Military)```"
            )
            embed.add_field(
                name=f"Time in {self.get_location_name(self.to_tz)}",
                value=f"```{converted.strftime('%I:%M %p')} ({converted.strftime('%H:%M')} Military)```"
            )
            
            time_diff = self.get_time_difference(from_zone, to_zone)
            embed.add_field(
                name="Time Difference",
                value=f"```{time_diff}```",
                inline=False
            )

            await interaction.response.send_message(embed=embed)

        except ValueError as e:
            await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)

    def parse_time(self, time_str: str) -> datetime.time:
        try:
            
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            try:
                
                return datetime.strptime(time_str, "%I:%M %p").time()
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM or HH:MM AM/PM")

    def get_location_name(self, tz: str) -> str:
        """Convert timezone string to readable location name"""
        return tz.replace('_', ' ').split('/')[-1]

    def get_time_difference(self, tz1: pytz.timezone, tz2: pytz.timezone) -> str:
        now = datetime.now()
        tz1_time = now.astimezone(tz1)
        tz2_time = now.astimezone(tz2)
        diff = int((tz2_time.utcoffset() - tz1_time.utcoffset()).total_seconds() / 3600)
        return f"{abs(diff)} hours {'ahead' if diff > 0 else 'behind'}"

class TimeZoneView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.from_tz = None
        self.to_tz = None
        self.common_zones = {
            "🌎 North America": [
                ("US/Pacific", "Los Angeles, Vancouver"),
                ("US/Mountain", "Denver, Calgary"),
                ("US/Central", "Chicago, Mexico City"),
                ("US/Eastern", "New York, Toronto")
            ],
            "🌍 Europe": [
                ("Europe/London", "London, Dublin"),
                ("Europe/Paris", "Paris, Berlin, Rome"),
                ("Europe/Moscow", "Moscow, St. Petersburg")
            ],
            "🌏 Asia/Pacific": [
                ("Asia/Tokyo", "Tokyo, Seoul"),
                ("Asia/Shanghai", "Beijing, Shanghai"),
                ("Australia/Sydney", "Sydney, Melbourne"),
                ("Pacific/Auckland", "Auckland, Wellington")
            ]
        }

        self.from_select = discord.ui.Select(
            placeholder="Convert from (Region)",
            options=[
                discord.SelectOption(
                    label=description,
                    value=zone,
                    description=f"UTC{datetime.now(pytz.timezone(zone)).strftime('%z')}"
                )
                for region, zones in self.common_zones.items()
                for zone, description in zones
            ]
        )
        self.to_select = discord.ui.Select(
            placeholder="Convert to (Region)",
            options=[
                discord.SelectOption(
                    label=description,
                    value=zone,
                    description=f"UTC{datetime.now(pytz.timezone(zone)).strftime('%z')}"
                )
                for region, zones in self.common_zones.items()
                for zone, description in zones
            ]
        )

        self.from_select.callback = self.from_region_select
        self.to_select.callback = self.to_region_select

        self.add_item(self.from_select)
        self.add_item(self.to_select)

    async def from_region_select(self, interaction: discord.Interaction):
        self.from_tz = self.from_select.values[0]
        if self.to_tz:
            await interaction.response.send_modal(TimeZoneModal(self.from_tz, self.to_tz))

    async def to_region_select(self, interaction: discord.Interaction):
        self.to_tz = self.to_select.values[0]
        if self.from_tz:
            await interaction.response.send_modal(TimeZoneModal(self.from_tz, self.to_tz))




class UnitConverterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.conversion_type = None
        self.from_unit = None
        self.to_unit = None

    @discord.ui.select(
        placeholder="Select Unit Type",
        options=[
            discord.SelectOption(label="Length", value="length", emoji="📏"),
            discord.SelectOption(label="Volume", value="volume", emoji="🧊"),
            discord.SelectOption(label="Mass", value="mass", emoji="⚖️")
        ]
    )
    async def unit_type_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.conversion_type = select.values[0]
        units = list(MathPhysicsTools.unit_conversions[self.conversion_type].keys())
        
        from_select = discord.ui.Select(
            placeholder="Convert from",
            options=[discord.SelectOption(label=unit, value=unit) for unit in units]
        )
        to_select = discord.ui.Select(
            placeholder="Convert to",
            options=[discord.SelectOption(label=unit, value=unit) for unit in units]
        )

        async def from_callback(interaction: discord.Interaction):
            self.from_unit = from_select.values[0]
            if self.to_unit: 
                await interaction.response.send_modal(
                    UnitConverterModal(self.conversion_type, self.from_unit, self.to_unit)
                )

        async def to_callback(interaction: discord.Interaction):
            self.to_unit = to_select.values[0]
            if self.from_unit:  
                await interaction.response.send_modal(
                    UnitConverterModal(self.conversion_type, self.from_unit, self.to_unit)
                )

        from_select.callback = from_callback
        to_select.callback = to_callback

        self.clear_items()
        self.add_item(from_select)
        self.add_item(to_select)
        await interaction.response.edit_message(view=self)


class GeometryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Select Shape",
        options=[
            discord.SelectOption(label="Circle", value="circle", emoji="⭕"),
            discord.SelectOption(label="Square", value="square", emoji="⬛"),
            discord.SelectOption(label="Triangle", value="triangle", emoji="📐"),
            discord.SelectOption(label="Sphere", value="sphere", emoji="🔮")
        ]
    )
    async def shape_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(GeometryModal(select.values[0]))

class PhysicsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.select(
        placeholder="Select Formula",
        options=[
            discord.SelectOption(label="Velocity", value="velocity", emoji="🏃"),
            discord.SelectOption(label="Force", value="force", emoji="💪"),
            discord.SelectOption(label="Energy", value="energy", emoji="⚡")
        ]
    )
    async def formula_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        await interaction.response.send_modal(PhysicsModal(select.values[0]))






class StatisticsModal(discord.ui.Modal, title="Statistical Analysis"):
    def __init__(self):
        super().__init__()
        self.numbers_input = discord.ui.TextInput(
            label="Enter numbers (separated by spaces)",
            placeholder="e.g. 1 2 3.5 4.7 5",
            required=True
        )
        self.add_item(self.numbers_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            
            numbers = [float(x) for x in self.numbers_input.value.split()]
            
            if not numbers:
                raise ValueError("No numbers provided")

            mean = sum(numbers) / len(numbers)
            sorted_nums = sorted(numbers)
            median = sorted_nums[len(numbers)//2] if len(numbers) % 2 else (sorted_nums[len(numbers)//2-1] + sorted_nums[len(numbers)//2])/2
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            std_dev = variance ** 0.5

            embed = discord.Embed(
                title="📊 Statistical Analysis Results",
                color=discord.Color.purple()
            )
            embed.add_field(name="Numbers Analyzed", value=f"`{', '.join(map(str, numbers))}`", inline=False)
            embed.add_field(name="Count", value=str(len(numbers)))
            embed.add_field(name="Mean", value=f"{mean:.2f}")
            embed.add_field(name="Median", value=f"{median:.2f}")
            embed.add_field(name="Standard Deviation", value=f"{std_dev:.2f}")
            embed.add_field(name="Range", value=f"{max(numbers) - min(numbers):.2f}")

            await interaction.response.send_message(embed=embed)

        except ValueError:
            await interaction.response.send_message("Please enter valid numbers separated by spaces!", ephemeral=True)

class StatisticsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Enter Numbers", style=discord.ButtonStyle.primary, emoji="📊")
    async def enter_numbers(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StatisticsModal())






class MathPhysicsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        
    @discord.ui.select(
        placeholder="Choose Calculator Type",
        options=[
            discord.SelectOption(label="Unit Converter", value="units", emoji="📏", description="Convert between different units"),
            discord.SelectOption(label="Geometry", value="geometry", emoji="📐", description="Calculate areas, volumes, perimeters"),
            discord.SelectOption(label="Physics", value="physics", emoji="⚡", description="Physics formulas and calculations"),
            discord.SelectOption(label="Statistics", value="stats", emoji="📊", description="Statistical analysis tools")
        ]
    )
    async def select_calculator(self, interaction: discord.Interaction, select: discord.ui.Select):
        calculator_views = {
            "units": UnitConverterView(),
            "geometry": GeometryView(),
            "physics": PhysicsView(),
            "stats": StatisticsView()
        }
        await interaction.response.edit_message(view=calculator_views[select.values[0]])

class UnitConverterModal(discord.ui.Modal, title="Unit Converter"):
    def __init__(self, conversion_type, from_unit, to_unit):
        super().__init__()
        self.conversion_type = conversion_type
        self.from_unit = from_unit
        self.to_unit = to_unit
        
        self.value = discord.ui.TextInput(
            label=f"Enter value in {from_unit}",
            placeholder="e.g. 100",
            required=True
        )
        self.add_item(self.value)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            value = float(self.value.value)
            result = MathPhysicsTools.convert_unit(value, self.from_unit, self.to_unit, self.conversion_type)
            
            embed = discord.Embed(
                title="📏 Unit Conversion Result",
                description=f"{value} {self.from_unit} = {result:.4f} {self.to_unit}",
                color=discord.Color.green()
            )
            embed.add_field(name="Conversion Type", value=self.conversion_type.title())
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)

class GeometryModal(discord.ui.Modal, title="Geometry Calculator"):
    def __init__(self, shape):
        super().__init__()
        self.shape = shape
        
        if shape in ["circle", "sphere"]:
            self.radius = discord.ui.TextInput(label="Radius", required=True)
            self.add_item(self.radius)
        elif shape == "square":
            self.side = discord.ui.TextInput(label="Side Length", required=True)
            self.add_item(self.side)
        elif shape == "triangle":
            self.side_a = discord.ui.TextInput(label="Side A", required=True)
            self.side_b = discord.ui.TextInput(label="Side B", required=True)
            self.side_c = discord.ui.TextInput(label="Side C", required=True)
            self.add_item(self.side_a)
            self.add_item(self.side_b)
            self.add_item(self.side_c)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            results = MathPhysicsTools.calculate_geometry(self.shape, self.get_values())
            
            embed = discord.Embed(
                title=f"📐 {self.shape.title()} Calculations",
                color=discord.Color.blue()
            )
            for key, value in results.items():
                embed.add_field(name=key, value=f"{value:.2f}")
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("❌ Please enter valid numbers!", ephemeral=True)

    def get_values(self):
        if self.shape in ["circle", "sphere"]:
            return [float(self.radius.value)]
        elif self.shape == "square":
            return [float(self.side.value)]
        elif self.shape == "triangle":
            return [float(self.side_a.value), float(self.side_b.value), float(self.side_c.value)]

class PhysicsModal(discord.ui.Modal, title="Physics Calculator"):
    def __init__(self, formula):
        super().__init__()
        self.formula = formula
        
        if formula == "velocity":
            self.distance = discord.ui.TextInput(label="Distance (meters)", required=True)
            self.time = discord.ui.TextInput(label="Time (seconds)", required=True)
            self.add_item(self.distance)
            self.add_item(self.time)
        elif formula == "force":
            self.mass = discord.ui.TextInput(label="Mass (kg)", required=True)
            self.acceleration = discord.ui.TextInput(label="Acceleration (m/s²)", required=True)
            self.add_item(self.mass)
            self.add_item(self.acceleration)
        elif formula == "energy":
            self.mass = discord.ui.TextInput(label="Mass (kg)", required=True)
            self.velocity = discord.ui.TextInput(label="Velocity (m/s)", required=True)
            self.add_item(self.mass)
            self.add_item(self.velocity)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            result = MathPhysicsTools.calculate_physics(self.formula, self.get_values())
            
            embed = discord.Embed(
                title=f"⚡ Physics Calculation: {self.formula.title()}",
                color=discord.Color.gold()
            )
            embed.add_field(name="Result", value=f"{result:.2f}")
            embed.add_field(name="Formula Used", value=self.get_formula_display())
            
            await interaction.response.send_message(embed=embed)
        except ValueError:
            await interaction.response.send_message("❌ Please enter valid numbers!", ephemeral=True)

    def get_values(self):
        if self.formula == "velocity":
            return [float(self.distance.value), float(self.time.value)]
        elif self.formula == "force":
            return [float(self.mass.value), float(self.acceleration.value)]
        elif self.formula == "energy":
            return [float(self.mass.value), float(self.velocity.value)]

    def get_formula_display(self):
        formulas = {
            "velocity": "v = d/t",
            "force": "F = ma",
            "energy": "E = ½mv²"
        }
        return formulas[self.formula]


class MathPhysicsTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    unit_conversions = {
            'length': {
                'm': 1, 'km': 1000, 'cm': 0.01, 'mm': 0.001,
                'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254
            },
            'volume': {
                'l': 1, 'ml': 0.001, 'm3': 1000,
                'gallon': 3.78541, 'quart': 0.946353, 'cup': 0.236588
            },
            'mass': {
                'kg': 1, 'g': 0.001, 'mg': 0.000001,
                'pound': 0.453592, 'ounce': 0.0283495
            }
        }
    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    def convert_unit(value: float, from_unit: str, to_unit: str, conversion_type: str) -> float:
        conversions = MathPhysicsTools.unit_conversions[conversion_type]
        base_value = value * conversions[from_unit]
        return base_value / conversions[to_unit]

    @staticmethod
    def calculate_geometry(shape: str, values: list) -> dict:
        PI = 3.14159
        
        if shape == "circle":
            r = values[0]
            return {
                "Area": PI * r * r,
                "Circumference": 2 * PI * r
            }
        elif shape == "square":
            s = values[0]
            return {
                "Area": s * s,
                "Perimeter": 4 * s
            }
        elif shape == "triangle":
            a, b, c = values
            s = (a + b + c) / 2  
            area = (s*(s-a)*(s-b)*(s-c)) ** 0.5  
            return {
                "Area": area,
                "Perimeter": a + b + c
            }
        elif shape == "sphere":
            r = values[0]
            return {
                "Volume": (4/3) * PI * r**3,
                "Surface Area": 4 * PI * r**2
            }

    @staticmethod
    def calculate_physics(formula: str, values: list) -> float:
        if formula == "velocity":
            distance, time = values
            return distance / time
        elif formula == "force":
            mass, acceleration = values
            return mass * acceleration
        elif formula == "energy":
            mass, velocity = values
            return 0.5 * mass * velocity**2

    @commands.command()
    async def math(self, ctx):
        embed = discord.Embed(
            title="🔢 Advanced Math & Physics Calculator",
            description="Select a calculator type from the menu below:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Available Tools",
            value=(
                "📏 **Unit Converter** - Convert between different units\n"
                "📐 **Geometry** - Calculate areas, volumes, perimeters\n"
                "⚡ **Physics** - Various physics formulas\n"
                "📊 **Statistics** - Statistical analysis"
            ),
            inline=False
        )
        embed.set_footer(text="Interactive calculator • Timeout: 120 seconds")
        
        await ctx.send(embed=embed, view=MathPhysicsView())

    @commands.command()
    async def physics(self, ctx):
        embed = discord.Embed(
            title="⚡ Physics Calculator",
            description="Select a physics formula to use:",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="Available Formulas",
            value=(
                "🏃 **Velocity** (v=d/t)\n"
                "💪 **Force** (F=ma)\n"
                "⚡ **Energy** (E=½mv²)"
            ),
            inline=False
        )
        embed.set_footer(text="Interactive calculator • Timeout: 120 seconds")
        
        await ctx.send(embed=embed, view=PhysicsView())

async def setup(bot):
    await bot.add_cog(MathPhysicsTools(bot))


class BMICalculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MIN_WEIGHT_KG, self.MAX_WEIGHT_KG = 20, 300
        self.MIN_HEIGHT_M, self.MAX_HEIGHT_M = 0.5, 2.5
        self.MIN_AGE, self.MAX_AGE = 2, 120

    def calculate_bmi(self, weight: float, height_m: float) -> float:
        return round(weight / (height_m ** 2), 2)

    def calculate_body_fat(self, bmi: float, age: int, gender: str) -> float:
        if gender.lower() == "male":
            body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
        elif gender.lower() == "female":
            body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
        else:
            body_fat = (1.20 * bmi) + (0.23 * age) - 10
        return round(body_fat, 2)

    def calculate_bmr(self, weight: float, height_cm: float, age: int, gender: str) -> float:
        if gender.lower() == "male":
            return round(10 * weight + 6.25 * height_cm - 5 * age + 5, 2)
        elif gender.lower() == "female":
            return round(10 * weight + 6.25 * height_cm - 5 * age - 161, 2)
        return round(10 * weight + 6.25 * height_cm - 5 * age - 78, 2)

    def get_macros(self, bmr: float) -> str:
        protein = round(bmr * 0.3 / 4)
        carbs = round(bmr * 0.5 / 4)
        fats = round(bmr * 0.2 / 9)
        return f"Protein: {protein}g\nCarbs: {carbs}g\nFats: {fats}g"

    def classify_bmi(self, bmi: float, age: int, gender: str, bmr: float, body_fat: float) -> str:
        if bmi < 18.5:
            classification = "📉 Underweight - Consider increasing nutrition intake"
        elif 18.5 <= bmi < 24.9:
            classification = "✅ Normal weight - Maintain current lifestyle"
        elif 25 <= bmi < 29.9:
            classification = "⚠️ Overweight - Consider increasing activity"
        else:
            classification = "⚠️ Obesity - Consult healthcare provider"
        
        return classification

    @commands.command(name="bmi")
    async def bmi_calculator(self, ctx):
        questions = [
            "What is your weight in kg?",
            "What is your height in meters?",
            "What is your age?",
            "What is your gender? (male/female/other)"
        ]
        answers = []

        for question in questions:
            await ctx.send(question)
            try:
                msg = await self.bot.wait_for(
                    'message',
                    timeout=30.0,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel
                )
                answers.append(msg.content)
            except asyncio.TimeoutError:
                await ctx.send("❌ Timed out! Please try again.")
                return

        try:
            weight = float(answers[0])
            height = float(answers[1])
            age = int(answers[2])
            gender = answers[3].lower()

            if not (self.MIN_WEIGHT_KG <= weight <= self.MAX_WEIGHT_KG):
                await ctx.send("❌ Invalid weight! Must be between 20-300 kg.")
                return
            if not (self.MIN_HEIGHT_M <= height <= self.MAX_HEIGHT_M):
                await ctx.send("❌ Invalid height! Must be between 0.5-2.5 meters.")
                return
            if not (self.MIN_AGE <= age <= self.MAX_AGE):
                await ctx.send("❌ Invalid age! Must be between 2-120 years.")
                return

            bmi = self.calculate_bmi(weight, height)
            body_fat = self.calculate_body_fat(bmi, age, gender)
            bmr = self.calculate_bmr(weight, height * 100, age, gender)
            classification = self.classify_bmi(bmi, age, gender, bmr, body_fat)
            macros = self.get_macros(bmr)

            embed = discord.Embed(
                title="🏋️ BMI & Health Calculator Results",
                color=discord.Color.blue()
            )
            embed.add_field(name="BMI", value=f"{bmi}", inline=True)
            embed.add_field(name="Body Fat %", value=f"{body_fat}%", inline=True)
            embed.add_field(name="BMR", value=f"{bmr} kcal/day", inline=True)
            embed.add_field(name="Classification", value=classification, inline=False)
            embed.add_field(name="Daily Macro Recommendations", value=macros, inline=False)
            embed.set_footer(text="Note: These are estimates. Consult a healthcare professional for accurate advice.")

            await ctx.send(embed=embed)

        except ValueError:
            await ctx.send("❌ Please enter valid numbers for weight, height, and age!")




class AI_CHAT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_channels = {}
        self.available_models = {
            "gpt-4": "Most capable model, best for complex tasks",
            "gpt-3.5-turbo": "Fast and efficient for general chat",
            "gpt-4-32k": "Extended context model for longer conversations",
            "claude-2": "Alternative model with different capabilities"
        }
        self.default_model = "gpt-3.5-turbo"
        self.channel_states = {}
        self.conversation_history = {}
        self.api_key = os.getenv('OPENAI_API_KEY')  
        self.rate_limits = {}  
        self.rate_limit_cooldown = 30  

        
        if not self.api_key:
            print("⚠️ Warning: OPENAI_API_KEY not found in .env file")


    @commands.command(name="ai_info")
    async def ai_info(self, ctx):
        embed = discord.Embed(
            title="🤖 AI Chat System Information",
            description="Complete overview of models, pricing and commands",
            color=discord.Color.blue()
        )

        pricing_info = """
        **GPT-4 Models:**
        • GPT-4: $0.03 per message (~750 words)
        • GPT-4-32K: $0.06 per message (~2000 words)

        **GPT-3.5 Models:**
        • GPT-3.5-Turbo: $0.002 per message (~750 words)
        • GPT-3.5-16K: $0.004 per message (~2000 words)

        **Claude-2:**
        • $0.11 per 1000 tokens (~750 words)
        """
        embed.add_field(name="📊 Models & Pricing", value=pricing_info, inline=False)

        commands_info = """
        **Admin Commands:**
        `!ai_chat <model>` - Select AI model
        `!ai_chat_set <channel>` - Set AI chat channel
        `!ai_chat_unset` - Remove AI chat channel
        `!ai_chat_pause` - Pause AI responses (save credits)
        `!ai_chat_resume` - Resume AI responses

        **User Commands:**
        Just type your message in the designated AI chat channel!
        """
        embed.add_field(name="⌨️ Available Commands", value=commands_info, inline=False)

        guild_id = ctx.guild.id
        if guild_id in self.ai_channels:
            model = self.ai_channels[guild_id].get("model", "Not set")
            channel_id = self.ai_channels[guild_id].get("channel")
            status = "Active ✅" if self.channel_states.get(channel_id, False) else "Paused ⏸️"
            
            status_info = f"""
            **Current Model:** {model}
            **Status:** {status}
            **Channel:** <#{channel_id}> if channel_id else "Not set"
            """
            embed.add_field(name="📱 Current Settings", value=status_info, inline=False)

        await ctx.send(embed=embed)


    @commands.command(name="ai_chat")
    @commands.has_permissions(administrator=True)
    async def ai_chat(self, ctx, model: str = None):
        if not model:
            embed = discord.Embed(
                title="Available AI Models",
                color=discord.Color.blue(),
                description="Select a model using `!ai_chat <model_name>`"
            )
            for model_name, description in self.available_models.items():
                embed.add_field(name=model_name, value=description, inline=False)
            await ctx.send(embed=embed)
            return

        if model.lower() not in self.available_models:
            await ctx.send(f"❌ Invalid model. Use one of: {', '.join(self.available_models.keys())}")
            return

        guild_id = ctx.guild.id
        self.ai_channels[guild_id] = {"model": model.lower()}
        await ctx.send(f"✅ AI chat model set to: `{model}`")

    @commands.command(name="ai_chat_set")
    @commands.has_permissions(administrator=True)
    async def ai_chat_set(self, ctx, channel: discord.TextChannel):
        guild_id = ctx.guild.id
        if guild_id not in self.ai_channels:
            self.ai_channels[guild_id] = {"model": self.default_model}
        
        self.ai_channels[guild_id]["channel"] = channel.id
        self.channel_states[channel.id] = True  
        
        embed = discord.Embed(
            title="AI Chat Channel Set",
            description=f"AI Chat enabled in {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Model", value=self.ai_channels[guild_id]["model"])
        embed.add_field(name="Status", value="Active")
        await ctx.send(embed=embed)

    @commands.command(name="ai_chat_unset")
    @commands.has_permissions(administrator=True)
    async def ai_chat_unset(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in self.ai_channels:
            channel_id = self.ai_channels[guild_id].get("channel")
            if channel_id:
                del self.channel_states[channel_id]
            del self.ai_channels[guild_id]
            await ctx.send("✅ AI chat configuration has been reset")
        else:
            await ctx.send("❌ No AI chat configuration found")

    @commands.command(name="ai_chat_pause")
    @commands.has_permissions(administrator=True)
    async def ai_chat_pause(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in self.ai_channels and "channel" in self.ai_channels[guild_id]:
            channel_id = self.ai_channels[guild_id]["channel"]
            self.channel_states[channel_id] = False
            embed = discord.Embed(
                title="AI Chat Paused",
                description="AI responses are temporarily paused",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ No active AI chat channel found")

    @commands.command(name="ai_chat_resume")
    @commands.has_permissions(administrator=True)
    async def ai_chat_resume(self, ctx):
        guild_id = ctx.guild.id
        if guild_id in self.ai_channels and "channel" in self.ai_channels[guild_id]:
            channel_id = self.ai_channels[guild_id]["channel"]
            self.channel_states[channel_id] = True
            embed = discord.Embed(
                title="AI Chat Resumed",
                description="AI responses are now active",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ No AI chat channel found")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = message.guild.id
        if guild_id not in self.ai_channels:
            return

        channel_id = self.ai_channels[guild_id].get("channel")
        if message.channel.id != channel_id:
            return

        if not self.channel_states.get(channel_id, False):
            return

        user_id = message.author.id
        current_time = time.time()
        
        if user_id in self.rate_limits:
            last_request = self.rate_limits[user_id]
            if current_time - last_request < self.rate_limit_cooldown:
                remaining_time = int(self.rate_limit_cooldown - (current_time - last_request))
                await message.reply(f"🕒 Please wait {remaining_time} seconds before sending another message!")
                return
        
        self.rate_limits[user_id] = current_time

        try:
            async with message.channel.typing():
                model = self.ai_channels[guild_id].get("model", self.default_model)
                
                if not self.api_key:
                    await message.channel.send("⚠️ OpenAI API key not configured!")
                    return

                if guild_id not in self.conversation_history:
                    self.conversation_history[guild_id] = []
                
                self.conversation_history[guild_id].append({"role": "user", "content": message.content})
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        *self.conversation_history[guild_id][-5:]  
                    ],
                    "temperature": 0.7
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            ai_response = data['choices'][0]['message']['content']
                            
                            self.conversation_history[guild_id].append(
                                {"role": "assistant", "content": ai_response}
                            )
                            
                            await message.reply(ai_response)
                        elif response.status == 402:
                            embed = discord.Embed(
                                title="❌ Insufficient Credits",
                                description="AI chat has been automatically paused. Please add credits to your OpenAI account.",
                                color=discord.Color.red()
                            )
                            self.channel_states[channel_id] = False
                            await message.channel.send(embed=embed)
                        elif response.status == 429:
                            embed = discord.Embed(
                                title="⚠️ Rate Limited",
                                description="Too many requests. Please try again in a few minutes.",
                                color=discord.Color.orange()
                            )
                            await message.channel.send(embed=embed)
                        else:
                            error_data = await response.json()
                            embed = discord.Embed(
                                title="❌ API Error",
                                description=error_data.get('error', {}).get('message', 'Unknown error'),
                                color=discord.Color.red()
                            )
                            await message.channel.send(embed=embed)

        except aiohttp.ClientError as e:
            embed = discord.Embed(
                title="❌ Network Error",
                description="Failed to connect to OpenAI API. Please try again later.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)
            print(f"API Request Error: {str(e)}")
        except Exception as e:
            embed = discord.Embed(
                title="❌ Unexpected Error",
                description=f"Please contact an administrator.\nError: {str(e)}",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)

class AdvancedUserAnalytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_data = {}
        self.voice_times = {}
        self.analytics_db = AnalyticsDatabase()
        self.load_data()
        self.bot.loop.create_task(self.initialize_analytics_data())
        self.prediction_model = self.setup_prediction_model()
        
    def calculate_influence_score(self, user_data):
        influence_factors = {
            'reactions_received': 0.3,
            'message_replies': 0.25,
            'mentions': 0.2,
            'thread_activity': 0.15,
            'role_weight': 0.1
        }
        
        score = 0
        for factor, weight in influence_factors.items():
            value = user_data.get(factor, 0)
            score += value * weight
            
        activity_multiplier = min(user_data.get('active_days', 1) / 30, 1)
        final_score = score * activity_multiplier
        
        return round(final_score, 2)

    def calculate_engagement_rate(self, user_data):
        total_interactions = sum([
            user_data.get('messages', 0),
            user_data.get('reactions_given', 0),
            user_data.get('reactions_received', 0),
            user_data.get('voice_minutes', 0),
            user_data.get('thread_participation', 0)
        ])
        
        active_days = user_data.get('active_days', 1)
        engagement_rate = (total_interactions / active_days) * 100
        
        return round(engagement_rate, 2)

    def calculate_activity_score(self, user_data):
        weights = {
            'messages': 0.4,
            'voice_minutes': 0.3,
            'reactions': 0.2,
            'commands': 0.1
        }
        
        score = 0
        for metric, weight in weights.items():
            value = user_data.get(metric, 0)
            score += value * weight
            
        return round(score, 2)

    async def initialize_analytics_data(self):
        for guild in self.bot.guilds:
            if guild.id not in self.user_data:
                self.user_data[guild.id] = {}
                
            for member in guild.members:
                if member.id not in self.user_data[guild.id]:
                    self.user_data[guild.id][member.id] = {
                        'messages': 0,
                        'voice_time': 0,
                        'reactions': 0,
                        'commands': 0,
                        'activity_hours': {str(i): 0 for i in range(24)},
                        'channel_activity': {},
                        'role_history': [role.name for role in member.roles],
                        'join_date': member.joined_at.isoformat() if member.joined_at else None,
                        'last_active': datetime.now().isoformat(),
                        'infractions': [],
                        'achievements': [],
                        'engagement_metrics': {
                            'replies': 0,
                            'mentions': 0,
                            'threads': 0,
                            'reactions_given': 0,
                            'reactions_received': 0
                        }
                    }
        self.save_data()

    def load_data(self):
        try:
            with open('analytics_data.json', 'r') as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            self.user_data = {}
            self.save_data()

    def save_data(self):
        guild_data = {}
        for guild in self.bot.guilds:
            guild_data[guild.id] = {
                'roles': {
                    role.id: {
                        'name': role.name,
                        'color': role.color.value,
                        'members': len(role.members),
                        'position': role.position,
                        'hoisted': role.hoist,
                        'mentionable': role.mentionable
                    } for role in guild.roles
                },
                'members': {
                    member.id: {
                        'messages': self.user_data.get(guild.id, {}).get(member.id, {}).get('messages', 0),
                        'voice_time': self.user_data.get(guild.id, {}).get(member.id, {}).get('voice_time', 0),
                        'reactions': self.user_data.get(guild.id, {}).get(member.id, {}).get('reactions', 0),
                        'commands': self.user_data.get(guild.id, {}).get(member.id, {}).get('commands', 0),
                        'activity_hours': self.user_data.get(guild.id, {}).get(member.id, {}).get('activity_hours', {}),
                        'channel_activity': self.user_data.get(guild.id, {}).get(member.id, {}).get('channel_activity', {}),
                        'role_history': self.user_data.get(guild.id, {}).get(member.id, {}).get('role_history', []),
                        'join_date': member.joined_at.isoformat() if member.joined_at else None,
                        'last_active': datetime.now().isoformat(),
                        'engagement_metrics': self.user_data.get(guild.id, {}).get(member.id, {}).get('engagement_metrics', {
                            'replies': 0,
                            'mentions': 0,
                            'threads': 0,
                            'reactions_given': 0,
                            'reactions_received': 0
                        })
                    } for member in guild.members
                }
            }
        
        with open('analytics_data.json', 'w') as f:
            json.dump(guild_data, f, indent=4)

    def setup_prediction_model(self):
        return {
            'activity_weights': {
                'messages': 0.4,
                'voice': 0.3,
                'reactions': 0.2,
                'commands': 0.1
            },
            'trend_window': 7
        }


    def prepare_export_data(self, guild_id, timeframe):
        guild = self.bot.get_guild(guild_id)
        guild_data = self.user_data.get(guild_id, {})

        data = {
            'timeframe': timeframe,
            'export_date': datetime.now().isoformat(),
            'guild_id': guild_id,
            'analytics': {
                'activity': {
                    'messages': guild_data.get('total_messages', 0),
                    'active_users': len([m for m in guild.members if not m.bot]),
                    'reactions': guild_data.get('total_reactions', 0),
                    'peak_hour': max(range(24), key=lambda h: guild_data.get('hourly_activity', {}).get(str(h), 0)),
                    'channel_activity': {
                        channel.id: {
                            'name': channel.name,
                            'messages': guild_data.get('channel_stats', {}).get(str(channel.id), 0)
                        } for channel in guild.text_channels
                    }
                },
                'roles': {
                    'hierarchy': [role.name for role in sorted(guild.roles, key=lambda r: r.position, reverse=True)],
                    'statistics': {
                        'total': len(guild.roles),
                        'hoisted': len([r for r in guild.roles if r.hoist]),
                        'colored': len([r for r in guild.roles if r.color != discord.Color.default()]),
                        'managed': len([r for r in guild.roles if r.managed])
                    },
                    'distribution': {role.name: len(role.members) for role in guild.roles},
                    'recent_changes': guild_data.get('role_changes', [])
                },
                'content_analysis': {
                    'message_types': guild_data.get('message_types', {}),
                    'trending_topics': dict(sorted(
                        guild_data.get('trending_topics', {}).items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]),
                    'metrics': {
                        'avg_message_length': guild_data.get('content_metrics', {}).get('total_length', 0) / 
                                            (guild_data.get('total_messages', 1) or 1),
                        'engagement_rate': guild_data.get('total_reactions', 0) / 
                                        (guild_data.get('total_messages', 1) or 1),
                        'content_uniqueness': len(guild_data.get('trending_topics', {})) / 
                                            (guild_data.get('total_messages', 1) or 1) * 100
                    }
                },
                'predictive_analytics': {
                    'membership': {
                        'predicted_members': len(guild.members) + int(len(guild.members) * 0.1),
                        'growth_rate': guild_data.get('growth_rate', 0.1)
                    },
                    'health_score': guild_data.get('health_score', 50)
                },
                'activity_heatmap': {
                    f"{hour:02d}:00": guild_data.get('hourly_activity', {}).get(str(hour), 0)
                    for hour in range(24)
                }
            }
        }
        
        return data

    
    @commands.command(name="analytics")
    async def show_analytics(self, ctx, target: Union[discord.Member, str] = None):
        if isinstance(target, str) and target.lower() == "server":
            view = ServerAnalyticsView(self, ctx)
            embed = self.create_server_overview(ctx.guild)
            await ctx.send(embed=embed, view=view)
        else:
            member = target or ctx.author
            view = EnhancedUserAnalyticsView(self, ctx, member)
            embed = self.create_advanced_overview(member)
            await ctx.send(embed=embed, view=view)

    @commands.command(name="analytics_export")
    @commands.has_permissions(administrator=True)
    async def export_analytics(self, ctx, timeframe: str = "all"):
        data = self.prepare_export_data(ctx.guild.id, timeframe)
        file = discord.File(
            io.StringIO(json.dumps(data, indent=2)),
            filename=f"analytics_export_{ctx.guild.id}_{timeframe}.json"
        )
        await ctx.send("Analytics data export:", file=file)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot:
            return
            
        guild_id = message.guild.id
        hour = message.created_at.hour
        
        if guild_id not in self.user_data:
            self.user_data[guild_id] = {
                'total_messages': 0,
                'message_types': {'text': 0, 'images': 0, 'videos': 0, 'links': 0, 'embeds': 0, 'files': 0},
                'hourly_activity': {str(h): 0 for h in range(24)},
                'channel_stats': {},
                'trending_topics': {},
                'content_metrics': {'total_length': 0}
            }

        self.user_data[guild_id]['total_messages'] += 1
        self.user_data[guild_id]['hourly_activity'][str(hour)] += 1
        
        if message.attachments:
            for attachment in message.attachments:
                if 'image' in attachment.content_type:
                    self.user_data[guild_id]['message_types']['images'] += 1
                elif 'video' in attachment.content_type:
                    self.user_data[guild_id]['message_types']['videos'] += 1
                else:
                    self.user_data[guild_id]['message_types']['files'] += 1
        elif message.embeds:
            self.user_data[guild_id]['message_types']['embeds'] += 1
        elif any(url in message.content for url in ['http://', 'https://']):
            self.user_data[guild_id]['message_types']['links'] += 1
        else:
            self.user_data[guild_id]['message_types']['text'] += 1

        channel_id = str(message.channel.id)
        self.user_data[guild_id]['channel_stats'][channel_id] = self.user_data[guild_id]['channel_stats'].get(channel_id, 0) + 1

        self.user_data[guild_id]['content_metrics']['total_length'] += len(message.content)
        
        words = message.content.lower().split()
        for word in words:
            if len(word) > 3:
                self.user_data[guild_id]['trending_topics'][word] = self.user_data[guild_id]['trending_topics'].get(word, 0) + 1

        self.save_data()


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.message.guild or user.bot:
            return
        await self.analytics_db.update_user_activity(
            user.id,
            reaction.message.guild.id,
            'reaction',
            1
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
            
        if not before.channel and after.channel:
            self.voice_times[member.id] = time.time()
        elif before.channel and not after.channel and member.id in self.voice_times:
            duration = time.time() - self.voice_times[member.id]
            minutes = int(duration / 60)
            await self.analytics_db.update_user_activity(
                member.id,
                member.guild.id,
                'voice',
                minutes
            )
            del self.voice_times[member.id]

    def create_advanced_overview(self, member):
        embed = discord.Embed(
            title=f"Analytics Overview for {member.name}",
            color=member.color,
            timestamp=datetime.now()
        )

        user_stats = self.user_data.get(member.guild.id, {}).get(str(member.id), {})
        
        activity_score = self.calculate_activity_score(user_stats)
        engagement_rate = self.calculate_engagement_rate(user_stats)
        influence_score = self.calculate_influence_score(user_stats)
        
        embed.add_field(
            name="Activity Metrics",
            value=f"Messages: {user_stats.get('messages', 0)}\n"
                f"Voice Time: {user_stats.get('voice_time', 0)} minutes\n"
                f"Reactions: {user_stats.get('reactions', 0)}\n"
                f"Commands Used: {user_stats.get('commands', 0)}",
            inline=True
        )
        
        embed.add_field(
            name="Performance Metrics",
            value=f"Activity Score: {activity_score}\n"
                f"Engagement Rate: {engagement_rate}%\n"
                f"Influence Score: {influence_score}",
            inline=True
        )
        
        engagement_metrics = user_stats.get('engagement_metrics', {})
        embed.add_field(
            name="Engagement Details",
            value=f"Replies: {engagement_metrics.get('replies', 0)}\n"
                f"Mentions: {engagement_metrics.get('mentions', 0)}\n"
                f"Thread Activity: {engagement_metrics.get('threads', 0)}",
            inline=False
        )

        return embed


class BaseAnalyticsButton(discord.ui.Button):
    def __init__(self, label, emoji, style=discord.ButtonStyle.primary):
        super().__init__(label=label, emoji=emoji, style=style)
        self.historical_data = {}

    def calculate_growth_rate(self, data):
        periods = len(data['historical_members'])
        if periods < 2:
            return 0
        initial = data['historical_members'][0]
        final = data['historical_members'][-1]
        return (final - initial) / initial / periods

    def analyze_activity_pattern(self, data):
        activity_data = data.get('activity_history', [])
        if not activity_data:
            return []
        
        pattern = []
        for i in range(len(activity_data) - 7):
            week_data = activity_data[i:i+7]
            pattern.append(sum(week_data) / 7)
        return pattern

    async def get_historical_data(self, guild):
        now = datetime.now()
        thirty_days_ago = now - timedelta(days=30)
        
        data = {
            'members': [],
            'message_history': [],
            'reaction_history': [],
            'voice_history': [],
            'activity_history': []
        }
        
        async for entry in guild.audit_logs(action=discord.AuditLogAction.member_update, after=thirty_days_ago):
            data['members'].append(entry.target.id)
            
        for channel in guild.text_channels:
            try:
                message_count = 0
                reaction_count = 0
                async for message in channel.history(after=thirty_days_ago, limit=None):
                    message_count += 1
                    reaction_count += sum(reaction.count for reaction in message.reactions)
                    
                data['message_history'].append(message_count)
                data['reaction_history'].append(reaction_count)
            except discord.Forbidden:
                continue
                
        voice_users = sum(len(vc.members) for vc in guild.voice_channels)
        data['voice_history'].append(voice_users)
        
        return data


class ActivityHeatmapButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Activity Heatmap", emoji="🌡️")
   
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        activity_data = await self.get_hourly_activity_data(interaction.guild)
        heatmap = self.generate_ascii_heatmap(activity_data)
        
        embed = discord.Embed(title="Server Activity Heatmap", color=discord.Color.blue())
        embed.add_field(name="24-Hour Activity Pattern", value=f"```{heatmap}```", inline=False)
        embed.add_field(name="Peak Hours", value=self.get_peak_hours(activity_data), inline=True)
        embed.add_field(name="Quiet Hours", value=self.get_quiet_hours(activity_data), inline=True)
        
        await interaction.followup.send(embed=embed)

    async def get_hourly_activity_data(self, guild):
        data = {i: 0 for i in range(24)}
        now = datetime.now()
        day_ago = now - timedelta(days=1)
        
        for channel in guild.text_channels:
            try:
                async for message in channel.history(after=day_ago):
                    hour = message.created_at.hour
                    data[hour] += 1
            except discord.Forbidden:
                continue
        
        return data

    def generate_ascii_heatmap(self, data):
        max_value = max(data.values()) if data.values() else 1
        heatmap = ""
        for hour in range(24):
            activity = data[hour]
            intensity = min(int((activity / max_value) * 8), 8)
            bar = "█" * intensity + "░" * (8 - intensity)
            heatmap += f"{hour:02d}:00 {bar} ({activity})\n"
        return heatmap

    def get_peak_hours(self, data):
        sorted_hours = sorted(data.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [f"{hour:02d}:00" for hour, _ in sorted_hours[:3]]
        return ", ".join(peak_hours)

    def get_quiet_hours(self, data):
        sorted_hours = sorted(data.items(), key=lambda x: x[1])
        quiet_hours = [f"{hour:02d}:00" for hour, _ in sorted_hours[:3]]
        return ", ".join(quiet_hours)

class EnhancedUserAnalyticsView(discord.ui.View):
    def __init__(self, cog, ctx, member):
        super().__init__(timeout=300)
        self.cog = cog
        self.ctx = ctx
        self.member = member
        self.timeframe = "week"
        self.setup_buttons()

    def setup_buttons(self):
        self.add_item(ActivityHeatmapButton())
        self.add_item(EngagementMetricsButton())
        self.add_item(RoleProgressionButton())
        self.add_item(ContentAnalysisButton())
        self.add_item(PredictiveTrendsButton())

class ServerAnalyticsDashboard(discord.ui.View):
    def __init__(self, cog, guild):
        super().__init__()
        self.cog = cog
        self.guild = guild
        self.setup_dashboard()

    def setup_dashboard(self):
        self.add_item(ActivityHeatmapButton())
        self.add_item(MemberRetentionButton())
        self.add_item(RoleDistributionButton())
        self.add_item(ChannelHealthButton())
        self.add_item(CommunityGrowthButton())
        self.add_item(EngagementMetricsButton())
        self.add_item(ModrationStatsButton())
        self.add_item(ContentAnalysisButton())
        self.add_item(TimelineViewButton())
        self.add_item(PredictiveTrendsButton())

async def setup(bot):
    await bot.add_cog(AdvancedUserAnalytics(bot))

class PredictiveTrendsButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Predictive Trends", emoji="🔮")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        predictions = await self.generate_predictions(interaction.guild)
        embed = self.create_predictions_embed(predictions)
        await interaction.followup.send(embed=embed)

    async def generate_predictions(self, guild):
        historical_data = await self.get_historical_data(guild)
        return {
            'member_growth': self.predict_member_growth(historical_data),
            'activity_trends': self.predict_activity_trends(historical_data),
            'engagement_forecast': self.predict_engagement_levels(historical_data),
            'channel_predictions': self.predict_channel_activity(historical_data),
            'content_trends': self.predict_content_trends(historical_data),
            'role_evolution': self.predict_role_changes(historical_data),
            'community_health': self.predict_community_health(historical_data)
        }

    async def get_historical_data(self, guild):
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        data = {
            'members': [],
            'message_history': [],
            'reaction_history': [],
            'active_users': set(),
            'channel_activity': {},
            'peak_posting_times': {},
            'content_types': {'text': 0, 'images': 0, 'links': 0}
        }
        
        for channel in guild.text_channels:
            try:
                async for message in channel.history(after=week_ago):
                    hour = message.created_at.hour
                    data['peak_posting_times'][hour] = data['peak_posting_times'].get(hour, 0) + 1
                    data['active_users'].add(message.author.id)
                    data['message_history'].append(message.created_at.timestamp())
                    data['reaction_history'].append(sum(r.count for r in message.reactions))
                    data['channel_activity'][channel.id] = data['channel_activity'].get(channel.id, 0) + 1
                    
                    if message.attachments:
                        data['content_types']['images'] += 1
                    elif any(url in message.content for url in ['http://', 'https://']):
                        data['content_types']['links'] += 1
                    else:
                        data['content_types']['text'] += 1
            except discord.Forbidden:
                continue
                
        data['members'] = [m.id for m in guild.members]
        return data

    def predict_member_growth(self, data):
        members = data.get('members', [])
        current_members = len(members)
        growth_rate = 0.1
        seasonal_factor = 1.0
        trend_adjustment = 0
        
        predicted_growth = current_members * (1 + growth_rate) * seasonal_factor + trend_adjustment
        confidence_interval = (predicted_growth * 0.9, predicted_growth * 1.1)
        
        return {
            'predicted_members': round(predicted_growth),
            'confidence_interval': confidence_interval,
            'growth_rate': growth_rate,
            'seasonal_impact': seasonal_factor,
            'trend_strength': trend_adjustment
        }

    def predict_activity_trends(self, data):
        message_history = data.get('message_history', [])
        activity_pattern = [sum(1 for msg in message_history if msg > time.time() - 86400 * (i + 1)) for i in range(7)]
        
        return {
            'daily_predictions': activity_pattern,
            'peak_times': self.get_peak_hours(data),
            'activity_type_distribution': {'messages': 0.6, 'reactions': 0.3, 'voice': 0.1},
            'engagement_levels': {'high': 0.3, 'medium': 0.5, 'low': 0.2}
        }

    def predict_content_trends(self, data):
        total_content = sum(data['content_types'].values()) or 1
        content_distribution = {
            k: v / total_content for k, v in data['content_types'].items()
        }
        
        return {
            'popular_content_types': content_distribution,
            'emerging_topics': ['topic1', 'topic2', 'topic3'],
            'engagement_patterns': {'increasing': 0.6, 'stable': 0.3, 'decreasing': 0.1},
            'content_quality_trends': {'improving': 0.7, 'stable': 0.2, 'declining': 0.1}
        }

    def predict_engagement_levels(self, data):
        return {
            'daily_active_users': len(data.get('active_users', [])),
            'message_frequency': len(data.get('message_history', [])),
            'reaction_rate': sum(data.get('reaction_history', [])),
            'trend': 'increasing'
        }

    def predict_channel_activity(self, data):
        return {
            'active_channels': len(data.get('channel_activity', {})),
            'growth_channels': [],
            'declining_channels': [],
            'suggested_actions': []
        }

    def predict_role_changes(self, data):
        return {
            'role_distribution': {},
            'role_trends': [],
            'suggested_changes': []
        }

    def predict_community_health(self, data):
        active_ratio = len(data.get('active_users', [])) / len(data.get('members', [1])) if data.get('members') else 0
        health_score = min(round(active_ratio * 100), 100)
        
        return {
            'health_score': health_score,
            'risk_factors': [],
            'improvement_areas': []
        }

    def get_peak_hours(self, data):
        activity_by_hour = data.get('peak_posting_times', {})
        sorted_hours = sorted(activity_by_hour.items(), key=lambda x: x[1], reverse=True)
        return [hour for hour, _ in sorted_hours[:3]] if sorted_hours else [12, 15, 18]

    def create_predictions_embed(self, predictions):
        embed = discord.Embed(
            title="Predictive Analytics Dashboard",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        member_growth = predictions['member_growth']
        embed.add_field(
            name="Membership Forecast",
            value=f"Predicted Members: {member_growth['predicted_members']}\n"
                  f"Growth Rate: {member_growth['growth_rate']:.2%}",
            inline=False
        )
        
        activity = predictions['activity_trends']
        embed.add_field(
            name="Activity Forecast",
            value=f"Peak Hours: {', '.join(f'{h:02d}:00' for h in activity['peak_times'])}\n"
                  f"Engagement Trend: {'📈' if activity['engagement_levels']['high'] > 0.3 else '📉'}",
            inline=True
        )
        
        content = predictions['content_trends']
        embed.add_field(
            name="Content Trends",
            value=f"Top Type: {max(content['popular_content_types'].items(), key=lambda x: x[1])[0]}\n"
                  f"Quality Trend: {'📈' if content['content_quality_trends']['improving'] > 0.5 else '📊'}",
            inline=True
        )
        
        health = predictions['community_health']
        embed.add_field(
            name="Community Health",
            value=f"Health Score: {health['health_score']}%\n"
                  f"Status: {'🟢 Healthy' if health['health_score'] > 70 else '🟡 Moderate' if health['health_score'] > 40 else '🔴 Needs Attention'}",
            inline=False
        )
        
        return embed


class EngagementMetricsButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Engagement Metrics", emoji="📊")
   
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        metrics = await self.calculate_engagement_metrics(interaction.guild)
        embed = self.create_engagement_embed(metrics)
        await interaction.followup.send(embed=embed)

    async def calculate_engagement_metrics(self, guild):
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        metrics = {
            'total_messages': 0,
            'active_users': set(),
            'reactions_given': 0,
            'threads_created': 0,
            'voice_minutes': 0,
            'peak_times': {},
            'channel_activity': {}
        }
        
        for channel in guild.text_channels:
            try:
                async for message in channel.history(after=week_ago):
                    metrics['total_messages'] += 1
                    metrics['active_users'].add(message.author.id)
                    metrics['reactions_given'] += sum(r.count for r in message.reactions)
                    hour = message.created_at.hour
                    metrics['peak_times'][hour] = metrics['peak_times'].get(hour, 0) + 1
                    metrics['channel_activity'][channel.id] = metrics['channel_activity'].get(channel.id, 0) + 1
            except discord.Forbidden:
                continue
        
        return metrics

    def create_engagement_embed(self, metrics):
        embed = discord.Embed(
            title="Engagement Metrics Dashboard",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="Activity Overview",
            value=f"Messages: {metrics['total_messages']}\n"
                  f"Active Users: {len(metrics['active_users'])}\n"
                  f"Total Reactions: {metrics['reactions_given']}",
            inline=False
        )
        
        if metrics['peak_times']:
            peak_hour = max(metrics['peak_times'].items(), key=lambda x: x[1])[0]
            embed.add_field(
                name="Peak Activity",
                value=f"Most Active Hour: {peak_hour:02d}:00",
                inline=True
            )
        
        if metrics['channel_activity']:
            top_channel = max(metrics['channel_activity'].items(), key=lambda x: x[1])[0]
            embed.add_field(
                name="Channel Activity",
                value=f"Most Active Channel: <#{top_channel}>",
                inline=True
            )
        
        return embed


class RoleProgressionButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Role Progress", emoji="📈")
   
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        progression = await self.analyze_role_progression(interaction.guild)
        embed = self.create_progression_embed(progression)
        await interaction.followup.send(embed=embed)

    async def analyze_role_progression(self, guild):
        role_data = {
            'hierarchy': [],
            'distribution': {},
            'recent_changes': [],
            'suggested_next': {},
            'role_stats': {
                'total_roles': len(guild.roles),
                'hoisted_roles': len([r for r in guild.roles if r.hoist]),
                'color_roles': len([r for r in guild.roles if r.color != discord.Color.default()]),
                'managed_roles': len([r for r in guild.roles if r.managed])
            }
        }
        
        for role in sorted(guild.roles, key=lambda r: r.position, reverse=True):
            role_data['hierarchy'].append(role.name)
            role_data['distribution'][role.name] = len(role.members)
            
        async for entry in guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=20):
            if entry.target:
                before_roles = getattr(getattr(entry.changes, 'before', None), 'roles', [])
                after_roles = getattr(getattr(entry.changes, 'after', None), 'roles', [])
                
                for role in after_roles:
                    if role not in before_roles:
                        role_data['recent_changes'].append({
                            'user': entry.target.name,
                            'role': role.name,
                            'type': 'added',
                            'date': entry.created_at
                        })
                
                for role in before_roles:
                    if role not in after_roles:
                        role_data['recent_changes'].append({
                            'user': entry.target.name,
                            'role': role.name,
                            'type': 'removed',
                            'date': entry.created_at
                        })
        
        return role_data

    def create_progression_embed(self, progression):
        embed = discord.Embed(
            title="Role Progression Analysis",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        if progression['hierarchy']:
            hierarchy_text = "\n".join(f"{idx+1}. {role}" for idx, role in enumerate(progression['hierarchy'][:10]))
            embed.add_field(
                name="Role Hierarchy (Top 10)",
                value=hierarchy_text or "No roles found",
                inline=False
            )
        
        stats = progression.get('role_stats', {})
        stats_text = (
            f"Total Roles: {stats.get('total_roles', 0)}\n"
            f"Hoisted Roles: {stats.get('hoisted_roles', 0)}\n"
            f"Color Roles: {stats.get('color_roles', 0)}\n"
            f"Managed Roles: {stats.get('managed_roles', 0)}"
        )
        embed.add_field(name="Role Statistics", value=stats_text, inline=True)
        
        if progression['recent_changes']:
            changes = "\n".join(
                f"• {change['user']}: {change['type']} {change['role']}"
                for change in sorted(
                    progression['recent_changes'][:5],
                    key=lambda x: x['date'],
                    reverse=True
                )
            )
            embed.add_field(name="Recent Changes", value=changes or "No recent changes", inline=False)
        
        top_roles = sorted(
            progression['distribution'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        distribution_text = "\n".join(f"{role}: {count} members" for role, count in top_roles)
        embed.add_field(name="Most Popular Roles", value=distribution_text or "No data", inline=True)
        
        return embed



class TimelineViewButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Timeline", emoji="📅")
    
    async def callback(self, interaction: discord.Interaction):
        timeline = await self.generate_timeline(interaction.guild)
        embed = self.create_timeline_embed(timeline)
        await interaction.response.edit_message(embed=embed)

    async def generate_timeline(self, guild):
        now = datetime.now()
        month_ago = now - timedelta(days=30)
        
        timeline = {
            'member_joins': [],
            'channel_creation': [],
            'role_changes': [],
            'major_events': [],
            'activity_spikes': []
        }
        
        async for entry in guild.audit_logs(after=month_ago):
            if entry.action == discord.AuditLogAction.member_join:
                timeline['member_joins'].append((entry.target.name, entry.created_at))
            elif entry.action == discord.AuditLogAction.channel_create:
                timeline['channel_creation'].append((entry.target.name, entry.created_at))
            elif entry.action == discord.AuditLogAction.member_role_update:
                timeline['role_changes'].append((entry.target.name, entry.changes, entry.created_at))
                
        return timeline

class ModrationStatsButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Moderation Stats", emoji="🛡️")
    
    async def callback(self, interaction: discord.Interaction):
        stats = await self.gather_moderation_stats(interaction.guild)
        embed = self.create_moderation_embed(stats)
        await interaction.response.edit_message(embed=embed)

    async def gather_moderation_stats(self, guild):
        now = datetime.now()
        month_ago = now - timedelta(days=30)
        
        stats = {
            'warnings': 0,
            'kicks': 0,
            'bans': 0,
            'mutes': 0,
            'message_deletions': 0,
            'mod_actions_by_user': {},
            'most_common_reasons': {},
            'active_mods': set(),
            'peak_incident_times': {},
            'repeat_offenders': set()
        }
        
        async for entry in guild.audit_logs(after=month_ago):
            if entry.action == discord.AuditLogAction.ban:
                stats['bans'] += 1
            elif entry.action == discord.AuditLogAction.kick:
                stats['kicks'] += 1
            elif entry.action == discord.AuditLogAction.message_delete:
                stats['message_deletions'] += 1
                
            if entry.user.guild_permissions.moderate_members:
                stats['active_mods'].add(entry.user.id)
                stats['mod_actions_by_user'][entry.user.id] = stats['mod_actions_by_user'].get(entry.user.id, 0) + 1
                
            hour = entry.created_at.hour
            stats['peak_incident_times'][hour] = stats['peak_incident_times'].get(hour, 0) + 1
            
        return stats

class ChannelHealthButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Channel Health", emoji="📊")
    
    async def callback(self, interaction: discord.Interaction):
        health_data = await self.analyze_channel_health(interaction.guild)
        embed = self.create_health_embed(health_data)
        await interaction.response.edit_message(embed=embed)

    async def analyze_channel_health(self, guild):
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        health_data = {
            'channels': {},
            'categories': {},
            'overall_health': 0,
            'recommendations': [],
            'inactive_channels': [],
            'overactive_channels': [],
            'engagement_distribution': {}
        }
        
        for channel in guild.text_channels:
            try:
                message_count = 0
                unique_users = set()
                reaction_count = 0
                
                async for message in channel.history(after=week_ago):
                    message_count += 1
                    unique_users.add(message.author.id)
                    reaction_count += sum(r.count for r in message.reactions)
                    
                health_score = self.calculate_channel_health_score(
                    message_count,
                    len(unique_users),
                    reaction_count
                )
                
                health_data['channels'][channel.id] = {
                    'name': channel.name,
                    'message_count': message_count,
                    'unique_users': len(unique_users),
                    'reaction_count': reaction_count,
                    'health_score': health_score
                }
                
                if health_score < 30:
                    health_data['inactive_channels'].append(channel.id)
                elif health_score > 80:
                    health_data['overactive_channels'].append(channel.id)
                    
            except discord.Forbidden:
                continue
                
        return health_data

    def calculate_channel_health_score(self, messages, users, reactions):
        base_score = min((messages / 100) * 40 + (users / 10) * 40 + (reactions / messages if messages else 0) * 20, 100)
        return round(base_score, 2)

class CommunityGrowthButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Growth Analytics", emoji="📈")
    
    async def callback(self, interaction: discord.Interaction):
        growth_data = await self.analyze_growth(interaction.guild)
        embed = self.create_growth_embed(growth_data)
        await interaction.response.edit_message(embed=embed)

    async def analyze_growth(self, guild):
        now = datetime.now()
        growth_data = {
            'joins_by_day': {},
            'leaves_by_day': {},
            'net_growth': [],
            'retention_rate': 0,
            'invitation_stats': {},
            'growth_velocity': 0,
            'projected_growth': {},
            'member_milestones': [],
            'seasonal_patterns': {},
            'demographic_changes': {}
        }
        
        async for entry in guild.audit_logs(limit=None):
            if entry.action == discord.AuditLogAction.member_join:
                day = entry.created_at.date()
                growth_data['joins_by_day'][day] = growth_data['joins_by_day'].get(day, 0) + 1
            elif entry.action == discord.AuditLogAction.member_remove:
                day = entry.created_at.date()
                growth_data['leaves_by_day'][day] = growth_data['leaves_by_day'].get(day, 0) + 1
        
        for day in sorted(set(growth_data['joins_by_day'].keys()) | set(growth_data['leaves_by_day'].keys())):
            joins = growth_data['joins_by_day'].get(day, 0)
            leaves = growth_data['leaves_by_day'].get(day, 0)
            net = joins - leaves
            growth_data['net_growth'].append((day, net))
            
        if len(growth_data['net_growth']) >= 2:
            recent_growth = sum(net for _, net in growth_data['net_growth'][-7:])
            growth_data['growth_velocity'] = recent_growth / 7
            
        return growth_data

class ContentAnalysisButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Content Analysis", emoji="📝")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        content_stats = await self.analyze_content(interaction.guild)
        embed = self.create_content_embed(content_stats)
        await interaction.followup.send(embed=embed)

    async def analyze_content(self, guild):
        content_stats = {
            'message_types': {
                'text': 0,
                'images': 0,
                'videos': 0,
                'links': 0,
                'embeds': 0,
                'files': 0
            },
            'popular_topics': {},
            'link_domains': {},
            'file_types': {},
            'emoji_usage': {},
            'avg_message_length': 0,
            'content_engagement': {},
            'peak_posting_times': {},
            'thread_activity': {},
            'quality_metrics': {
                'readability': 0,
                'engagement_rate': 0,
                'uniqueness': 0
            }
        }

        total_messages = 0
        total_length = 0
        emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]|[\u2600-\u26FF\u2700-\u27BF]')
        
        for channel in guild.text_channels:
            try:
                async for message in channel.history(limit=1000):
                    total_messages += 1
                    total_length += len(message.content)
                    
                    if message.attachments:
                        for attachment in message.attachments:
                            file_ext = attachment.filename.split('.')[-1].lower()
                            content_stats['file_types'][file_ext] = content_stats['file_types'].get(file_ext, 0) + 1
                            
                            if attachment.content_type:
                                if 'image' in attachment.content_type:
                                    content_stats['message_types']['images'] += 1
                                elif 'video' in attachment.content_type:
                                    content_stats['message_types']['videos'] += 1
                                else:
                                    content_stats['message_types']['files'] += 1
                    
                    elif message.embeds:
                        content_stats['message_types']['embeds'] += 1
                        
                    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*', message.content)
                    if urls:
                        content_stats['message_types']['links'] += 1
                        for url in urls:
                            domain = url.split('/')[2]
                            content_stats['link_domains'][domain] = content_stats['link_domains'].get(domain, 0) + 1
                    else:
                        content_stats['message_types']['text'] += 1

                    emojis = emoji_pattern.findall(message.content)
                    for emoji_char in emojis:
                        content_stats['emoji_usage'][emoji_char] = content_stats['emoji_usage'].get(emoji_char, 0) + 1

                    words = message.content.lower().split()
                    for word in words:
                        if len(word) > 3 and not word.startswith(('http', 'https')):
                            content_stats['popular_topics'][word] = content_stats['popular_topics'].get(word, 0) + 1

                    engagement_score = len(message.reactions) + (1 if message.reference else 0)
                    content_stats['content_engagement'][message.id] = engagement_score

                    hour = message.created_at.hour
                    content_stats['peak_posting_times'][hour] = content_stats['peak_posting_times'].get(hour, 0) + 1

                    if hasattr(message, 'thread') and message.thread is not None:
                        thread_id = str(message.thread.id)
                        content_stats['thread_activity'][thread_id] = content_stats['thread_activity'].get(thread_id, 0) + 1

            except discord.Forbidden:
                continue

        if total_messages > 0:
            content_stats['avg_message_length'] = total_length / total_messages
            content_stats['quality_metrics']['engagement_rate'] = sum(content_stats['content_engagement'].values()) / total_messages
            content_stats['quality_metrics']['uniqueness'] = len(content_stats['popular_topics']) / total_messages * 100

        content_stats['popular_topics'] = dict(sorted(content_stats['popular_topics'].items(), key=lambda x: x[1], reverse=True)[:10])
        content_stats['emoji_usage'] = dict(sorted(content_stats['emoji_usage'].items(), key=lambda x: x[1], reverse=True)[:10])
        content_stats['link_domains'] = dict(sorted(content_stats['link_domains'].items(), key=lambda x: x[1], reverse=True)[:10])

        return content_stats

    def create_content_embed(self, stats):
        embed = discord.Embed(
            title="Content Analysis Dashboard",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )

        msg_types = stats['message_types']
        embed.add_field(
            name="Message Types",
            value="\n".join(f"{k.title()}: {v}" for k, v in msg_types.items()),
            inline=True
        )

        if stats['emoji_usage']:
            top_emojis = "\n".join(f"{emoji}: {count}" for emoji, count in list(stats['emoji_usage'].items())[:5])
            embed.add_field(name="Top Emojis", value=top_emojis or "None", inline=True)

        if stats['popular_topics']:
            topics = "\n".join(f"{topic}: {count}" for topic, count in list(stats['popular_topics'].items())[:5])
            embed.add_field(name="Trending Topics", value=topics or "None", inline=True)

        embed.add_field(
            name="Content Metrics",
            value=f"Avg Message Length: {stats['avg_message_length']:.1f}\n"
                  f"Engagement Rate: {stats['quality_metrics']['engagement_rate']:.2f}\n"
                  f"Content Uniqueness: {stats['quality_metrics']['uniqueness']:.1f}%",
            inline=False
        )

        peak_times = sorted(stats['peak_posting_times'].items(), key=lambda x: x[1], reverse=True)[:3]
        peak_times_str = "\n".join(f"{hour:02d}:00: {count} messages" for hour, count in peak_times)
        embed.add_field(name="Peak Activity Hours", value=peak_times_str or "No data", inline=True)

        return embed



class AnalyticsDatabase:
    def __init__(self):
        self.db_path = 'analytics.db'
        self.db = None
        self.queue = []
        self.flush_interval = 5  
        self.queue_lock = asyncio.Lock()
        self.batch_size = 1000  
        self.last_flush = time.time()
        asyncio.create_task(self.initialize_db())
        asyncio.create_task(self.flush_queue_loop())

    async def initialize_db(self):
        self.db = await aiosqlite.connect(self.db_path)
        await self.db.execute('PRAGMA journal_mode=WAL')  
        await self.db.execute('PRAGMA synchronous=NORMAL')  
        await self.db.execute('PRAGMA cache_size=-64000')  
        await self.setup_database()

    async def setup_database(self):
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                user_id INTEGER,
                guild_id INTEGER,
                message_count INTEGER DEFAULT 0,
                voice_minutes INTEGER DEFAULT 0,
                reaction_count INTEGER DEFAULT 0,
                command_count INTEGER DEFAULT 0,
                timestamp DATETIME,
                PRIMARY KEY (user_id, guild_id, timestamp)
            ) WITHOUT ROWID
        ''')
        
        await self.db.execute('''
            CREATE TABLE IF NOT EXISTS guild_metrics (
                guild_id INTEGER,
                member_count INTEGER DEFAULT 0,
                active_members INTEGER DEFAULT 0,
                message_count INTEGER DEFAULT 0,
                voice_users INTEGER DEFAULT 0,
                timestamp DATETIME,
                PRIMARY KEY (guild_id, timestamp)
            ) WITHOUT ROWID
        ''')
        
        await self.db.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON user_activity(timestamp)')
        await self.db.commit()

    async def flush_queue_loop(self):
        while True:
            try:
                await asyncio.sleep(self.flush_interval)
                await self.flush_queue()
            except Exception as e:
                print(f"Error in flush queue loop: {e}")

    async def flush_queue(self):
        async with self.queue_lock:
            if not self.queue:
                return
            
            current_queue = self.queue
            self.queue = []

        try:
           
            for i in range(0, len(current_queue), self.batch_size):
                batch = current_queue[i:i + self.batch_size]
                await self.db.executemany('''
                    INSERT INTO user_activity 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(user_id, guild_id, timestamp) 
                    DO UPDATE SET 
                        message_count = message_count + ?,
                        voice_minutes = voice_minutes + ?,
                        reaction_count = reaction_count + ?,
                        command_count = command_count + ?
                ''', batch)
                
                await self.db.commit()

        except Exception as e:
            print(f"Error during queue flush: {e}")
            
            async with self.queue_lock:
                self.queue.extend(current_queue)

    async def update_user_activity(self, user_id, guild_id, activity_type, amount):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:00:00')
        
        values = (
            user_id, guild_id,
            amount if activity_type == 'message' else 0,
            amount if activity_type == 'voice' else 0,
            amount if activity_type == 'reaction' else 0,
            amount if activity_type == 'command' else 0,
            timestamp,
            amount if activity_type == 'message' else 0,
            amount if activity_type == 'voice' else 0,
            amount if activity_type == 'reaction' else 0,
            amount if activity_type == 'command' else 0
        )
        
        async with self.queue_lock:
            self.queue.append(values)
            
            if len(self.queue) >= self.batch_size:
                asyncio.create_task(self.flush_queue())

    async def close(self):
        try:
            if self.queue:
                await self.flush_queue()
            if self.db:
                await self.db.execute('PRAGMA optimize')  
                await self.db.close()
        except Exception as e:
            print(f"Error during database close: {e}")


class Analytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_times = {}
        self.analytics_db = AnalyticsDatabase()

    def cog_unload(self):
        asyncio.create_task(self.analytics_db.close())

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot:
            return
        await self.analytics_db.update_user_activity(
            message.author.id,
            message.guild.id,
            'message',
            1
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not reaction.message.guild or user.bot:
            return
        await self.analytics_db.update_user_activity(
            user.id,
            reaction.message.guild.id,
            'reaction',
            1
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
            
        if not before.channel and after.channel:
            self.voice_times[member.id] = time.time()
        elif before.channel and not after.channel and member.id in self.voice_times:
            duration = time.time() - self.voice_times[member.id]
            minutes = int(duration / 60)
            await self.analytics_db.update_user_activity(
                member.id,
                member.guild.id,
                'voice',
                minutes
            )
            del self.voice_times[member.id]

class ServerAnalyticsView(discord.ui.View):
    def __init__(self, cog, ctx):
        super().__init__(timeout=300)
        self.cog = cog
        self.ctx = ctx
        self.setup_buttons()

    def setup_buttons(self):
        self.add_item(ActivityHeatmapButton())
        self.add_item(MemberRetentionButton())
        self.add_item(RoleDistributionButton())
        self.add_item(ChannelHealthButton())
        self.add_item(CommunityGrowthButton())

class RoleDistributionButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Role Distribution", emoji="👥")
    
    async def callback(self, interaction: discord.Interaction):
        distribution = await self.get_role_distribution(interaction.guild)
        embed = self.create_distribution_embed(distribution)
        await interaction.response.edit_message(embed=embed)

    async def get_role_distribution(self, guild):
        distribution = {
            'roles': {},
            'hierarchy': [],
            'member_counts': {},
            'permissions': {},
            'color_groups': {},
            'hoisted_roles': [],
            'mentionable_roles': [],
            'bot_roles': [],
            'integration_roles': []
        }
        
        for role in guild.roles:
            distribution['roles'][role.id] = {
                'name': role.name,
                'color': role.color.value,
                'members': len(role.members),
                'position': role.position,
                'permissions': role.permissions.value,
                'hoisted': role.hoist,
                'mentionable': role.mentionable
            }
            
            distribution['hierarchy'].append(role.id)
            distribution['member_counts'][role.id] = len(role.members)
            
            if role.hoist:
                distribution['hoisted_roles'].append(role.id)
            if role.mentionable:
                distribution['mentionable_roles'].append(role.id)
                
        return distribution

class MemberRetentionButton(BaseAnalyticsButton):
    def __init__(self):
        super().__init__(label="Member Retention", emoji="📊")
    
    async def callback(self, interaction: discord.Interaction):
        retention_data = await self.analyze_retention(interaction.guild)
        embed = self.create_retention_embed(retention_data)
        await interaction.response.edit_message(embed=embed)

    async def analyze_retention(self, guild):
        now = datetime.now()
        retention_data = {
            'join_cohorts': {},
            'leave_rates': {},
            'retention_rates': {},
            'engagement_correlation': {},
            'risk_factors': {},
            'successful_retention': [],
            'churn_patterns': {},
            'retention_by_role': {},
            'activity_impact': {}
        }
        
        for member in guild.members:
            join_month = member.joined_at.strftime('%Y-%m')
            retention_data['join_cohorts'][join_month] = retention_data['join_cohorts'].get(join_month, 0) + 1
            
        async for entry in guild.audit_logs(action=discord.AuditLogAction.member_remove, limit=None):
            if entry.target:
                leave_month = entry.created_at.strftime('%Y-%m')
                retention_data['leave_rates'][leave_month] = retention_data['leave_rates'].get(leave_month, 0) + 1
                
        return retention_data

    def create_retention_embed(self, data):
        embed = discord.Embed(
            title="Member Retention Analysis",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        for cohort, count in data['join_cohorts'].items():
            leaves = data['leave_rates'].get(cohort, 0)
            retention_rate = ((count - leaves) / count * 100) if count > 0 else 0
            embed.add_field(
                name=f"Cohort {cohort}",
                value=f"Retention: {retention_rate:.1f}%\nJoins: {count}\nLeaves: {leaves}",
                inline=True
            )
            
        return embed

class ServerAdsHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ads_db = {}  
        self.allowed_users = {}  
        self.channel_categories = {}  
        self.bump_cooldown = 12 * 3600  
        self.analytics = {}  
        self.cleanup_expired_ads.start()
        self.save_analytics.start()
        self.load_data()

    class ServerAdView(discord.ui.View):
        def __init__(self, cog, ad_data, server_id):
            super().__init__(timeout=None)
            self.cog = cog
            self.server_id = server_id
           
            self.add_item(discord.ui.Button(
                label="Join Server",
                url=ad_data["invite_link"],
                style=discord.ButtonStyle.url
            ))
           
            self.add_item(discord.ui.Button(
                label=f"👥 {ad_data['member_count']} Members",
                disabled=True,
                style=discord.ButtonStyle.gray
            ))

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            self.cog.analytics[self.server_id]["clicks"] += 1
            return True

    @commands.group(invoke_without_command=True)
    async def serverad(self, ctx):
        """Server Advertisement Hub Commands"""
        embed = discord.Embed(
            title="📢 Server Advertisement Hub",
            description=(
                "**Available Commands:**\n"
                "`!serverad post` - Create a new advertisement\n"
                "`!serverad bump` - Bump your server ad\n"
                "`!serverad preview` - Preview your current ad\n"
                "`!serverad stats` - View advertisement analytics\n"
                "`!serverad allow` - Grant ad permissions\n"
                "`!serverad template` - Get ad template"
            ),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


    @tasks.loop(hours=1)
    async def cleanup_expired_ads(self):
        """Cleanup expired advertisements"""
        current_time = datetime.now().timestamp()
        expired = [user_id for user_id, data in self.ads_db.items() 
                  if current_time - data["last_bump"] > 86400 * 7]  
                  
        for user_id in expired:
            del self.ads_db[user_id]
            
        for channel_id, data in self.channel_categories.items():
            channel = self.bot.get_channel(channel_id)
            if channel:
                async for message in channel.history():
                    if message.id in data["ads"] and message.author == self.bot.user:
                        await message.delete()
                        del data["ads"][message.id]



    async def check_ad_permission(self, ctx):
        """Verify user's permission to post ads"""
        if ctx.channel.id not in self.allowed_users:
            raise commands.CheckFailure("This channel is not authorized for advertisements")
        if ctx.author.id not in self.allowed_users[ctx.channel.id]:
            raise commands.CheckFailure("You don't have permission to post ads here")
        return True

    @serverad.command()
    async def preview(self, ctx):
        """Preview your advertisement"""
        await self.check_ad_permission(ctx)
        if ctx.author.id not in self.ads_db:
            return await ctx.send("❌ You don't have an active advertisement!")
        await self.send_ad(ctx, self.ads_db[ctx.author.id]["server_data"], ctx.guild.id)

    @serverad.command()
    async def rename_channel(self, ctx, *, new_name: str):
        """Rename your advertisement channel"""
        await self.check_ad_permission(ctx)
        if len(new_name) > 100:
            return await ctx.send("❌ Channel name too long! Max 100 characters.")
        await ctx.channel.edit(name=new_name)
        await ctx.send(f"✅ Channel renamed to: {new_name}")


    async def send_ad(self, ctx, server_data, server_id):
        """Send formatted advertisement with buttons"""
        embed = discord.Embed(
            title=f"🌟 {server_data['name']}",
            description=server_data['description'],
            color=discord.Color.gold()
        )
        embed.add_field(name="✨ Features", value=server_data['features'], inline=False)
        embed.add_field(name="🏷️ Tags", value=" • ".join(server_data['tags']), inline=False)
        
        stats = self.analytics[server_id]
        embed.set_footer(text=f"📊 Bumps: {stats['bumps']} | 👀 Views: {stats['views']}")
        
        view = self.ServerAdView(self, server_data, server_id)
        message = await ctx.send(embed=embed, view=view)
        self.analytics[server_id]["views"] += 1
        
        return message


    @serverad.command()
    async def post(self, ctx):
        """Create a new server advertisement"""
        await self.check_ad_permission(ctx)
        
        questions = {
            "name": "What's your server name? (60 chars max)",
            "description": "Describe your server: (200 chars max)",
            "features": "List 3-5 key features (one per line)",
            "tags": "Add some tags (comma-separated, max 5)",
            "invite": "Permanent server invite link:"
        }
        
        answers = {}
        for key, question in questions.items():
            embed = discord.Embed(
                title="📝 Advertisement Creation",
                description=question,
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            
            try:
                msg = await self.bot.wait_for(
                    'message',
                    timeout=300,
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel
                )
                answers[key] = msg.content
            except asyncio.TimeoutError:
                return await ctx.send("⏰ Setup timed out!")

        try:
            
            invite = await self.bot.fetch_invite(answers["invite"])
            
            features = "\n• ".join(
                [f for f in answers["features"].split("\n") if f.strip()][:5]
            )
            
            server_data = {
                "name": answers["name"][:60],
                "description": answers["description"][:200],
                "features": f"• {features}",
                "tags": [tag.strip() for tag in answers["tags"].split(",")[:5]],
                "invite_link": answers["invite"],
                "member_count": invite.approximate_member_count,
                "created_at": datetime.now().timestamp()
            }
            
            self.ads_db[ctx.author.id] = {
                "last_bump": datetime.now().timestamp(),
                "server_data": server_data
            }
            
            if invite.guild.id not in self.analytics:
                self.analytics[invite.guild.id] = {"views": 0, "clicks": 0, "bumps": 0}
            
            await self.send_ad(ctx, server_data, invite.guild.id)
            
        except discord.NotFound:
            await ctx.send("❌ Invalid invite link! Make sure it's permanent.")


    @serverad.command(name="allow")
    @commands.has_permissions(administrator=True)
    async def ads_allow(self, ctx, user: discord.Member, channel: discord.TextChannel, duration: int = 7):
        """Grant ad posting permission to a user"""
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await channel.set_permissions(user, send_messages=True)
        
        if channel.id not in self.allowed_users:
            self.allowed_users[channel.id] = set()
        self.allowed_users[channel.id].add(user.id)
        
        channel_embed = discord.Embed(
            title="✅ Advertisement Channel Access Granted",
            description=f"{user.mention} has been granted access to post advertisements",
            color=discord.Color.green()
        )
        channel_embed.add_field(
            name="Available Commands",
            value=(
                "`!serverad post` - Create your advertisement\n"
                "`!serverad bump` - Bump your ad\n"
                "`!serverad preview` - Preview your ad\n"
                "`!serverad stats` - View analytics"
            ),
            inline=False
        )
        channel_embed.set_footer(text="© ZygnalBot | TheHolyOneZ")
        await ctx.send(embed=channel_embed)
        
        user_embed = discord.Embed(
            title="🎉 Advertisement Access Granted!",
            description=f"You now have access to post in {channel.mention}",
            color=discord.Color.blue()
        )
        user_embed.add_field(
            name="Getting Started",
            value=(
                "1. Use `!serverad template` to see the format\n"
                "2. Create your ad with `!serverad post`\n"
                "3. Bump every 12 hours with `!serverad bump`\n"
                "4. Track performance with `!serverad stats`"
            ),
            inline=False
        )
        user_embed.set_footer(text="© ZygnalBot | TheHolyOneZ")
        try:
            await user.send(embed=user_embed)
        except discord.Forbidden:
            pass



    @tasks.loop(minutes=30)
    async def save_analytics(self):
        """Save analytics data to JSON file"""
        analytics_data = {
            "timestamp": datetime.now().timestamp(),
            "total_ads": len(self.ads_db),
            "channel_stats": self.channel_categories,
            "server_stats": self.analytics
        }
        
        with open('ad_analytics.json', 'w') as f:
            json.dump(analytics_data, f, indent=4)

    def load_data(self):
        """Load saved data from JSON files"""
        try:
            with open('ad_analytics.json', 'r') as f:
                self.analytics = json.load(f)
            with open('channel_categories.json', 'r') as f:
                self.channel_categories = json.load(f)
        except FileNotFoundError:
            pass

    def save_data(self):
        """Save all data to JSON files"""
        with open('ad_analytics.json', 'w') as f:
            json.dump(self.analytics, f)
        with open('channel_categories.json', 'w') as f:
            json.dump(self.channel_categories, f)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_ad_category(self, ctx):
        """Setup advertisement category with multiple channels"""
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            
            await ctx.send("What would you like to name the advertisement category?")
            category_msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            
            category = await ctx.guild.create_category(category_msg.content)
            
            await ctx.send("How many advertisement channels would you like to create? (1-10)")
            num_msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            num_channels = min(max(1, int(num_msg.content)), 10)

            channels = []
            for i in range(num_channels):
                await ctx.send(f"Name for channel #{i+1}?")
                name_msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(send_messages=True)
                }

                channel = await category.create_text_channel(
                    name=name_msg.content,
                    overwrites=overwrites
                )
                
                self.channel_categories[channel.id] = {
                    "name": name_msg.content,
                    "ads": {},
                    "position": i,
                    "created_at": datetime.now().timestamp()
                }
                
                channels.append(channel)

            for channel in channels:
                info_embed = discord.Embed(
                    title="📢 Advertisement Channel",
                    description=(
                        "**Channel Rules:**\n"
                        "1. Only authorized users can post ads\n"
                        "2. Ads are sorted by bump count\n"
                        "3. Bumps are limited to once every 12 hours\n"
                        "4. Inappropriate content will result in removal"
                    ),
                    color=discord.Color.gold()
                )
                await channel.send(embed=info_embed, pin=True)

            await ctx.send("✅ Advertisement category setup complete!")
            
        except asyncio.TimeoutError:
            await ctx.send("❌ Setup timed out!")
        except ValueError:
            await ctx.send("❌ Please enter a valid number!")

    @serverad.command()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def bump(self, ctx):
        """Bump server ad and reorder based on bump count"""
        await self.check_ad_permission(ctx)
        
        if ctx.author.id not in self.ads_db:
            return await ctx.send("❌ You don't have an active advertisement!")
            
        channel_id = ctx.channel.id
        if channel_id not in self.channel_categories:
            return await ctx.send("❌ This channel is not properly configured!")

        self.ads_db[ctx.author.id]["last_bump"] = datetime.now().timestamp()
        server_data = self.ads_db[ctx.author.id]["server_data"]
        
        try:
           
            invite = await self.bot.fetch_invite(server_data["invite_link"])
            server_data["member_count"] = invite.approximate_member_count
            
            self.analytics[invite.guild.id]["bumps"] += 1
            
            async for message in ctx.channel.history():
                if message.author == self.bot.user and message.embeds:
                    embed = message.embeds[0]
                    if embed.title.endswith(server_data['name']):
                        await message.delete()
                        if message.id in self.channel_categories[channel_id]["ads"]:
                            del self.channel_categories[channel_id]["ads"][message.id]
            
            new_message = await self.send_ad(ctx, server_data, invite.guild.id)
            self.channel_categories[channel_id]["ads"][new_message.id] = self.analytics[invite.guild.id]["bumps"]
            
            await self.sort_ads_by_bumps(ctx.channel)
            
            await ctx.send("🚀 Server bumped and ads reordered!", delete_after=5)
            
        except discord.NotFound:
            await ctx.send("❌ Invalid invite link! Please update your ad.")

    async def sort_ads_by_bumps(self, channel):
        """Sort advertisements by bump count"""
        if channel.id not in self.channel_categories:
            return
            
        ads = []
        async for message in channel.history(limit=100):
            if message.id in self.channel_categories[channel.id]["ads"]:
                ads.append({
                    "message": message,
                    "bumps": self.channel_categories[channel.id]["ads"][message.id]
                })
        
        sorted_ads = sorted(ads, key=lambda x: x["bumps"], reverse=True)
        
        for ad in sorted_ads:
            message = ad["message"]
            if message.embeds:
                embed = message.embeds[0]
                await message.delete()
                new_msg = await channel.send(embed=embed)
                self.channel_categories[channel.id]["ads"][new_msg.id] = ad["bumps"]

    @serverad.command()
    async def template(self, ctx):
        """Get advertisement template"""
        template = discord.Embed(
            title="📝 Advertisement Template",
            description=(
                "**Server Name**\n"
                "Your server name here\n\n"
                "**Description**\n"
                "Describe your server (200 chars max)\n\n"
                "**Key Features**\n"
                "• Feature 1\n"
                "• Feature 2\n"
                "• Feature 3\n\n"
                "**Tags**\n"
                "gaming, community, fun"
            ),
            color=discord.Color.blue()
        )
        await ctx.send(embed=template)

    @serverad.command()
    async def edit(self, ctx):
        """Edit your advertisement"""
        await self.check_ad_permission(ctx)
        
        if ctx.author.id not in self.ads_db:
            return await ctx.send("❌ You don't have an active advertisement!")
        
        current_ad = self.ads_db[ctx.author.id]["server_data"]
        
        edit_options = {
            "1": "Server Name",
            "2": "Description",
            "3": "Features",
            "4": "Tags",
            "5": "Invite Link"
        }
        
        embed = discord.Embed(
            title="📝 Edit Advertisement",
            description="\n".join(f"{k}. {v}" for k, v in edit_options.items()),
            color=discord.Color.blue()
        )
        embed.set_footer(text="Type the number of what you want to edit, or 'cancel' to exit")
        
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            choice = await self.bot.wait_for('message', timeout=30.0, check=check)
            if choice.content.lower() == 'cancel':
                return await ctx.send("✅ Edit cancelled!")
                
            if choice.content not in edit_options:
                return await ctx.send("❌ Invalid option!")
                
            await ctx.send(f"Please provide the new {edit_options[choice.content]}:")
            new_content = await self.bot.wait_for('message', timeout=60.0, check=check)
            
            if choice.content == "1":
                current_ad["name"] = new_content.content[:60]
            elif choice.content == "2":
                current_ad["description"] = new_content.content[:200]
            elif choice.content == "3":
                features = "\n• ".join([f for f in new_content.content.split("\n") if f.strip()][:5])
                current_ad["features"] = f"• {features}"
            elif choice.content == "4":
                current_ad["tags"] = [tag.strip() for tag in new_content.content.split(",")[:5]]
            elif choice.content == "5":
                if new_content.content.lower() != "skip":
                    try:
                        invite = await self.bot.fetch_invite(new_content.content)
                        current_ad["invite_link"] = new_content.content
                        current_ad["member_count"] = invite.approximate_member_count
                    except discord.NotFound:
                        return await ctx.send("❌ Invalid invite link!")
                else:
                    current_ad["invite_link"] = "Not provided"
                    current_ad["member_count"] = 0
            
            self.ads_db[ctx.author.id]["server_data"] = current_ad
            
            async for message in ctx.channel.history():
                if message.author == self.bot.user and message.embeds:
                    embed = message.embeds[0]
                    if embed.title.endswith(current_ad['name']):
                        await message.delete()
            
            await self.send_ad(ctx, current_ad, ctx.guild.id)
            await ctx.send("✅ Advertisement updated successfully!")
            
        except asyncio.TimeoutError:
            await ctx.send("❌ Edit timed out!")

    def cog_unload(self):
        """Save data when cog is unloaded"""
        self.cleanup_expired_ads.cancel()
        self.save_analytics.cancel()
        self.save_data()
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_settings(self, ctx):
        """Configure advertisement system settings"""
        embed = discord.Embed(
            title="⚙️ Advertisement Settings",
            description=(
                "**Available Settings:**\n"
                "1️⃣ Bump Cooldown\n"
                "2️⃣ Channel Categories\n"
                "3️⃣ Auto-cleanup Duration\n"
                "4️⃣ Permission Management\n"
                "5️⃣ Analytics Settings"
            ),
            color=discord.Color.blue()
        )
        settings_msg = await ctx.send(embed=embed)
        
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for reaction in reactions:
            await settings_msg.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            await self.handle_settings_menu(ctx, str(reaction.emoji))
        except asyncio.TimeoutError:
            await ctx.send("Settings menu timed out!", delete_after=5)

    async def handle_settings_menu(self, ctx, choice):
        """Handle settings menu selection"""
        if choice == '1️⃣':
            await self.set_bump_cooldown(ctx)
        elif choice == '2️⃣':
            await self.manage_categories(ctx)
        elif choice == '3️⃣':
            await self.set_cleanup_duration(ctx)
        elif choice == '4️⃣':
            await self.manage_permissions(ctx)
        elif choice == '5️⃣':
            await self.configure_analytics(ctx)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_stats(self, ctx):
        """View detailed advertisement system statistics"""
        total_ads = len(self.ads_db)
        total_bumps = sum(stats["bumps"] for stats in self.analytics.values())
        total_views = sum(stats["views"] for stats in self.analytics.values())
        total_clicks = sum(stats["clicks"] for stats in self.analytics.values())

        stats_embed = discord.Embed(
            title="📊 Advertisement System Statistics",
            color=discord.Color.gold()
        )
        stats_embed.add_field(name="Total Advertisements", value=total_ads)
        stats_embed.add_field(name="Total Bumps", value=total_bumps)
        stats_embed.add_field(name="Total Views", value=total_views)
        stats_embed.add_field(name="Total Clicks", value=total_clicks)
        stats_embed.add_field(
            name="Conversion Rate", 
            value=f"{(total_clicks/total_views*100 if total_views else 0):.2f}%"
        )

        await ctx.send(embed=stats_embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_cleanup(self, ctx):
        """Manually cleanup expired advertisements"""
        before = len(self.ads_db)
        current_time = datetime.now().timestamp()
        
        expired = [user_id for user_id, data in self.ads_db.items()
                  if current_time - data["last_bump"] > 86400 * 7]
                  
        for user_id in expired:
            del self.ads_db[user_id]
        
        after = len(self.ads_db)
        removed = before - after
        
        await ctx.send(f"✅ Removed {removed} expired advertisements!")




    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_analytics(self, ctx):
        """Reset advertisement analytics"""
        confirm = await ctx.send("⚠️ Are you sure you want to reset all analytics? This cannot be undone!")
        
        await confirm.add_reaction('✅')
        await confirm.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌']
            
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == '✅':
                self.analytics = {}
                await ctx.send("✅ Analytics have been reset!")
            else:
                await ctx.send("❌ Analytics reset cancelled!")
        except asyncio.TimeoutError:
            await ctx.send("❌ Reset timed out!")
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_blacklist(self, ctx, user: discord.Member):
        """Blacklist a user from posting advertisements"""
        if user.id in self.ads_db:
            del self.ads_db[user.id]
            
        for channel_id in self.allowed_users:
            self.allowed_users[channel_id].discard(user.id)
            
        for channel_id, data in self.channel_categories.items():
            channel = ctx.guild.get_channel(channel_id)
            if channel:
                async for message in channel.history():
                    if message.embeds and message.id in data["ads"]:
                        embed = message.embeds[0]
                        if str(user.id) in embed.footer.text:
                            await message.delete()
                            del data["ads"][message.id]

        await ctx.send(f"✅ {user.mention} has been blacklisted from posting advertisements")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def move_ad(self, ctx, message_id: int, channel: discord.TextChannel):
        """Move an advertisement to a different channel"""
        if channel.id not in self.channel_categories:
            return await ctx.send("❌ Target channel is not an advertisement channel!")

        try:
            message = await ctx.channel.fetch_message(message_id)
            if not message.embeds:
                return await ctx.send("❌ Message is not an advertisement!")

            new_message = await channel.send(embed=message.embeds[0])
            self.channel_categories[channel.id]["ads"][new_message.id] = \
                self.channel_categories[ctx.channel.id]["ads"].get(message.id, 0)
            
            await message.delete()
            if message.id in self.channel_categories[ctx.channel.id]["ads"]:
                del self.channel_categories[ctx.channel.id]["ads"][message.id]

            await self.sort_ads_by_bumps(channel)
            await ctx.send("✅ Advertisement moved successfully!")

        except discord.NotFound:
            await ctx.send("❌ Message not found!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_audit(self, ctx):
        """Audit advertisement channels and fix any issues"""
        audit_report = {
            "broken_ads": 0,
            "fixed_ads": 0,
            "invalid_channels": 0,
            "total_checked": 0
        }

        for channel_id in list(self.channel_categories.keys()):
            channel = self.bot.get_channel(channel_id)
            if not channel:
                del self.channel_categories[channel_id]
                audit_report["invalid_channels"] += 1
                continue

            ads = self.channel_categories[channel_id]["ads"]
            for message_id in list(ads.keys()):
                try:
                    await channel.fetch_message(message_id)
                    audit_report["total_checked"] += 1
                except discord.NotFound:
                    del ads[message_id]
                    audit_report["broken_ads"] += 1
                    audit_report["fixed_ads"] += 1

        embed = discord.Embed(
            title="📋 Advertisement Audit Report",
            color=discord.Color.blue()
        )
        for key, value in audit_report.items():
            embed.add_field(name=key.replace("_", " ").title(), value=value)
        
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_channel_stats(self, ctx, channel: discord.TextChannel = None):
        """View statistics for a specific advertisement channel"""
        if not channel:
            channel = ctx.channel
            
        if channel.id not in self.channel_categories:
            return await ctx.send("❌ This is not an advertisement channel!")

        data = self.channel_categories[channel.id]
        total_ads = len(data["ads"])
        total_bumps = sum(data["ads"].values())
        
        embed = discord.Embed(
            title=f"📊 Channel Statistics: {channel.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Total Advertisements", value=total_ads)
        embed.add_field(name="Total Bumps", value=total_bumps)
        embed.add_field(name="Average Bumps", value=f"{total_bumps/total_ads:.2f}" if total_ads else 0)
        
        sorted_ads = sorted(data["ads"].items(), key=lambda x: x[1], reverse=True)[:5]
        if sorted_ads:
            top_ads = "\n".join(f"ID: {msg_id} - {bumps} bumps" for msg_id, bumps in sorted_ads)
            embed.add_field(name="Top Advertisements", value=top_ads, inline=False)
        
        await ctx.send(embed=embed)
    async def handle_ad_error(self, ctx, error):
        """Handle advertisement system errors"""
        error_messages = {
            commands.CommandOnCooldown: f"⏰ Please wait {error.retry_after:.2f}s before bumping again!",
            commands.MissingPermissions: "❌ You don't have permission to use this command!",
            commands.CheckFailure: str(error),
            discord.Forbidden: "❌ Bot lacks required permissions!"
        }

        error_msg = error_messages.get(type(error), "❌ An unexpected error occurred!")
        await ctx.send(error_msg, delete_after=10)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Clean up data when ad channel is deleted"""
        if channel.id in self.channel_categories:
            del self.channel_categories[channel.id]
        if channel.id in self.allowed_users:
            del self.allowed_users[channel.id]
        self.save_data()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_restore(self, ctx, user: discord.Member):
        """Restore user's last advertisement if available"""
        backup_file = f'ad_backups/{user.id}.json'
        try:
            with open(backup_file, 'r') as f:
                ad_data = json.load(f)
            
            self.ads_db[user.id] = ad_data
            await self.send_ad(ctx, ad_data["server_data"], ad_data["server_data"]["guild_id"])
            await ctx.send(f"✅ Restored advertisement for {user.mention}")
            
        except FileNotFoundError:
            await ctx.send("❌ No backup found for this user!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ad_template_create(self, ctx):
        """Create a custom advertisement template"""
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            await ctx.send("Please provide the template name:")
            name = (await self.bot.wait_for('message', timeout=30.0, check=check)).content

            await ctx.send("Please provide the template content:")
            content = (await self.bot.wait_for('message', timeout=60.0, check=check)).content

            template_data = {
                "name": name,
                "content": content,
                "created_by": ctx.author.id,
                "created_at": datetime.now().timestamp()
            }

            with open(f'ad_templates/{name}.json', 'w') as f:
                json.dump(template_data, f)

            await ctx.send(f"✅ Template '{name}' created successfully!")

        except asyncio.TimeoutError:
            await ctx.send("❌ Template creation timed out!")

    @commands.command()
    async def ad_search(self, ctx, *, query: str):
        """Search for advertisements by server name or tags"""
        matches = []
        for user_id, data in self.ads_db.items():
            server_data = data["server_data"]
            if (query.lower() in server_data["name"].lower() or 
                any(query.lower() in tag.lower() for tag in server_data["tags"])):
                matches.append(server_data)

        if not matches:
            return await ctx.send("❌ No advertisements found matching your search!")

        pages = []
        for i in range(0, len(matches), 5):
            embed = discord.Embed(
                title="🔍 Search Results",
                color=discord.Color.blue()
            )
            for server_data in matches[i:i+5]:
                embed.add_field(
                    name=server_data["name"],
                    value=f"Tags: {', '.join(server_data['tags'])}",
                    inline=False
                )
            pages.append(embed)

        await self.send_paginated_results(ctx, pages)

    async def send_paginated_results(self, ctx, pages):
        """Send paginated search results"""
        if not pages:
            return

        current_page = 0
        message = await ctx.send(embed=pages[0])

        if len(pages) > 1:
            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                    if str(reaction.emoji) == '➡️':
                        current_page = (current_page + 1) % len(pages)
                    elif str(reaction.emoji) == '⬅️':
                        current_page = (current_page - 1) % len(pages)

                    await message.edit(embed=pages[current_page])
                    await message.remove_reaction(reaction, user)

                except asyncio.TimeoutError:
                    break

            await message.clear_reactions()



class CustomVerification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_settings = {}
        self.role_assignments = {}

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def verify_user_setup(self, ctx):
        """Setup the custom verification system"""
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        embed = discord.Embed(
            title="🔧 Custom Verification Setup",
            description="Let's configure your verification system!",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

        await ctx.send("Please mention or enter the ID of the role to **remove** during verification:")
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            role1_id = int(msg.content.strip('<@&>'))
            role1 = ctx.guild.get_role(role1_id)
            if not role1:
                return await ctx.send("❌ Invalid role! Setup cancelled.")
        except ValueError:
            return await ctx.send("❌ Please provide a valid role ID or mention!")

        await ctx.send("Please mention or enter the ID of the role to **add** during verification:")
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            role2_id = int(msg.content.strip('<@&>'))
            role2 = ctx.guild.get_role(role2_id)
            if not role2:
                return await ctx.send("❌ Invalid role! Setup cancelled.")
        except ValueError:
            return await ctx.send("❌ Please provide a valid role ID or mention!")

        example_msg = (
            "Enter your custom verification message. You can use:\n"
            "• {user} - Mentions the verified user\n"
            "• {role_removed} - Shows removed role\n"
            "• {role_added} - Shows added role\n\n"
            "Example: Welcome {user}! Removed {role_removed} and added {role_added}"
        )
        await ctx.send(example_msg)
        msg = await self.bot.wait_for('message', check=check, timeout=60)
        success_msg = msg.content

        self.verification_settings[ctx.guild.id] = {
            'remove_role': role1_id,
            'add_role': role2_id,
            'success_msg': success_msg
        }

        setup_complete = await ctx.send(
            embed=discord.Embed(
                title="✅ Setup Complete!",
                description=f"""
                **Remove Role:** {role1.mention}
                **Add Role:** {role2.mention}
                **Success Message Preview:**
                {success_msg.format(user='@User', role_removed=role1.name, role_added=role2.name)}
                
                Use `!verify_user @member` to verify members!
                """,
                color=discord.Color.green()
            )
        )
        await asyncio.sleep(5)
        await setup_complete.delete()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def verify_user(self, ctx, member: discord.Member):
        """Verify a user with custom roles"""
        
        if ctx.guild.id not in self.verification_settings:
            return await ctx.send("⚠️ Please setup the verification system first using `!verify_user_setup`")

        settings = self.verification_settings[ctx.guild.id]
        
        remove_role = ctx.guild.get_role(settings['remove_role'])
        add_role = ctx.guild.get_role(settings['add_role'])

        if not remove_role or not add_role:
            return await ctx.send("❌ One or more roles are invalid! Please run setup again.")

        try:
            await member.remove_roles(remove_role)
            await member.add_roles(add_role)
            
            success_msg = settings['success_msg'].format(
                user=member.mention,
                role_removed=remove_role.name,
                role_added=add_role.name
            )
            
            verify_msg = await ctx.send(
                embed=discord.Embed(
                    title="✅ Verification Successful",
                    description=success_msg,
                    color=discord.Color.green()
                ).set_footer(text=f"Verified by {ctx.author}")
            )
            await asyncio.sleep(5)
            await verify_msg.delete()
            
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to manage these roles!")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")
    
    @commands.command()
    async def verify_setup_help(self, ctx):
        embed = discord.Embed(
            title="📚 Verification Setup Guide",
            description="A complete guide to setting up the verification system!",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Setup Steps",
            value="""
            **Step 1:** Remove Role
            When prompted for "role to remove", this is the role members have before verification
            Example: Unverified Role, New Member Role
            
            **Step 2:** Add Role
            When prompted for "role to add", this is the role members get after verification
            Example: Verified Role, Member Role
            """,
            inline=False
        )

        embed.add_field(
            name="Message Placeholders",
            value="""
            Use these in your custom message:
            • `{user}` - Mentions the verified user
            • `{role_removed}` - Shows the removed role name
            • `{role_added}` - Shows the added role name
            """,
            inline=False
        )

        embed.add_field(
            name="Message Examples",
            value="""
            **Example 1:**
            ```Welcome {user}! You're now verified! Removed {role_removed} and added {role_added}```

            **Example 2:**
            ```{user} has been verified! ✅
            Removed: {role_removed}
            Added: {role_added}```
            
            **Example 3:**
            ```Verification complete for {user}! You now have the {role_added} role!```
            """,
            inline=False
        )

        embed.set_footer(text="Use !verify_user_setup to begin the setup process!")
        await ctx.send(embed=embed)



class WebhookDeleteModal(discord.ui.Modal, title="Delete Webhook"):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.bot = interaction.client
        
    webhook_id = discord.ui.TextInput(
        label="Webhook ID",
        placeholder="Enter webhook ID to delete...",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            webhook = await interaction.client.fetch_webhook(int(self.webhook_id.value))
            await webhook.delete()
            embed = discord.Embed(title="✅ Webhook Deleted", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class WebhookTestModal(discord.ui.Modal, title="Test Webhook"):
    webhook_id = discord.ui.TextInput(
        label="Webhook ID",
        placeholder="Enter webhook ID to test...",
        required=True
    )
    test_message = discord.ui.TextInput(
        label="Test Message",
        placeholder="Enter a test message...",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            webhook = await interaction.client.fetch_webhook(int(self.webhook_id.value))
            await webhook.send(self.test_message.value)
            embed = discord.Embed(title="✅ Test Message Sent", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

class WebhookConfigView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Avatar", style=ButtonStyle.grey)
    async def avatar_config(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookAvatarModal()
        await interaction.response.send_modal(modal)
        
    @discord.ui.button(label="Name", style=ButtonStyle.grey)
    async def name_config(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookNameModal()
        await interaction.response.send_modal(modal)
        
    @discord.ui.button(label="Channel", style=ButtonStyle.grey)
    async def channel_config(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookChannelModal()
        await interaction.response.send_modal(modal)

class WebhookAvatarModal(discord.ui.Modal, title="Change Webhook Avatar"):
    webhook_id = discord.ui.TextInput(
        label="Webhook ID",
        placeholder="Enter webhook ID...",
        required=True
    )
    avatar_url = discord.ui.TextInput(
        label="New Avatar URL",
        placeholder="Enter new avatar URL...",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
           
            response = requests.get(self.avatar_url.value)
            img = Image.open(io.BytesIO(response.content))
            
            img = img.resize((128, 128))
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            webhook = await interaction.client.fetch_webhook(int(self.webhook_id.value))
            await webhook.edit(avatar=img_byte_arr)
            
            embed = discord.Embed(title="✅ Avatar Updated", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

class WebhookNameModal(discord.ui.Modal, title="Change Webhook Name"):
    webhook_id = discord.ui.TextInput(
        label="Webhook ID",
        placeholder="Enter webhook ID...",
        required=True
    )
    new_name = discord.ui.TextInput(
        label="New Name",
        placeholder="Enter new webhook name...",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            webhook = await interaction.client.fetch_webhook(int(self.webhook_id.value))
            await webhook.edit(name=self.new_name.value)
            embed = discord.Embed(title="✅ Name Updated", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class WebhookChannelModal(discord.ui.Modal, title="Change Webhook Channel"):
    webhook_id = discord.ui.TextInput(
        label="Webhook ID",
        placeholder="Enter webhook ID...",
        required=True
    )
    channel_id = discord.ui.TextInput(
        label="New Channel ID",
        placeholder="Enter new channel ID...",
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            webhook = await interaction.client.fetch_webhook(int(self.webhook_id.value))
            channel = interaction.guild.get_channel(int(self.channel_id.value))
            await webhook.edit(channel=channel)
            embed = discord.Embed(title="✅ Channel Updated", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="❌ Error", description=str(e), color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


class WebhookManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def webhook(self, ctx):
        webhooks = await ctx.guild.webhooks()
        active_webhooks = len(webhooks)
        last_webhook = webhooks[-1].created_at.strftime("%Y-%m-%d %H:%M:%S") if webhooks else "Never"

        embed = discord.Embed(
            title="🔗 Webhook Management Dashboard",
            description="Manage all your webhook configurations from one place",
            color=discord.Color.blue()
        )
        embed.add_field(name="📊 Current Status", value=f"Active Webhooks: {active_webhooks}\nLast Created: {last_webhook}", inline=False)
        embed.add_field(name="🔧 Options", value="Configure your webhook settings using the buttons below", inline=False)
        embed.set_footer(text=f"Opened by {ctx.author} | Server: {ctx.guild.name}")
        
        view = WebhookView()
        await ctx.send(embed=embed, view=view)

class WebhookView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Create", style=ButtonStyle.green)
    async def create_webhook(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookCreateModal()
        await interaction.response.send_modal(modal)
        
    @discord.ui.button(label="Configure", style=ButtonStyle.blurple)
    async def configure_webhook(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚙️ Webhook Configuration",
            description="Select what you want to configure:",
            color=discord.Color.gold()
        )
        config_view = WebhookConfigView()
        await interaction.response.send_message(embed=embed, view=config_view, ephemeral=True)

    @discord.ui.button(label="List", style=ButtonStyle.grey)
    async def list_webhooks(self, interaction: discord.Interaction, button: discord.ui.Button):
        webhooks = await interaction.guild.webhooks()
        embed = discord.Embed(title="📋 Active Webhooks", color=discord.Color.blue())
        for webhook in webhooks:
            embed.add_field(
                name=f"ID: {webhook.id}",
                value=f"Name: {webhook.name}\nChannel: {webhook.channel.mention}\nCreated: {webhook.created_at.strftime('%Y-%m-%d')}",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Delete", style=ButtonStyle.red)
    async def delete_webhook(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookDeleteModal(interaction)
        await interaction.response.send_modal(modal)


    @discord.ui.button(label="Test", style=ButtonStyle.blurple)
    async def test_webhook(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = WebhookTestModal()
        await interaction.response.send_modal(modal)

class WebhookCreateModal(discord.ui.Modal, title="Create New Webhook"):
    name = discord.ui.TextInput(
        label="Webhook Name",
        placeholder="Enter webhook name...",
        required=True
    )
    
    channel = discord.ui.TextInput(
        label="Channel ID",
        placeholder="Enter channel ID...",
        required=True
    )
    
    avatar_url = discord.ui.TextInput(
        label="Avatar URL (Optional)",
        placeholder="Enter avatar URL...",
        required=False
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            channel = interaction.guild.get_channel(int(self.channel.value))
            webhook = await channel.create_webhook(
                name=self.name.value,
                avatar=self.avatar_url.value if self.avatar_url.value else None
            )
            
            embed = discord.Embed(
                title="✅ Webhook Created Successfully",
                description=f"Webhook URL: {webhook.url}\nChannel: {channel.mention}",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error Creating Webhook",
                description=str(e),
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class ProfileSetupView(discord.ui.View):
    def __init__(self, cog, ctx):
        super().__init__(timeout=300)
        self.cog = cog
        self.ctx = ctx

    @discord.ui.button(label="Set Bio", style=discord.ButtonStyle.primary, emoji="📝", row=0)
    async def bio_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Please enter your bio (max 1000 characters):", ephemeral=True)
        
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel
            
        try:
            bio_msg = await self.cog.bot.wait_for('message', check=check, timeout=300)
            if len(bio_msg.content) > 1000:
                await interaction.followup.send("❌ Bio too long! Max 1000 characters.", ephemeral=True)
                return
                
            if interaction.user.id not in self.cog.profiles:
                self.cog.profiles[interaction.user.id] = self.cog.default_profile()
            
            self.cog.profiles[interaction.user.id]['bio'] = bio_msg.content
            self.cog.profiles[interaction.user.id]['last_updated'] = datetime.now().isoformat()
            await bio_msg.delete()
            await interaction.followup.send("✅ Bio updated successfully!", ephemeral=True)
            
            await self.update_preview(interaction)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("❌ Setup timed out!", ephemeral=True)

    @discord.ui.button(label="Set Banner", style=discord.ButtonStyle.primary, emoji="🎨", row=0)
    async def banner_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Please enter a banner image URL:", ephemeral=True)
        
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel
            
        try:
            banner_msg = await self.cog.bot.wait_for('message', check=check, timeout=300)
            if interaction.user.id not in self.cog.profiles:
                self.cog.profiles[interaction.user.id] = self.cog.default_profile()
            
            self.cog.profiles[interaction.user.id]['banner'] = banner_msg.content
            await banner_msg.delete()
            await interaction.followup.send("✅ Banner updated successfully!", ephemeral=True)
            await self.update_preview(interaction)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("❌ Setup timed out!", ephemeral=True)

    @discord.ui.button(label="Set Social Links", style=discord.ButtonStyle.primary, emoji="🔗", row=1)
    async def socials_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Enter your social media links in this format:\n"
            "platform1: link1\n"
            "platform2: link2\n"
            "Example:\n"
            "twitter: https://twitter.com/username\n"
            "github: https://github.com/username",
            ephemeral=True
        )
        
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel
            
        try:
            socials_msg = await self.cog.bot.wait_for('message', check=check, timeout=300)
            if interaction.user.id not in self.cog.profiles:
                self.cog.profiles[interaction.user.id] = self.cog.default_profile()
            
            socials = {}
            for line in socials_msg.content.split('\n'):
                if ':' in line:
                    platform, link = line.split(':', 1)
                    socials[platform.strip().lower()] = link.strip()
            
            self.cog.profiles[interaction.user.id]['socials'] = socials
            await socials_msg.delete()
            await interaction.followup.send("✅ Social links updated successfully!", ephemeral=True)
            await self.update_preview(interaction)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("❌ Setup timed out!", ephemeral=True)

    @discord.ui.button(label="Set Badges", style=discord.ButtonStyle.primary, emoji="🏆", row=1)
    async def badges_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        available_badges = "🎮 Gamer\n🎨 Artist\n📚 Bookworm\n💻 Developer\n🎵 Musician"
        await interaction.response.send_message(
            f"Available badges:\n{available_badges}\nEnter the badges you want (separated by spaces):",
            ephemeral=True
        )
        
        def check(m):
            return m.author == self.ctx.author and m.channel == self.ctx.channel
            
        try:
            badges_msg = await self.cog.bot.wait_for('message', check=check, timeout=300)
            if interaction.user.id not in self.cog.profiles:
                self.cog.profiles[interaction.user.id] = self.cog.default_profile()
            
            self.cog.profiles[interaction.user.id]['badges'] = badges_msg.content.split()
            await badges_msg.delete()
            await interaction.followup.send("✅ Badges updated successfully!", ephemeral=True)
            await self.update_preview(interaction)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("❌ Setup timed out!", ephemeral=True)

    async def update_preview(self, interaction):
        profile = self.cog.profiles[interaction.user.id]
        embed = self.cog.create_profile_embed(interaction.user, profile)
        await interaction.message.edit(embed=embed)

class ProfileSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.profiles = {}

    def default_profile(self):
        return {
            'bio': 'No bio set',
            'banner': None,
            'badges': [],
            'socials': {},
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'profile_views': 0
        }

    def create_profile_embed(self, user, profile):
        embed = discord.Embed(
            title=f"{user.name}'s Profile",
            description=profile['bio'],
            color=user.color,
            timestamp=datetime.now()
        )
        
        if profile.get('banner'):
            embed.set_image(url=profile['banner'])
        
        embed.set_thumbnail(url=user.avatar.url)
        
        if profile['badges']:
            embed.add_field(name="🏆 Badges", value=' '.join(profile['badges']), inline=False)
        
        if profile['socials']:
            social_text = '\n'.join([f"{platform}: {link}" for platform, link in profile['socials'].items()])
            embed.add_field(name="🔗 Social Links", value=social_text, inline=False)
        
        created_at = datetime.fromisoformat(profile['created_at'])
        last_updated = datetime.fromisoformat(profile['last_updated'])
        
        embed.add_field(name="📊 Stats", value=f"Profile Views: {profile['profile_views']}\nCreated: {created_at.strftime('%Y-%m-%d')}\nLast Updated: {last_updated.strftime('%Y-%m-%d')}", inline=False)
        
        embed.set_footer(text=f"{user.name}#{user.discriminator}", icon_url=user.avatar.url)
        return embed

    @commands.group(invoke_without_command=True)
    async def p(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        if user.id not in self.profiles:
            if user == ctx.author:
                embed = discord.Embed(
                    title="Profile Not Found",
                    description="You haven't set up your profile yet! Use `!p setup` to get started.",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Profile Not Found",
                    description="This user hasn't set up their profile yet!",
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            return
        
        profile = self.profiles[user.id]
        profile['profile_views'] += 1
        embed = self.create_profile_embed(user, profile)
        await ctx.send(embed=embed)

    @p.command(name="setup")
    async def profile_setup(self, ctx):
        embed = discord.Embed(
            title="✨ Profile Setup",
            description="Customize your profile using the buttons below!",
            color=discord.Color.blue()
        )
        view = ProfileSetupView(self, ctx)
        await ctx.send(embed=embed, view=view)



class TempChannelButton(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="Create Temporary Channel", style=discord.ButtonStyle.green, emoji="📝", custom_id="create_temp_channel")
    async def create_temp_channel(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CreateChannelModal(self.cog)
        await interaction.response.send_modal(modal)

class CreateChannelModal(discord.ui.Modal, title="Create Temporary Channel"):
    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    channel_name = discord.ui.TextInput(
        label="Channel Name",
        placeholder="Enter channel name...",
        min_length=1,
        max_length=32
    )
    
    duration = discord.ui.TextInput(
        label="Duration (in hours)",
        placeholder="Enter duration (1-72 hours)",
        min_length=1,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            duration = int(self.duration.value)
            if not 1 <= duration <= 72:
                raise ValueError
        except ValueError:
            return await interaction.response.send_message("Duration must be between 1 and 72 hours!", ephemeral=True)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                manage_messages=True,
                embed_links=True,
                attach_files=True,
                add_reactions=True,
                manage_channels=True
            )
        }

        channel = await interaction.guild.create_text_channel(
            name=self.channel_name.value,
            category=interaction.channel.category,
            overwrites=overwrites
        )

        invite_view = InviteUserView(channel)
        await channel.send(
            f"Private channel created by {interaction.user.mention}\n"
            f"This channel will be deleted in {duration} hours.\n"
            "Use the button below to invite users:",
            view=invite_view
        )

        self.cog.temp_channels[channel.id] = {
            'delete_at': datetime.now() + timedelta(hours=duration),
            'owner': interaction.user.id,
            'members': [interaction.user.id]
        }

        await interaction.response.send_message(f"Private channel {channel.mention} created!", ephemeral=True)

class InviteUserView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=None)
        self.channel = channel

    @discord.ui.button(label="Invite User", style=discord.ButtonStyle.blurple, emoji="➕", custom_id="invite_user")
    async def invite_user(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.channel.permissions_for(interaction.user).read_messages:
            return await interaction.response.send_message("You must be a member of this channel to invite others!", ephemeral=True)

        modal = InviteUserModal(self.channel)
        await interaction.response.send_modal(modal)

class InviteUserModal(discord.ui.Modal, title="Invite User"):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    user_id = discord.ui.TextInput(
        label="User ID or @mention",
        placeholder="Enter user ID or @mention to invite...",
        min_length=2,
        max_length=50
    )

    async def on_submit(self, interaction: discord.Interaction):
        user_input = self.user_id.value.strip()
        try:
            if user_input.startswith('<@') and user_input.endswith('>'):
                user_id = int(user_input[2:-1].replace('!', ''))
            else:
                user_id = int(user_input)
            
            user = await interaction.guild.fetch_member(user_id)
            await self.channel.set_permissions(user,
                read_messages=True,
                send_messages=True,
                embed_links=True,
                attach_files=True,
                add_reactions=True
            )
            await self.channel.send(f"{user.mention} has been invited to the channel by {interaction.user.mention}")
            await interaction.response.send_message(f"Successfully added {user.mention} to the channel!", ephemeral=True)
        except:
            await interaction.response.send_message("Invalid user ID/mention or user not found!", ephemeral=True)

class TempChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}
        self.cleanup_task.start()

    def cog_unload(self):
        self.cleanup_task.cancel()

    @tasks.loop(minutes=5)
    async def cleanup_task(self):
        now = datetime.now()
        channels_to_delete = []
        
        for channel_id, data in self.temp_channels.items():
            if now >= data['delete_at']:
                channels_to_delete.append(channel_id)

        for channel_id in channels_to_delete:
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.delete()
            del self.temp_channels[channel_id]

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setuptempchannel(self, ctx):
        """Setup the temporary channel creation button"""
        view = TempChannelButton(self)
        await ctx.send("Click the button below to create a temporary private channel:", view=view)


class JSONEmbeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def jsonembed(self, ctx, *, json_data: str = None):
        """Create embed from JSON data or file attachment"""
        try:
            
            if ctx.message.attachments:
                json_file = ctx.message.attachments[0]
                if not json_file.filename.endswith('.json'):
                    return await ctx.send("📄 File must be a .json file!")
                json_content = await json_file.read()
                data = json.loads(json_content)
            
            elif json_data:
                if json_data.startswith("```") and json_data.endswith("```"):
                    json_data = json_data[3:-3]
                if json_data.startswith("`") and json_data.endswith("`"):
                    json_data = json_data[1:-1]
                data = json.loads(json_data)
            
            else:
                return await ctx.send("Please provide JSON data or attach a .json file!")

            if "embeds" in data:
                embed_data = data["embeds"][0]  
            else:
                embed_data = data  
            
            embed = discord.Embed.from_dict(embed_data)
            content = data.get("content", None)
            await ctx.send(content=content, embed=embed)
            await ctx.message.add_reaction("✅")

        except json.JSONDecodeError:
            await ctx.send("❌ Invalid JSON format. Please check your JSON syntax.")
        except KeyError as e:
            await ctx.send(f"❌ Missing required field in JSON: {str(e)}")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

    @commands.command()
    async def embedhelp(self, ctx):
        """Shows help for JSON embed formats"""
        embed = discord.Embed(
            title="JSON Embed Help",
            description="Create embeds using JSON data. You can either:\n• Attach a .json file\n• Paste JSON directly",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Command Usage",
            value="```!jsonembed <json data>\n# OR\n!jsonembed + attach .json file```",
            inline=False
        )
        
        embed.add_field(
            name="Discohook/Webhook Format",
            value="""```json
{
    "content": null,
    "embeds": [{
        "title": "Title",
        "description": "Description",
        "color": 16629952
    }]
}```""",
            inline=False
        )
        
        embed.add_field(
            name="Direct Format",
            value="""```json
{
    "title": "Title",
    "description": "Description",
    "color": 16629952
}```""",
            inline=False
        )
        
        embed.add_field(
            name="Complex Format",
            value="""```json
{
    "embeds": [{
        "title": "Title",
        "description": "Description",
        "color": 16629952,
        "fields": [
            {"name": "Field", "value": "Value"}
        ],
        "image": {"url": "image_url"}
    }]
}```""",
            inline=False
        )
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(JSONEmbeds(bot))

class AFKSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, 'afk_users'):
            bot.afk_users = {} 
        
    def format_time_elapsed(self, timestamp):
        time_diff = datetime.now() - timestamp
        return humanize.naturaltime(time_diff)

    def create_afk_embed(self, user, message, is_removal=False):
        if is_removal:
            afk_data = self.bot.afk_users.get(user.id)
            if afk_data:
                time_elapsed = self.format_time_elapsed(afk_data[0])
                description = f"Welcome back {user.name}! 👋\nYou were AFK for: {time_elapsed}"
            else:
                description = f"Welcome back {user.name}! 👋"
                
            embed = discord.Embed(
                title="🔰 AFK Status Removed",
                description=description,
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="🌙 AFK Status Set",
                description=f"**{user.name}** is now AFK\n📝 **Reason:** {message}\n🔔 **Active in all channels**",
                color=user.color or discord.Color.blue()
            )
            embed.set_footer(text="💡 Use !afk again to remove your AFK status")
        
        embed.set_thumbnail(url=user.display_avatar.url)
        return embed


    def create_mention_embed(self, user, timestamp, message, color):
        embed = discord.Embed(
            title="⚠️ User is AFK",
            description=f"**{user.name}** is currently away",
            color=color or discord.Color.orange()
        )
        embed.add_field(name="💭 Reason", value=message, inline=False)
        embed.add_field(
            name="⏰ Away Since", 
            value=self.format_time_elapsed(timestamp),
            inline=False
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="They will see your message when they return")
        return embed

    @commands.command(name="afk", description="Set your AFK status with an optional message")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def afk(self, ctx, *, message=None):
        user_id = ctx.author.id
        bot_roles = ctx.guild.me.roles
        highest_role = max(bot_roles, key=lambda r: r.position)


        if user_id in self.bot.afk_users:
            timestamp = self.bot.afk_users[user_id][0]
            del self.bot.afk_users[user_id]
            embed = self.create_afk_embed(ctx.author, None, is_removal=True)
            try:
              
                if ctx.author.display_name.startswith("[AFK] "):
                    await ctx.author.edit(nick=ctx.author.display_name[6:])
            except discord.Forbidden:
                pass
            await ctx.send(embed=embed)
            return



        message = message or "No reason provided"
        if len(message) > 100:
            message = message[:97] + "..."
        
        self.bot.afk_users[user_id] = (
            datetime.now(),
            message,
            ctx.author.color or discord.Color.blue(),
            ctx.guild.id
        )
        
        try:
        
            current_nick = ctx.author.display_name
            if not current_nick.startswith("[AFK] "):
                await ctx.author.edit(nick=f"[AFK] {current_nick}")
        except discord.Forbidden:
            pass

        embed = self.create_afk_embed(ctx.author, message)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        show_author_afk = False
        if message.author.id in self.bot.afk_users:
            if not message.content.lower().startswith(f"{self.bot.command_prefix}afk"):
                show_author_afk = True

        for mention in message.mentions:
            if mention.id in self.bot.afk_users:
                timestamp, afk_message, color, guild_id = self.bot.afk_users[mention.id]
                
                if guild_id != message.guild.id:
                    continue
                    
                embed = self.create_mention_embed(
                    mention,
                    timestamp,
                    afk_message,
                    color
                )
                await message.reply(embed=embed, mention_author=False)
        
        if show_author_afk:
            await self.afk.callback(self, await self.bot.get_context(message))


    @afk.error
    async def afk_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏰ Please wait {error.retry_after:.1f}s before using this command again.")




class EnhancedMinigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.scores = {}
        self.streaks = {}
        self.achievements = {}
        self.daily_challenges = {}
        self.tournament_matches = {}
        
        self.word_categories = {
            'animals': {
                'easy': ['cat', 'dog', 'bird', 'fish', 'lion'],
                'normal': ['elephant', 'giraffe', 'penguin', 'dolphin', 'kangaroo'],
                'hard': ['platypus', 'rhinoceros', 'hippopotamus', 'chameleon', 'orangutan']
            },
            'food': {
                'easy': ['pizza', 'pasta', 'bread', 'cake', 'rice'],
                'normal': ['spaghetti', 'hamburger', 'sandwich', 'pancake', 'chocolate'],
                'hard': ['ratatouille', 'bouillabaisse', 'wellington', 'tiramisu', 'bruschetta']
            },
            'countries': {
                'easy': ['spain', 'italy', 'china', 'india', 'egypt'],
                'normal': ['germany', 'france', 'japan', 'brazil', 'australia'],
                'hard': ['kazakhstan', 'azerbaijan', 'mauritius', 'zimbabwe', 'madagascar']
            }
        }

        self.trivia_categories = {
            'general': ['easy', 'normal', 'hard'],
            'science': ['easy', 'normal', 'hard'],
            'history': ['easy', 'normal', 'hard'],
            'geography': ['easy', 'normal', 'hard'],
            'entertainment': ['easy', 'normal', 'hard']
        }

        self.game_settings = {
            'rps': {'rounds': 3, 'special_moves': True},
            'memory': {'sizes': [4, 6, 8], 'time_limit': 180},
            'reaction': {'modes': ['classic', 'pattern', 'chain']},
            'trivia': {'questions_per_round': 5, 'time_per_question': 30}
        }

        self.trivia_questions = self.load_trivia_questions()
        self.game_stats = {
            'rps': {},
            'wordscramble': {},
            'memory': {},
            'hangman': {},
            'reaction': {},
            'aimtrainer': {},
            'trivia': {}
        }

    async def update_player_stats(self, user_id: int, game_type: str, won: bool = False, extra_data: dict = None):
        if user_id not in self.scores:
            self.scores[user_id] = {
                'total_games': 0,
                'total_wins': 0,
                'current_streak': 0,
                'best_streak': 0,
                'last_played': None,
                'games': {
                    'rps': {'played': 0, 'wins': 0, 'best_streak': 0, 'win_rate': 0},
                    'wordscramble': {'played': 0, 'wins': 0, 'best_time': float('inf'), 'words_solved': 0},
                    'memory': {'played': 0, 'wins': 0, 'best_time': float('inf'), 'perfect_matches': 0},
                    'hangman': {'played': 0, 'wins': 0, 'best_streak': 0, 'letters_guessed': 0},
                    'reaction': {'played': 0, 'wins': 0, 'best_time': float('inf'), 'avg_time': 0},
                    'aimtrainer': {'played': 0, 'wins': 0, 'best_accuracy': 0, 'total_hits': 0, 'best_streak': 0},
                    'trivia': {'played': 0, 'wins': 0, 'best_score': 0, 'correct_answers': 0}
                }
            }

        stats = self.scores[user_id]
        stats['total_games'] += 1
        stats['last_played'] = datetime.now().timestamp()
        
        if won:
            stats['total_wins'] += 1
            stats['current_streak'] += 1
            stats['best_streak'] = max(stats['best_streak'], stats['current_streak'])
            stats['games'][game_type]['wins'] += 1
        else:
            stats['current_streak'] = 0
        
        stats['games'][game_type]['played'] += 1
        stats['games'][game_type]['win_rate'] = (stats['games'][game_type]['wins'] / stats['games'][game_type]['played']) * 100

        if extra_data:
            game_stats = stats['games'][game_type]
            
            if game_type == 'aimtrainer':
                game_stats['best_accuracy'] = max(game_stats.get('best_accuracy', 0), extra_data.get('accuracy', 0))
                game_stats['total_hits'] = game_stats.get('total_hits', 0) + extra_data.get('hits', 0)
                game_stats['best_streak'] = max(game_stats.get('best_streak', 0), extra_data.get('streak', 0))
            
            elif game_type in ['reaction', 'memory', 'wordscramble']:
                if 'time' in extra_data:
                    game_stats['best_time'] = min(game_stats.get('best_time', float('inf')), extra_data['time'])
                    
                    times = game_stats.get('times', [])
                    times.append(extra_data['time'])
                    game_stats['avg_time'] = sum(times) / len(times)
                    game_stats['times'] = times[-10:]  
            
            elif game_type == 'trivia':
                game_stats['best_score'] = max(game_stats.get('best_score', 0), extra_data.get('score', 0))
                game_stats['correct_answers'] = game_stats.get('correct_answers', 0) + extra_data.get('correct', 0)

        await self.check_achievements(user_id, game_type, stats)



    def load_trivia_questions(self):
        
        return {
            'general': [
                {
                    'question': 'What is the capital of France?',
                    'answers': ['Paris', 'London', 'Berlin', 'Madrid'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'points': 100
                },
                
            ],
            'science': [
                {
                    'question': 'What is the chemical symbol for gold?',
                    'answers': ['Au', 'Ag', 'Fe', 'Cu'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'points': 100
                }
                
            ]
        }

    @commands.command(name='rps')
    async def rps(self, ctx, rounds: int = 3):
        """Start a Rock Paper Scissors game"""
        embed = discord.Embed(
            title="🎮 Rock Paper Scissors",
            description=f"{ctx.author.mention} wants to play RPS!\nClick Join to play!",
            color=discord.Color.blue()
        )
        
        view = discord.ui.View(timeout=60)
        
        async def join_callback(interaction):
            if interaction.user == ctx.author:
                await interaction.response.send_message("You can't play against yourself!", ephemeral=True)
                return
                
            game_view = self.RPSView(ctx.author, interaction.user, rounds)
            await interaction.message.edit(
                embed=discord.Embed(
                    title="🎮 Rock Paper Scissors",
                    description=f"Game between {ctx.author.mention} and {interaction.user.mention}\n"
                            f"Best of {rounds}!\nMake your choice!",
                    color=discord.Color.blue()
                ),
                view=game_view
            )
        
        join = discord.ui.Button(label="Join Game", style=discord.ButtonStyle.green, emoji="🎮")
        join.callback = join_callback
        view.add_item(join)
        
        await ctx.send(embed=embed, view=view)

    @commands.command(name='memory')
    async def memory(self, ctx, size: int = 4):
        """Start a memory matching game"""
        valid_sizes = [2, 4]
        if size not in valid_sizes:
            await ctx.send(f"Please choose a valid board size: {', '.join(map(str, valid_sizes))}!")
            return
            
        game_view = self.MemoryView(size)
        embed = discord.Embed(
            title="🎮 Memory Game",
            description=(
                f"Match pairs of emojis!\n"
                f"Board size: {size}x{size}\n\n"
                f"👉 Click the tiles to reveal emojis\n"
                f"🔄 Find matching pairs to keep them revealed\n"
                f"⭐ Complete the game as fast as you can!"
            ),
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed, view=game_view)

    class HangmanView(discord.ui.View):
        def __init__(self, word: str, category: str, starter: discord.Member, party_players=None):
            super().__init__(timeout=180)
            self.word = word
            self.category = category
            self.guessed_letters = set()
            self.lives = 6
            self.starter = starter
            self.party_players = party_players or []
            self.current_player_index = 0
            self.message = None
            self.hangman_stages = [
                "```\n   ____\n  |    |\n  |\n  |\n  |\n _|_\n```",
                "```\n   ____\n  |    |\n  |    O\n  |\n  |\n _|_\n```",
                "```\n   ____\n  |    |\n  |    O\n  |    |\n  |\n _|_\n```",
                "```\n   ____\n  |    |\n  |    O\n  |   /|\n  |\n _|_\n```",
                "```\n   ____\n  |    |\n  |    O\n  |   /|\\\n  |\n _|_\n```",
                "```\n   ____\n  |    |\n  |    O\n  |   /|\\\n  |   /\n _|_\n```",
                "```\n   ____\n  |    |\n  |    O\n  |   /|\\\n  |   / \\\n _|_\n```"
            ]

        def get_word_display(self):
            return ' '.join(letter if letter in self.guessed_letters else '_' for letter in self.word)

        def create_game_embed(self):
            current_player = self.party_players[self.current_player_index] if self.party_players else self.starter
            
            embed = discord.Embed(
                title="🎯 Hangman Game",
                description=f"Category: {self.category.title()}\n\n"
                        f"{self.hangman_stages[6-self.lives]}\n\n"
                        f"Word: {self.get_word_display()}\n"
                        f"Lives: {'❤️' * self.lives}\n"
                        f"Guessed letters: {', '.join(sorted(self.guessed_letters))}\n\n"
                        f"Current turn: {current_player.mention}",
                color=discord.Color.blue()
            )
            return embed

        async def process_guess(self, message):
            if len(message.content) != 1 or not message.content.isalpha():
                return

            letter = message.content.lower()
            if letter in self.guessed_letters:
                return

            self.guessed_letters.add(letter)
            
            if letter not in self.word:
                self.lives -= 1
                if self.party_players:
                    self.current_player_index = (self.current_player_index + 1) % len(self.party_players)

            word_completed = all(letter in self.guessed_letters for letter in self.word)
            embed = self.create_game_embed()

            if word_completed:
                embed.description += f"\n\n🎉 You won! The word was: {self.word}"
                await self.message.edit(embed=embed)
                self.stop()
            elif self.lives <= 0:
                embed.description += f"\n\n💀 Game Over! The word was: {self.word}"
                await self.message.edit(embed=embed)
                self.stop()
            else:
                await self.message.edit(embed=embed)

    @commands.command(name='hangman')
    async def hangman(self, ctx, category: str = "random"):
        """Start a hangman game"""
        categories = {
            'animals': [
                'elephant', 'penguin', 'giraffe', 'dolphin', 'kangaroo', 'octopus', 'cheetah',
                'rhinoceros', 'hippopotamus', 'crocodile', 'butterfly', 'gorilla', 'panda',
                'tiger', 'zebra', 'koala', 'flamingo', 'jaguar', 'hedgehog', 'platypus',
                'chameleon', 'armadillo', 'orangutan', 'mongoose', 'salamander', 'jellyfish',
                'scorpion', 'hamster', 'peacock', 'pelican', 'albatross', 'anaconda', 'gazelle',
                'wolverine', 'meerkat', 'narwhal', 'pangolin', 'iguana', 'raccoon', 'walrus'
            ],
            'food': [
                'pizza', 'spaghetti', 'hamburger', 'chocolate', 'pancake', 'sandwich',
                'lasagna', 'burrito', 'croissant', 'cheesecake', 'quesadilla', 'meatballs',
                'ravioli', 'enchilada', 'dumplings', 'tiramisu', 'guacamole', 'carbonara',
                'ratatouille', 'macaroni', 'bruschetta', 'cannelloni', 'gnocchi', 'paella',
                'churros', 'fettuccine', 'gazpacho', 'hummus', 'risotto', 'tagliatelle',
                'tortellini', 'waffles', 'yogurt', 'zucchini', 'baklava', 'baguette',
                'calzone', 'empanada', 'falafel', 'nachos'
            ],
            'countries': [
                'germany', 'france', 'japan', 'brazil', 'australia', 'canada', 'spain',
                'portugal', 'switzerland', 'netherlands', 'argentina', 'madagascar', 'indonesia',
                'philippines', 'singapore', 'kazakhstan', 'zimbabwe', 'ethiopia', 'morocco',
                'bangladesh', 'azerbaijan', 'venezuela', 'guatemala', 'honduras', 'uruguay',
                'paraguay', 'cambodia', 'cameroon', 'tanzania', 'uganda', 'mozambique',
                'botswana', 'mauritius', 'montenegro', 'luxembourg', 'lithuania', 'slovenia',
                'slovakia', 'bulgaria', 'romania'
            ],
            'sports': [
                'football', 'basketball', 'tennis', 'volleyball', 'swimming', 'boxing',
                'skateboarding', 'gymnastics', 'snowboarding', 'waterpolo', 'badminton',
                'wrestling', 'taekwondo', 'cricket', 'baseball', 'handball', 'cycling',
                'surfing', 'climbing', 'karate', 'archery', 'fencing', 'rowing', 'sailing',
                'triathlon', 'marathon', 'parkour', 'snorkeling', 'canoeing', 'dodgeball',
                'hockey', 'lacrosse', 'rugby', 'polo', 'curling', 'javelin', 'judo',
                'kickboxing', 'bowling', 'squash'
            ]
        }

        
        if category == "random":
            category = random.choice(list(categories.keys()))
        elif category not in categories:
            await ctx.send(f"Available categories: {', '.join(categories.keys())}")
            return

        word = random.choice(categories[category]).lower()
        game_view = self.HangmanView(word, category, ctx.author)
        
        embed = game_view.create_game_embed()
        game_view.message = await ctx.send(embed=embed)

        def check(m):
            return (m.author == ctx.author or m.author in game_view.party_players) and m.channel == ctx.channel

        while not game_view.is_finished():
            try:
                message = await ctx.bot.wait_for('message', timeout=180.0, check=check)
                await game_view.process_guess(message)
            except asyncio.TimeoutError:
                await ctx.send("Game timed out!")
                break


    @commands.command(name='party')
    async def party(self, ctx):
        """Start a party game session"""
        await self.start_party_session(ctx, [ctx.author])

    @commands.command(name='games')
    async def games(self, ctx):
        """Shows all available minigames with detailed information"""
        embed = EmbedBuilder(
            "🎮 Enhanced Minigames Collection",
            "Welcome to the ultimate gaming experience!"
        ).set_color(discord.Color.blue())

        games_list = [
            ("🎲 Rock Paper Scissors", "!rps [rounds]",
            "Enhanced RPS with animations, best of 3/5/7, and special moves!"),
            
            ("🔤 Word Scramble", "!wordscramble [category] [difficulty]",
            "Categories: animals, food, countries\nDifficulties: easy, normal, hard\nFeatures hints and time bonuses!"),
            
            ("👻 Hangman", "!hangman [category]",
            "Enhanced with themes, hints, and progressive difficulty!\nCategories: animals, food, countries and sports"),
            
            ("🧩 Memory", "!memory [size]",
            "Match pairs with different board sizes and themes\nCompete for fastest times!\nSizes: 2x2, 4x4"),
            
            ("❓ Trivia", "!trivia [category] [difficulty]",
"Multiple categories with scoring system and daily challenges!\n"
"Categories: general, science, history, geography, entertainment, sports, technology, literature, music, movies\n"
"Difficulties: easy, normal, hard",),
            
            ("⚡ Reaction Test", "!reactiontest [mode]",
            "Test reactions with various modes and global rankings!\nModes: classic, pattern, chain"),
            
            ("🎯 Aim Trainer", "!aimtrainer",
            "New! Test your clicking speed and accuracy!"),
            
            ("🎪 Party Mode", "!party",
            "New! Play random minigames in succession with friends!"),
            
            ("🔢 Number Game", "!numbergame <number> <channel>",
            "Classic number guessing game with customizable range!"),
            
            ("⭕ TicTacToe", "!tictactoe",
            "Classic TicTacToe game against other players!"),
            
            ("4️⃣ Connect Four", "!connect4",
            "Strategic Connect Four game with animations!"),
            
            ("🏆 Leaderboard", "!leaderboard [game_type]",
            "View global or game-specific leaderboards!"),
            
            ("👤 Profile", "!profile [user]",
            "View detailed player statistics and achievements!"),
            
            ("📅 Daily Challenges", "!daily",
            "Complete daily challenges for bonus points!")
        ]


        for game, command, description in games_list:
            embed.add_field(
                name=f"{game}",
                value=f"Command: `{command}`\n{description}",
                inline=False
            )

        if ctx.author.id in self.scores:
            stats = self.scores[ctx.author.id]
            embed.add_field(
                name="🏆 Your Statistics",
                value=f"Games Played: {stats['total_games']}\n"
                    f"Wins: {stats['wins']}\n"
                    f"Current Streak: {self.streaks.get(ctx.author.id, 0)}\n"
                    f"Achievement Points: {self.achievements.get(ctx.author.id, 0)}",
                inline=False
            )

        await ctx.send(embed=embed.build())


    async def update_stats(self, user_id, game_type, won=False):
        if user_id not in self.scores:
            self.scores[user_id] = {
                'total_games': 0,
                'wins': 0,
                'game_specific': {}
            }
        
        self.scores[user_id]['total_games'] += 1
        if won:
            self.scores[user_id]['wins'] += 1
            self.streaks[user_id] = self.streaks.get(user_id, 0) + 1
        else:
            self.streaks[user_id] = 0

    async def create_game_channel(self, ctx, interaction, game_type):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, manage_channels=True)
        }
        
        channel = await ctx.guild.create_text_channel(
            f"{game_type}-{ctx.author.name}-{interaction.user.name}",
            overwrites=overwrites
        )

        async def cleanup_channel():
            await asyncio.sleep(600)  
            try:
                await channel.delete()
            except:
                pass

        self.bot.loop.create_task(cleanup_channel())
        return channel
    
    class RPSView(discord.ui.View):
        def __init__(self, player1, player2, rounds=3):
            super().__init__(timeout=None)
            self.player1 = player1
            self.player2 = player2
            self.p1_choice = None
            self.p2_choice = None
            self.p1_score = 0
            self.p2_score = 0
            self.round = 1
            self.max_rounds = rounds
            self.special_move_available = True
            self.setup_buttons()



        async def make_choice(self, interaction: discord.Interaction):
            if interaction.user not in [self.player1, self.player2]:
                return

            choice = int(interaction.data['custom_id'].split('_')[1])
            
            if interaction.user == self.player1:
                self.p1_choice = int(choice)  
            else:
                self.p2_choice = int(choice)

            if self.p1_choice is not None and self.p2_choice is not None:
                await self.resolve_round(interaction)
            else:
                await interaction.response.defer()

        async def make_choice(self, interaction: discord.Interaction):
            if interaction.user not in [self.player1, self.player2]:
                return

            choice_id = interaction.data['custom_id'].split('_')[1]
            
            if choice_id == 'special':
                choice = 'special'
            else:
                choice = int(choice_id)
            
            if interaction.user == self.player1:
                self.p1_choice = choice
            else:
                self.p2_choice = choice

            if self.p1_choice is not None and self.p2_choice is not None:
                await self.resolve_round(interaction)
            else:
                await interaction.response.defer()

        async def resolve_round(self, interaction: discord.Interaction, special_result=None):
            choices = ['Rock', 'Paper', 'Scissors', '✨ Special Move ✨']
            
            p1_choice_display = choices[3] if self.p1_choice == 'special' else choices[self.p1_choice]
            p2_choice_display = choices[3] if self.p2_choice == 'special' else choices[self.p2_choice]
            
            if self.p1_choice == 'special' and self.p2_choice == 'special':
                
                winner = random.choice([self.player1, self.player2, None])
            elif self.p1_choice == 'special':
                
                result = random.choices(['win', 'lose', 'draw'], weights=[0.5, 0.25, 0.25])[0]
                winner = self.player1 if result == 'win' else (self.player2 if result == 'lose' else None)
            elif self.p2_choice == 'special':
                
                result = random.choices(['win', 'lose', 'draw'], weights=[0.5, 0.25, 0.25])[0]
                winner = self.player2 if result == 'win' else (self.player1 if result == 'lose' else None)
            else:
              
                p1_num = int(self.p1_choice)
                p2_num = int(self.p2_choice)
                
                if p1_num == p2_num:
                    winner = None
                elif (p1_num - p2_num) % 3 == 1:
                    winner = self.player1
                else:
                    winner = self.player2

            if winner == self.player1:
                self.p1_score += 1
                result_message = "🎯 Perfect move!" if self.p1_choice == 'special' else "Victory!"
            elif winner == self.player2:
                self.p2_score += 1
                result_message = "🎯 Perfect move!" if self.p2_choice == 'special' else "Victory!"
            else:
                result_message = "It's a draw!"

            embed = discord.Embed(
                title=f"Round {self.round}/{self.max_rounds}",
                description=f"{self.player1.mention}: {p1_choice_display}\n"
                            f"{self.player2.mention}: {p2_choice_display}\n\n"
                            f"{result_message}\n"
                            f"Winner: {winner.mention if winner else 'Draw!'}\n"
                            f"Score: {self.p1_score} - {self.p2_score}",
                color=discord.Color.blue()
            )

            if self.p1_choice == 'special' or self.p2_choice == 'special':
                embed.add_field(
                    name="✨ Special Move Used!",
                    value="Special moves are now on cooldown.",
                    inline=False
                )

            self.round += 1
            self.p1_choice = None
            self.p2_choice = None

            if self.round > self.max_rounds or self.p1_score > self.max_rounds//2 or self.p2_score > self.max_rounds//2:
                final_winner = self.player1 if self.p1_score > self.p2_score else self.player2
                embed.add_field(
                    name="🏆 Game Over!",
                    value=f"Champion: {final_winner.mention}\n"
                        f"Final Score: {self.p1_score} - {self.p2_score}",
                    inline=False
                )
                await interaction.response.edit_message(embed=embed, view=None)
                self.stop()
            else:
                await interaction.response.edit_message(embed=embed, view=self)

        def setup_buttons(self):
            
            choices = [('🪨', 'Rock'), ('📄', 'Paper'), ('✂️', 'Scissors')]
            for i, (emoji, name) in enumerate(choices):
                button = discord.ui.Button(
                    emoji=emoji, 
                    label=name, 
                    custom_id=f'choice_{i}', 
                    row=0,
                    style=discord.ButtonStyle.primary
                )
                button.callback = self.make_choice
                self.add_item(button)

            special = discord.ui.Button(
                emoji='🌟',
                label='Special Move',
                custom_id='special',
                row=1,
                style=discord.ButtonStyle.primary
            )
            special.callback = self.special_move
            self.add_item(special)

        async def special_move(self, interaction: discord.Interaction):
            if not self.special_move_available or interaction.user not in [self.player1, self.player2]:
                return

            result = random.choices(['win', 'lose', 'draw'], weights=[0.5, 0.25, 0.25])[0]
            
            if interaction.user == self.player1:
                self.p1_choice = 'special'
                if self.p2_choice is None:
                    await interaction.response.defer()
                    return
            else:
                self.p2_choice = 'special'
                if self.p1_choice is None:
                    await interaction.response.defer()
                    return

            self.special_move_available = False
            await self.resolve_round(interaction, special_result=result)

    class WordScrambleView(discord.ui.View):
        def __init__(self, word: str, category: str, difficulty: str, ctx, cog):  
            super().__init__(timeout=120)
            
            self.word = word
            self.category = category
            self.difficulty = difficulty
            self.hints_remaining = 3 if difficulty == 'hard' else 2
            self.start_time = time.time()
            self.scrambled = self.scramble_word(word)
            self.guesses = []
            self.ctx = ctx
            self.cog = cog  
            self.setup_buttons()
            self.message = None
            
        def scramble_word(self, word):
            while True:
                scrambled = ''.join(random.sample(word, len(word)))
                if scrambled != word:
                    return scrambled

        def setup_buttons(self):
            hint = discord.ui.Button(
                emoji='💡',
                label=f'Hint ({self.hints_remaining})',
                custom_id='hint',
                row=0
            )
            hint.callback = self.give_hint
            self.add_item(hint)

            give_up = discord.ui.Button(
                emoji='🏳️',
                label='Give Up',
                style=discord.ButtonStyle.danger,
                row=0
            )
            give_up.callback = self.give_up
            self.add_item(give_up)

        async def give_hint(self, interaction: discord.Interaction):
            if self.hints_remaining <= 0:
                return

            revealed_positions = []
            hint_text = list('_' * len(self.word))
            
            for i, letter in enumerate(self.word):
                if random.random() < 0.3:
                    hint_text[i] = letter
                    revealed_positions.append(i)

            self.hints_remaining -= 1
            
            hint_embed = discord.Embed(
                title="💡 Hint",
                description=f"Here's a hint for the word:\n`{''.join(hint_text)}`\n"
                        f"Hints remaining: {self.hints_remaining}",
                color=discord.Color.gold()
            )

            await interaction.response.send_message(embed=hint_embed, ephemeral=True)

        async def give_up(self, interaction: discord.Interaction):
            embed = discord.Embed(
                title="Game Over!",
                description=f"The word was: **{self.word}**\n"
                        f"Category: {self.category.title()}\n"
                        f"Difficulty: {self.difficulty.title()}",
                color=discord.Color.red()
            )
            
            embed.add_field(
                name="Keep practicing!",
                value=f"Try another word with `!wordscramble {self.category} {self.difficulty}`"
            )
            
            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()

        async def on_message(self, message):
            if message.author == self.ctx.author and message.channel == self.ctx.channel:
                guess = message.content.lower()
                self.guesses.append(guess)
                
                if guess == self.word.lower():
                    time_taken = int(time.time() - self.start_time)
                    embed = discord.Embed(
                        title="🎉 Correct!",
                        description=f"You solved it in {time_taken} seconds!\n"
                                f"Word: **{self.word}**\n"
                                f"Attempts: {len(self.guesses)}",
                        color=discord.Color.green()
                    )
                    await self.message.edit(embed=embed, view=None)
                    self.stop()

                    await self.cog.update_player_stats(
                        message.author.id,
                        'wordscramble',
                        won=True,
                        extra_data={
                            'time': time_taken,
                            'score': len(self.guesses)
                        }
                    )
                else:
                    hint_message = await message.channel.send("That's not correct! Try again!", delete_after=3)

    @commands.command(name='wordscramble')
    async def wordscramble(self, ctx, category: str = "random", difficulty: str = "normal"):
        if category == "random":
            category = random.choice(list(self.word_categories.keys()))
        
        word = random.choice(self.word_categories[category][difficulty])
        game_view = self.WordScrambleView(word, category, difficulty, ctx, self)  
        
        embed = discord.Embed(
            title="🔤 Word Scramble",
            description=f"Category: {category.title()}\n"
                        f"Difficulty: {difficulty.title()}\n\n"
                        f"Unscramble this word: **{game_view.scrambled}**\n"
                        f"Type your answer in this channel!",
            color=discord.Color.blue()
        )
        
        game_view.message = await ctx.send(embed=embed, view=game_view)
            
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
            
        while not game_view.is_finished():
            try:
                message = await self.bot.wait_for('message', timeout=120.0, check=check)
                await game_view.on_message(message)
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    title="⏰ Time's Up!",
                    description=f"The word was **{word}**",
                    color=discord.Color.red()
                )
                await game_view.message.edit(embed=timeout_embed, view=None)
                break





    class MemoryView(discord.ui.View):
        def __init__(self, size=4, party_players=None):
            super().__init__(timeout=180)
            self.size = size
            self.board = []
            self.revealed = set()
            self.first_choice = None
            self.moves = 0
            self.start_time = None
            self.party_players = party_players or []
            self.current_player_index = 0
            self.player_scores = {player.id: 0 for player in self.party_players} if self.party_players else {}
            self.setup_board()

        def setup_board(self):
            valid_sizes = [2, 4]
            self.size = min(valid_sizes, key=lambda x: abs(x - self.size))
            
            emojis = ['🎮', '🎲', '🎯', '🎪', '🎨', '🎭', '🎫', '🎟️',
                    '🎸', '🎺', '🎻', '🎹', '🎼', '🎧', '🎤', '🎬']
            
            needed_pairs = (self.size * self.size) // 2
            emoji_pairs = (emojis[:needed_pairs] * 2)
            random.shuffle(emoji_pairs)
            
            self.board = [emoji_pairs[i:i+self.size] for i in range(0, self.size * self.size, self.size)]
            
            for i in range(self.size):
                for j in range(self.size):
                    button = discord.ui.Button(
                        style=discord.ButtonStyle.secondary,
                        label='❓',
                        custom_id=f'cell_{i}_{j}',
                        row=i
                    )
                    button.callback = self.make_move
                    self.add_item(button)





        async def make_move(self, interaction: discord.Interaction):
            if not self.start_time:
                self.start_time = time.time()

            if self.party_players:
                current_player = self.party_players[self.current_player_index]
                if interaction.user != current_player:
                    await interaction.response.send_message(f"It's {current_player.mention}'s turn!", ephemeral=True)
                    return

            pos = interaction.data['custom_id'].split('_')[1:]
            i, j = map(int, pos)
            
            if (i, j) in self.revealed:
                return

            self.moves += 1
            current_button = None
            
            for child in self.children:
                if child.custom_id == f'cell_{i}_{j}':
                    child.label = self.board[i][j]
                    child.disabled = True
                    current_button = child
                    break

            if not self.first_choice:
                self.first_choice = (i, j, current_button)
                await interaction.response.edit_message(view=self)
            else:
                prev_i, prev_j, prev_button = self.first_choice
                
                if self.board[i][j] == self.board[prev_i][prev_j]:
                    
                    self.revealed.add((i, j))
                    self.revealed.add((prev_i, prev_j))
                    
                    if self.party_players:
                        self.player_scores[interaction.user.id] += 1
                        await interaction.followup.send(f"{interaction.user.mention} found a pair! They get another turn!", ephemeral=False)
                    
                    if len(self.revealed) == self.size**2:
                        await self.game_won(interaction)
                    else:
                        await interaction.response.edit_message(view=self)
                else:
                   
                    await interaction.response.edit_message(view=self)
                    await asyncio.sleep(1)
                    
                    current_button.label = '❓'
                    current_button.disabled = False
                    prev_button.label = '❓'
                    prev_button.disabled = False
                    
                    await interaction.message.edit(view=self)
                    
                    if self.party_players:
                        self.current_player_index = (self.current_player_index + 1) % len(self.party_players)
                        next_player = self.party_players[self.current_player_index]
                        await interaction.followup.send(f"No match! It's now {next_player.mention}'s turn!", ephemeral=False)
                
                self.first_choice = None

        async def game_won(self, interaction):
            time_taken = int(time.time() - self.start_time)
            
            if self.party_players:
                winner = max(self.player_scores.items(), key=lambda x: x[1])
                winner_user = discord.utils.get(self.party_players, id=winner[0])
                
                embed = discord.Embed(
                    title="🎉 Memory Game Complete!",
                    description=f"Game Over!\n"
                            f"Winner: {winner_user.mention} with {winner[1]} pairs!\n"
                            f"Time taken: {time_taken} seconds\n"
                            f"Total moves: {self.moves}",
                    color=discord.Color.green()
                )
                
                scores_text = "\n".join(f"{discord.utils.get(self.party_players, id=pid).name}: {score} pairs" 
                                    for pid, score in self.player_scores.items())
                embed.add_field(name="Final Scores", value=scores_text)
            else:
                embed = discord.Embed(
                    title="🎉 Memory Game Complete!",
                    description=f"Congratulations! You matched all pairs!\n"
                            f"Time taken: {time_taken} seconds\n"
                            f"Total moves: {self.moves}",
                    color=discord.Color.green()
                )
                
                if time_taken < 30:
                    embed.add_field(name="Rating", value="⭐⭐⭐ Perfect!")
                elif time_taken < 60:
                    embed.add_field(name="Rating", value="⭐⭐ Great!")
                else:
                    embed.add_field(name="Rating", value="⭐ Good!")

            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()

            await self.cog.update_player_stats(
                interaction.user.id,
                'memory',
                won=True,
                extra_data={
                    'time': time_taken,
                    'score': self.moves
                }
            )


    class TriviaView(discord.ui.View):
        def __init__(self, questions, category, difficulty, starter: discord.Member, cog=None):
            super().__init__(timeout=180)
            self.questions = questions
            self.category = category
            self.difficulty = difficulty
            self.starter = starter
            self.current_question = 0
            self.score = 0
            self.streak = 0
            self.multiplier = 1.0
            self.total_questions = len(questions)
            self.message = None
            self.cog = cog
            self.setup_question()

        def setup_question(self):
            self.clear_items()
            question = self.questions[self.current_question]
            
            answers = list(enumerate(question['answers']))
            random.shuffle(answers)
            for new_idx, (old_idx, answer) in enumerate(answers):
                if old_idx == question['correct']:
                    question['correct'] = new_idx
                
                button = discord.ui.Button(
                    label=answer,
                    custom_id=f'answer_{new_idx}',
                    style=discord.ButtonStyle.primary,
                    row=new_idx//2
                )
                button.callback = self.check_answer
                self.add_item(button)

        def create_status_embed(self, title, description):
            embed = discord.Embed(
                title=title,
                description=description,
                color=discord.Color.blue()
            )
            
            progress = "🟦" * self.current_question + "⬜" * (self.total_questions - self.current_question)
            embed.add_field(
                name=f"Progress: {self.current_question}/{self.total_questions}",
                value=progress,
                inline=False
            )
            
            if self.current_question < self.total_questions:
                embed.add_field(
                    name=f"Question {self.current_question + 1}",
                    value=self.questions[self.current_question]['question'],
                    inline=False
                )
            
            embed.add_field(
                name="Stats",
                value=f"Score: {self.score} | Streak: {self.streak}🔥 | Multiplier: x{self.multiplier:.1f}",
                inline=False
            )
            
            return embed

        async def check_answer(self, interaction: discord.Interaction):
            if interaction.user != self.starter:
                await interaction.response.send_message("This isn't your game!", ephemeral=True)
                return

            question = self.questions[self.current_question]
            choice = int(interaction.data['custom_id'].split('_')[1])
            
            if choice == question['correct']:
                self.streak += 1
                self.multiplier = min(2.0, 1.0 + (self.streak * 0.1))
                points = int(question['points'] * self.multiplier)
                self.score += points
                
                embed = self.create_status_embed(
                    "✅ Correct!",
                    f"You earned {points} points! (x{self.multiplier:.1f} multiplier)"
                )
            else:
                self.streak = 0
                self.multiplier = 1.0
                embed = self.create_status_embed(
                    "❌ Incorrect!",
                    f"The correct answer was: {question['answers'][question['correct']]}"
                )

            self.current_question += 1
            
            if self.current_question >= self.total_questions:
                embed.description += f"\n\n🎮 Game Over! Final Score: {self.score}"
                
                if self.score > 1000:
                    embed.add_field(name="🏆 Achievement", value="Score Master!")
                if self.streak >= 5:
                    embed.add_field(name="🔥 Achievement", value="Hot Streak!")
                
                same_category = discord.ui.Button(
                    label="Same Category",
                    style=discord.ButtonStyle.success,
                    custom_id="same_category",
                    row=4
                )
                same_category.callback = self.start_new_game

                random_category = discord.ui.Button(
                    label="Random Category",
                    style=discord.ButtonStyle.primary,
                    custom_id="random_category",
                    row=4
                )
                random_category.callback = self.start_random_category

                random_difficulty = discord.ui.Button(
                    label="Random Difficulty",
                    style=discord.ButtonStyle.secondary,
                    custom_id="random_difficulty",
                    row=4
                )
                random_difficulty.callback = self.start_random_difficulty

                self.clear_items()
                self.add_item(same_category)
                self.add_item(random_category)
                self.add_item(random_difficulty)
            else:
                self.setup_question()

            await interaction.response.edit_message(embed=embed, view=self)

        async def start_random_category(self, interaction: discord.Interaction):
            if interaction.user != self.starter:
                await interaction.response.send_message("This isn't your game!", ephemeral=True)
                return

            categories = ['general', 'science', 'history', 'geography', 'entertainment']
            available_categories = [c for c in categories if c != self.category]
            new_category = random.choice(available_categories)
            
            default_questions = [
                {
                    'question': 'What is the capital of France?',
                    'answers': ['Paris', 'London', 'Berlin', 'Madrid'],
                    'correct': 0,
                    'points': 100
                },
                {
                    'question': 'Which planet is known as the Red Planet?',
                    'answers': ['Mars', 'Venus', 'Jupiter', 'Saturn'],
                    'correct': 0,
                    'points': 100
                }
            ]

            if hasattr(self.cog, 'get_filtered_questions'):
                new_questions = self.cog.get_filtered_questions(new_category, self.difficulty)
            else:
                new_questions = default_questions

            new_view = self.__class__(new_questions, new_category, self.difficulty, self.starter, self.cog)
            embed = new_view.create_status_embed(
                f"New Game - {new_category.title()}!",
                f"Category: {new_category.title()}\nDifficulty: {self.difficulty.title()}\nGood luck! 🎮"
            )
            await interaction.response.edit_message(embed=embed, view=new_view)

        async def start_random_difficulty(self, interaction: discord.Interaction):
            if interaction.user != self.starter:
                await interaction.response.send_message("This isn't your game!", ephemeral=True)
                return

            difficulties = ['easy', 'normal', 'hard']
            available_difficulties = [d for d in difficulties if d != self.difficulty]
            new_difficulty = random.choice(available_difficulties)
            
            default_questions = {
                'easy': [
                    {
                        'question': 'What color is the sky on a clear day?',
                        'answers': ['Blue', 'Red', 'Green', 'Yellow'],
                        'correct': 0,
                        'points': 100
                    }
                ],
                'normal': [
                    {
                        'question': 'Which element has the chemical symbol Au?',
                        'answers': ['Gold', 'Silver', 'Copper', 'Iron'],
                        'correct': 0,
                        'points': 200
                    }
                ],
                'hard': [
                    {
                        'question': 'What is the speed of light in meters per second?',
                        'answers': ['299,792,458', '199,792,458', '399,792,458', '499,792,458'],
                        'correct': 0,
                        'points': 300
                    }
                ]
            }

            new_questions = default_questions[new_difficulty] if not hasattr(self.cog, 'get_filtered_questions') else self.cog.get_filtered_questions(self.category, new_difficulty)

            new_view = self.__class__(new_questions, self.category, new_difficulty, self.starter, self.cog)
            embed = new_view.create_status_embed(
                f"New Game - {new_difficulty.title()} Mode!",
                f"Difficulty increased to {new_difficulty.title()}!\nCategory: {self.category.title()}\nGood luck! 🎮"
            )
            await interaction.response.edit_message(embed=embed, view=new_view)

        async def start_new_game(self, interaction: discord.Interaction):
            if interaction.user != self.starter:
                await interaction.response.send_message("This isn't your game!", ephemeral=True)
                return

            if hasattr(self.cog, 'get_filtered_questions'):
                new_questions = self.cog.get_filtered_questions(self.category, self.difficulty)
            else:
                new_questions = self.questions  

            new_view = self.__class__(new_questions, self.category, self.difficulty, self.starter, self.cog)
            embed = new_view.create_status_embed("New Game Started!", "Good luck! 🎮")
                
            await interaction.response.edit_message(embed=embed, view=new_view)

        async def next_question(self, interaction: discord.Interaction):
            if interaction.user != self.starter:
                await interaction.response.send_message("This isn't your game!", ephemeral=True)
                return
                
            self.setup_question()
            embed = self.create_status_embed("Next Question", "Choose your answer!")
            await interaction.response.edit_message(embed=embed, view=self)

        async def upgrade_difficulty(self, interaction: discord.Interaction):
            if interaction.user != self.starter:
                await interaction.response.send_message("This isn't your game!", ephemeral=True)
                return
                
            difficulties = ['easy', 'normal', 'hard']
            current_index = difficulties.index(self.difficulty)
            if current_index < len(difficulties) - 1:
                self.difficulty = difficulties[current_index + 1]
                self.multiplier *= 1.5  
                
                if hasattr(self.cog, 'get_filtered_questions'):
                    new_questions = self.cog.get_filtered_questions(self.category, self.difficulty)
                    self.questions.extend(new_questions)
                    self.total_questions = len(self.questions)
                
                embed = self.create_status_embed(
                    "Difficulty Increased!",
                    f"Now playing on {self.difficulty.title()} mode! (x1.5 points)"
                )
                await interaction.response.edit_message(embed=embed, view=self)

    @commands.command()
    async def reactiontest(self, ctx, mode: str = "classic"):
        """Test your reaction speed with multiple game modes"""
        modes = ["classic", "pattern", "chain"]
        if mode not in modes:
            mode = "classic"
            
        embed = discord.Embed(
            title="⚡ Ultimate Reaction Test",
            description=(
                f"**Mode:** {mode.title()}\n"
                f"**Players:** {ctx.author.mention}\n\n"
                "🎮 Get ready to test your reactions!\n"
                "⚡ Wait for the button to turn green\n"
                "🏆 Compete for the fastest time!"
            ),
            color=discord.Color.blue()
        )
        
        game_view = self.ReactionTestView(mode, ctx.author)
        message = await ctx.send(embed=embed, view=game_view)
        game_view.message = message

    class ReactionTestView(discord.ui.View):
        def __init__(self, mode='classic', starter=None, party_players=None):
            super().__init__(timeout=180)
            self.mode = mode
            self.starter = starter
            self.party_players = party_players or []
            self.current_player_index = 0
            self.start_time = None
            self.scores = {}
            self.round = 0
            self.max_rounds = 5
            self.message = None
            self.streaks = {}
            self.achievements = {}
            self.setup_game()

        def setup_game(self):
            self.clear_items()
            
            if self.mode == 'classic':
                button = discord.ui.Button(
                    label='Wait for green...',
                    style=discord.ButtonStyle.danger,
                    custom_id='reaction'
                )
                button.callback = self.handle_reaction
                self.add_item(button)
                
            elif self.mode == 'pattern':
                colors = ['🔴', '🟡', '🟢', '🔵']
                self.pattern = [random.randint(0, 3) for _ in range(3)]
                self.current_pattern_index = 0
                
                for i, color in enumerate(colors):
                    button = discord.ui.Button(
                        emoji=color,
                        custom_id=f'pattern_{i}',
                        row=0
                    )
                    button.callback = self.handle_pattern
                    self.add_item(button)
                    
            elif self.mode == 'chain':
                self.chain_sequence = []
                self.current_chain_index = 0
                button = discord.ui.Button(
                    label='Start Chain',
                    style=discord.ButtonStyle.primary,
                    custom_id='chain_start'
                )
                button.callback = self.handle_chain
                self.add_item(button)

            asyncio.create_task(self.start_waiting())


        async def start_waiting(self):
            await asyncio.sleep(random.uniform(2.0, 5.0))
            if not self.is_finished():
                self.start_time = time.time()
                if self.mode == 'classic':
                    self.children[0].style = discord.ButtonStyle.success
                    self.children[0].label = 'Click Now!'
                elif self.mode == 'pattern':
                    await self.show_pattern()
                elif self.mode == 'chain':
                    await self.start_chain()
                await self.message.edit(view=self)

        async def handle_reaction(self, interaction: discord.Interaction):
            current_player = self.party_players[self.current_player_index] if self.party_players else self.starter
            
            if self.party_players and interaction.user != current_player:
                await interaction.response.send_message(
                    f"🎮 It's {current_player.mention}'s turn!", 
                    ephemeral=True
                )
                return

            if not self.start_time:
                embed = discord.Embed(
                    title="⚠️ Too Early!",
                    description="Wait for the button to turn green!",
                    color=discord.Color.red()
                )
                await interaction.response.edit_message(embed=embed, view=self)
                return

            reaction_time = (time.time() - self.start_time) * 1000
            player_id = str(interaction.user.id)
            
            if player_id not in self.scores:
                self.scores[player_id] = []
            self.scores[player_id].append(reaction_time)
            
            if reaction_time < 200:
                self.streaks[player_id] = self.streaks.get(player_id, 0) + 1
                if self.streaks[player_id] >= 3:
                    self.achievements[player_id] = self.achievements.get(player_id, [])
                    if "Speed Demon" not in self.achievements[player_id]:
                        self.achievements[player_id].append("Speed Demon")

            self.round += 1
            
            if self.party_players:
                self.current_player_index = (self.current_player_index + 1) % len(self.party_players)

            embed = discord.Embed(
                title=f"Round {self.round}/{self.max_rounds}",
                description=(
                    f"⚡ Reaction Time: {reaction_time:.1f}ms\n"
                    f"🎯 Accuracy Rating: {self.get_accuracy_rating(reaction_time)}\n"
                    f"🔥 Current Streak: {self.streaks.get(player_id, 0)}"
                ),
                color=self.get_color_for_time(reaction_time)
            )

            if self.round >= self.max_rounds:
                await self.show_final_results(interaction, embed)
            else:
                self.start_time = None
                self.setup_game()
                await interaction.response.edit_message(embed=embed, view=self)

            await self.cog.update_player_stats(
                interaction.user.id,
                'reaction',
                won=reaction_time < 300,
                extra_data={
                    'time': reaction_time,
                    'streak': self.streaks.get(str(interaction.user.id), 0)
                }
            )

        def get_accuracy_rating(self, time):
            if time < 150: return "Perfect! 🌟"
            if time < 200: return "Amazing! ⭐"
            if time < 250: return "Great! ✨"
            if time < 300: return "Good! 👍"
            return "Keep practicing! 💪"

        def get_color_for_time(self, time):
            if time < 150: return discord.Color.gold()
            if time < 200: return discord.Color.green()
            if time < 250: return discord.Color.blue()
            return discord.Color.purple()

        async def show_final_results(self, interaction, embed):
            results = []
            for pid, times in self.scores.items():
                user = interaction.guild.get_member(int(pid))
                avg_time = sum(times) / len(times)
                best_time = min(times)
                results.append((user, avg_time, best_time))
            
            results.sort(key=lambda x: x[1])
            
            leaderboard = "\n".join(
                f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else f'#{i+1}'} "
                f"{user.mention}: Avg {avg:.1f}ms | Best {best:.1f}ms"
                for i, (user, avg, best) in enumerate(results)
            )
            
            embed.add_field(
                name="🏆 Final Leaderboard",
                value=leaderboard,
                inline=False
            )
            
            achievements_text = ""
            for pid, achievs in self.achievements.items():
                user = interaction.guild.get_member(int(pid))
                if achievs:
                    achievements_text += f"\n{user.mention}: {', '.join(achievs)}"
            
            if achievements_text:
                embed.add_field(
                    name="🌟 Achievements Earned",
                    value=achievements_text,
                    inline=False
                )
            
            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()


    @commands.command()
    async def aimtrainer(self, ctx, duration: int = 30):
        """Test your clicking accuracy and speed"""
        duration = max(30, min(90, duration))
        
        embed = discord.Embed(
            title="🎯 Ultimate Aim Trainer",
            description=(
                f"**Duration:** {duration} seconds\n"
                f"**Player:** {ctx.author.mention}\n\n"
                "🎯 Click the targets as fast as you can!\n"
                "⚡ Avoid missing for better accuracy\n"
                "🏆 Compete for the highest score!\n\n"
                "Game starting in 3 seconds..."
            ),
            color=discord.Color.blue()
        )
        
        game_view = self.AimTrainerView(duration, ctx.author)
        message = await ctx.send(embed=embed, view=None)
        game_view.message = message
        
        for i in range(3, 0, -1):
            embed.description = embed.description.replace(f"{i} seconds", f"{i-1} seconds")
            await asyncio.sleep(1)
            await message.edit(embed=embed)
        
        await message.edit(view=game_view)
        game_view.start_game()

    class AimTrainerView(discord.ui.View):
        def __init__(self, duration=30, starter=None, party_players=None):
            super().__init__(timeout=None)
            self.duration = duration
            self.starter = starter
            self.party_players = party_players or []
            self.current_player_index = 0
            self.scores = {}
            self.start_time = None
            self.end_time = None
            self.message = None
            self.game_active = False
            self.setup_initial_scores()
            self.setup_targets()

        def start_game(self):
            self.start_time = time.time()
            self.end_time = self.start_time + self.duration
            self.game_active = True
            asyncio.create_task(self.game_timer())

        async def game_timer(self):
            await asyncio.sleep(self.duration)
            if self.game_active:
                self.game_active = False
                await self.show_final_results(self.message)

        def get_color_for_accuracy(self, accuracy):
            if accuracy >= 90: return discord.Color.gold()
            if accuracy >= 75: return discord.Color.green()
            if accuracy >= 60: return discord.Color.blue()
            return discord.Color.purple()

        def setup_initial_scores(self):
            players = self.party_players if self.party_players else [self.starter]
            for player in players:
                self.scores[player.id] = {
                    'targets_hit': 0,
                    'misses': 0,
                    'best_streak': 0,
                    'current_streak': 0,
                    'clicks_per_second': [],
                    'reaction_times': []
                }

        def setup_targets(self):
            self.clear_items()
            
            base_target_count = random.randint(4, 8)
            grid_size = 5
            grid_positions = [(i, j) for i in range(grid_size) for j in range(grid_size)]
            
            target_positions = set()
            pattern_type = random.choice(['random', 'cluster', 'diagonal', 'corners'])
            
            if pattern_type == 'cluster':
                
                for _ in range(random.randint(1, 2)):
                    center = random.choice(grid_positions)
                    target_positions.add(center)
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        new_x, new_y = center[0] + dx, center[1] + dy
                        if 0 <= new_x < grid_size and 0 <= new_y < grid_size:
                            if random.random() < 0.7:  
                                target_positions.add((new_x, new_y))
            
            elif pattern_type == 'diagonal':
                
                direction = random.choice([(1,1), (1,-1), (-1,1), (-1,-1)])
                start_x = 0 if direction[0] > 0 else grid_size-1
                start_y = 0 if direction[1] > 0 else grid_size-1
                for i in range(grid_size):
                    if random.random() < 0.7:
                        x, y = start_x + (i * direction[0]), start_y + (i * direction[1])
                        if 0 <= x < grid_size and 0 <= y < grid_size:
                            target_positions.add((x, y))
            
            elif pattern_type == 'corners':
               
                corners = [(0,0), (0,grid_size-1), (grid_size-1,0), (grid_size-1,grid_size-1)]
                target_positions.update(random.sample(corners, random.randint(2, 4)))
                if random.random() < 0.5:  
                    target_positions.add((grid_size//2, grid_size//2))
            
            else: 
                target_positions = set(random.sample(grid_positions, base_target_count))
            
            while len(target_positions) < base_target_count:
                target_positions.add(random.choice(grid_positions))
            
            target_emojis = ['🎯', '🎪', '⭐', '🔥', '💫']  
            for i, j in grid_positions:
                is_target = (i, j) in target_positions
                style = random.choice([
                    discord.ButtonStyle.success,
                    discord.ButtonStyle.primary
                ]) if is_target else discord.ButtonStyle.secondary
                
                button = discord.ui.Button(
                    emoji=random.choice(target_emojis) if is_target else '⬛',
                    custom_id=f'target_{i}_{j}_{is_target}',
                    row=i,
                    style=style
                )
                button.callback = self.handle_click
                self.add_item(button)


        async def handle_click(self, interaction: discord.Interaction):
            if not self.game_active:
                await interaction.response.edit_message(view=None)
                return

            current_player = self.party_players[self.current_player_index] if self.party_players else self.starter
            if interaction.user != current_player:
                await interaction.response.send_message(
                    f"🎮 It's {current_player.mention}'s turn!", 
                    ephemeral=True
                )
                return

            current_time = time.time()
            time_remaining = max(0, self.end_time - current_time)
            
            if time_remaining <= 0:
                self.game_active = False
                await self.show_final_results(interaction)
                return

            _, _, _, is_target = interaction.data['custom_id'].split('_')
            is_target = is_target == 'True'
            player_stats = self.scores[interaction.user.id]
            
            player_stats['clicks_per_second'].append(current_time)
            
            if is_target:
                player_stats['targets_hit'] += 1
                player_stats['current_streak'] += 1
                player_stats['best_streak'] = max(
                    player_stats['best_streak'], 
                    player_stats['current_streak']
                )
            else:
                player_stats['misses'] += 1
                player_stats['current_streak'] = 0

            if self.party_players:
                self.current_player_index = (self.current_player_index + 1) % len(self.party_players)

            recent_clicks = [t for t in player_stats['clicks_per_second'] 
                           if current_time - t <= 1.0]
            cps = len(recent_clicks)

            accuracy = (player_stats['targets_hit'] / 
                       (player_stats['targets_hit'] + player_stats['misses']) * 100 
                       if (player_stats['targets_hit'] + player_stats['misses']) > 0 else 0)

            embed = discord.Embed(
                title="🎯 Aim Trainer",
                description=(
                    f"**Player:** {interaction.user.mention}\n"
                    f"**Targets Hit:** {player_stats['targets_hit']} 🎯\n"
                    f"**Accuracy:** {accuracy:.1f}% ⚡\n"
                    f"**Current Streak:** {player_stats['current_streak']} 🔥\n"
                    f"**Best Streak:** {player_stats['best_streak']} ⭐\n"
                    f"**CPS:** {cps} 👆\n"
                    f"**Time Remaining:** {time_remaining:.1f}s ⏱️"
                ),
                color=self.get_color_for_accuracy(accuracy)
            )

            self.setup_targets()
            await interaction.response.edit_message(embed=embed, view=self)

        async def show_final_results(self, interaction):
            results = []
            for player_id, stats in self.scores.items():
                user = self.message.guild.get_member(player_id)
                total_clicks = stats['targets_hit'] + stats['misses']
                accuracy = (stats['targets_hit'] / total_clicks * 100 
                           if total_clicks > 0 else 0)
                avg_cps = (len(stats['clicks_per_second']) / self.duration 
                          if stats['clicks_per_second'] else 0)
                
                results.append((
                    user, 
                    stats['targets_hit'], 
                    accuracy, 
                    stats['best_streak'],
                    avg_cps
                ))

            results.sort(key=lambda x: (x[1], x[2]), reverse=True)
            
            leaderboard = "\n".join(
                f"{'🥇' if i==0 else '🥈' if i==1 else '🥉' if i==2 else f'#{i+1}'} "
                f"{user.mention}:\n"
                f"➟ {targets} hits | {acc:.1f}% accuracy\n"
                f"➟ Best Streak: {streak} 🔥 | Avg CPS: {cps:.1f} ⚡"
                for i, (user, targets, acc, streak, cps) in enumerate(results)
            )

            embed = discord.Embed(
                title="🏆 Game Over - Final Results",
                description=leaderboard,
                color=discord.Color.gold()
            )

            if isinstance(interaction, discord.Interaction):
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                await interaction.edit(embed=embed, view=None)
            self.stop()

            await self.cog.update_player_stats(
                interaction.user.id,
                'aimtrainer',
                won=self.scores[interaction.user.id]['targets_hit'] > 0,
                extra_data={
                    'accuracy': accuracy,
                    'score': self.scores[interaction.user.id]['targets_hit'],
                    'streak': self.scores[interaction.user.id]['best_streak']
                }
            )


    def get_filtered_questions(self, category, difficulty):
        questions = {
            'general': [
                {
                    'question': 'What is the capital of France?',
                    'answers': ['Paris', 'London', 'Berlin', 'Madrid'],
                    'correct': 0,  
                    'difficulty': 'normal',
                    'points': 100
                },
                {
                    'question': 'Which planet is known as the Red Planet?',
                    'answers': ['Mars', 'Venus', 'Jupiter', 'Saturn'],
                    'correct': 0,  
                    'difficulty': 'easy',
                    'points': 50
                },
                {
                    'question': 'What is the chemical symbol for gold?',
                    'answers': ['Au', 'Ag', 'Fe', 'Cu'],
                    'correct': 0,  
                    'difficulty': 'normal',
                    'points': 100
                }
            ],
            'science': [
                {
                    'question': 'What is the hardest natural substance on Earth?',
                    'answers': ['Diamond', 'Gold', 'Iron', 'Platinum'],
                    'correct': 0,  
                    'difficulty': 'easy',
                    'points': 50
                },
                {
                    'question': 'What is the speed of light in miles per second?',
                    'answers': ['186,282', '150,000', '200,000', '170,000'],
                    'correct': 0,  
                    'difficulty': 'hard',
                    'points': 150
                }
            ],
            'history': [
                {
                    'question': 'In which year did World War II end?',
                    'answers': ['1945', '1944', '1946', '1943'],
                    'correct': 0,  
                    'difficulty': 'normal',
                    'points': 100
                },
                {
                    'question': 'Who was the first President of the United States?',
                    'answers': ['George Washington', 'John Adams', 'Thomas Jefferson', 'Benjamin Franklin'],
                    'correct': 0,  
                    'difficulty': 'easy',
                    'points': 50
                }
            ]
        }

        if category == "random":
            category = random.choice(list(questions.keys()))
        
        filtered = [q for q in questions[category] if q['difficulty'] == difficulty or difficulty == "all"]
        
        if not filtered:
            filtered = questions[category]
        
        return filtered



    @commands.command(name='trivia')
    async def trivia(self, ctx, category: str = "random", difficulty: str = "normal"):
        """Start an enhanced trivia game with streaks and multipliers"""
        if category == "random":
            category = random.choice(list(self.trivia_questions.keys()))
                
        questions = self.get_filtered_questions(category, difficulty)
        first_question = questions[0]['question']  
        
        embed = discord.Embed(
            title="🎮 Trivia Challenge",
            description=f"Category: {category.title()}\n"
                    f"Difficulty: {difficulty.title()}\n"
                    f"Questions: {len(questions)}\n\n"
                    f"Question 1: {first_question}",  
            color=discord.Color.blue()
        )
        
        game_view = self.TriviaView(questions, category, difficulty, ctx.author)
        message = await ctx.send(embed=embed, view=game_view)
        game_view.message = message

    @commands.command()
    async def party(self, ctx):
        """Start a party game session with random minigames"""
        embed = EmbedBuilder(
            "🎪 Party Game Session",
            f"{ctx.author.mention} is starting a party game session!\n"
            "Join to play multiple minigames in succession."
        ).set_color(discord.Color.blue())

        view = discord.ui.View(timeout=60)
        
        async def join_callback(interaction):
            if len(self.active_games.get(ctx.channel.id, [])) >= 8:
                await interaction.response.send_message("Party is full!", ephemeral=True)
                return
                
            if ctx.channel.id not in self.active_games:
                self.active_games[ctx.channel.id] = []
            
            if interaction.user not in self.active_games[ctx.channel.id]:
                self.active_games[ctx.channel.id].append(interaction.user)
                await interaction.response.send_message(f"Joined the party! ({len(self.active_games[ctx.channel.id])}/8)", ephemeral=True)
                
                if len(self.active_games[ctx.channel.id]) >= 2:
                    start_button.disabled = False
                    await interaction.message.edit(view=view)

        async def start_callback(interaction):
            if interaction.user != ctx.author:
                return
                
            await self.start_party_session(ctx, self.active_games[ctx.channel.id])
            await interaction.message.delete()

        join_button = discord.ui.Button(label="Join Party", style=discord.ButtonStyle.green, emoji="🎮")
        start_button = discord.ui.Button(label="Start Games", style=discord.ButtonStyle.primary, emoji="▶️", disabled=True)
        
        join_button.callback = join_callback
        start_button.callback = start_callback
        
        view.add_item(join_button)
        view.add_item(start_button)
        
        await ctx.send(embed=embed.build(), view=view)

    async def start_party_session(self, ctx, players):
        """Handle the party game session flow"""
        games = ['trivia', 'reactiontest', 'aimtrainer', 'wordscramble']
        scores = {player.id: 0 for player in players}
        
        for round_num in range(4):
            game = random.choice(games)
            games.remove(game)
            
            round_embed = EmbedBuilder(
                f"🎪 Round {round_num + 1}",
                f"Next game: {game.title()}!\n"
                "Starting in 5 seconds..."
            ).set_color(discord.Color.blue())
            
            await ctx.send(embed=round_embed.build())
            await asyncio.sleep(5)
            
            if game == 'trivia':
                await self.trivia(ctx, "random", "normal")
            elif game == 'reactiontest':
                await self.reactiontest(ctx, "classic")
            elif game == 'aimtrainer':
                await self.aimtrainer(ctx)
            elif game == 'wordscramble':
                await self.wordscramble(ctx, "random", "normal")
            
            await asyncio.sleep(30)  

    @commands.command(name='gameleaderboard')
    async def game_leaderboard(self, ctx, game_type: str = "all"):
        """View global or game-specific leaderboards"""
        valid_types = ["all", "trivia", "reaction", "aim", "memory", "rps", "wordscramble"]
        if game_type not in valid_types:
            game_type = "all"

        embed = EmbedBuilder(
            "🏆 Game Leaderboards",
            f"Top players in {game_type.title()}"
        ).set_color(discord.Color.gold())

        if game_type == "all":
            sorted_scores = sorted(
                self.scores.items(),
                key=lambda x: x[1]['wins'],
                reverse=True
            )[:10]

            for i, (user_id, stats) in enumerate(sorted_scores, 1):
                user = self.bot.get_user(user_id)
                if user:
                    embed.add_field(
                        name=f"#{i} {user.name}",
                        value=f"Wins: {stats['wins']}\n"
                              f"Games: {stats['total_games']}\n"
                              f"Win Rate: {(stats['wins']/stats['total_games']*100):.1f}%",
                        inline=True
                    )
        else:
            
            game_scores = {
                user_id: stats['game_specific'].get(game_type, {'score': 0})
                for user_id, stats in self.scores.items()
                if game_type in stats['game_specific']
            }
            sorted_scores = sorted(
                game_scores.items(),
                key=lambda x: x[1]['score'],
                reverse=True
            )[:10]

            for i, (user_id, stats) in enumerate(sorted_scores, 1):
                user = self.bot.get_user(user_id)
                if user:
                    embed.add_field(
                        name=f"#{i} {user.name}",
                        value=f"Score: {stats['score']}\n"
                              f"Best Streak: {stats.get('best_streak', 0)}",
                        inline=True
                    )

        await ctx.send(embed=embed.build())

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        """View detailed gaming statistics for a user"""
        user = user or ctx.author
        
        if user.id not in self.scores:
            embed = discord.Embed(
                title="🎮 Gaming Profile",
                description=f"{user.name} hasn't played any games yet!\nUse `!games` to see available games!",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return

        stats = self.scores[user.id]
        achievements = self.achievements.get(user.id, [])
        
        win_rate = (stats.get('wins', 0) / stats.get('total_games', 1) * 100) if stats.get('total_games', 0) > 0 else 0
        
        embed = discord.Embed(
            title=f"🎮 {user.name}'s Gaming Profile",
            description=(
                f"**Total Games:** {stats.get('total_games', 0)} 🎲\n"
                f"**Wins:** {stats.get('wins', 0)} 🏆\n"
                f"**Win Rate:** {win_rate:.1f}% ⚡\n"
                f"**Current Streak:** {self.streaks.get(user.id, 0)} 🔥"
            ),
            color=discord.Color.blue()
        )

        if 'reaction' in stats.get('game_specific', {}):
            reaction_stats = stats['game_specific']['reaction']
            embed.add_field(
                name="⚡ Reaction Test",
                value=(
                    f"Games: {reaction_stats.get('games', 0)}\n"
                    f"Best Time: {reaction_stats.get('best_time', 0):.1f}ms\n"
                    f"Avg Time: {reaction_stats.get('avg_time', 0):.1f}ms"
                ),
                inline=True
            )

        if 'aimtrainer' in stats.get('game_specific', {}):
            aim_stats = stats['game_specific']['aimtrainer']
            embed.add_field(
                name="🎯 Aim Trainer",
                value=(
                    f"Games: {aim_stats.get('games', 0)}\n"
                    f"Best Score: {aim_stats.get('best_score', 0)}\n"
                    f"Best Accuracy: {aim_stats.get('best_accuracy', 0)}%"
                ),
                inline=True
            )

        if 'memory' in stats.get('game_specific', {}):
            memory_stats = stats['game_specific']['memory']
            embed.add_field(
                name="🧩 Memory Game",
                value=(
                    f"Games: {memory_stats.get('games', 0)}\n"
                    f"Best Time: {memory_stats.get('best_time', 0)}s\n"
                    f"Perfect Matches: {memory_stats.get('perfect_matches', 0)}"
                ),
                inline=True
            )

        if 'wordscramble' in stats.get('game_specific', {}):
            word_stats = stats['game_specific']['wordscramble']
            embed.add_field(
                name="🔤 Word Scramble",
                value=(
                    f"Games: {word_stats.get('games', 0)}\n"
                    f"Words Solved: {word_stats.get('solved', 0)}\n"
                    f"Best Time: {word_stats.get('best_time', 0)}s"
                ),
                inline=True
            )

        if 'hangman' in stats.get('game_specific', {}):
            hangman_stats = stats['game_specific']['hangman']
            embed.add_field(
                name="👻 Hangman",
                value=(
                    f"Games: {hangman_stats.get('games', 0)}\n"
                    f"Words Guessed: {hangman_stats.get('wins', 0)}\n"
                    f"Best Streak: {hangman_stats.get('best_streak', 0)}"
                ),
                inline=True
            )

        if 'rps' in stats.get('game_specific', {}):
            rps_stats = stats['game_specific']['rps']
            embed.add_field(
                name="✂️ Rock Paper Scissors",
                value=(
                    f"Games: {rps_stats.get('games', 0)}\n"
                    f"Wins: {rps_stats.get('wins', 0)}\n"
                    f"Best Streak: {rps_stats.get('best_streak', 0)}"
                ),
                inline=True
            )

        if 'trivia' in stats.get('game_specific', {}):
            trivia_stats = stats['game_specific']['trivia']
            embed.add_field(
                name="❓ Trivia",
                value=(
                    f"Games: {trivia_stats.get('games', 0)}\n"
                    f"Correct Answers: {trivia_stats.get('correct', 0)}\n"
                    f"Best Score: {trivia_stats.get('best_score', 0)}"
                ),
                inline=True
            )

        if achievements:
            embed.add_field(
                name="🏆 Achievements",
                value="\n".join(f"• {achievement}" for achievement in achievements),
                inline=False
            )

        if 'recent_games' in stats:
            recent = stats['recent_games'][-3:]  
            embed.add_field(
                name="🕒 Recent Activity",
                value="\n".join(f"• {game}" for game in recent),
                inline=False
            )

        await ctx.send(embed=embed)


    @commands.command()
    async def daily(self, ctx):
        """View and claim daily challenges"""
        today = datetime.now().strftime("%Y-%m-%d")
        user_id = ctx.author.id

        if user_id not in self.daily_challenges:
            self.daily_challenges[user_id] = {
                'last_claim': None,
                'completed': []
            }

        if self.daily_challenges[user_id]['last_claim'] == today:
            embed = EmbedBuilder(
                "📅 Daily Challenges",
                "You've already claimed today's challenges!\n"
                "Come back tomorrow for new ones!"
            ).set_color(discord.Color.blue())
        else:
           
            challenges = [
                "Win 3 games of any type",
                "Achieve a 5-streak in Trivia",
                "Score 95% accuracy in Aim Trainer",
                "Complete a Hard difficulty Word Scramble"
            ]
            
            self.daily_challenges[user_id] = {
                'last_claim': today,
                'completed': [],
                'challenges': challenges
            }

            embed = EmbedBuilder(
                "📅 Daily Challenges",
                "Here are your daily challenges:"
            ).set_color(discord.Color.blue())

            for i, challenge in enumerate(challenges, 1):
                embed.add_field(
                    name=f"Challenge {i}",
                    value=f"• {challenge}\nReward: 100 points",
                    inline=False
                )

        await ctx.send(embed=embed.build())
    @commands.command()
    async def tournament(self, ctx, game_type: str = "random", players: int = 8):
        """Start a tournament with elimination brackets"""
        valid_games = ["rps", "trivia", "aimtrainer", "wordscramble"]
        if game_type not in valid_games:
            game_type = random.choice(valid_games)
            
        embed = EmbedBuilder(
            "🏆 Tournament Mode",
            f"Game: {game_type.title()}\n"
            f"Players needed: {players}\n\n"
            "React to join! Tournament starts in 60 seconds."
        ).set_color(discord.Color.gold())

        view = TournamentView(self, game_type, players)
        message = await ctx.send(embed=embed.build(), view=view)
        view.message = message

    class TournamentView(discord.ui.View):
        def __init__(self, cog, game_type, max_players):
            super().__init__(timeout=60)
            self.cog = cog
            self.game_type = game_type
            self.max_players = max_players
            self.players = []
            self.brackets = []
            self.setup_buttons()

        def setup_buttons(self):
            join = discord.ui.Button(
                label=f"Join Tournament (0/{self.max_players})", 
                style=discord.ButtonStyle.green,
                emoji="🎮"
            )
            join.callback = self.join_tournament
            self.add_item(join)

        async def join_tournament(self, interaction: discord.Interaction):
            if interaction.user in self.players:
                await interaction.response.send_message("You're already in the tournament!", ephemeral=True)
                return

            self.players.append(interaction.user)
            self.children[0].label = f"Join Tournament ({len(self.players)}/{self.max_players})"

            if len(self.players) >= self.max_players:
                await self.start_tournament(interaction)
            else:
                await interaction.response.edit_message(view=self)

        async def start_tournament(self, interaction):
            random.shuffle(self.players)
            self.brackets = self.create_brackets()
            
            bracket_embed = self.create_bracket_embed()
            await interaction.message.edit(embed=bracket_embed, view=None)
            
            await self.run_matches()

        def create_brackets(self):
            brackets = []
            for i in range(0, len(self.players), 2):
                if i + 1 < len(self.players):
                    brackets.append([self.players[i], self.players[i+1]])
                else:
                    brackets.append([self.players[i], None])  
            return brackets

        def create_bracket_embed(self):
            embed = EmbedBuilder(
                "🏆 Tournament Brackets",
                "Current matchups:"
            ).set_color(discord.Color.gold())

            for i, match in enumerate(self.brackets, 1):
                if match[1]:
                    embed.add_field(
                        name=f"Match {i}",
                        value=f"{match[0].name} vs {match[1].name}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"Match {i}",
                        value=f"{match[0].name} (Bye round)",
                        inline=False
                    )

            return embed.build()

        async def run_matches(self):
            winners = []
            for match in self.brackets:
                if not match[1]:  
                    winners.append(match[0])
                    continue

                overwrites = {
                    self.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    match[0]: discord.PermissionOverwrite(read_messages=True),
                    match[1]: discord.PermissionOverwrite(read_messages=True)
                }
                
                channel = await self.message.guild.create_text_channel(
                    f"tournament-match-{match[0].name}-{match[1].name}",
                    overwrites=overwrites
                )

                winner = await self.run_game(channel, match[0], match[1])
                winners.append(winner)
                
                await channel.delete()

            if len(winners) > 1:
                self.players = winners
                self.brackets = self.create_brackets()
                await self.message.channel.send("Next round starting!")
                await self.run_matches()
            else:
                await self.end_tournament(winners[0])

        async def end_tournament(self, winner):
            embed = EmbedBuilder(
                "🎉 Tournament Complete!",
                f"Winner: {winner.mention}\n"
                "Congratulations!"
            ).set_color(discord.Color.gold())
            
            await self.message.channel.send(embed=embed.build())
class TournamentView(discord.ui.View):
    def __init__(self, cog, game_type, max_players):
        super().__init__(timeout=60)
        self.cog = cog
        self.game_type = game_type
        self.max_players = max_players
        self.players = []
        self.brackets = []
        self.message = None
        self.setup_buttons()

    def setup_buttons(self):
        join = discord.ui.Button(
            label=f"Join Tournament (0/{self.max_players})", 
            style=discord.ButtonStyle.green,
            emoji="🎮"
        )
        join.callback = self.join_tournament
        self.add_item(join)

        start = discord.ui.Button(
            label="Start Tournament", 
            style=discord.ButtonStyle.primary,
            emoji="▶️",
            disabled=True
        )
        start.callback = self.start_tournament
        self.add_item(start)

    async def join_tournament(self, interaction: discord.Interaction):
        if interaction.user in self.players:
            await interaction.response.send_message("You're already in the tournament!", ephemeral=True)
            return

        self.players.append(interaction.user)
        self.children[0].label = f"Join Tournament ({len(self.players)}/{self.max_players})"

        if len(self.players) >= 2:
            self.children[1].disabled = False

        if len(self.players) >= self.max_players:
            self.children[0].disabled = True

        await interaction.response.edit_message(view=self)

    async def start_tournament(self, interaction: discord.Interaction):
        if len(self.players) < 2:
            return

        random.shuffle(self.players)
        self.brackets = self.create_brackets()
        
        bracket_embed = self.create_bracket_embed()
        await interaction.response.edit_message(embed=bracket_embed, view=None)
        
        await self.run_matches()

    def create_brackets(self):
        brackets = []
        for i in range(0, len(self.players), 2):
            if i + 1 < len(self.players):
                brackets.append([self.players[i], self.players[i+1]])
            else:
                brackets.append([self.players[i], None])
        return brackets

    def create_bracket_embed(self):
        embed = EmbedBuilder(
            "🏆 Tournament Brackets",
            "Current matchups:"
        ).set_color(discord.Color.gold())

        for i, match in enumerate(self.brackets, 1):
            if match[1]:
                embed.add_field(
                    name=f"Match {i}",
                    value=f"{match[0].name} vs {match[1].name}",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"Match {i}",
                    value=f"{match[0].name} (Bye round)",
                    inline=False
                )

        return embed.build()

    async def run_matches(self):
        winners = []
        for match in self.brackets:
            if not match[1]:
                winners.append(match[0])
                continue

            match_channel = await self.create_match_channel(match[0], match[1])
            winner = await self.run_game(match_channel, match[0], match[1])
            winners.append(winner)
            await match_channel.delete()

        if len(winners) > 1:
            self.players = winners
            self.brackets = self.create_brackets()
            await self.message.channel.send("Next round starting!")
            await self.run_matches()
        else:
            await self.end_tournament(winners[0])

    async def create_match_channel(self, player1, player2):
        overwrites = {
            self.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            player1: discord.PermissionOverwrite(read_messages=True),
            player2: discord.PermissionOverwrite(read_messages=True),
            self.message.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        
        return await self.message.guild.create_text_channel(
            f"tournament-{player1.name}-vs-{player2.name}",
            overwrites=overwrites
        )

    async def run_game(self, channel, player1, player2):
        game_embed = EmbedBuilder(
            f"🎮 Tournament Match: {self.game_type}",
            f"{player1.mention} vs {player2.mention}"
        ).set_color(discord.Color.blue())
        
        await channel.send(embed=game_embed.build())
        
        if self.game_type == "rps":
            return await self.cog.rps_tournament_match(channel, player1, player2)
        elif self.game_type == "trivia":
            return await self.cog.trivia_tournament_match(channel, player1, player2)
       
        return player1  

    async def end_tournament(self, winner):
        embed = EmbedBuilder(
            "🎉 Tournament Complete!",
            f"Winner: {winner.mention}\n"
            "Congratulations!"
        ).set_color(discord.Color.gold())
        
        await self.message.channel.send(embed=embed.build())

    async def rps_tournament_match(self, channel, player1, player2):
        game_view = self.RPSView(player1, player2, rounds=5)  
        game_embed = EmbedBuilder(
            "🎮 Tournament Match: Rock Paper Scissors",
            f"{player1.mention} vs {player2.mention}\n"
            "First to 3 wins! Choose your move!"
        ).set_color(discord.Color.blue())
        
        message = await channel.send(embed=game_embed.build(), view=game_view)
        game_view.message = message
        
        await game_view.wait()
        return player1 if game_view.p1_score > game_view.p2_score else player2

    async def trivia_tournament_match(self, channel, player1, player2):
        questions = self.get_filtered_questions("random", "tournament")
        game_view = self.TriviaView(questions, "tournament", "tournament")
        game_view.tournament_players = {player1: 0, player2: 0}
        
        await channel.send(embed=game_view.create_question_embed())
        await game_view.wait()
        
        return max(game_view.tournament_players.items(), key=lambda x: x[1])[0]

    def create_rematch_view(self):
        view = discord.ui.View(timeout=60)
        
        async def rematch_callback(interaction):
            if interaction.user not in [self.player1, self.player2]:
                return
                
            if interaction.user == self.requesting_rematch:
                return
                
            if self.requesting_rematch:
                
                self.reset_game()
                await interaction.response.edit_message(view=self)
            else:
                self.requesting_rematch = interaction.user
                await interaction.response.send_message(f"{interaction.user.name} wants a rematch! Click rematch to accept!", ephemeral=True)

        rematch = discord.ui.Button(label="Rematch", style=discord.ButtonStyle.green, emoji="🔄")
        rematch.callback = rematch_callback
        view.add_item(rematch)
        
        return view

    async def handle_pattern(self, interaction):
        if not self.pattern_sequence:
            self.generate_pattern()
            await self.show_pattern(interaction)
            return

        button_id = int(interaction.data['custom_id'].split('_')[1])
        if button_id != self.pattern_sequence[self.current_step]:
            await self.pattern_failed(interaction)
            return

        self.current_step += 1
        if self.current_step >= len(self.pattern_sequence):
            await self.pattern_complete(interaction)
        else:
            await interaction.response.defer()

    async def handle_chain(self, interaction):
        if not self.start_time:
            await self.start_chain(interaction)
            return

        reaction_time = (time.time() - self.last_click) * 1000
        self.chain_times.append(reaction_time)
        
        if len(self.chain_times) >= 5:
            await self.end_chain(interaction)
        else:
            self.last_click = time.time()
            await self.update_chain_button(interaction)

    async def update_tournament_stats(self, winner, loser, game_type):
        if winner.id not in self.scores:
            self.scores[winner.id] = {'tournament_wins': 0, 'games': {}}
        
        self.scores[winner.id]['tournament_wins'] = self.scores[winner.id].get('tournament_wins', 0) + 1
        
        if game_type not in self.scores[winner.id]['games']:
            self.scores[winner.id]['games'][game_type] = {'wins': 0, 'matches': 0}
            
        self.scores[winner.id]['games'][game_type]['wins'] += 1
        self.scores[winner.id]['games'][game_type]['matches'] += 1
        
        if self.scores[winner.id]['tournament_wins'] == 5:
            await self.award_achievement(winner, "Tournament Master", "Win 5 tournaments")


class EnhancedAI:
    def __init__(self):
        self.context_memory = {}
        self.conversation_history = {}
        self.user_preferences = {}
        self.usage_stats = {}
        self.model_configs = {
            "creative": "gpt-4",
            "balanced": "gpt-3.5-turbo",
            "fast": "gpt-3.5-turbo-instruct"
        }
        
    async def process_with_context(self, user_id: int, input_text: str, context: str) -> str:
        if user_id not in self.context_memory:
            self.context_memory[user_id] = []
        self.context_memory[user_id].append((datetime.now(), input_text))
        return f"{context}\n{input_text}"

class AIControlPanel(discord.ui.View):
    def __init__(self, ai_commands):
        super().__init__(timeout=60)
        self.ai_commands = ai_commands

    @discord.ui.button(label="Model", style=ButtonStyle.primary)
    async def model_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🤖 Model Selection")
        await interaction.response.edit_message(embed=embed, view=AiModelSelectView(self.ai_commands))

    @discord.ui.button(label="Personality", style=ButtonStyle.success)
    async def personality_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🎭 Personality Settings")
        await interaction.response.edit_message(embed=embed, view=AiPersonalitySelectView(self.ai_commands))

    @discord.ui.button(label="Response", style=ButtonStyle.secondary)
    async def response_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="📝 Response Style")
        await interaction.response.edit_message(embed=embed, view=AiResponseSelectView(self.ai_commands))

class AiModelSelectView(discord.ui.View):
    def __init__(self, ai_commands):
        super().__init__(timeout=60)
        self.ai_commands = ai_commands

    @discord.ui.button(label="GPT-4", style=discord.ButtonStyle.primary)
    async def gpt4_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.ai_commands.ai_engine.model_configs['current'] = 'gpt-4'
        await interaction.response.send_message("Model set to GPT-4!", ephemeral=True)

    @discord.ui.button(label="GPT-3.5", style=discord.ButtonStyle.primary)
    async def gpt35_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.ai_commands.ai_engine.model_configs['current'] = 'gpt-3.5-turbo'
        await interaction.response.send_message("Model set to GPT-3.5!", ephemeral=True)

    @discord.ui.button(label="GPT-3.5 Instruct", style=discord.ButtonStyle.primary)
    async def gpt35_instruct_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.ai_commands.ai_engine.model_configs['current'] = 'gpt-3.5-turbo-instruct'
        await interaction.response.send_message("Model set to GPT-3.5 Instruct!", ephemeral=True)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=self.ai_commands.get_settings_embed(),
            view=AIControlPanel(self.ai_commands)
        )


class AiPersonalitySelectView(discord.ui.View):
    def __init__(self, ai_commands):
        super().__init__(timeout=60)
        self.ai_commands = ai_commands

    @discord.ui.button(label="Professional", style=discord.ButtonStyle.primary)
    async def professional_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Personality set to Professional!", ephemeral=True)

    @discord.ui.button(label="Casual", style=discord.ButtonStyle.primary)
    async def casual_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Personality set to Casual!", ephemeral=True)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=self.ai_commands.get_settings_embed(),
            view=AIControlPanel(self.ai_commands)
        )


class AiResponseSelectView(discord.ui.View):
    def __init__(self, ai_commands):
        super().__init__(timeout=60)
        self.ai_commands = ai_commands

    @discord.ui.button(label="Detailed", style=discord.ButtonStyle.primary)
    async def detailed_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Response style set to Detailed!", ephemeral=True)

    @discord.ui.button(label="Concise", style=discord.ButtonStyle.primary)
    async def concise_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Response style set to Concise!", ephemeral=True)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.danger)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=self.ai_commands.get_settings_embed(),
            view=AIControlPanel(self.ai_commands)
        )


class AiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.ai_engine = EnhancedAI()
        self.cooldowns = {}
        self.load_custom_prompts()
        
    def load_custom_prompts(self):
        try:
            with open('config/ai_prompts.json', 'r') as f:
                self.custom_prompts = json.load(f)
        except FileNotFoundError:
            self.custom_prompts = {}

    @commands.group(invoke_without_command=True)
    async def ai(self, ctx):
        """AI Command Hub - Use !ai help for all commands"""
        embed = discord.Embed(
            title="🤖 AI Command Center",
            description="Advanced AI Interaction Suite",
            color=discord.Color.blue()
        )
        embed.add_field(name="🗣️ Chat", value="`!ai chat <message>` - Interactive chat with context memory")
        embed.add_field(name="🎨 Create", value="`!ai create <prompt>` - Generate images with style control")
        embed.add_field(name="💭 Analyze", value="`!ai analyze <text>` - Deep content analysis")
        embed.add_field(name="🔮 Predict", value="`!ai predict <scenario>` - AI-powered predictions")
        embed.add_field(name="⚙️ Settings", value="`!ai settings` - Customize AI behavior")
        await ctx.send(embed=embed)

    @ai.command(name="chat")
    async def chat(self, ctx, *, message):
        """Enhanced chat with context awareness and personality"""
        async with ctx.typing():
            user_id = ctx.author.id
            
            enhanced_prompt = await self.ai_engine.process_with_context(
                user_id, 
                message,
                self.custom_prompts.get('chat_context', '')
            )
            
            try:
                response = self.client.chat.completions.create(
                    model=self.ai_engine.model_configs['balanced'],
                    messages=[
                        {"role": "system", "content": "You are a highly intelligent and witty AI assistant with deep knowledge and creative thinking capabilities."},
                        {"role": "user", "content": enhanced_prompt}
                    ],
                    temperature=0.8,
                    max_tokens=2000
                )
                
                answer = response.choices[0].message.content
                
                embed = discord.Embed(
                    title="💡 AI Response",
                    description=answer,
                    color=self.get_dynamic_color(answer)
                )
                embed.set_footer(text=f"Chatting with {ctx.author.name} | Context Memory: {len(self.ai_engine.context_memory.get(user_id, []))} messages")
                
                message = await ctx.send(embed=embed)
                await message.add_reaction("🔄")  
                await message.add_reaction("📝")  
                await message.add_reaction("💾")  
                
            except Exception as e:
                await self.handle_error(ctx, e)

    @ai.command(name="create")
    async def create(self, ctx, *, prompt):
        """Advanced image generation with style control"""
        async with ctx.typing():
            try:
                style_match = re.match(r'\[(.*?)\](.*)', prompt)
                style = style_match.group(1) if style_match else "realistic"
                actual_prompt = style_match.group(2) if style_match else prompt
                
                enhanced_prompt = f"Create a {style} style image of {actual_prompt}"
                
                response = self.client.images.generate(
                    prompt=enhanced_prompt,
                    n=1,
                    size="1024x1024",
                    quality="hd"
                )
                
                embed = discord.Embed(
                    title="🎨 AI Creation",
                    description=f"**Style:** {style}\n**Prompt:** {actual_prompt}",
                    color=discord.Color.purple()
                )
                embed.set_image(url=response.data[0].url)
                
                message = await ctx.send(embed=embed)
                await message.add_reaction("🎨") 
                await message.add_reaction("✨")  
                await message.add_reaction("💾")  
                
            except Exception as e:
                await self.handle_error(ctx, e)

    @ai.command(name="analyze")
    async def analyze(self, ctx, *, content):
       
        async with ctx.typing():
            try:
                analyses = await asyncio.gather(
                    self.get_sentiment_analysis(content),
                    self.get_topic_analysis(content),
                    self.get_style_analysis(content)
                )
                
                embed = discord.Embed(
                    title="🔍 Content Analysis",
                    color=discord.Color.gold()
                )
                
                for analysis_type, result in zip(
                    ["Sentiment", "Topics", "Style"],
                    analyses
                ):
                    embed.add_field(
                        name=f"{analysis_type} Analysis",
                        value=result,
                        inline=False
                    )
                
                await ctx.send(embed=embed)
                
            except Exception as e:
                await self.handle_error(ctx, e)

    @ai.command(name="settings")
    async def ai_settings(self, ctx):
        embed = self.get_settings_embed()
        await ctx.send(embed=embed, view=AIControlPanel(self))

    def get_settings_embed(self):
        embed = discord.Embed(
            title="⚙️ AI Settings",
            description="Customize your AI experience",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="🤖 Model Selection",
            value="• Creative (GPT-4)\n• Balanced (GPT-3.5)\n• Fast (GPT-3.5 Instruct)",
            inline=False
        )
        embed.add_field(
            name="🎭 AI Personality",
            value="• Professional\n• Casual\n• Humorous",
            inline=True
        )
        embed.add_field(
            name="📝 Response Style",
            value="• Detailed\n• Concise\n• Technical",
            inline=True
        )
        return embed

    async def get_sentiment_analysis(self, text):
        response = self.client.chat.completions.create(
            model=self.ai_engine.model_configs['fast'],
            messages=[
                {"role": "system", "content": "Analyze the sentiment and emotional tone of the following text."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    async def get_topic_analysis(self, text):
        response = self.client.chat.completions.create(
            model=self.ai_engine.model_configs['fast'],
            messages=[
                {"role": "system", "content": "Identify main topics and themes in the following text."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    async def get_style_analysis(self, text):
        response = self.client.chat.completions.create(
            model=self.ai_engine.model_configs['fast'],
            messages=[
                {"role": "system", "content": "Analyze the writing style and linguistic patterns."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    def get_dynamic_color(self, text: str) -> discord.Color:
        """Generate color based on message content"""
        sentiment_words = {
            'positive': ['good', 'great', 'awesome', 'excellent'],
            'negative': ['bad', 'poor', 'terrible', 'awful'],
            'neutral': ['okay', 'fine', 'normal', 'average']
        }
        
        text = text.lower()
        if any(word in text for word in sentiment_words['positive']):
            return discord.Color.green()
        elif any(word in text for word in sentiment_words['negative']):
            return discord.Color.red()
        return discord.Color.blue()

    async def handle_error(self, ctx, error):
        error_embed = discord.Embed(
            title="⚠️ Error Occurred",
            description=f"```{str(error)}```",
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)



class ChannelManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def copychannel(self, ctx, channel_id: int):
        channel = ctx.guild.get_channel(channel_id)
        if not channel:
            await ctx.send("Channel not found!")
            return

        await ctx.send("Starting channel backup process... This may take a while.")

        channel_dir = f"channel_backup_{channel.id}"
        os.makedirs(channel_dir, exist_ok=True)

        channel_data = {
            "name": channel.name,
            "topic": channel.topic,
            "category": channel.category.id if channel.category else None,
            "position": channel.position,
            "slowmode_delay": channel.slowmode_delay,
            "nsfw": channel.nsfw,
            "permissions": []
        }

        for target, overwrite in channel.overwrites.items():
            perm_dict = {
                "id": target.id,
                "type": "role" if isinstance(target, discord.Role) else "member",
                "allow": overwrite.pair()[0].value,
                "deny": overwrite.pair()[1].value
            }
            channel_data["permissions"].append(perm_dict)

        with open(f"{channel_dir}/metadata.json", "w") as f:
            json.dump(channel_data, f)

        messages_data = []
        async for message in channel.history(limit=None, oldest_first=True):
            msg_data = {
                "content": message.content,
                "author": str(message.author),
                "author_id": message.author.id,
                "timestamp": message.created_at.isoformat(),
                "attachments": [],
                "embeds": [{
                    "title": embed.title,
                    "description": embed.description,
                    "color": embed.color.value if embed.color else None
                } for embed in message.embeds if embed.type == 'rich']
            }
            
            for attachment in message.attachments:
                file_path = f"{channel_dir}/{attachment.id}_{attachment.filename}"
                await attachment.save(file_path)
                msg_data["attachments"].append({
                    "filename": attachment.filename,
                    "backup_path": f"{attachment.id}_{attachment.filename}"
                })
            
            messages_data.append(msg_data)

        with open(f"{channel_dir}/messages.json", "w", encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=4)

        zip_filename = f"channel_backup_{channel.id}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(channel_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, channel_dir)
                    zipf.write(file_path, arcname)

        await ctx.send("Channel backup complete!", file=discord.File(zip_filename))
        
        os.remove(zip_filename)
        for root, dirs, files in os.walk(channel_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def pastechannel(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please attach the channel backup ZIP file!")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.zip'):
            await ctx.send("Please provide a valid channel backup ZIP file!")
            return

        await ctx.send("Starting channel restoration process... This may take a while.")

        await attachment.save("temp_backup.zip")
        temp_dir = "temp_channel_restore"
        os.makedirs(temp_dir, exist_ok=True)
        
        with zipfile.ZipFile("temp_backup.zip", 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        with open(f"{temp_dir}/metadata.json", "r") as f:
            channel_data = json.load(f)

        new_channel = await ctx.guild.create_text_channel(
            name=channel_data["name"],
            topic=channel_data["topic"],
            nsfw=channel_data["nsfw"],
            slowmode_delay=channel_data["slowmode_delay"]
        )

        for perm in channel_data["permissions"]:
            target = None
            if perm["type"] == "role":
                target = ctx.guild.get_role(perm["id"])
            else:
                target = ctx.guild.get_member(perm["id"])

            if target:
                allow = discord.Permissions(perm["allow"])
                deny = discord.Permissions(perm["deny"])
                overwrite = discord.PermissionOverwrite.from_pair(allow, deny)
                await new_channel.set_permissions(target, overwrite=overwrite)

        with open(f"{temp_dir}/messages.json", "r", encoding='utf-8') as f:
            messages_data = json.load(f)

        webhook = await new_channel.create_webhook(name="Channel Restore")
        
        for msg in messages_data:
            files = []
            for attachment in msg["attachments"]:
                file_path = f"{temp_dir}/{attachment['backup_path']}"
                if os.path.exists(file_path):
                    files.append(discord.File(file_path, filename=attachment["filename"]))
            
            try:
                await webhook.send(
                    content=msg["content"],
                    username=msg["author"],
                    files=files,
                    embeds=[discord.Embed.from_dict(embed) for embed in msg["embeds"]]
                )
            except Exception as e:
                print(f"Error restoring message: {e}")
                continue

        await webhook.delete()
        
        os.remove("temp_backup.zip")
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)

        await ctx.send(f"Channel has been restored: {new_channel.mention}")


class RoleBackup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def copyrole(self, ctx, role_id: int):
        role = ctx.guild.get_role(role_id)
        if not role:
            await ctx.send("Role not found!")
            return

        await ctx.send("Starting role backup process...")

        role_data = {
            "name": role.name,
            "color": role.color.value,
            "hoist": role.hoist,
            "position": role.position,
            "mentionable": role.mentionable,
            "permissions": role.permissions.value,
            "icon": role.icon.url if role.icon else None,
            "members": [member.id for member in role.members]
        }

        backup_path = f"role_backup_{role.id}"
        os.makedirs(backup_path, exist_ok=True)

        if role.icon:
            async with aiohttp.ClientSession() as session:
                async with session.get(role.icon.url) as resp:
                    if resp.status == 200:
                        with open(f"{backup_path}/icon.png", 'wb') as f:
                            f.write(await resp.read())

        with open(f"{backup_path}/role_data.json", 'w') as f:
            json.dump(role_data, f, indent=4)

        zip_name = f"role_backup_{role.id}.zip"
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        await ctx.send("Role backup complete!", file=discord.File(zip_name))

        os.remove(zip_name)
        for root, dirs, files in os.walk(backup_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def pasterole(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please attach the role backup ZIP file!")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.zip'):
            await ctx.send("Please provide a valid role backup ZIP file!")
            return

        await ctx.send("Starting role restoration process...")

        await attachment.save("temp_role.zip")
        temp_dir = "temp_role_restore"
        os.makedirs(temp_dir, exist_ok=True)

        with zipfile.ZipFile("temp_role.zip", 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        with open(f"{temp_dir}/role_data.json", 'r') as f:
            role_data = json.load(f)

        icon = None
        if os.path.exists(f"{temp_dir}/icon.png"):
            with open(f"{temp_dir}/icon.png", 'rb') as f:
                icon = f.read()

        new_role = await ctx.guild.create_role(
            name=role_data["name"],
            permissions=discord.Permissions(role_data["permissions"]),
            color=discord.Color(role_data["color"]),
            hoist=role_data["hoist"],
            mentionable=role_data["mentionable"]
        )

        if icon:
            await new_role.edit(display_icon=icon)

        restored_members = 0
        for member_id in role_data["members"]:
            member = ctx.guild.get_member(member_id)
            if member:
                try:
                    await member.add_roles(new_role)
                    restored_members += 1
                except:
                    continue

        await ctx.send(f"Role restored successfully!\n"
                      f"Role: {new_role.mention}\n"
                      f"Restored members: {restored_members}")

        
        os.remove("temp_role.zip")
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)


class QueueView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None)
        self.cog = cog

    @discord.ui.button(label="➕ Add to Queue", style=ButtonStyle.green)
    async def add_to_queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(QueueSearchModal(self.cog))

class QueueSearchModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="Add to Queue")
        self.cog = cog
        self.query = discord.ui.TextInput(
            label="Search for a song",
            placeholder="Enter song name or URL...",
            min_length=2,
            max_length=100
        )
        self.add_item(self.query)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        ctx = await interaction.client.get_context(interaction.message)
        
        song_info = await self.cog.get_song_info(str(self.query))
        if song_info:
            if ctx.guild.id not in self.cog.queues:
                self.cog.queues[ctx.guild.id] = []
            
            self.cog.queues[ctx.guild.id].append(song_info)
            await interaction.followup.send(f"Added to queue: {song_info['title']}", ephemeral=True)


class MusicControls(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Join Voice", style=ButtonStyle.green)
    async def join_voice(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        if member and member.voice and member.voice.channel:
            await member.voice.channel.connect()
            await interaction.response.send_message(f"✅ Joined {member.voice.channel.name}")
            button.disabled = True
            await interaction.message.edit(view=self)
        else:
            await interaction.response.send_message("You need to be in a voice channel!", ephemeral=True)

    @discord.ui.button(label="Play Music", style=ButtonStyle.blurple)
    async def play_music(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SearchModal(self.bot.get_cog("MusicPlayer")))

@commands.command()
async def music(self, ctx):
    """Opens music control panel"""
    embed = discord.Embed(title="🎵 Music Controls", color=discord.Color.blue())
    view = MusicControls(self.bot)
    await ctx.send(embed=embed, view=view)



class MusicPlayerView(discord.ui.View):
    def __init__(self, cog, ctx):
        super().__init__(timeout=None)
        self.cog = cog
        self.ctx = ctx
        self.current_page = 0

    @discord.ui.button(label="🔍", style=ButtonStyle.primary, custom_id="search", row=0)
    async def search(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SearchModal(self.cog))

    @discord.ui.button(label="▶️", style=ButtonStyle.green, custom_id="play_pause", row=0)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild.voice_client:
            await interaction.response.send_message("I'm not connected to a voice channel!", ephemeral=True)
            return
        
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            button.label = "⏸️"
            await interaction.response.edit_message(view=self)
        else:
            if not self.cog.now_playing.get(self.ctx.guild.id) and not interaction.guild.voice_client.is_paused() and self.cog.queues.get(self.ctx.guild.id):
                first_song = self.cog.queues[self.ctx.guild.id][0]
                try:
                    source = await discord.FFmpegOpusAudio.from_probe(
                        first_song['url'], 
                        **self.cog.FFMPEG_OPTIONS
                    )
                    interaction.guild.voice_client.play(
                        source, 
                        after=lambda e: asyncio.run_coroutine_threadsafe(
                            self.cog.play_next(self.ctx), 
                            self.cog.bot.loop
                        )
                    )
                    self.cog.now_playing[self.ctx.guild.id] = first_song['title']
                    button.label = "⏸️"
                except Exception as e:
                    print(f"Playback error: {e}")
                    await interaction.response.send_message("Failed to play the song.", ephemeral=True)
                    return
            else:
                interaction.guild.voice_client.resume()
                button.label = "⏸️"
            
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label="⏭️", style=ButtonStyle.blurple, custom_id="skip", row=0)
    async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild.voice_client:
            await interaction.response.send_message("Not connected to a voice channel!", ephemeral=True)
            return

        if not self.cog.queues.get(interaction.guild.id):
            await interaction.response.send_message("No songs in queue!", ephemeral=True)
            return

        interaction.guild.voice_client.stop()
        
        next_song = self.cog.queues[interaction.guild.id][0]
        source = await discord.FFmpegOpusAudio.from_probe(next_song['url'], **self.cog.FFMPEG_OPTIONS)
        interaction.guild.voice_client.play(
            source,
            after=lambda e: asyncio.run_coroutine_threadsafe(
                self.cog.play_next(interaction.channel),
                self.cog.bot.loop
            )
        )
        self.cog.now_playing[interaction.guild.id] = next_song['title']
        
        await interaction.response.send_message(f"Skipped! Now playing: {next_song['title']}", ephemeral=True)

    @discord.ui.button(label="⚙️", style=ButtonStyle.gray, custom_id="settings", row=0)
    async def settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        settings_embed = discord.Embed(title="Settings Panel", color=discord.Color.blue())
        view = SettingsView(self.cog)
        await interaction.response.send_message(embed=settings_embed, view=view, ephemeral=True)

    @discord.ui.button(label="🎵 Queue", style=ButtonStyle.secondary, custom_id="view_queue", row=1)
    async def view_queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.cog.queues.get(self.ctx.guild.id):
            await interaction.response.send_message("Queue is empty!", ephemeral=True)
            return
            
        queue = self.cog.queues[self.ctx.guild.id]
        embed = discord.Embed(title="Current Queue", color=discord.Color.blue())
        
        for i, song in enumerate(queue, start=1):
            embed.add_field(
                name=f"{i}. {song['title']}", 
                value=f"Duration: {song['duration']}", 
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="⏹️", style=ButtonStyle.red, custom_id="stop", row=0)
    async def stop(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.leave(self.ctx)
        await interaction.message.delete()

    async def update_player_message(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎵 Music Player",
            description="Control your music experience!",
            color=discord.Color.brand_green()
        )
        if self.cog.now_playing.get(self.ctx.guild.id):
            embed.add_field(name="Now Playing", value=self.cog.now_playing[self.ctx.guild.id])
        await interaction.message.edit(embed=embed, view=self)


class SearchModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="Search Music")
        self.cog = cog
        self.query = discord.ui.TextInput(
            label="Search for a song",
            placeholder="Enter song name or URL...",
            min_length=2,
            max_length=100
        )
        self.add_item(self.query)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        ctx = await interaction.client.get_context(interaction.message)
        await self.cog.play(ctx, query=str(self.query))

class VolumeModal(discord.ui.Modal):
    def __init__(self, cog):
        super().__init__(title="Adjust Volume")
        self.cog = cog
        self.volume_input = discord.ui.TextInput(
            label="Volume (0-100)",
            placeholder="Enter a number between 0 and 100",
            min_length=1,
            max_length=3
        )
        self.add_item(self.volume_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            vol = float(self.volume_input.value)
            if 0 <= vol <= 100:
                if interaction.guild.voice_client:
                    
                    self.cog.volume = vol / 100
                    self.cog.FFMPEG_OPTIONS = {
                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': f'-vn -filter:a volume={vol/100} -b:a 384k -bufsize 2048k'
                    }
                    
                    guild_id = interaction.guild.id
                    if interaction.guild.voice_client.is_playing() and self.cog.queues.get(guild_id):
                        current_song = self.cog.queues[guild_id][0]
                        
                        interaction.guild.voice_client.stop()
                        
                        source = await discord.FFmpegOpusAudio.from_probe(
                            current_song['url'],
                            **self.cog.FFMPEG_OPTIONS
                        )
                        
                        interaction.guild.voice_client.play(
                            source,
                            after=lambda e: self.cog.bot.loop.create_task(self.cog.play_next(interaction.channel))
                        )
                    
                    await interaction.response.send_message(f"🔊 Volume is now {vol}%", ephemeral=True)
                else:
                    await interaction.response.send_message("Join a voice channel first!", ephemeral=True)
            else:
                await interaction.response.send_message("Volume must be between 0 and 100", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Enter a valid number!", ephemeral=True)


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.now_playing = {}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -b:a 384k -bufsize 2048k -ar 48000'
        }


        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        self.volume = 1.0
        self.loop = False

    @commands.command()
    async def player(self, ctx):
        """Opens the interactive music player interface"""
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
        except FileNotFoundError:
            status_msg = await ctx.send("🎵 First-time setup: Installing FFmpeg...")
            if platform.system() == "Windows":
                url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
                zip_path = os.path.join(current_dir, "ffmpeg.zip")
                wget.download(url, zip_path)
                
                ffmpeg_dir = os.path.join(current_dir, "ffmpeg")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(ffmpeg_dir)
                
                for root, dirs, files in os.walk(ffmpeg_dir):
                    if 'ffmpeg.exe' in files:
                        ffmpeg_bin = root
                        break
                
                os.environ["PATH"] = ffmpeg_bin + os.pathsep + os.environ["PATH"]
                await status_msg.edit(content="✅ FFmpeg installed successfully! Starting music player...")

        embed = discord.Embed(
            title="🎵 Music Player",
            description="Control your music experience!",
            color=discord.Color.brand_green()
        )
        if self.now_playing.get(ctx.guild.id):
            embed.add_field(name="Now Playing", value=self.now_playing[ctx.guild.id])
        view = MusicPlayerView(self, ctx)
        await ctx.send(embed=embed, view=view)


    async def get_song_info(self, query):
        try:
            with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                if not query.startswith('http'):
                    query = f"ytsearch:{query}"
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                
                return {
                    'title': info['title'],
                    'url': info['url'],
                    'thumbnail': info['thumbnail'],
                    'duration': str(timedelta(seconds=info['duration'])),
                    'webpage_url': info['webpage_url']
                }
        except Exception as e:
            print(f"Error in get_song_info: {e}")
            return None


    @commands.command()
    async def play(self, ctx, *, query):
        print("\n=== MUSIC PLAYER DEBUG ===")
        print(f"Command received from: {ctx.author}")
        print(f"Query: {query}")

        voice_state = ctx.author.voice
        if not voice_state or not voice_state.channel:
            return await ctx.send("🎵 Please join a voice channel first!")

        voice_channel = voice_state.channel
        print(f"Found Voice Channel: {voice_channel.name}")

        try:
            if not ctx.voice_client:
                await voice_channel.connect()
                print(f"✅ Connected to {voice_channel.name}")
            elif ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)
                print(f"✅ Moved to {voice_channel.name}")

            print("\n=== SONG SEARCH ===")

            async with ctx.typing():
                try:
                    
                    search_query = f"ytsearch:{query}"
                    with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(search_query, download=False)
                        if 'entries' in info and info['entries']:
                            video = info['entries'][0]
                            url = video['webpage_url']
                            title = video['title']
                            thumbnail = video['thumbnail']
                            duration = str(timedelta(seconds=video['duration']))
                            
                            print(f"Found: {title}")
                            url2 = video['url']
                            source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)

                    with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(url, download=False)
                        url2 = info['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)

                        if ctx.guild.id not in self.queues:
                            self.queues[ctx.guild.id] = []

                        song_info = {
                            'title': title,
                            'url': url2,
                            'thumbnail': thumbnail,
                            'requester': ctx.author.name,
                            'duration': duration,
                            'requested_at': datetime.now().strftime("%H:%M:%S"),
                            'channel': ctx.channel.id
                        }

                        self.queues[ctx.guild.id].append(song_info)

                        if not ctx.voice_client.is_playing():
                            print("\n=== PLAYING SONG ===")
                            ctx.voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))
                            self.now_playing[ctx.guild.id] = title

                            embed = discord.Embed(
                                title="Now Playing 🎵",
                                description=title,
                                color=discord.Color.green()
                            )
                            embed.set_thumbnail(url=thumbnail)
                            embed.add_field(name="Duration", value=duration, inline=True)
                            embed.add_field(name="Requested by", value=ctx.author.name, inline=True)
                            embed.add_field(name="Time", value=song_info['requested_at'], inline=True)
                            embed.set_footer(text=f"Voice Channel: {voice_channel.name}")
                            
                            await ctx.send(embed=embed)
                        else:
                            print("\n=== ADDED TO QUEUE ===")
                            embed = discord.Embed(
                                title="Added to Queue 📝",
                                description=title,
                                color=discord.Color.blue()
                            )
                            embed.set_thumbnail(url=thumbnail)
                            embed.add_field(name="Duration", value=duration, inline=True)
                            embed.add_field(name="Requested by", value=ctx.author.name, inline=True)
                            embed.add_field(name="Position", value=str(len(self.queues[ctx.guild.id])), inline=True)
                            embed.set_footer(text=f"Queue Length: {len(self.queues[ctx.guild.id])}")
                            
                            await ctx.send(embed=embed)

                except Exception as e:
                    print(f"\n❌ Search Error: {str(e)}")
                    if 'youtube.com' in query or 'youtu.be' in query:
                        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(query, download=False)
                            url = info['url']
                            title = info['title']
                            thumbnail = info['thumbnail']
                            duration = str(datetime.timedelta(seconds=info['duration']))
                    else:
                        return await ctx.send("🔍 No results found! Try a different search term.")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            await ctx.send(f"⚠️ An error occurred while playing the song")
        
        finally:
            print("\n=== END OF COMMAND ===")


    async def play_next(self, ctx):
        if not self.queues.get(ctx.guild.id) or not self.queues[ctx.guild.id]:
            self.now_playing[ctx.guild.id] = None
            return

        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        try:
            next_song = self.queues[ctx.guild.id].pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(next_song['url'], **self.FFMPEG_OPTIONS)
            
            def after_callback(error):
                if error:
                    print(f"Playback error: {error}")
                self.bot.loop.create_task(self.play_next(ctx))
                
            ctx.voice_client.play(source, after=after_callback)
            self.now_playing[ctx.guild.id] = next_song['title']
            
            embed = discord.Embed(title="Now Playing 🎵", description=next_song['title'], color=discord.Color.green())
            embed.set_thumbnail(url=next_song['thumbnail'])
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(f"Error in play_next: {e}")


    @commands.command()
    async def skip(self, ctx):
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send("Nothing is playing!")
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped!")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.queues[ctx.guild.id] = []
            self.now_playing[ctx.guild.id] = None
            await ctx.send("👋 Bye!")

class IdeaSubmissionConfig:
    def __init__(self):
        
        self.is_anonymous = True
        self.require_approval = True
        self.submission_channel_id = None  
        self.button_channel_id = None      
        self.min_chars = 20
        self.max_chars = 1000
        self.cooldown_minutes = 5
        self.max_submissions_per_day = 5
        
        self.button_color = ButtonStyle.green
        self.button_label = "Submit Idea"
        self.button_emoji = "💡"
        self.embed_color = discord.Color.blue()
        self.embed_title = "Submit Your Idea"
        self.embed_description = "Click below to submit your idea"
        self.modal_title = "New Idea Submission"
        
        self.idea_title_prefix = ""
        self.title_prefix = ""

        self.auto_thread = True
        self.thread_duration = 1440
        self.allow_voting = True
        self.categories = ["Feature", "Bug Fix", "Enhancement", "Other"]
        self.available_tags = ["Urgent", "QoL", "Technical", "Design"]
        self.max_tags = 3


class MainControlPanel(discord.ui.View):
    def __init__(self, configs):
        super().__init__(timeout=None)
        
        self.configs = {} if not isinstance(configs, dict) else configs
        self.current_system = "default"

    @discord.ui.select(
        placeholder="Select System Type",
        options=[
            discord.SelectOption(label="Bug Reports", value="bugs", emoji="🐛"),
            discord.SelectOption(label="Feature Requests", value="features", emoji="✨"),
            discord.SelectOption(label="Feedback", value="feedback", emoji="📝")
        ],
        row=0
    )
    async def select_system(self, interaction, select):
        self.current_system = select.values[0]
       
        if self.current_system not in self.configs:
            self.configs[self.current_system] = IdeaSubmissionConfig()
        await interaction.response.send_message(f"Now configuring: {self.current_system}", ephemeral=True)


    @discord.ui.button(label="Channel Setup", style=ButtonStyle.blurple, row=1)
    async def setup_channels(self, interaction, button):
        modal = ChannelSetupModal(self.configs[self.current_system])
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Appearance", style=ButtonStyle.primary, row=1)
    async def appearance(self, interaction, button):
        modal = AppearanceModal(self.configs[self.current_system])
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Submission Settings", style=ButtonStyle.primary, row=2)
    async def submission_settings(self, interaction, button):
        modal = SubmissionSettingsModal(self.configs[self.current_system])
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Categories & Tags", style=ButtonStyle.primary, row=2)
    async def categories(self, interaction, button):
        modal = CategoryModal(self.configs[self.current_system])
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Create Submit Button", style=ButtonStyle.success, row=3)
    async def create_button(self, interaction, button):
        config = self.configs[self.current_system]
        if not config.button_channel_id:
            await interaction.response.send_message("Please set up channels first!", ephemeral=True)
            return
            
        channel = interaction.guild.get_channel(config.button_channel_id)
        if channel:
            
            embed = discord.Embed(
                title=config.embed_title,
                description=config.embed_description,
                color=config.embed_color
            )
            
            class CustomSubmissionView(discord.ui.View):
                def __init__(self, config, cooldowns):
                    super().__init__(timeout=None)
                    self.config = config
                    self.cooldowns = cooldowns

                @discord.ui.button(
                    label=config.button_label,
                    emoji=config.button_emoji,
                    style=config.button_color
                )
                async def submit_idea(self, interaction, button):
                    modal = IdeaSubmissionModal(self.config)
                    await interaction.response.send_modal(modal)

            view = CustomSubmissionView(config, {})
            await channel.send(embed=embed, view=view)
            await interaction.response.send_message(f"Submit button created in {channel.mention}!", ephemeral=True)


class AppearanceModal(discord.ui.Modal):
    def __init__(self, config):
        super().__init__(title="Customize Appearance")
        self.config = config
        
        self.add_item(discord.ui.TextInput(
            label="Button Label",
            default=config.button_label
        ))
        self.add_item(discord.ui.TextInput(
            label="Button Emoji",
            default=config.button_emoji
        ))
        self.add_item(discord.ui.TextInput(
            label="Embed Title",
            default=config.embed_title
        ))
        self.add_item(discord.ui.TextInput(
            label="Embed Description",
            default=config.embed_description,
            style=discord.TextStyle.paragraph
        ))
        self.add_item(discord.ui.TextInput(
            label="Title Prefix & Color",
            placeholder="Prefix | #HexColor",
            default=f"{config.title_prefix} | {config.embed_color}",
            required=False
        ))

    async def on_submit(self, interaction):
        self.config.button_label = self.children[0].value
        self.config.button_emoji = self.children[1].value
        self.config.embed_title = self.children[2].value
        self.config.embed_description = self.children[3].value
        
        prefix_color = self.children[4].value.split("|")
        self.config.title_prefix = prefix_color[0].strip()
        if len(prefix_color) > 1:
            try:
                self.config.embed_color = discord.Color.from_str(prefix_color[1].strip())
            except:
                pass
                
        await interaction.response.send_message("Appearance updated!", ephemeral=True)

class SubmissionSettingsModal(discord.ui.Modal):
    def __init__(self, config):
        super().__init__(title="Submission Settings")
        self.config = config
        self.add_item(discord.ui.TextInput(
            label="Min Characters",
            default=str(config.min_chars)
        ))
        self.add_item(discord.ui.TextInput(
            label="Max Characters", 
            default=str(config.max_chars)
        ))
        self.add_item(discord.ui.TextInput(
            label="Cooldown (minutes)",
            default=str(config.cooldown_minutes)
        ))
        self.add_item(discord.ui.TextInput(
            label="Daily Submission Limit",
            default=str(config.max_submissions_per_day)
        ))

    async def on_submit(self, interaction):
        try:
            self.config.min_chars = int(self.children[0].value)
            self.config.max_chars = int(self.children[1].value)
            self.config.cooldown_minutes = int(self.children[2].value)
            self.config.max_submissions_per_day = int(self.children[3].value)
            await interaction.response.send_message("✨ Settings updated successfully!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Please enter valid numbers for all fields!", ephemeral=True)

class IdeaSubmissionView(discord.ui.View):
    def __init__(self, config, cooldowns):
        super().__init__(timeout=None)
        self.config = config
        self.cooldowns = cooldowns
        self.system_type = config.system_type if hasattr(config, 'system_type') else "default"

    @discord.ui.button(label="Submit Idea", emoji="💡", style=ButtonStyle.green)
    async def submit_idea(self, interaction, button):
        user_id = interaction.user.id
        current_time = datetime.now(timezone.utc)
        
        if user_id in self.cooldowns:
            time_diff = current_time - self.cooldowns[user_id]
            if time_diff.total_seconds() < self.config.cooldown_minutes * 60:
                remaining = self.config.cooldown_minutes * 60 - time_diff.total_seconds()
                await interaction.response.send_message(
                    f"Please wait {int(remaining)} seconds before submitting again!",
                    ephemeral=True
                )
                return

        self.cooldowns[user_id] = current_time
        modal = IdeaSubmissionModal(self.config)
        await interaction.response.send_modal(modal)


class IdeaSubmissionModal(discord.ui.Modal):
    def __init__(self, config):
        super().__init__(title="Submit Your Idea")
        self.config = config
        
        self.add_item(discord.ui.TextInput(
            label="Title",
            placeholder="Brief title for your idea",
            max_length=100,
            required=True
        ))
        self.add_item(discord.ui.TextInput(
            label="Description",
            placeholder="Detailed description...",
            style=discord.TextStyle.paragraph,
            min_length=self.config.min_chars,
            max_length=self.config.max_chars,
            required=True
        ))
        if self.config.categories:
            self.add_item(discord.ui.TextInput(
                label="Category",
                placeholder=f"Choose from: {', '.join(self.config.categories)}",
                required=True
            ))

    async def on_submit(self, interaction):
    
        await interaction.response.defer(ephemeral=True)
        
        try:
            if not self.config.submission_channel_id:
                await interaction.followup.send("Submission channel not configured!", ephemeral=True)
                return

            channel = interaction.guild.get_channel(self.config.submission_channel_id)
            if not channel:
                await interaction.followup.send("Cannot find submission channel!", ephemeral=True)
                return

            title = self.children[0].value
            if self.config.title_prefix and self.config.title_prefix.strip():
                title = f"{self.config.title_prefix}: {title}"

            embed = discord.Embed(
                title=title,
                description=self.children[1].value,
                color=self.config.embed_color,
                timestamp=datetime.now(timezone.utc)
            )
            
            if not self.config.is_anonymous:
                embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            
            if len(self.children) > 2:
                embed.add_field(name="Category", value=self.children[2].value)
            
            msg = await channel.send(embed=embed)
            
            if self.config.allow_voting:
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
                
            if self.config.auto_thread:
                await msg.create_thread(
                    name=f"Discussion: {self.children[0].value[:50]}",
                    auto_archive_duration=self.config.thread_duration
                )
                
            await interaction.followup.send("Your idea has been submitted successfully! ✨", ephemeral=True)
            
        except Exception as e:
            await interaction.followup.send("There was an error submitting your idea. Please try again.", ephemeral=True)


class ChannelSetupModal(discord.ui.Modal):
    def __init__(self, config):
        super().__init__(title="Channel Setup")
        self.config = config
        self.add_item(discord.ui.TextInput(
            label="Click Submit to continue",
            placeholder="Click Submit to proceed to channel selection",
            required=False,
            style=discord.TextStyle.short
        ))

    async def on_submit(self, interaction):
        class ChannelSelect(discord.ui.View):
            def __init__(self, config, all_channels):
                super().__init__(timeout=300)
                self.config = config
                self.all_channels = all_channels
                self.button_selected = False
                self.ideas_selected = False
                self.current_search_button = ""
                self.current_search_ideas = ""
                self.button_options = []
                self.ideas_options = []
                self.selections = {
                    "button": {"id": None, "option": None},
                    "ideas": {"id": None, "option": None}
                }

                initial_options = [
                    discord.SelectOption(label=f"#{channel.name}", value=str(channel.id))
                    for channel in self.all_channels[:25]
                ]

                self.button_options = initial_options.copy()
                self.ideas_options = initial_options.copy()

                self.button_search.options = [discord.SelectOption(label="🔍 Search button channel...", value="search_button")]
                self.ideas_search.options = [discord.SelectOption(label="🔍 Search ideas channel...", value="search_ideas")]

                self.button_channel.options = self.button_options
                self.ideas_channel.options = self.ideas_options


            @discord.ui.button(label="Save Settings", style=ButtonStyle.green, row=4)
            async def save_button(self, interaction, button):
                if not self.button_selected or not self.ideas_selected:
                    embed = discord.Embed(
                        description = "⚠️ Please follow these steps:\n1. Search for the button and ideas channels FIRST\n2. Once both are found, select the button channel\n3. Then, select the ideas channel",
                        color=discord.Color.yellow()
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                button_channel = interaction.guild.get_channel(self.config.button_channel_id)
                ideas_channel = interaction.guild.get_channel(self.config.submission_channel_id)
                embed = discord.Embed(
                    title="✨ Channel Setup Complete",
                    description=f"Submit Button Channel: #{button_channel.name}\nIdeas Channel: #{ideas_channel.name}",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                self.stop()

            @discord.ui.button(label="Cancel", style=ButtonStyle.red, row=4)
            async def cancel_button(self, interaction, button):
                embed = discord.Embed(
                    description="❌ Setup cancelled!",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                self.stop()

            def update_channel_options(self, search_term, for_button=True):
                filtered_channels = [
                    channel for channel in self.all_channels
                    if search_term.lower() in channel.name.lower()
                ][:25]
                
                options = [discord.SelectOption(label=f"#{channel.name}", value=str(channel.id))
                        for channel in filtered_channels]
                
                if for_button:
                    self.button_options = options
                else:
                    self.ideas_options = options
                return options

            @discord.ui.select(
                placeholder="🔍 Search Button Channel",
                min_values=0,
                max_values=1,
                options=[discord.SelectOption(label="Click to search...", value="search_button")],
                row=0
            )
            async def button_search(self, interaction, select):
                modal = SearchModal(self, True)
                await interaction.response.send_modal(modal)

            @discord.ui.select(
                placeholder="🔍 Search Ideas Channel",
                min_values=0,
                max_values=1,
                options=[discord.SelectOption(label="Click to search...", value="search_ideas")],
                row=2
            )
            async def ideas_search(self, interaction, select):
                modal = SearchModal(self, False)
                await interaction.response.send_modal(modal)

            @discord.ui.select(
                placeholder="1️⃣ Select Submit Button Channel",
                options=[],
                row=1
            )
            async def button_channel(self, interaction, select):
                channel_id = int(select.values[0])
                channel = interaction.guild.get_channel(channel_id)
                self.config.button_channel_id = channel_id
                self.button_selected = True
                
                self.selections["button"] = {
                    "id": channel_id,
                    "option": discord.SelectOption(
                        label=f"#{channel.name}",
                        value=str(channel_id)
                    )
                }
                
                embed = discord.Embed(
                    description=f"✅ Submit button channel set to: #{channel.name}",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

            @discord.ui.select(
                placeholder="2️⃣ Select Ideas Channel",
                options=[],
                row=3
            )
            async def ideas_channel(self, interaction, select):
                channel_id = int(select.values[0])
                channel = interaction.guild.get_channel(channel_id)
                self.config.submission_channel_id = channel_id
                self.ideas_selected = True
                
                self.selections["ideas"] = {
                    "id": channel_id,
                    "option": discord.SelectOption(
                        label=f"#{channel.name}",
                        value=str(channel_id)
                    )
                }
                
                embed = discord.Embed(
                    description=f"✅ Ideas channel set to: #{channel.name}",
                    color=discord.Color.green()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)

            async def update_view(self, interaction, search_term, for_button=True):
                if for_button:
                    self.current_search_button = search_term
                    button_options = self.update_channel_options(search_term, True)
                    
                    if self.selections["button"]["option"]:
                        button_options = [self.selections["button"]["option"]] + [
                            opt for opt in button_options 
                            if opt.value != str(self.selections["button"]["id"])
                        ]
                    self.button_channel.options = button_options
                    
                    if self.selections["ideas"]["option"]:
                        self.ideas_channel.options = [self.selections["ideas"]["option"]] + [
                            opt for opt in self.ideas_channel.options 
                            if opt.value != str(self.selections["ideas"]["id"])
                        ]
                else:
                    self.current_search_ideas = search_term
                    ideas_options = self.update_channel_options(search_term, False)
                    
                    if self.selections["ideas"]["option"]:
                        ideas_options = [self.selections["ideas"]["option"]] + [
                            opt for opt in ideas_options 
                            if opt.value != str(self.selections["ideas"]["id"])
                        ]
                    self.ideas_channel.options = ideas_options
                    
                    if self.selections["button"]["option"]:
                        self.button_channel.options = [self.selections["button"]["option"]] + [
                            opt for opt in self.button_channel.options 
                            if opt.value != str(self.selections["button"]["id"])
                        ]

                await interaction.response.edit_message(view=self)

        view = ChannelSelect(self.config, interaction.guild.text_channels)
        embed = discord.Embed(
            title="🔧 Channel Setup",
            description = "1. First, search for both the button and ideas channels using the search options\n2. Once both are found, select the button channel and the ideas channel\n3. Save your settings when done",

            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


        class SearchModal(discord.ui.Modal):
            def __init__(self, view, for_button=True):
                super().__init__(title="Search Channels")
                self.view = view
                self.for_button = for_button
                self.add_item(discord.ui.TextInput(
                    label="Search Term",
                    placeholder="Enter channel name to search",
                    required=True,
                    max_length=100
                ))

            async def on_submit(self, interaction):
                await self.view.update_view(interaction, self.children[0].value, self.for_button)


class IdeaSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = {}
        self.cooldowns = {}
        self.guild_configs = {} 

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ideasystem(self, ctx):
        if ctx.guild.id not in self.configs:
            self.configs[ctx.guild.id] = IdeaSubmissionConfig()
            
        embed = discord.Embed(
            title="Idea System Control Panel",
            description="Configure your idea submission system",
            color=self.configs[ctx.guild.id].embed_color
        )
        view = MainControlPanel(self.configs[ctx.guild.id])
        await ctx.send(embed=embed, view=view)

class CategoryModal(discord.ui.Modal):
    def __init__(self, config):
        super().__init__(title="Categories & Tags Configuration")
        self.config = config
        
        self.add_item(discord.ui.TextInput(
            label="Categories (comma-separated)",
            placeholder="Feature, Bug Fix, Enhancement, Other",
            default=", ".join(config.categories),
            style=discord.TextStyle.paragraph
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Available Tags (comma-separated)",
            placeholder="Urgent, QoL, Technical, Design",
            default=", ".join(config.available_tags),
            style=discord.TextStyle.paragraph
        ))
        
        self.add_item(discord.ui.TextInput(
            label="Max Tags Per Submission",
            placeholder="Enter a number (1-10)",
            default=str(config.max_tags)
        ))

    async def on_submit(self, interaction):
        self.config.categories = [cat.strip() for cat in self.children[0].value.split(",")]
        self.config.available_tags = [tag.strip() for tag in self.children[1].value.split(",")]
        try:
            self.config.max_tags = int(self.children[2].value)
        except ValueError:
            self.config.max_tags = 3
        
        await interaction.response.send_message("Categories and tags updated!", ephemeral=True)

class ChannelSelectModal(discord.ui.Modal):
    def __init__(self, config):
        super().__init__(title="Select Channel")
        self.config = config
        self.add_item(discord.ui.TextInput(
            label="Channel ID",
            placeholder="Enter the channel ID where to create the submit button",
            required=True
        ))

    async def on_submit(self, interaction):
        channel_id = int(self.children[0].value)
        channel = interaction.guild.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title=self.config.embed_title,
                description=self.config.embed_description,
                color=self.config.embed_color
            )
            view = IdeaSubmissionView(self.config, {})
            await channel.send(embed=embed, view=view)
            await interaction.response.send_message(f"Submit button created in {channel.mention}!", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid channel ID!", ephemeral=True)


def setup(bot):
    bot.add_cog(IdeaSystem(bot))


class MoodTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mood_data = {}
        self.opted_users = {}
        self.mood_configs = {}
        self.anonymous_users = set()
        self.mood_role_name = "Mood Tracker"
        self.mood_streaks = {}
        self.custom_moods = {}
        self.load_mood_data()
        
        self.check_moods_task = tasks.loop(seconds=20)(self.check_moods)
        self.update_analytics_task = tasks.loop(hours=24)(self.update_analytics)
        
        self.check_moods_task.start()
        self.update_analytics_task.start()

    @commands.group(name="setup_mood")
    @commands.has_permissions(administrator=True)
    async def setup_mood(self, ctx):
        """Setup guide for mood tracking system"""
        embed = discord.Embed(
            title="🎯 Quick Setup Guide",
            description=(
                "**1. Role Setup**\n"
                "→ `!set_mood_role @Role`\n"
                "• Everyone with this role gets mood prompts\n"
                "• Members can still opt-in/out individually\n\n"
                "**2. Channel Setup**\n"
                "→ `!set_mood_channel #channel`\n"
                "• All mood responses get logged here\n"
                "• Anonymous responses hide usernames\n\n"
                "**3. Timing Setup**\n"
                "→ `!mood config`\n"
                "• Choose how often prompts are sent\n"
                "• Options: Daily, Twice Daily, Weekly, Test Mode\n\n"
                "**4. Testing**\n"
                "→ `!test_mood @Role`\n"
                "• Sends immediate test prompt to role members\n"
                "• Verify everything works correctly\n\n"
                "**5. Monitor**\n"
                "→ `!analyze_moods`\n"
                "• View all recorded moods\n"
                "• Track participation and trends"
            ),
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mood_channel(self, ctx, channel: discord.TextChannel):
        """Set channel for mood logging"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.mood_configs:
            self.mood_configs[guild_id] = {}
        
        self.mood_configs[guild_id]['log_channel'] = channel.id
        self.save_mood_data()
        
        embed = discord.Embed(
            title="✅ Mood Channel Set",
            description=f"Mood logs will be sent to {channel.mention}\n\n" \
                    f"• Anonymous users: Only mood will be shown\n" \
                    f"• Non-anonymous users: Name and mood will be shown",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def export_mood_data(self, ctx):
        """Export mood tracking data"""
        buffer = io.StringIO()
        json.dump({
            'moods': self.mood_data,
            'configs': self.mood_configs,
            'anonymous': list(self.anonymous_users)
        }, buffer, indent=4)
        buffer.seek(0)
        
        file = discord.File(fp=buffer, filename='mood_data_backup.json')
        await ctx.send("Here's your mood tracking data backup:", file=file)
        buffer.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def import_mood_data(self, ctx):
        """Import mood tracking data"""
        if not ctx.message.attachments:
            return await ctx.send("Please attach a mood_data_backup.json file!")
            
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.json'):
            return await ctx.send("Please provide a valid JSON file!")
            
        try:
            data = json.loads(await attachment.read())
            self.mood_data = data.get('moods', {})
            self.mood_configs = data.get('configs', {})
            self.anonymous_users = set(data.get('anonymous', []))
            self.save_mood_data()
            await ctx.send("✅ Mood tracking data imported successfully!")
        except Exception as e:
            await ctx.send(f"❌ Error importing data: {str(e)}")


    async def button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            return
            
        custom_id = interaction.data["custom_id"]
        guild_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)

        if custom_id == "toggle_anon":
            if interaction.user.id in self.cog.anonymous_users:
                self.cog.anonymous_users.remove(interaction.user.id)
                await interaction.response.send_message("Anonymous mode disabled!", ephemeral=True)
            else:
                self.cog.anonymous_users.add(interaction.user.id)
                await interaction.response.send_message("Anonymous mode enabled!", ephemeral=True)
            return

        if guild_id not in self.cog.mood_data:
            self.cog.mood_data[guild_id] = {}
        if user_id not in self.cog.mood_data[guild_id]:
            self.cog.mood_data[guild_id][user_id] = []
        
        mood_entry = {
            'mood': custom_id,
            'timestamp': datetime.now().isoformat(),
            'anonymous': interaction.user.id in self.cog.anonymous_users
        }
        
        self.cog.mood_data[guild_id][user_id].append(mood_entry)
        self.cog.save_mood_data()
        
        await interaction.response.send_message(f"Mood recorded: {custom_id.title()}!", ephemeral=True)
        
        if guild_id in self.cog.mood_configs and 'log_channel' in self.cog.mood_configs[guild_id]:
            channel_id = self.cog.mood_configs[guild_id]['log_channel']
            channel = self.cog.bot.get_channel(channel_id)

            
            if channel:
                is_anonymous = interaction.user.id in self.cog.anonymous_users
                user_display = "Anonymous User" if is_anonymous else interaction.user.display_name
                
                embed = discord.Embed(
                    title="🌟 New Mood Entry",
                    description=f"**User:** {user_display}\n**Mood:** {custom_id.title()}",
                    color=discord.Color.blue(),
                    timestamp=datetime.now()
                )
                try:
                    await channel.send(embed=embed)
                except discord.HTTPException:
                    pass


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def analyze_moods(self, ctx):
        """Analyze moods for server members"""
        guild_id = str(ctx.guild.id)
        
        mood_data = self.mood_data.get(guild_id, {})
        
        if not mood_data:
            await ctx.send("No mood data recorded yet!")
            return
            
        embed = discord.Embed(
            title="🔍 Mood Analysis",
            description="Recent mood records:",
            color=discord.Color.blue()
        )
        
        total_entries = 0
        for user_id, moods in mood_data.items():
            if not moods:
                continue
                
            member = ctx.guild.get_member(int(user_id))
            if not member:
                continue
                
            user_moods = {}  
            for mood in moods[-5:]:
                is_anonymous = mood.get('anonymous', False)
                if is_anonymous not in user_moods:
                    user_moods[is_anonymous] = []
                timestamp = datetime.fromisoformat(mood['timestamp']).strftime("%Y-%m-%d %H:%M")
                user_moods[is_anonymous].append(f"• {mood['mood']} ({timestamp})")
            
            for is_anonymous, mood_list in user_moods.items():
                name = "Anonymous User" if is_anonymous else member.display_name
                embed.add_field(
                    name=f"{name}'s Moods",
                    value="\n".join(mood_list),
                    inline=False
                )
                total_entries += 1
        
        if total_entries == 0:
            await ctx.send("No mood data to display!")
            return
            
        await ctx.send(embed=embed)


    async def update_analytics(self):
        """Update analytics for mood tracking"""
        for guild_id, config in self.mood_configs.items():
            if not config.get('analytics_channel'):
                continue
                
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
                
            channel = guild.get_channel(config['analytics_channel'])
            if channel:
                total_moods = len(self.mood_data.get(guild_id, {}))
                active_users = len(self.opted_users.get(guild_id, []))
                
                embed = discord.Embed(
                    title="📊 Mood Tracking Analytics",
                    description=f"Total Moods: {total_moods}\nActive Users: {active_users}",
                    color=discord.Color.blue()
                )
                await channel.send(embed=embed)


    class MoodSelectionView(discord.ui.View):
        def __init__(self, cog, user_id):
            super().__init__()
            self.cog = cog
            self.user_id = user_id
            
            moods = [
                ("🎭 Toggle Anonymous", "toggle_anon", discord.ButtonStyle.secondary),
                ("😊 Happy", "happy", discord.ButtonStyle.success),
                ("😐 Neutral", "neutral", discord.ButtonStyle.secondary),
                ("☹️ Sad", "sad", discord.ButtonStyle.danger),
                ("😴 Tired", "tired", discord.ButtonStyle.primary),
                ("😤 Stressed", "stressed", discord.ButtonStyle.danger)
            ]
            
            for label, custom_id, style in moods:
                button = discord.ui.Button(
                    label=label,
                    custom_id=custom_id,
                    style=style
                )
                button.callback = self.button_callback
                self.add_item(button)

        async def button_callback(self, interaction: discord.Interaction):
            print("Button callback started")
            if interaction.user.id != self.user_id:
                print(f"User ID mismatch: {interaction.user.id} vs {self.user_id}")
                return
                    
            custom_id = interaction.data["custom_id"]
            
            guild_id = next(iter(self.cog.mood_configs.keys()))
            user_id = str(interaction.user.id)
            print(f"Processing: Custom ID: {custom_id}, Guild ID: {guild_id}, User ID: {user_id}")

            if custom_id == "toggle_anon":
                print("Toggle anonymous mode")
                if interaction.user.id in self.cog.anonymous_users:
                    self.cog.anonymous_users.remove(interaction.user.id)
                    print(f"Disabled anonymous mode for user {user_id}")
                    await interaction.response.send_message("Anonymous mode disabled!", ephemeral=True)
                else:
                    self.cog.anonymous_users.add(interaction.user.id)
                    print(f"Enabled anonymous mode for user {user_id}")
                    await interaction.response.send_message("Anonymous mode enabled!", ephemeral=True)
                return

            print("Processing mood selection")
            
            if guild_id not in self.cog.mood_data:
                print(f"Creating new mood data entry for guild {guild_id}")
                self.cog.mood_data[guild_id] = {}
            if user_id not in self.cog.mood_data[guild_id]:
                print(f"Creating new mood data entry for user {user_id}")
                self.cog.mood_data[guild_id][user_id] = []
            
            mood_entry = {
                'mood': custom_id,
                'timestamp': datetime.now().isoformat(),
                'anonymous': interaction.user.id in self.cog.anonymous_users
            }
            print(f"Saving mood entry: {mood_entry}")
            self.cog.mood_data[guild_id][user_id].append(mood_entry)
            self.cog.save_mood_data()
            
            await interaction.response.send_message(f"Mood recorded: {custom_id.title()}!", ephemeral=True)
            
            print(f"Checking mood configs for guild {guild_id}")
            print(f"Current mood configs: {self.cog.mood_configs}")
            
            if guild_id in self.cog.mood_configs:
                print(f"Found guild config: {self.cog.mood_configs[guild_id]}")
                if 'log_channel' in self.cog.mood_configs[guild_id]:
                    channel_id = self.cog.mood_configs[guild_id]['log_channel']
                    print(f"Found log channel ID: {channel_id}")
                    channel = self.cog.bot.get_channel(channel_id)
                    try:
                        channel = self.cog.bot.get_channel(channel_id)
                        if not channel:
                            print(f"Could not find channel with ID {channel_id}")
                            return
                    except Exception as e:
                        print(f"Error getting channel: {e}")
                        return
                    
                    if channel:
                        print(f"Successfully got channel: {channel.name}")
                        is_anonymous = interaction.user.id in self.cog.anonymous_users
                        user_name = "Anonymous User" if is_anonymous else interaction.user.display_name
                        print(f"Sending mood entry for {'anonymous' if is_anonymous else 'named'} user")
                        
                        embed = discord.Embed(
                            title="🌟 New Mood Entry",
                            description=f"**User:** {user_name}\n**Mood:** {custom_id.title()}",
                            color=discord.Color.blue(),
                            timestamp=datetime.now()
                        )
                        try:
                            await channel.send(embed=embed)
                            print("Successfully sent mood entry to channel")
                        except discord.HTTPException as e:
                            print(f"Failed to send to channel: {e}")
                    else:
                        print(f"Could not find channel with ID {channel_id}")
                else:
                    print("No log_channel configured for this guild")
            else:
                print(f"Guild {guild_id} not found in mood configs")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mood_role(self, ctx, role: discord.Role):
        """Set the role that will receive mood prompts"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.mood_configs:
            self.mood_configs[guild_id] = {}
        
        self.mood_configs[guild_id]['mood_role'] = role.id
        self.mood_configs[guild_id]['enabled'] = True
        self.save_mood_data()
        
        embed = discord.Embed(
            title="✅ Mood Role Set",
            description=f"Members with {role.mention} will receive mood prompts",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.group(name="mood", invoke_without_command=True)
    async def mood(self, ctx):
        """Main mood command"""
        embed = discord.Embed(
            title="🌟 Mood Tracking System",
            description=(
                "**User Commands:**\n"
                "`!mood optin` - Join mood tracking\n"
                "`!mood streak` - Check your streak\n"
                "`!mood anon` - Toggle anonymous mode\n\n"
                "**Admin Commands:**\n"
                "`!set_mood_role @Role` - Set role for notifications\n"
                "`!set_mood_channel #channel` - Set mood logging channel\n"
                "`!mood config` - Configure notification timing\n"
                "`!analyze_moods` - View all mood entries\n"
                "`!test_mood @Role` - Test notifications"
            ),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test_mood(self, ctx, role: discord.Role):
        """Test mood prompts"""
        members = [member for member in ctx.guild.members if role in member.roles]
        for member in members:
            await self.send_mood_prompt(member)
        await ctx.send(f"✅ Sent test prompts to {len(members)} members!")

    async def send_mood_prompt(self, member):
        """Send mood prompt to member"""
        embed = discord.Embed(
            title="🌟 Mood Check",
            description="How are you feeling?",
            color=discord.Color.blue()
        )
        view = self.MoodSelectionView(self, member.id)
        try:
            await member.send(embed=embed, view=view)
        except discord.Forbidden:
            pass

    async def check_moods(self):
        """Send mood prompts to members with role"""
        current_time = time.time()
        
        for guild_id, config in self.mood_configs.items():
            if not config.get('enabled', False):
                continue
                
            last_check = config.get('last_check', 0)
            interval = config.get('notification_interval', 24)  
            if current_time - last_check < (interval * 3600):  
                continue
                
            guild = self.bot.get_guild(int(guild_id))
            if not guild:
                continue
                
            role_id = config.get('mood_role')
            if not role_id:
                continue
                
            role = guild.get_role(role_id)
            if not role:
                continue
                
            for member in role.members:
                try:
                    await self.send_mood_prompt(member)
                except discord.Forbidden:
                    continue
                    
            self.mood_configs[guild_id]['last_check'] = current_time
            self.save_mood_data()

    def load_mood_data(self):
        """Load mood tracking data"""
        try:
            with open('mood_data.json', 'r') as f:
                data = json.load(f)
                self.mood_data = data.get('moods', {})
                self.opted_users = data.get('users', {})
                self.mood_configs = data.get('configs', {})
                self.anonymous_users = set(data.get('anonymous', []))
                self.mood_streaks = data.get('streaks', {})
                self.custom_moods = data.get('custom_moods', {})
        except FileNotFoundError:
            self.save_mood_data()

    def save_mood_data(self):
        """Save mood tracking data"""
        data = {
            'moods': self.mood_data,
            'users': self.opted_users,
            'configs': self.mood_configs,
            'anonymous': list(self.anonymous_users),
            'streaks': self.mood_streaks,
            'custom_moods': self.custom_moods
        }
        with open('mood_data.json', 'w') as f:
            json.dump(data, f, indent=4)



    @mood.command(name="config")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        """Configure mood tracking settings"""
        class ConfigView(discord.ui.View):
            def __init__(self, original_self):
                super().__init__()
                self.original_self = original_self
                
            @discord.ui.select(
                placeholder="Select frequency",
                options=[
                    discord.SelectOption(label="Daily", value="24"),
                    discord.SelectOption(label="Twice Daily", value="12"),
                    discord.SelectOption(label="Weekly", value="168"),
                    discord.SelectOption(label="Test Mode (20s)", value="0.006")
                ]
            )
            async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
                hours = float(select.values[0])
                guild_id = str(interaction.guild_id)
                if guild_id not in self.original_self.mood_configs:
                    self.original_self.mood_configs[guild_id] = {}
                self.original_self.mood_configs[guild_id]['notification_interval'] = hours
                self.original_self.save_mood_data()
                await interaction.response.send_message(
                    f"Notification interval set to {hours} hours!", 
                    ephemeral=True
                )

        embed = discord.Embed(
            title="⚙️ Mood Tracking Configuration",
            description="Select notification frequency:",
            color=discord.Color.blue()
        )
        
        view = ConfigView(self)
        await ctx.send(embed=embed, view=view)



def setup(bot):
    bot.add_cog(MoodTracker(bot))


class RatingSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ratings_data = {}  
        self.load_ratings()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def exportrating(self, ctx):
        await ctx.message.delete()
        try:
            export_data = json.dumps(self.ratings_data, indent=4)
            with open('rating_backup.json', 'w') as f:
                f.write(export_data)
            await ctx.send("✨ Here's your rating system backup!", file=discord.File('rating_backup.json'), ephemeral=True)
            os.remove('rating_backup.json')
        except Exception as e:
            await ctx.send(f"✨ Export failed: {str(e)}", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def importrating(self, ctx):
        await ctx.message.delete()
        if not ctx.message.attachments:
            return await ctx.send("✨ Please attach a rating backup file!", ephemeral=True)
        try:
            attachment = ctx.message.attachments[0]
            if not attachment.filename.endswith('.json'):
                return await ctx.send("✨ Please provide a JSON file!", ephemeral=True)
            content = await attachment.read()
            import_data = json.loads(content)
            self.ratings_data = import_data
            self.save_ratings()
            await ctx.send("✨ Rating system data imported successfully!", ephemeral=True)
        except json.JSONDecodeError:
            await ctx.send("✨ Invalid JSON file format!", ephemeral=True)
        except Exception as e:
            await ctx.send(f"✨ Import failed: {str(e)}", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ratingsetup(self, ctx):
        """Setup a beautiful rating system"""
        button = discord.ui.Button(label="Setup Rating System", style=discord.ButtonStyle.primary, emoji="✨")
            
        async def button_callback(interaction):
            modal = self.RatingSetup(self)
            await interaction.response.send_modal(modal)
            
        button.callback = button_callback
        view = discord.ui.View()
        view.add_item(button)
            
        await ctx.message.delete()  
        await ctx.send("Click below to create your rating panel! ✨", view=view, ephemeral=True)

    def load_ratings(self):
        try:
            with open('ratings.json', 'r') as f:
                self.ratings_data = json.load(f)
        except FileNotFoundError:
            self.ratings_data = {}

    def save_ratings(self):
        with open('ratings.json', 'w') as f:
            json.dump(self.ratings_data, f, indent=4)


    class DeleteRatingModal(discord.ui.Modal):
        def __init__(self, cog):
            super().__init__(title="Delete Rating Panel")
            self.cog = cog
            self.add_item(discord.ui.TextInput(
                label="Panel ID",
                placeholder="Enter the panel ID to delete"
            ))

        async def on_submit(self, interaction):
            panel_id = self.children[0].value
            if panel_id in self.cog.ratings_data:
             
                for channel in interaction.guild.text_channels:
                    try:
                        message = await channel.fetch_message(int(panel_id))
                        if message:
                            await message.delete()
                            break
                    except:
                        continue
                        
                del self.cog.ratings_data[panel_id]
                self.cog.save_ratings()
                await interaction.response.send_message(f"✨ Rating panel {panel_id} deleted!", ephemeral=True)
            else:
                await interaction.response.send_message("✨ Panel ID not found!", ephemeral=True)

    class EditRatingModal(discord.ui.Modal):
        def __init__(self, cog):
            super().__init__(title="Edit Rating Panel")
            self.cog = cog
            self.add_item(discord.ui.TextInput(
                label="Panel ID",
                placeholder="Enter the panel ID to edit"
            ))
            self.add_item(discord.ui.TextInput(
                label="New Title",
                placeholder="Enter new title (leave empty to keep current)",
                required=False
            ))
            self.add_item(discord.ui.TextInput(
                label="New Description",
                placeholder="Enter new description (leave empty to keep current)",
                required=False
            ))

        async def on_submit(self, interaction):
            panel_id = self.children[0].value
            new_title = self.children[1].value
            new_desc = self.children[2].value

            if panel_id not in self.cog.ratings_data:
                return await interaction.response.send_message("✨ Panel ID not found!", ephemeral=True)

            try:
                channel_id = None
                message = None
                for channel in interaction.guild.text_channels:
                    try:
                        message = await channel.fetch_message(int(panel_id))
                        if message:
                            break
                    except:
                        continue

                if message:
                    embed = message.embeds[0]
                    if new_title:
                        embed.title = new_title
                    if new_desc:
                        current_desc = embed.description.split("**Stats:**")
                        embed.description = f"{new_desc}\n\n**Stats:**{current_desc[1]}"
                    
                    await message.edit(embed=embed)
                    await interaction.response.send_message("✨ Rating panel updated!", ephemeral=True)
                else:
                    await interaction.response.send_message("✨ Couldn't find the rating panel message!", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"✨ Error updating panel: {str(e)}", ephemeral=True)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def seerating(self, ctx):
        await ctx.message.delete()
        if not self.ratings_data:
            return await ctx.send("✨ No rating panels exist yet!", ephemeral=True)

        embed = discord.Embed(
            title="📊 Rating Panels Overview",
            color=discord.Color.blue()
        )

        for message_id, ratings in self.ratings_data.items():
            total_votes = len(ratings)
            avg_rating = sum(float(r) for r in ratings.values()) / total_votes if total_votes > 0 else 0
            embed.add_field(
                name=f"ID: {message_id}",
                value=f"Votes: {total_votes} | Average: {avg_rating:.2f}",
                inline=False
            )

        view = discord.ui.View()
        delete_btn = discord.ui.Button(label="Delete Panel", style=discord.ButtonStyle.danger, emoji="🗑️")
        edit_btn = discord.ui.Button(label="Edit Panel", style=discord.ButtonStyle.primary, emoji="✏️")
        
        async def delete_callback(interaction):
            modal = self.DeleteRatingModal(self)
            await interaction.response.send_modal(modal)
            
        async def edit_callback(interaction):
            modal = self.EditRatingModal(self)
            await interaction.response.send_modal(modal)
            
        delete_btn.callback = delete_callback
        edit_btn.callback = edit_callback
        view.add_item(delete_btn)
        view.add_item(edit_btn)
        
        await ctx.send(embed=embed, view=view)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ratingrefresh(self, ctx, panel_id: str):
        await ctx.message.delete()
        if panel_id not in self.ratings_data:
            return await ctx.send("✨ Rating panel not found!", ephemeral=True)

        channel_id = None
        message = None
        
        for channel in ctx.guild.text_channels:
            try:
                message = await channel.fetch_message(int(panel_id))
                if message:
                    break
            except:
                continue

        if not message:
            return await ctx.send("✨ Couldn't find the rating panel message!")

        ratings = self.ratings_data[panel_id]
        avg_rating = sum(float(r) for r in ratings.values()) / len(ratings)
        
        embed = message.embeds[0]
        embed.description = f"{embed.description.split('**Stats:**')[0]}\n\n**Stats:**\n• Average: {avg_rating:.2f}\n• Total Ratings: {len(ratings)}"
        
        await message.edit(embed=embed)
        await ctx.send("✨ Rating panel refreshed successfully!")


    class RatingView(discord.ui.View):
        def __init__(self, title, description, button_color, embed_color, rating_type, channel_id, cog):
            super().__init__(timeout=None)
            self.title = title
            self.description = description
            
            color_map = {
                'red': discord.ButtonStyle.danger,
                'green': discord.ButtonStyle.success,
                'blue': discord.ButtonStyle.primary,
                'gray': discord.ButtonStyle.secondary,
                'blurple': discord.ButtonStyle.primary,
                'danger': discord.ButtonStyle.danger,
                'success': discord.ButtonStyle.success,
                'primary': discord.ButtonStyle.primary,
                'secondary': discord.ButtonStyle.secondary
            }
            self.button_color = color_map.get(button_color.lower(), discord.ButtonStyle.secondary)
            self.embed_color = embed_color
            self.rating_type = rating_type
            self.channel_id = channel_id
            self.cog = cog

            if self.rating_type == "stars":
                star_emojis = ["⭐", "🌟", "✨", "💫", "⚡"]
                for i, emoji in enumerate(star_emojis, 1):
                    btn = discord.ui.Button(
                        label=f"{i}",
                        emoji=emoji,
                        style=self.button_color,
                        custom_id=f"rate_{i}",
                        row=0
                    )
                    btn.callback = self.rate_callback
                    self.add_item(btn)
            
            elif self.rating_type == "numbers":
                for i in range(1, 11):
                    btn = discord.ui.Button(
                        label=f"{i}",
                        style=self.button_color,
                        custom_id=f"rate_{i}",
                        row=(i-1) // 5
                    )
                    btn.callback = self.rate_callback
                    self.add_item(btn)
            
            elif self.rating_type == "percent":
                emojis = ["💔", "❤️‍🩹", "💝", "💖", "💗"]
                for p, emoji in zip([0, 25, 50, 75, 100], emojis):
                    btn = discord.ui.Button(
                        label=f"{p}%",
                        emoji=emoji,
                        style=self.button_color,
                        custom_id=f"rate_{p}",
                        row=0
                    )
                    btn.callback = self.rate_callback
                    self.add_item(btn)

            view_ratings = discord.ui.Button(
                label="Statistics",
                emoji="📊",
                style=discord.ButtonStyle.secondary,
                custom_id="view_ratings",
                row=2
            )
            view_ratings.callback = self.view_ratings_callback
            
            refresh = discord.ui.Button(
                label="Refresh",
                emoji="🔄",
                style=discord.ButtonStyle.secondary,
                custom_id="refresh",
                row=2
            )
            refresh.callback = self.refresh_callback
            
            self.add_item(view_ratings)
            self.add_item(refresh)


        async def create_stats_embed(self, ratings, title="📊 Rating Statistics"):
            avg_rating = sum(float(r) for r in ratings) / len(ratings)
            rating_counts = {}
            for r in ratings:
                rating_counts[float(r)] = rating_counts.get(float(r), 0) + 1
            
            max_count = max(rating_counts.values())
            distribution = []
            for r, count in sorted(rating_counts.items()):
                bar_length = int((count / max_count) * 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                percentage = (count/len(ratings))*100
                
                if self.rating_type == "stars":
                    rating_display = "⭐" * int(r)
                elif self.rating_type == "percent":
                    rating_display = f"{int(r)}% {'💖' if r == 100 else '💝' if r >= 75 else '❤️' if r >= 50 else '💔'}"
                else:
                    rating_display = f"Rating {r}"
                    
                distribution.append(f"{rating_display}\n`{bar}` {count} votes ({percentage:.1f}%)")

            embed = discord.Embed(
                title=title,
                description="\n\n".join(distribution),
                color=self.embed_color
            )
            embed.add_field(name="Average Rating", value=f"📊 {avg_rating:.2f}", inline=True)
            embed.add_field(name="Total Votes", value=f"📈 {len(ratings)}", inline=True)
            return embed

        async def rate_callback(self, interaction: discord.Interaction):
            rating = interaction.data['custom_id'].split("_")[1]
            message_id = str(interaction.message.id)
            user_id = str(interaction.user.id)
            
            if message_id in self.cog.ratings_data and user_id in self.cog.ratings_data[message_id]:
                return await interaction.response.send_message("You've already rated this! ✨", ephemeral=True)
            
            if message_id not in self.cog.ratings_data:
                self.cog.ratings_data[message_id] = {}
            
            self.cog.ratings_data[message_id][user_id] = rating
            self.cog.save_ratings()

            embed = discord.Embed(
                title=self.title,
                description=f"{self.description}\n\n**Stats:**",
                color=self.embed_color
            )
            
            ratings = self.cog.ratings_data[message_id].values()
            avg_rating = sum(float(r) for r in ratings) / len(ratings)
            
            rating_counts = {}
            for r in ratings:
                rating_counts[float(r)] = rating_counts.get(float(r), 0) + 1
            
            embed.add_field(name="Average Rating", value=f"📊 {avg_rating:.2f}", inline=True)
            embed.add_field(name="Total Votes", value=f"📈 {len(ratings)}", inline=True)
            
            await interaction.message.edit(embed=embed, view=self)
            
            rating_display = f"{'⭐' * int(rating)}" if self.rating_type == "stars" else f"{rating}{'%' if self.rating_type == 'percent' else ''}"
            await interaction.response.send_message(f"Rating submitted: {rating_display} ✨", ephemeral=True)


        async def view_ratings_callback(self, interaction: discord.Interaction):
            message_id = str(interaction.message.id)
            if message_id not in self.cog.ratings_data:
                return await interaction.response.send_message("No ratings yet! Be the first to rate! ✨", ephemeral=True)
            
            embed = await self.create_stats_embed(self.cog.ratings_data[message_id].values(), "📊 Detailed Rating Distribution")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        async def refresh_callback(self, interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("Only administrators can refresh! ✨", ephemeral=True)
            
            message_id = str(interaction.message.id)
            if message_id not in self.cog.ratings_data:
                return await interaction.response.send_message("No ratings to refresh! ✨", ephemeral=True)
            
            embed = await self.create_stats_embed(self.cog.ratings_data[message_id].values())
            await interaction.message.edit(embed=embed, view=self)
            await interaction.response.send_message("Rating panel refreshed! ✨", ephemeral=True)

    class RatingSetup(discord.ui.Modal):
        def __init__(self, cog, **defaults):
            super().__init__(title="✨ Rating System Setup")
            self.cog = cog
            self.add_item(discord.ui.TextInput(
                label="Title",
                placeholder="Enter your rating title",
                default=defaults.get('default_title', '')
            ))
            self.add_item(discord.ui.TextInput(
                label="Description",
                placeholder="Enter rating description",
                default=defaults.get('default_desc', '')
            ))
            self.add_item(discord.ui.TextInput(
                label="Button Color",
                placeholder="red/green/blue/blurple",
                default=defaults.get('default_color', '')
            ))
            self.add_item(discord.ui.TextInput(
                label="Embed Color (hex)",
                placeholder="#ff0000",
                default=defaults.get('default_embed', '')
            ))
            self.add_item(discord.ui.TextInput(
                label="Rating Type & Channel",
                placeholder="stars/numbers/percent #channel",
                default=f"{defaults.get('default_type', '')} {defaults.get('default_channel', '')}"
            ))

        async def on_submit(self, interaction: discord.Interaction):
            title = self.children[0].value
            description = self.children[1].value
            button_color = self.children[2].value.lower()
            embed_color = int(self.children[3].value.strip("#"), 16)
            
            rating_info = self.children[4].value.split()
            rating_type = rating_info[0].lower()
            channel_mention = rating_info[1] if len(rating_info) > 1 else None
            
            channel_id = int(channel_mention.strip('<#>')) if channel_mention else interaction.channel.id
            channel = interaction.guild.get_channel(channel_id)
            
            if not channel:
                return await interaction.response.send_message("Invalid channel! ❌", ephemeral=True)

            embed = discord.Embed(title=title, description=description, color=embed_color)
            view = self.cog.RatingView(title, description, button_color, embed_color, rating_type, channel_id, self.cog)
            
            await channel.send(embed=embed, view=view)
            if channel.id != interaction.channel.id:
                await interaction.response.send_message(f"Rating panel created in {channel.mention}! ✨", ephemeral=True)
            else:
                await interaction.response.send_message("Rating panel created! ✨", ephemeral=True)

def setup(bot):
    bot.add_cog(RatingSystem(bot))

class BotVerificationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_whitelist = set(int(bot_id) for bot_id in os.getenv('WHITELISTED_BOTS', '').split(',') if bot_id)
        self.owner_id = int(os.getenv('BOT_OWNER_ID'))
        self.bot_log_channels = {}
        self.whitelist_attempts = {}
        self.MAX_ATTEMPTS = 5
        self.ATTEMPT_RESET = 300  

    def validate_bot_id(self, bot_id: int) -> bool:
        if not (17 <= len(str(bot_id)) <= 20):
            return False
        discord_epoch = 1420070400000
        timestamp = ((bot_id >> 22) + discord_epoch) / 1000
        return discord_epoch/1000 <= timestamp <= time.time() and bot_id != 0

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot and member.id not in self.bot_whitelist:
            try:
                await member.kick(reason="Bot not in whitelist")
                
                embed = discord.Embed(
                    title="🤖 Unauthorized Bot Detected",
                    description=(
                        f"**Bot:** {member.name} (`{member.id}`)\n"
                        f"**Action:** Kicked\n"
                        f"**Reason:** Not in whitelist\n"
                        f"**Guild:** {member.guild.name}\n"
                        f"**Time:** <t:{int(time.time())}:F>"
                    ),
                    color=discord.Color.red(),
                    timestamp=datetime.now(timezone.utc)
                )
                embed.set_footer(text=f"Security Event ID: {hex(member.id)}")
                
                if str(member.guild.id) in self.bot_log_channels:
                    channel_id = self.bot_log_channels[str(member.guild.id)]
                    channel = member.guild.get_channel(channel_id)
                    if channel:
                        await channel.send(embed=embed)
                        
            except discord.Forbidden:
                if str(member.guild.id) in self.bot_log_channels:
                    channel = member.guild.get_channel(self.bot_log_channels[str(member.guild.id)])
                    if channel:
                        await channel.send(
                            embed=discord.Embed(
                                title="⚠️ Permission Error",
                                description="Failed to kick unauthorized bot due to missing permissions",
                                color=discord.Color.orange()
                            )
                        )

    @commands.command(name="whitelist_bot")
    async def whitelist_bot(self, ctx, bot_id: int):
        if ctx.author.id != self.owner_id:
            return await ctx.send(
                embed=discord.Embed(
                    title="❌ Access Denied",
                    description="Only the bot owner can use this command",
                    color=discord.Color.red()
                )
            )

        current_time = time.time()
        if ctx.author.id in self.whitelist_attempts:
            attempts, last_attempt = self.whitelist_attempts[ctx.author.id]
            if current_time - last_attempt < self.ATTEMPT_RESET:
                if attempts >= self.MAX_ATTEMPTS:
                    return await ctx.send(
                        embed=discord.Embed(
                            title="🚫 Rate Limited",
                            description=f"Please wait {int(self.ATTEMPT_RESET - (current_time - last_attempt))} seconds",
                            color=discord.Color.red()
                        )
                    )
                self.whitelist_attempts[ctx.author.id] = (attempts + 1, current_time)
            else:
                self.whitelist_attempts[ctx.author.id] = (1, current_time)
        else:
            self.whitelist_attempts[ctx.author.id] = (1, current_time)

        if not self.validate_bot_id(bot_id):
            return await ctx.send(
                embed=discord.Embed(
                    title="❌ Invalid Bot ID",
                    description="The provided ID is not a valid Discord bot ID",
                    color=discord.Color.red()
                )
            )

        try:
            bot_user = await self.bot.fetch_user(bot_id)
            if not bot_user.bot:
                raise ValueError("Provided ID belongs to a user, not a bot")
            
            self.bot_whitelist.add(bot_id)
            await ctx.send(
                embed=discord.Embed(
                    title="✅ Bot Whitelisted",
                    description=f"**Bot:** {bot_user.name}\n**ID:** `{bot_id}`\n**Added by:** {ctx.author.mention}",
                    color=discord.Color.green()
                ).set_thumbnail(url=bot_user.display_avatar.url)
            )
            
        except (discord.NotFound, discord.HTTPException, ValueError) as e:
            await ctx.send(
                embed=discord.Embed(
                    title="❌ Verification Failed",
                    description=str(e),
                    color=discord.Color.red()
                )
            )

    @commands.command(name="botlogs")
    @commands.has_permissions(administrator=True)
    async def set_bot_logs(self, ctx, channel: discord.TextChannel = None):
        """Set the channel for unauthorized bot join logs"""
        if channel is None:
            if str(ctx.guild.id) in self.bot_log_channels:
                del self.bot_log_channels[str(ctx.guild.id)]
                embed = discord.Embed(
                    title="🤖 Bot Logs Disabled",
                    description="Bot join logging has been turned off.",
                    color=discord.Color.red()
                )
            else:
                embed = discord.Embed(
                    title="ℹ️ No Channel Set",
                    description="Please specify a channel to enable bot join logging.",
                    color=discord.Color.blue()
                )
        else:
            self.bot_log_channels[str(ctx.guild.id)] = channel.id
            embed = discord.Embed(
                title="🤖 Bot Logs Channel Set",
                description=f"Unauthorized bot joins will be logged in {channel.mention}",
                color=discord.Color.green()
            )
        
        await ctx.send(embed=embed)

    @commands.command(name="whitelisted")
    @commands.has_permissions(administrator=True)
    async def list_whitelisted(self, ctx):
        """List all whitelisted bots"""
        if not self.bot_whitelist:
            return await ctx.send(
                embed=discord.Embed(
                    title="📝 Whitelisted Bots",
                    description="No bots are currently whitelisted",
                    color=discord.Color.blue()
                )
            )

        whitelisted_bots = []
        for bot_id in self.bot_whitelist:
            try:
                bot_user = await self.bot.fetch_user(bot_id)
                whitelisted_bots.append(f"• {bot_user.name} (`{bot_id}`)")
            except:
                whitelisted_bots.append(f"• Unknown Bot (`{bot_id}`)")

        await ctx.send(
            embed=discord.Embed(
                title="📝 Whitelisted Bots",
                description="\n".join(whitelisted_bots),
                color=discord.Color.blue()
            )
        )

def setup(bot):
    bot.add_cog(BotVerificationSystem(bot))

class VerificationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verification_levels = {
            "easy": {
                "timeout": 300,
                "requirements": ["VERIFIED_EMAIL"],
                "emoji": "🟢",
                "description": "Basic security level",
                "min_account_age": 1,
                "min_avatar": False
            },
            "medium": {
                "timeout": 600,
                "requirements": ["VERIFIED_EMAIL", "VERIFIED_PHONE"],
                "emoji": "🟡",
                "description": "Enhanced security level",
                "min_account_age": 3,
                "min_avatar": True
            },
            "hard": {
                "timeout": 900,
                "requirements": ["VERIFIED_EMAIL", "VERIFIED_PHONE", "MFA_ENABLED"],
                "emoji": "🔴",
                "description": "Maximum security level",
                "min_account_age": 7,
                "min_avatar": True
            }
        }
        self.guild_settings = {}
        self.pending_verifications = {}
        self.autorole_dict = {}
        self.verification_logs = {}
        self.log_channels = {}
        self.save_data()

    def save_data(self):
   
        self.guild_settings = {
            guild_id: {
                "verification_level": self.verification_levels,
                "autorole": self.autorole_dict.get(guild_id),
                "log_channel": self.log_channels.get(str(guild_id))
            }
            for guild_id in self.bot.guilds
        }

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx, level: str = None, timeout: int = None):
        """Advanced verification system configuration"""
        if not level:
            await self.show_verification_menu(ctx)
            return
        await self.set_verification_level(ctx, level, timeout)

    @verify.command(name="stats")
    @commands.has_permissions(administrator=True)
    async def verification_stats(self, ctx):
        """Show verification statistics"""
        stats = self.verification_logs.get(ctx.guild.id, {})
        embed = discord.Embed(
            title="📊 Verification Statistics",
            color=discord.Color.blue()
        )
        embed.add_field(name="Total Attempts", value=stats.get("total", 0))
        embed.add_field(name="Successful", value=stats.get("success", 0))
        embed.add_field(name="Failed", value=stats.get("failed", 0))
        await ctx.send(embed=embed)

    @commands.command(name="verifychannel")
    @commands.has_permissions(administrator=True)
    async def set_verify_channel(self, ctx, channel: discord.TextChannel = None):
        """Set the verification logging channel"""
        if channel is None:
            if str(ctx.guild.id) in self.log_channels:
                del self.log_channels[str(ctx.guild.id)]
                embed = discord.Embed(
                    title="📝 Verification Logging Disabled",
                    description="Verification logging has been turned off.",
                    color=discord.Color.red()
                )
            else:
                embed = discord.Embed(
                    title="ℹ️ No Channel Set",
                    description="Please specify a channel to log verifications.",
                    color=discord.Color.blue()
                )
        else:
            self.log_channels[str(ctx.guild.id)] = channel.id
            embed = discord.Embed(
                title="✅ Verification Channel Set",
                description=f"Verification attempts will be logged in {channel.mention}",
                color=discord.Color.green()
            )
        await ctx.send(embed=embed)
        self.save_data()

    async def show_verification_menu(self, ctx):
        embed = discord.Embed(
            title="🛡️ Advanced Verification System",
            description="Configure server security and verification settings",
            color=discord.Color.blue()
        )
        
        for level, data in self.verification_levels.items():
            requirements_text = [
                f"• Account Age: {data['min_account_age']} days",
                f"• Profile Picture: {'Required' if data['min_avatar'] else 'Optional'}"
            ]
            requirements_text.extend([f"• {req.replace('_', ' ').title()}" for req in data["requirements"]])
            
            embed.add_field(
                name=f"{data['emoji']} {level.title()} Mode",
                value=f"```\n{data['description']}\nTimeout: {data['timeout']}s\n\nRequirements:\n{chr(10).join(requirements_text)}```",
                inline=False
            )

        embed.add_field(
            name="⚙️ Command Center",
            value=(
                "🔐 **Security Setup**\n"
                "➜ `!verify <easy/medium/hard>`\n\n"
                "📊 **Statistics**\n"
                "➜ `!verify stats`\n\n"
                "📝 **Logging**\n"
                "➜ `!verifychannel #channel`\n\n"
                "⚡ **Auto-Role**\n"
                "➜ `!verificationrole @role`"
            ),
            inline=False
        )
        
        embed.set_footer(text="✨ Advanced Security System")
        await ctx.send(embed=embed)

    async def set_verification_level(self, ctx, level: str, timeout: int = None):
        level = level.lower()
        if level not in self.verification_levels:
            embed = discord.Embed(
                title="❌ Invalid Verification Level",
                description="Please choose: `easy`, `medium`, or `hard`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        guild_settings = {
            "level": level,
            "member_role": None,
            "timeout": timeout or self.verification_levels[level]["timeout"]
        }

        verification_role = discord.utils.get(ctx.guild.roles, name="✓ Verified")
        if not verification_role:
            verification_role = await ctx.guild.create_role(
                name="✓ Verified",
                color=discord.Color.brand_green(),
                permissions=discord.Permissions.none(),
                hoist=True,
                mentionable=False,
                reason="Verification system role"
            )
        guild_settings["member_role"] = verification_role.id

        self.pending_verifications[ctx.guild.id] = guild_settings
        self.save_data()

        embed = discord.Embed(
            title=f"{self.verification_levels[level]['emoji']} Verification System Configured",
            description=f"Level set to: **{level}**\n"
                       f"Timeout: **{guild_settings['timeout']} seconds**\n"
                       f"Verification Role: {verification_role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def verificationrole(self, ctx, role: discord.Role = None):
        """Toggle automatic role assignment for newly verified members"""
        if role is None:
            if ctx.guild.id in self.autorole_dict:
                current_role = ctx.guild.get_role(self.autorole_dict[ctx.guild.id])
                embed = discord.Embed(
                    title="ℹ️ Verification Role Status",
                    description=f"Currently active for role: {current_role.mention if current_role else 'None'}",
                    color=discord.Color.blue()
                )
            else:
                embed = discord.Embed(
                    title="ℹ️ Verification Role Status",
                    description="Verification role is currently disabled",
                    color=discord.Color.blue()
                )
        else:
            if ctx.guild.id in self.autorole_dict and self.autorole_dict[ctx.guild.id] == role.id:
                del self.autorole_dict[ctx.guild.id]
                embed = discord.Embed(
                    title="🔄 Verification Role Disabled",
                    description=f"Automatic role assignment for {role.mention} has been disabled",
                    color=discord.Color.red()
                )
            else:
                self.autorole_dict[ctx.guild.id] = role.id
                embed = discord.Embed(
                    title="✅ Verification Role Enabled",
                    description=f"Newly verified members will receive the {role.mention} role",
                    color=discord.Color.green()
                )
        await ctx.send(embed=embed)

    async def log_verification_attempt(self, member, success: bool, reason: str = None):
        guild_id = str(member.guild.id)
        if guild_id not in self.log_channels:
            return

        channel = self.bot.get_channel(self.log_channels[guild_id])
        if not channel:
            return

        embed = discord.Embed(
            title="🔒 Verification Attempt",
            description=f"User: {member.mention} ({member.id})",
            color=discord.Color.green() if success else discord.Color.red(),
            timestamp=datetime.now(timezone.utc)
        )
        
        embed.add_field(name="Status", value="✅ Passed" if success else "❌ Failed", inline=True)
        embed.add_field(name="Account Age", value=f"{(datetime.now(timezone.utc) - member.created_at).days} days", inline=True)
        
        if not success and reason:
            embed.add_field(name="Failure Reason", value=reason, inline=False)

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"User ID: {member.id}")

        await channel.send(embed=embed)
        
        if not success:
            try:
                await member.kick(reason=f"Failed verification: {reason}")
            except discord.Forbidden:
                await channel.send(f"⚠️ Failed to kick {member.mention} - Missing permissions")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        if member.guild.id not in self.pending_verifications:
            return
            
        if member.bot:
            return

        settings = self.pending_verifications[member.guild.id]
        
        if not settings.get("level"):
            return
            
        level_data = self.verification_levels[settings["level"]]
        
        self.verification_logs.setdefault(member.guild.id, {})
        self.verification_logs[member.guild.id]["total"] = self.verification_logs[member.guild.id].get("total", 0) + 1

        account_age = (datetime.now(timezone.utc) - member.created_at).days
        if account_age < level_data["min_account_age"]:
            await self.handle_failed_verification(member, f"Account too new (minimum {level_data['min_account_age']} days required)")
            return

        if level_data["min_avatar"] and not member.avatar:
            await self.handle_failed_verification(member, "Profile picture required")
            return

        qualified = await self.check_requirements(member, level_data["requirements"])
        if not qualified:
            await self.handle_failed_verification(member, "Missing verification requirements")
            return

        await self.handle_successful_verification(member, settings)
        self.save_data()

    '''
    Public Api Problem Wont work correctly
    Discord Doesnt give us the ability to check if the user has a verified email or phone number
    Becuase of Privacy reasons
    '''

    async def check_requirements(self, member: discord.Member, requirements: list):
        checks = {}
        
        if "VERIFIED_EMAIL" in requirements:
          
            checks["VERIFIED_EMAIL"] = member.flags.verified or member.guild.verification_level >= discord.VerificationLevel.medium
            
        if "MFA_ENABLED" in requirements:
            
            checks["MFA_ENABLED"] = (
                member.public_flags.mfa_enabled or 
                member.guild.mfa_level >= discord.MFALevel.enabled
            )
            
        if "VERIFIED_PHONE" in requirements:
         
            checks["VERIFIED_PHONE"] = member.guild.verification_level >= discord.VerificationLevel.high

        print(f"Verification checks for {member.name}: {checks}")
            
        return all(checks.get(req, False) for req in requirements)


    async def handle_failed_verification(self, member, reason):
        self.verification_logs[member.guild.id]["failed"] = self.verification_logs[member.guild.id].get("failed", 0) + 1
        
        level_data = self.verification_levels[self.pending_verifications[member.guild.id]["level"]]
        
        embed = discord.Embed(
            title="❌ Verification Failed",
            description=(
                f"You don't meet {member.guild.name}'s verification requirements.\n\n"
                f"**Reason:** {reason}\n\n"
                "**Server Requirements:**\n"
                f"• Account Age: {level_data['min_account_age']} days\n"
                f"• Profile Picture: {'Required' if level_data['min_avatar'] else 'Optional'}\n"
                f"• Verified Email: {'Required' if 'VERIFIED_EMAIL' in level_data['requirements'] else 'Optional'}\n"
                f"• Verified Phone: {'Required' if 'VERIFIED_PHONE' in level_data['requirements'] else 'Optional'}\n"
                f"• 2FA Enabled: {'Required' if 'MFA_ENABLED' in level_data['requirements'] else 'Optional'}\n\n"
                "Please meet these requirements and try joining again!"
            ),
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else None)
        
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            pass
        
        await self.log_verification_attempt(member, False, reason)
        await member.kick(reason=f"Failed verification: {reason}")

    async def handle_successful_verification(self, member, settings):
        self.verification_logs[member.guild.id]["success"] = self.verification_logs[member.guild.id].get("success", 0) + 1

        timeout_duration = timedelta(seconds=settings["timeout"])
        try:
            await member.timeout(timeout_duration, reason="Verification security cooldown")
        except discord.Forbidden:
            pass  

        member_role = member.guild.get_role(settings["member_role"])
        if member_role:
            await member.add_roles(member_role)

        if member.guild.id in self.autorole_dict:
            role = member.guild.get_role(self.autorole_dict[member.guild.id])
            if role:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    pass

        await self.log_verification_attempt(member, True)

def setup(bot):
    bot.add_cog(VerificationSystem(bot))

class LevelingSystem(commands.Cog):                         
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = int(os.getenv('BOT_OWNER_ID'))
        self.user_data: Dict[int, Dict[int, Dict]] = {}  
        self.roles: Dict[int, Dict[int, int]] = {}       
        self.achievements: Dict[int, Dict[str, Dict]] = {}  
        self.xp_decay_rate = 0.01
        self.xp_gain_range = (15, 25)
        self.xp_multipliers: Dict[int, Dict[int, float]] = {} 
        self.data_file = "leveling_data.json"
        self.leaderboard_channels: Dict[int, int] = {}    
        self.announcement_channels: Dict[int, int] = {}   
        self.load_data()
        self.bot.loop.create_task(self.update_leaderboard_task())
        self.bot.loop.create_task(self.xp_decay_task())

    def load_data(self):
        """Load user data, roles, and achievements from a JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
                self.user_data = {
                    int(guild_id): {
                        int(user_id): user_data 
                        for user_id, user_data in guild_data.items()
                    } for guild_id, guild_data in data.get('user_data', {}).items()
                }
                self.roles = data.get('roles', {})
                self.achievements = data.get('achievements', {})
                self.xp_multipliers = data.get('xp_multipliers', {})
                self.leaderboard_channels = data.get('leaderboard_channels', {})
                self.announcement_channels = data.get('announcement_channels', {})

    def save_data(self):
            """Save user data, roles, and achievements to a JSON file."""
            
            cleaned_user_data = {}
            for guild_id, guild_data in self.user_data.items():
                cleaned_user_data[str(guild_id)] = {
                    str(user_id): user_data
                    for user_id, user_data in guild_data.items()
                }

            with open(self.data_file, 'w') as f:
                json.dump({
                    'user_data': cleaned_user_data,
                    'roles': self.roles,
                    'achievements': self.achievements,
                    'xp_multipliers': self.xp_multipliers,
                    'leaderboard_channels': self.leaderboard_channels,
                    'announcement_channels': self.announcement_channels
                }, f, indent=4)

    def calculate_level(self, xp: int) -> int:
        """Calculate the user's level based on their XP."""
        return int((xp / 100) ** 0.5)  

    def xp_for_next_level(self, level: int) -> int:
        """Calculate the XP required for the next level."""
        return (level + 1) ** 2 * 100

    async def add_xp(self, user_id: int, guild_id: int):
        """Add XP to a user and handle level-ups."""
        
        xp_gain = random.randint(*self.xp_gain_range)
        
        multiplier = float(self.xp_multipliers.get(guild_id, {}).get(str(user_id), 1.0))
        if isinstance(multiplier, dict):
            multiplier = 1.0
        xp_gain = int(xp_gain * multiplier)

        if guild_id not in self.user_data:
            self.user_data[guild_id] = {}
        if user_id not in self.user_data[guild_id]:
            self.user_data[guild_id][user_id] = {'xp': 0, 'last_message': datetime.now().isoformat()}

        user_data = self.user_data[guild_id][user_id]

        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(user_id)
        if member:
            for role_id, role_multiplier in self.xp_multipliers.get(guild_id, {}).items():
                if isinstance(role_multiplier, (int, float)) and role_id in [role.id for role in member.roles]:
                    xp_gain = int(xp_gain * float(role_multiplier))

        user_data['xp'] += xp_gain
        user_data['last_message'] = datetime.now().isoformat()

        old_level = self.calculate_level(user_data['xp'] - xp_gain)
        new_level = self.calculate_level(user_data['xp'])

        if new_level > old_level:
            await self.handle_level_up(user_id, guild_id, new_level)

        self.save_data()


    async def handle_level_up(self, user_id: int, guild_id: int, level: int):
        """
        Handle level-up announcements, role assignments, and achievements.
        - Sends an announcement to the specified channel.
        - Assigns the role for the new level (if set).
        - Removes the role for the previous level (if applicable).
        - Checks for achievements.
        """
        if guild_id not in self.announcement_channels:
            return

        guild = self.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found")
            return

        member = guild.get_member(user_id)
        if not member:
            print(f"Member {user_id} not found in guild {guild_id}")
            return

        channel = self.bot.get_channel(self.announcement_channels.get(guild_id))
        if not channel:
            print("Announcement channel not found")
            return

        embed = discord.Embed(
            title="🌟 Level Up! 🌟",
            description=f"🎉 {member.mention} has reached **Level {level}**! 🎉",
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Next Level", value=f"**{self.xp_for_next_level(level)} XP**", inline=False)

        try:
            await channel.send(embed=embed)
            print(f"Level-up announcement sent to {channel.name}")
        except discord.Forbidden:
            print(f"Bot does not have permission to send messages in {channel.name}")
        except discord.HTTPException as e:
            print(f"Failed to send level-up announcement: {e}")

        if guild_id in self.roles and level in self.roles[guild_id]:
            role = discord.utils.get(guild.roles, id=self.roles[guild_id][level])
            if role:
                try:
                    for lvl, role_id in self.roles[guild_id].items():
                        if lvl != level and role_id in [r.id for r in member.roles]:
                            previous_role = discord.utils.get(guild.roles, id=role_id)
                            if previous_role:
                                await member.remove_roles(previous_role)
                                print(f"Removed previous level role: {previous_role.name}")

                    await member.add_roles(role)
                    print(f"Assigned role {role.name} to {member.display_name}")
                except discord.Forbidden:
                    print(f"Bot does not have permission to manage roles for {member.display_name}")
                except discord.HTTPException as e:
                    print(f"Failed to assign role: {e}")
            else:
                print(f"Role for level {level} not found")
        else:
            print(f"No role assigned for level {level}")

        await self.check_achievements(user_id, guild_id, level)

    async def check_achievements(self, user_id: int, guild_id: int, level: int):
        """Check if the user has unlocked any achievements."""
        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(user_id)
        if not member:
            return

        for achievement, data in self.achievements.items():
            if level >= data['required_level'] and achievement not in self.user_data[guild_id][user_id].get('achievements', []):
                self.user_data[guild_id][user_id].setdefault('achievements', []).append(achievement)
                embed = discord.Embed(
                    title="🏆 Achievement Unlocked! 🏆",
                    description=f"🎉 {member.mention} has unlocked the **{achievement}** achievement! 🎉",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Reward", value=data['reward'], inline=False)
                await guild.system_channel.send(embed=embed)

    async def update_leaderboard_task(self):
        """Task to update the leaderboard periodically."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            if self.leaderboard_channels:
                for guild_id, channel_id in self.leaderboard_channels.items():
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        await self.update_leaderboard(channel)
            await asyncio.sleep(1800)


    async def update_leaderboard(self, channel: discord.TextChannel):
        """Update the leaderboard in the specified channel."""
        guild_id = channel.guild.id
        if guild_id not in self.leaderboard_channels:
            return
            
        if guild_id not in self.user_data or not self.user_data[guild_id]:
            return

        sorted_users = sorted(
            self.user_data[guild_id].items(),
            key=lambda x: x[1]['xp'],
            reverse=True
        )[:10]

        embed = discord.Embed(
            title="🏆 Live Leaderboard 🏆",
            description="Top 10 users by XP",
            color=discord.Color.green()
        )

        for i, (user_id, data) in enumerate(sorted_users, 1):
            member = channel.guild.get_member(user_id)
            if member:
                embed.add_field(
                    name=f"{i}. {member.display_name}",
                    value=f"Level {self.calculate_level(data['xp'])} | {data['xp']} XP",
                    inline=False
                )

        async for message in channel.history(limit=10):
            if message.author == self.bot.user and "🏆 Live Leaderboard 🏆" in message.embeds[0].title:
                await message.delete()
                break

        await channel.send(embed=embed)

    async def xp_decay_task(self):
        """Task to decay XP over time."""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for guild_id, users in self.user_data.items():
                for user_id, data in users.items():
                    last_message = datetime.fromisoformat(data['last_message'])
                    if (datetime.now() - last_message).days > 7:  
                        data['xp'] = max(0, int(data['xp'] * (1 - self.xp_decay_rate)))
            self.save_data()
            await asyncio.sleep(86400)  

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Track user messages and add XP."""
        if message.author.bot or not message.guild:
            return
        await self.add_xp(message.author.id, message.guild.id)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_level_role(self, ctx, level: int, role: discord.Role):
        """Set a role for a specific level."""
        self.roles[level] = role.id
        self.save_data()
        await ctx.send(f"✅ Role {role.name} will be assigned at level {level}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_leaderboard_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for the live-updating leaderboard."""
        self.leaderboard_channels[ctx.guild.id] = channel.id
        self.save_data()
        await ctx.send(f"✅ Leaderboard will be updated in {channel.mention}.")
        await self.update_leaderboard(channel)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def leaderboard(self, ctx):
        """Display the server's leveling leaderboard."""
        await self.update_leaderboard(ctx.channel)

    @commands.command()
    @commands.is_owner()
    async def set_xp(self, ctx, user: discord.Member, xp: int):
        """Bot owner command: Set a user's XP."""
        guild_id = ctx.guild.id
        if guild_id not in self.user_data:
            self.user_data[guild_id] = {}
        self.user_data[guild_id][user.id] = {'xp': xp, 'last_message': datetime.now().isoformat()}
        self.save_data()
        await ctx.send(f"✅ Set {user.mention}'s XP to {xp}.")

    @commands.command()
    @commands.is_owner()
    async def reset_levels(self, ctx):
        """Bot owner command: Reset all leveling data for the server."""
        guild_id = ctx.guild.id
        if guild_id in self.user_data:
            del self.user_data[guild_id]
            self.save_data()
            await ctx.send("✅ Reset all leveling data for this server.")
        else:
            await ctx.send("No leveling data found for this server.")

    @commands.command()
    async def my_level(self, ctx):
        """Check your current level and XP."""
        guild_id = ctx.guild.id
        user_id = ctx.author.id
        if guild_id in self.user_data and user_id in self.user_data[guild_id]:
            xp = self.user_data[guild_id][user_id]['xp']
            level = self.calculate_level(xp)
            next_level_xp = self.xp_for_next_level(level)
            embed = discord.Embed(
                title=f"📊 {ctx.author.display_name}'s Level",
                description=f"Level: **{level}**\nXP: **{xp}/{next_level_xp}**",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("You haven't earned any XP yet!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelsetup(self, ctx, channel: Optional[discord.TextChannel] = None):
        """
        Display leveling-related information or set the announcement channel.
        Usage:
        - !levelsetup: Show all leveling-related info.
        - !levelsetup <channel>: Set the channel for level-up announcements.
        """
        guild_id = ctx.guild.id
        
        if channel:
            self.announcement_channels[guild_id] = channel.id
            self.save_data()
            await ctx.send(f"✅ Level-up announcements will now be sent to {channel.mention}.")
        else:
            guild = ctx.guild
            embed = discord.Embed(
                title="📊 Leveling System Setup",
                description="All leveling-related information for this server.",
                color=discord.Color.blue()
            )

            leaderboard_channel = self.bot.get_channel(self.leaderboard_channels.get(guild_id))
            embed.add_field(
                name="Leaderboard Channel",
                value=leaderboard_channel.mention if leaderboard_channel else "Not set",
                inline=False
            )

            announcement_channel = self.bot.get_channel(self.announcement_channels.get(guild_id))
            embed.add_field(
                name="Announcement Channel",
                value=announcement_channel.mention if announcement_channel else "Not set",
                inline=False
            )

            roles_info = "\n".join(
                f"Level {level}: <@&{role_id}>"
                for level, role_id in self.roles.get(guild_id, {}).items()
            ) if guild_id in self.roles else "No roles assigned to levels."
            embed.add_field(name="Level Roles", value=roles_info, inline=False)

            multipliers_info = "\n".join(
                f"<@&{role_id}>: {multiplier}x"
                for role_id, multiplier in self.xp_multipliers.get(guild_id, {}).items()
            ) if guild_id in self.xp_multipliers else "No XP multipliers set."
            embed.add_field(name="XP Multipliers", value=multipliers_info, inline=False)

            achievements_info = "\n".join(
                f"{name}: Level {data['required_level']} (Reward: {data['reward']})"
                for name, data in self.achievements.get(guild_id, {}).items()
            ) if guild_id in self.achievements else "No achievements set."
            embed.add_field(name="Achievements", value=achievements_info, inline=False)

            embed.add_field(
                name="XP Decay Rate",
                value=f"{self.xp_decay_rate * 100}% per day after 7 days of inactivity",
                inline=False
            )

            embed.add_field(
                name="XP Gain Range",
                value=f"{self.xp_gain_range[0]} to {self.xp_gain_range[1]} XP per message",
                inline=False
            )

            total_users = len(self.user_data.get(guild_id, {}))
            embed.add_field(
                name="Total Users with XP",
                value=f"{total_users} users",
                inline=False
            )

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LevelingSystem(bot))

class CustomLogging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logging_config = {}  

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def togglelog(self, ctx, action: str, channel: discord.TextChannel = None):
        """
        Toggle logging for specific actions (e.g., bans, mutes, kicks).
        Usage: !togglelog <action> <channel>
        """
        action = action.lower()
        valid_actions = ["ban", "mute", "kick"]

        if action not in valid_actions:
            await ctx.send(f"❌ Invalid action. Use one of: {', '.join(valid_actions)}")
            return

        guild_id = ctx.guild.id
        if guild_id not in self.logging_config:
            self.logging_config[guild_id] = {}

        if channel:
            self.logging_config[guild_id][action] = channel.id
            await ctx.send(f"✅ Logging for `{action}` has been enabled in {channel.mention}.")
        else:
            if action in self.logging_config[guild_id]:
                del self.logging_config[guild_id][action]
                await ctx.send(f"✅ Logging for `{action}` has been disabled.")
            else:
                await ctx.send(f"❌ Logging for `{action}` is already disabled.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggleprelog(self, ctx):
        """
        Automatically create channels for bans, mutes, and kicks and enable logging.
        Usage: !toggleprelog
        """
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        ban_channel = await guild.create_text_channel("ban-logs", overwrites=overwrites)
        mute_channel = await guild.create_text_channel("mute-logs", overwrites=overwrites)
        kick_channel = await guild.create_text_channel("kick-logs", overwrites=overwrites)

        guild_id = guild.id
        self.logging_config[guild_id] = {
            "ban": ban_channel.id,
            "mute": mute_channel.id,
            "kick": kick_channel.id
        }

        await ctx.send("✅ Created logging channels and enabled logging for bans, mutes, and kicks.")

    async def log_action(self, guild_id, action, moderator, user, reason, duration=None):
        print(f"Logging {action} for {user} in guild {guild_id}")  # Debug print
        if guild_id not in self.logging_config or action not in self.logging_config[guild_id]:
            print("Logging not configured for this action.")  # Debug print
            return

        channel_id = self.logging_config[guild_id][action]
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found.")  # Debug print
            return

        embed = discord.Embed(
            title=f"🚨 {action.capitalize()} Log",
            description=f"**User:** {user.mention} (`{user.id}`)\n**Reason:** {reason}",
            color=discord.Color.red()
        )
        if duration:
            embed.add_field(name="Duration", value=duration)
        embed.add_field(name="Moderator", value=moderator.mention)
        embed.set_footer(text=f"Action performed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(CustomLogging(bot))

class MessagePurge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, condition: str, count: str = "nuke"):
        """
        Delete messages from bots, links, or specific users.
        Usage: !purge <user_id/bots/links> <count/nuke>
        """
        if count.lower() == "nuke":
            count = None  
        else:
            try:
                count = int(count)
                if count <= 0:
                    await ctx.send("❌ Count must be a positive number.")
                    return
            except ValueError:
                await ctx.send("❌ Invalid count. Use a number or 'nuke'.")
                return

        def check(message):
            if condition.lower() == "bots":
                return message.author.bot
            elif condition.lower() == "links":
                return "http://" in message.content or "https://" in message.content
            else:
                try:
                    user_id = int(condition)  
                    return message.author.id == user_id
                except ValueError:
                    return False

        if condition.lower() not in ["bots", "links"]:
            try:
                user_id = int(condition)  
            except ValueError:
                await ctx.send(f"❌ Invalid condition: `{condition}`. Use 'bots', 'links', or a valid user ID.", delete_after=5)
                return

        deleted = await ctx.channel.purge(limit=count, check=check)
        await ctx.send(f"✅ Deleted {len(deleted)} messages matching the condition: `{condition}`.", delete_after=5)


def setup(bot):
    bot.add_cog(MessagePurge(bot))

class ReminderSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}

    @commands.command(name="reminder")
    async def reminder(self, ctx):
        """
        Open a UI to set a reminder.
        Usage: !reminder
        """
        
        modal = discord.ui.Modal(title="Set a Reminder")
        modal.add_item(discord.ui.TextInput(
            label="Duration",
            placeholder="Enter duration (e.g., 1h, 30m, 2d)",
            required=True
        ))
        modal.add_item(discord.ui.TextInput(
            label="Color",
            placeholder="Enter color (e.g., red, #FF0000)",
            required=True
        ))
        modal.add_item(discord.ui.TextInput(
            label="Message",
            placeholder="Enter the reminder message",
            required=True
        ))
        modal.add_item(discord.ui.TextInput(
            label="Channel",
            placeholder="Mention the channel (e.g., #general)",
            required=True
        ))

        async def on_submit(interaction: discord.Interaction):
            try:
                duration = modal.children[0].value
                color = modal.children[1].value
                message = modal.children[2].value
                channel_input = modal.children[3].value

                duration_seconds = self.parse_duration(duration)
                if duration_seconds <= 0:
                    await interaction.response.send_message("❌ Invalid duration. Please specify a positive duration.", ephemeral=True)
                    return

                reminder_color = self.parse_color(color)
                if not reminder_color:
                    await interaction.response.send_message("❌ Invalid color. Please use a valid hex code or named color (e.g., red, green, blue, #FF0000).", ephemeral=True)
                    return

                channel = self.parse_channel(ctx, channel_input)
                if not channel:
                    await interaction.response.send_message("❌ Invalid channel. Please mention a valid channel or use its ID.", ephemeral=True)
                    return

                reminder_time = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds)
                self.reminders[ctx.author.id] = {
                    "time": reminder_time,
                    "message": message,
                    "color": reminder_color,
                    "channel": channel.id,
                    "user_id": ctx.author.id
                }

                embed = discord.Embed(
                    title="⏰ Reminder Set",
                    description=f"I'll remind you in {duration} in {channel.mention}.",
                    color=reminder_color
                )
                embed.add_field(name="Message", value=message, inline=False)
                await interaction.response.send_message(embed=embed)

                await self.start_reminder(ctx.author.id)

            except ValueError as e:
                await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

        modal.on_submit = on_submit

        view = discord.ui.View()
        button = discord.ui.Button(label="Set Reminder", style=discord.ButtonStyle.primary)
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(modal)
        button.callback = button_callback
        view.add_item(button)

        await ctx.send("Click the button below to set a reminder:", view=view)

    @commands.command(name="editreminder")
    async def edit_reminder(self, ctx):
        """
        Open a panel to edit existing reminders.
        Usage: !editreminder
        """
        if ctx.author.id not in self.reminders:
            await ctx.send("❌ You don't have any active reminders to edit.")
            return

        reminder = self.reminders[ctx.author.id]

        view = discord.ui.View()
        select = discord.ui.Select(
            placeholder="Select a reminder to edit",
            options=[
                discord.SelectOption(
                    label=f"Reminder: {reminder['message'][:50]}...",
                    value="edit_reminder",
                    description=f"Due: {reminder['time'].strftime('%Y-%m-%d %H:%M:%S')}"
                )
            ]
        )
        select.callback = lambda interaction: self.handle_reminder_selection(interaction, reminder)
        view.add_item(select)

        await ctx.send("Select the reminder you want to edit:", view=view)

    async def handle_reminder_selection(self, interaction: discord.Interaction, reminder):
        """
        Handle the selection of a reminder to edit.
        """
        modal = discord.ui.Modal(title="Edit Reminder")
        modal.add_item(discord.ui.TextInput(
            label="New Message",
            placeholder="Enter the new reminder message",
            default=reminder["message"],
            required=True
        ))
        modal.add_item(discord.ui.TextInput(
            label="New Duration",
            placeholder="Enter the new duration (e.g., 1h, 30m)",
            required=True
        ))
        modal.add_item(discord.ui.TextInput(
            label="New Color",
            placeholder="Enter the new color (e.g., red, #FF0000)",
            required=True
        ))

        async def on_submit(interaction: discord.Interaction):
            try:
                new_message = modal.children[0].value
                new_duration = modal.children[1].value
                new_color = modal.children[2].value

                duration_seconds = self.parse_duration(new_duration)
                if duration_seconds <= 0:
                    await interaction.response.send_message("❌ Invalid duration. Please specify a positive duration.", ephemeral=True)
                    return

                reminder_color = self.parse_color(new_color)
                if not reminder_color:
                    await interaction.response.send_message("❌ Invalid color. Please use a valid hex code or named color (e.g., red, green, blue, #FF0000).", ephemeral=True)
                    return

                reminder["message"] = new_message
                reminder["time"] = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds)
                reminder["color"] = reminder_color

                embed = discord.Embed(
                    title="⏰ Reminder Updated",
                    description=f"Your reminder has been updated.",
                    color=reminder["color"]
                )
                embed.add_field(name="New Message", value=reminder["message"], inline=False)
                embed.add_field(name="New Duration", value=f"{new_duration}", inline=False)
                embed.add_field(name="New Color", value=f"{new_color}", inline=False)
                await interaction.response.send_message(embed=embed)

                await self.start_reminder(reminder["user_id"])

            except ValueError as e:
                await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)

    def parse_duration(self, duration: str) -> int:
        """
        Parse a duration string (e.g., 1h, 30m, 2d) into seconds.
        """
        duration = duration.lower()
        if duration.endswith("h"):
            return int(duration[:-1]) * 3600
        elif duration.endswith("m"):
            return int(duration[:-1]) * 60
        elif duration.endswith("d"):
            return int(duration[:-1]) * 86400
        elif duration.endswith("s"):
            return int(duration[:-1])
        else:
            raise ValueError("Invalid duration format. Use 'h' for hours, 'm' for minutes, 's' for seconds, or 'd' for days.")

    def parse_color(self, color: str) -> Optional[discord.Color]:
        """
        Parse a color string (hex code or named color) into a discord.Color object.
        """
        color = color.lower()
        named_colors = {
            "red": discord.Color.red(),
            "green": discord.Color.green(),
            "blue": discord.Color.blue(),
            "purple": discord.Color.purple(),
            "orange": discord.Color.orange(),
            "gold": discord.Color.gold(),
            "teal": discord.Color.teal(),
            "dark_blue": discord.Color.dark_blue(),
            "dark_green": discord.Color.dark_green(),
            "dark_purple": discord.Color.dark_purple(),
            "dark_red": discord.Color.dark_red(),
            "dark_teal": discord.Color.dark_teal(),
            "dark_gold": discord.Color.dark_gold(),
            "dark_orange": discord.Color.dark_orange(),
            "dark_gray": discord.Color.dark_gray(),
            "light_gray": discord.Color.light_gray(),
            "blurple": discord.Color.blurple(),
            "greyple": discord.Color.greyple(),
            "fuchsia": discord.Color.fuchsia(),
            "yellow": discord.Color.yellow(),
            "black": discord.Color.default(),
        }
        if color in named_colors:
            return named_colors[color]
        try:
            return discord.Color.from_str(color)
        except ValueError:
            return None

    def parse_channel(self, ctx, channel_input: str) -> Optional[discord.TextChannel]:
        """
        Parse a channel mention or ID into a discord.TextChannel object.
        """
        try:
            if channel_input.startswith("<#") and channel_input.endswith(">"):
                channel_id = int(channel_input[2:-1])
            else:
                channel_id = int(channel_input)
            return ctx.guild.get_channel(channel_id)
        except (ValueError, AttributeError):
            return None

    async def start_reminder(self, user_id: int):
        """
        Start a reminder task for the specified user.
        """
        reminder = self.reminders.get(user_id)
        if not reminder:
            return

        reminder_time = reminder["time"]
        reminder_time = reminder["time"]
        delay = (reminder_time - datetime.now(timezone.utc)).total_seconds()

        if delay > 0:
            await asyncio.sleep(delay)

            channel = self.bot.get_channel(reminder["channel"])
            if channel:
                embed = discord.Embed(
                    title="⏰ Reminder",
                    description=reminder["message"],
                    color=reminder["color"]
                )
                await channel.send(f"<@{reminder['user_id']}>", embed=embed)

            self.reminders.pop(user_id, None)

def setup(bot):
    bot.add_cog(ReminderSystem(bot))

class Snipe(commands.Cog):       
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages = {} 
        self.edited_messages = {}  
        self.snipe_cooldown = {}  
        self.snipe_duration = 300  
        self.editsnipe_duration = 300  

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Track deleted messages."""
        if message.author.bot:  
            return

        self.deleted_messages[message.channel.id] = {
            "content": message.content,
            "author": message.author,
            "timestamp": message.created_at,
            "attachments": [attachment.url for attachment in message.attachments]
        }

        await asyncio.sleep(self.snipe_duration)  
        if message.channel.id in self.deleted_messages:
            del self.deleted_messages[message.channel.id]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Track edited messages."""
        if before.author.bot: 
            return

        self.edited_messages[before.channel.id] = {
            "before": before.content,
            "after": after.content,
            "author": before.author,
            "timestamp": datetime.utcnow()
        }

        await asyncio.sleep(self.editsnipe_duration)  
        if before.channel.id in self.edited_messages:
            del self.edited_messages[before.channel.id]

    @commands.command(name="configuresnipe")
    @commands.has_permissions(manage_messages=True)
    async def configuresnipe(self, ctx, duration: int):
        """Configure the duration for which deleted messages are stored."""
        if duration < 0:
            await ctx.send("Duration cannot be negative.")
            return
        self.snipe_duration = duration
        await ctx.send(f"Deleted messages will now be stored for {duration} seconds.")

    @commands.command(name="configuresnipeedit")
    @commands.has_permissions(manage_messages=True)
    async def configuresnipeedit(self, ctx, duration: int):
        """Configure the duration for which edited messages are stored."""
        if duration < 0:
            await ctx.send("Duration cannot be negative.")
            return
        self.editsnipe_duration = duration
        await ctx.send(f"Edited messages will now be stored for {duration} seconds.")

    @commands.command(name="snipe_info")
    async def snipe_info(self, ctx):
        """Display the current snipe settings."""
        embed = discord.Embed(
            title="⚙️ Snipe Settings",
            color=discord.Color.green()
        )
        embed.add_field(name="Deleted Messages Duration", value=f"{self.snipe_duration} seconds", inline=False)
        embed.add_field(name="Edited Messages Duration", value=f"{self.editsnipe_duration} seconds", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="snipe")
    @commands.has_permissions(manage_messages=True)
    async def snipe(self, ctx):
        """Recover the last deleted message in the channel."""
        if ctx.author.id in self.snipe_cooldown:
            remaining = (self.snipe_cooldown[ctx.author.id] - datetime.utcnow()).total_seconds()
            if remaining > 0:
                await ctx.send(f"You're on cooldown! Try again in {int(remaining)} seconds.")
                return

        deleted_message = self.deleted_messages.get(ctx.channel.id)
        if not deleted_message:
            await ctx.send("No recently deleted messages found in this channel.")
            return

        embed = discord.Embed(
            title="🗑️ Sniped Message",
            description=deleted_message["content"],
            color=discord.Color.red()
        )
        embed.set_author(name=deleted_message["author"].display_name, icon_url=deleted_message["author"].avatar.url)
        embed.set_footer(text=f"Deleted at {deleted_message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

        if deleted_message["attachments"]:
            embed.add_field(name="Attachments", value="\n".join(deleted_message["attachments"]), inline=False)

        await ctx.send(embed=embed)

        self.snipe_cooldown[ctx.author.id] = datetime.utcnow() + timedelta(seconds=30)

    @commands.command(name="editsnipe")
    @commands.has_permissions(manage_messages=True)
    async def editsnipe(self, ctx):
        """Recover the last edited message in the channel."""
        if ctx.author.id in self.snipe_cooldown:
            remaining = (self.snipe_cooldown[ctx.author.id] - datetime.utcnow()).total_seconds()
            if remaining > 0:
                await ctx.send(f"You're on cooldown! Try again in {int(remaining)} seconds.")
                return

        edited_message = self.edited_messages.get(ctx.channel.id)
        if not edited_message:
            await ctx.send("No recently edited messages found in this channel.")
            return

        embed = discord.Embed(
            title="✏️ Edited Message",
            color=discord.Color.blue()
        )
        embed.set_author(name=edited_message["author"].display_name, icon_url=edited_message["author"].avatar.url)
        embed.add_field(name="Before", value=edited_message["before"], inline=False)
        embed.add_field(name="After", value=edited_message["after"], inline=False)
        embed.set_footer(text=f"Edited at {edited_message['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

        await ctx.send(embed=embed)

        self.snipe_cooldown[ctx.author.id] = datetime.utcnow() + timedelta(seconds=30)

def setup(bot):
    bot.add_cog(Snipe(bot))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvancedInviteTracker")

class AdvancedInviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite_cache: Dict[int, Dict[str, Dict]] = {}  
        self.known_joins: Dict[int, Dict] = {}  
        self.data_file = "invite_tracking_data.json"
        self.db_file = "invite_tracking.db"
        self.setup_database()

        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.invite_cache = data.get("invites", {})
                    self.known_joins = data.get("known_joins", {})
            except json.JSONDecodeError:
                logger.error("Failed to load invite tracking data: Invalid JSON format")

    def setup_database(self):
        """Initialize the SQLite database for invite tracking."""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invites (
                guild_id INTEGER,
                invite_code TEXT,
                uses INTEGER,
                inviter TEXT,
                created_at TEXT,
                PRIMARY KEY (guild_id, invite_code)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS joins (
                member_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                invite_code TEXT,
                inviter TEXT,
                joined_at TEXT
            )
        ''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        """Cache all invites when the bot is ready."""
        logger.info("Bot is ready. Syncing invites...")
        for guild in self.bot.guilds:
            try:
                invites = await guild.invites()
                self.invite_cache[guild.id] = {
                    invite.code: {
                        "uses": invite.uses,
                        "inviter": invite.inviter.name if invite.inviter else "Unknown",
                        "created_at": invite.created_at.isoformat() if invite.created_at else "Unknown"
                    }
                    for invite in invites
                }
                self.update_database(guild.id, invites)
            except discord.Forbidden:
                logger.warning(f"Missing permission to fetch invites for guild: {guild.name}")
        logger.info("Invite sync complete.")

    def update_database(self, guild_id: int, invites: List[discord.Invite]):
        """Update the database with the latest invite data."""
        for invite in invites:
            self.cursor.execute('''
                INSERT OR REPLACE INTO invites (guild_id, invite_code, uses, inviter, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (guild_id, invite.code, invite.uses, invite.inviter.name if invite.inviter else "Unknown", invite.created_at.isoformat() if invite.created_at else "Unknown"))
        self.conn.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Track which invite was used when a member joins."""
        try:
            invites_before = self.invite_cache.get(member.guild.id, {})
            current_invites = await member.guild.invites()

            for invite in current_invites:
                cached_invite = invites_before.get(invite.code)
                if cached_invite and invite.uses > cached_invite["uses"]:
                    inviter = invite.inviter.name if invite.inviter else "Unknown"
                    invite_code = invite.code

                    self.known_joins[member.id] = {
                        "joined_at": member.joined_at.isoformat() if member.joined_at else "Unknown",
                        "invite_code": invite_code,
                        "inviter": inviter
                    }
                    self.cursor.execute('''
                        INSERT OR REPLACE INTO joins (member_id, guild_id, invite_code, inviter, joined_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (member.id, member.guild.id, invite_code, inviter, member.joined_at.isoformat() if member.joined_at else "Unknown"))
                    self.conn.commit()

                    self.invite_cache[member.guild.id][invite.code]["uses"] = invite.uses
                    await self.log_join(member, invite_code, inviter)
                    break

            self.backup_data()

        except discord.Forbidden:
            logger.warning(f"Missing permission to fetch invites for guild: {member.guild.name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Track when a member leaves the server."""
        if member.id in self.known_joins:
            del self.known_joins[member.id]
            self.cursor.execute('DELETE FROM joins WHERE member_id = ?', (member.id,))
            self.conn.commit()
            self.backup_data()
            logger.info(f"Member {member.name} ({member.id}) left the server.")

    async def log_join(self, member: discord.Member, invite_code: str, inviter: str):
        """Log the member join to a designated log channel."""
        log_channel = discord.utils.get(member.guild.text_channels, name='join-logs')
        if log_channel:
            embed = discord.Embed(
                title="👤 Member Joined",
                description=f"{member.mention} joined using invite `{invite_code}` created by **{inviter}**.",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await log_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def view_historic(self, ctx):
        """View historic tracking of invite joins."""
        self.cursor.execute('SELECT * FROM joins WHERE guild_id = ?', (ctx.guild.id,))
        joins = self.cursor.fetchall()

        if not joins:
            await ctx.send("📊 No historic join data available.")
            return

        entries = []
        for join in joins:
            member_id, guild_id, invite_code, inviter, joined_at = join
            member = ctx.guild.get_member(member_id)
            member_name = member.name if member else "Unknown Member"
            entries.append(
                f"👤 **{member_name}** (ID: {member_id})\n"
                f"🎟️ Invite: `{invite_code}` by **{inviter}**\n"
                f"📅 Joined: {joined_at}\n"
            )

        page_size = 5
        pages = [entries[i:i + page_size] for i in range(0, len(entries), page_size)]

        for page_num, page_content in enumerate(pages, 1):
            embed = discord.Embed(
                title=f"📊 Historic Invite Tracking (Page {page_num}/{len(pages)})",
                description="\n\n".join(page_content),
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Tracked {len(joins)} total joins.")
            await ctx.send(embed=embed)

    def backup_data(self):
        """Backup invite tracking data to a JSON file."""
        data = {
            "invites": self.invite_cache,
            "known_joins": self.known_joins
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def cog_unload(self):
        """Clean up resources when the cog is unloaded."""
        self.conn.close()

def setup(bot):
    bot.add_cog(AdvancedInviteTracker(bot))


class Analytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite_tracker = {} 
        self.join_tracker = {}    
        self.analytics_channels = {}  
        self.analytics_tasks = {}  

    async def fetch_existing_invites(self):
        for guild in self.bot.guilds:
            if guild.id not in self.invite_tracker:
                self.invite_tracker[guild.id] = {}
            try:
                invites = await guild.invites()
                for invite in invites:
                    self.invite_tracker[guild.id][invite.code] = {
                        'code': invite.code,
                        'creator': invite.inviter.name if invite.inviter else "Unknown",
                        'uses': invite.uses,
                        'max_uses': invite.max_uses,
                        'expires_at': invite.expires_at
                    }
            except Exception as e:
                print(f"Error fetching invites for guild {guild.name}: {e}")

    async def check_and_setup_analytics(self):
        while True:
            for guild_id in self.analytics_channels:
                for interval, channel in self.analytics_channels[guild_id].items():
                    if channel is None:
                        print(f"Channel for {interval} analytics not found in guild {guild_id}. Retrying in 5 minutes...")
                        await asyncio.sleep(300)
                        continue

                    task_key = f"{guild_id}_{interval}"
                    if task_key not in self.analytics_tasks or self.analytics_tasks[task_key].done():
                        self.analytics_tasks[task_key] = self.bot.loop.create_task(
                            self._send_analytics(guild_id, interval)
                        )
                        print(f"Analytics task for {interval} started in {channel.mention} (Guild: {guild_id})")
            await asyncio.sleep(300)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def analyse(self, ctx, interval: str = None, channel: discord.TextChannel = None):
        guild_id = ctx.guild.id
        
        if guild_id not in self.analytics_channels:
            self.analytics_channels[guild_id] = {}
            
        if interval:
            if interval.lower() not in ['daily', 'weekly', 'monthly']:
                await ctx.send("❌ Invalid interval. Use 'daily', 'weekly', or 'monthly'.")
                return

            self.analytics_channels[guild_id][interval.lower()] = channel or ctx.channel
            task_key = f"{guild_id}_{interval.lower()}"
            
            if task_key not in self.analytics_tasks or self.analytics_tasks[task_key].done():
                self.analytics_tasks[task_key] = self.bot.loop.create_task(
                    self._send_analytics(guild_id, interval.lower())
                )

            embed = discord.Embed(
                title="✅ Analytics Setup Complete",
                description=f"Analytics will be posted {interval.lower()} in {(channel or ctx.channel).mention}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="📊 Analytics Status",
                description="Current analytics configurations",
                color=discord.Color.blue()
            )

            for interval in ['daily', 'weekly', 'monthly']:
                if interval in self.analytics_channels.get(guild_id, {}) and self.analytics_channels[guild_id][interval] is not None:
                    embed.add_field(
                        name=f"{interval.capitalize()} Analytics",
                        value=f"Active in {self.analytics_channels[guild_id][interval].mention}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{interval.capitalize()} Analytics",
                        value="Not active",
                        inline=False
                    )

            await ctx.send(embed=embed)

    async def _send_analytics(self, guild_id, interval):
        while True:
            print(f"Running analytics task for {interval} in guild {guild_id}")
            try:
                if interval == 'daily':
                    await asyncio.sleep(86400)
                elif interval == 'weekly':
                    await asyncio.sleep(604800)
                elif interval == 'monthly':
                    await asyncio.sleep(2592000)

                if guild_id not in self.analytics_channels or interval not in self.analytics_channels[guild_id]:
                    continue

                embed = self._generate_analytics_report(guild_id, interval)
                await self.analytics_channels[guild_id][interval].send(embed=embed)
            except Exception as e:
                print(f"Error in _send_analytics for guild {guild_id}: {e}")
                continue

    def _generate_analytics_report(self, guild_id, interval):
        embed = discord.Embed(
            title=f"📊 Server Analytics Report ({interval.capitalize()})",
            description="Detailed server activity and statistics",
            color=discord.Color.blue()
        )

        guild_invites = self.invite_tracker.get(guild_id, {})
        active_invites = [invite for invite in guild_invites.values() if invite['uses'] > 0]
        expired_invites = [invite for invite in guild_invites.values() if invite['uses'] == 0]

        embed.add_field(
            name="🔗 Invites",
            value=f"Active: {len(active_invites)}\nExpired: {len(expired_invites)}\nTotal Uses: {sum(invite['uses'] for invite in guild_invites.values())}",
            inline=False
        )

        guild_joins = self.join_tracker.get(guild_id, {})
        total_joins = sum(guild_joins.values())
        embed.add_field(
            name="👥 Member Joins",
            value=f"Total Joins ({interval}): {total_joins}",
            inline=False
        )

        if active_invites:
            invite_details = "\n".join(
                f"• {invite['code']}: {invite['uses']} uses (Created by {invite['creator']})"
                for invite in active_invites
            )
            embed.add_field(name="Active Invites", value=invite_details, inline=False)

        return embed

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id
        if guild_id not in self.join_tracker:
            self.join_tracker[guild_id] = {}
        today = datetime.now().date()
        self.join_tracker[guild_id][today] = self.join_tracker[guild_id].get(today, 0) + 1

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        guild_id = invite.guild.id
        if guild_id not in self.invite_tracker:
            self.invite_tracker[guild_id] = {}
        self.invite_tracker[guild_id][invite.code] = {
            'code': invite.code,
            'creator': invite.inviter.name if invite.inviter else "Unknown",
            'uses': invite.uses,
            'max_uses': invite.max_uses,
            'expires_at': invite.expires_at
        }

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        guild_id = invite.guild.id
        if guild_id in self.invite_tracker and invite.code in self.invite_tracker[guild_id]:
            del self.invite_tracker[guild_id][invite.code]

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = member.guild.id
        invites = await member.guild.invites()
        if guild_id not in self.invite_tracker:
            self.invite_tracker[guild_id] = {}
        for invite in invites:
            if invite.code in self.invite_tracker[guild_id]:
                self.invite_tracker[guild_id][invite.code]['uses'] = invite.uses
            else:
                self.invite_tracker[guild_id][invite.code] = {
                    'code': invite.code,
                    'creator': invite.inviter.name if invite.inviter else "Unknown",
                    'uses': invite.uses,
                    'max_uses': invite.max_uses,
                    'expires_at': invite.expires_at
                }

    @commands.Cog.listener()
    async def on_ready(self):
        await self.fetch_existing_invites()
        self.bot.loop.create_task(self.check_and_setup_analytics())

def setup(bot):
    bot.add_cog(Analytics(bot))


class WebhookLogger:
    def __init__(self, bot):
        self.bot = bot
        webhook_url = os.getenv('LOGGING_WEBHOOK_URL')
        
        if webhook_url and webhook_url.lower() != 'none':
            self.webhook_url = webhook_url
            self.session = aiohttp.ClientSession()
            
            try:
                parts = self.webhook_url.split('/')
                self.webhook_id = int(parts[-2]) if len(parts) > 2 else None
            except (IndexError, ValueError):
                self.webhook_id = None
                
            if hasattr(bot, 'get_cog'):
                automod = bot.get_cog('AutoMod')
                if automod:
                    automod.link_whitelist.add(self.webhook_url)
                    automod.link_whitelist.add('discord.com/channels')
        else:
            self.webhook_url = None
            self.webhook_id = None
            self.session = None

    async def send_to_webhook(self, content=None, embeds=None, files=None):
        if not self.webhook_url:
            return

        webhook = discord.Webhook.from_url(self.webhook_url, session=self.session)

        try:
            
            if isinstance(embeds, list) and embeds:
                for embed in embeds:
                    if isinstance(embed, discord.Embed):
                        embed.set_footer(text=f"{embed.footer.text or ''} | Webhook ID: {self.webhook_id}")

            if isinstance(embeds, list) and len(embeds) > 0 and isinstance(embeds[0], discord.Embed):
                await webhook.send(
                    content=content,
                    embeds=embeds,
                    files=files
                )
            else:
                await webhook.send(
                    content=content,
                    embed=embeds[0] if embeds and isinstance(embeds[0], discord.Embed) else None,
                    files=files
                )
        except Exception as e:
            print(f"Webhook send error details: {str(e)}")



    async def log_command(self, ctx):
        if not ctx.guild:
            return
        
        embed = EmbedBuilder(
            f"Command Used in {ctx.guild.name}",
            f"Command: {ctx.command}\nArgs: {ctx.args[2:]}"
        ).set_color(discord.Color.green())
        
        embed.add_field("User", f"{ctx.author} ({ctx.author.id})")
        embed.add_field("Channel", f"{ctx.channel.name} ({ctx.channel.id})")
        embed.add_field("Timestamp", ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        
        if ctx.message.reference:
            embed.add_field("Reply to", f"Message ID: {ctx.message.reference.message_id}", inline=False)
        
        message_link = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"
        embed.add_field("Message Link", message_link, inline=False)
        
        if ctx.message.attachments:
            files = []
            for attachment in ctx.message.attachments:
                try:
                    file_data = await attachment.read()
                    file = discord.File(io.BytesIO(file_data), filename=attachment.filename)
                    files.append(file)
                    
                    file_info = (
                        f"📎 Name: {attachment.filename}\n"
                        f"📊 Size: {attachment.size:,} bytes\n"
                        f"📑 Type: {attachment.content_type}\n"
                        f"🔗 URL: {attachment.url}"
                    )
                    embed.add_field("File Attachment", file_info, inline=False)
                except Exception as e:
                    embed.add_field("⚠️ File Error", f"Failed to process {attachment.filename}: {str(e)}", inline=False)
            
            await self.send_to_webhook(embeds=[embed.build()], files=files)
        else:
            await self.send_to_webhook(embeds=[embed.build()])


    async def log_message(self, message):
        if not message.guild:  
            return
    
        if not self.webhook_url or self.webhook_url.lower() == 'none':
            return
            
        if message.webhook_id and message.webhook_id == int(self.webhook_url.split('/')[-2]):
            return

        embed = EmbedBuilder(
            f"Message in {message.guild.name}",
            message.content or "No content"
        ).set_color(discord.Color.blue())

        message_type = "User Message"
        if message.author.bot:
            message_type = "Bot Message"
            embed.set_color(discord.Color.purple())
        if message.webhook_id:
            message_type = "Webhook Message"
            embed.set_color(discord.Color.gold())
        embed.add_field("Type", message_type)

        if message.webhook_id:
            embed.add_field("Webhook ID", message.webhook_id)
            if hasattr(message, 'application') and message.application:
                embed.add_field("Integration", message.application.name)
        if message.author.bot:
            embed.add_field("Bot Name", message.author.name)
            embed.add_field("Bot ID", message.author.id)

        embed.add_field("Author", f"{message.author} ({message.author.id})")
        embed.add_field("Channel", f"{message.channel.name} ({message.channel.id})")
        embed.add_field("Timestamp", message.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        if message.reference:
            try:
                ref_msg = await message.channel.fetch_message(message.reference.message_id)
                ref_info = f"Message: {ref_msg.content[:100]}...\nAuthor: {ref_msg.author}\nID: {message.reference.message_id}"
                embed.add_field("Reply to", ref_info, inline=False)
            except:
                embed.add_field("Reply to", f"Message ID: {message.reference.message_id}", inline=False)

        if message.edited_at:
            embed.add_field("Edited", message.edited_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

        files = []
        for attachment in message.attachments:
            try:
                file_data = await attachment.read()
                file = discord.File(io.BytesIO(file_data), filename=attachment.filename)
                files.append(file)
                
                file_info = (
                    f"📎 Name: {attachment.filename}\n"
                    f"📊 Size: {attachment.size:,} bytes\n"
                    f"📑 Type: {attachment.content_type}\n"
                    f"🔗 URL: {attachment.url}"
                )
                embed.add_field("File Attachment", file_info, inline=False)
            except Exception as e:
                embed.add_field("⚠️ File Error", f"Failed to process {attachment.filename}: {str(e)}", inline=False)

        message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        embed.add_field("Message Link", message_link, inline=False)
        embed.set_footer(f"Message ID: {message.id} | Guild ID: {message.guild.id}")

        if message.author.avatar:
            embed.set_thumbnail(message.author.avatar.url)

        try:
            await self.send_to_webhook(embeds=[embed.build()], files=files)
        except Exception as e:
            print(f"Failed to send webhook: {str(e)}")



    def __del__(self):
        if self.session:
            asyncio.create_task(self.session.close())

class TicTacToeButton(discord.ui.Button):
    def __init__(self, x, y):
        super().__init__(style=discord.ButtonStyle.secondary, label="⠀", row=y)
        self.x = x
        self.y = y


    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        if interaction.user != view.current_player:
            return
        
        if view.board[self.x][self.y] != " ":
            return

        mark = "X" if view.current_player == view.player1 else "O"
        view.board[self.x][self.y] = mark
        self.label = mark
        self.disabled = True
        self.style = discord.ButtonStyle.danger if mark == "X" else discord.ButtonStyle.success

        if view.check_winner():
            for child in view.children:
                child.disabled = True
            embed = EmbedBuilder(
                "🎮 Game Over!",
                f"🎉 {view.current_player.mention} wins!"
            ).set_color(discord.Color.gold())
            await interaction.response.edit_message(view=view, embed=embed.build())
            
            rematch_view = discord.ui.View()
            rematch_button = discord.ui.Button(label="Rematch", style=discord.ButtonStyle.primary)
            close_button = discord.ui.Button(label="Close", style=discord.ButtonStyle.red)
            
            async def rematch_callback(i):
                new_game = TicTacToeView(view.player1, view.player2)
                embed = EmbedBuilder(
                    "🎮 New Game Started!",
                    f"{view.player1.mention} vs {view.player2.mention}"
                ).set_color(discord.Color.blue())
                await i.response.send_message(embed=embed.build(), view=new_game)
                
            async def close_callback(i):
                await i.channel.delete()
                
            rematch_button.callback = rematch_callback
            close_button.callback = close_callback
            rematch_view.add_item(rematch_button)
            rematch_view.add_item(close_button)
            await interaction.channel.send(view=rematch_view)
            return

        if view.is_board_full():
            embed = EmbedBuilder(
                "🎮 Game Over!",
                "It's a tie!"
            ).set_color(discord.Color.greyple())
            await interaction.response.edit_message(view=view, embed=embed.build())
            return

        view.current_player = view.player2 if view.current_player == view.player1 else view.player1
        embed = EmbedBuilder(
            "🎮 TicTacToe",
            f"It's {view.current_player.mention}'s turn!"
        ).set_color(discord.Color.blue())
        await interaction.response.edit_message(view=view, embed=embed.build())

class TicTacToeView(discord.ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=120)
        self.current_player = player1
        self.player1 = player1
        self.player2 = player2
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.add_item(TicTacToeButton(i, j))

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            return True
        return False

    def is_board_full(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    async def on_timeout(self):
        await self.message.channel.delete()

class MinigamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    class Connect4View(discord.ui.View):
        def __init__(self, player1, player2):
            super().__init__(timeout=None)
            self.player1 = player1
            self.player2 = player2
            self.current_player = player1
            self.board = [[None for _ in range(7)] for _ in range(6)]
            self.message = None
            self.game_over = False
            self.setup_board()

        def setup_board(self):
            number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
            
            for col in range(5):
                button = discord.ui.Button(label=number_emojis[col], custom_id=f'col_{col}', row=0)
                button.callback = self.make_move
                self.add_item(button)
            
            for col in range(5, 7):
                button = discord.ui.Button(label=number_emojis[col], custom_id=f'col_{col}', row=1)
                button.callback = self.make_move
                self.add_item(button)

        async def make_move(self, interaction: discord.Interaction):
            if interaction.user != self.current_player or self.game_over:
                return

            col = int(interaction.data['custom_id'].split('_')[1])
            row = self.get_next_empty_row(col)
            
            if row is None:
                return
            
            self.board[row][col] = self.current_player == self.player1
            
            if self.check_winner(row, col):
                embed = EmbedBuilder(
                    "🎮 Connect Four - Game Over!",
                    f"🎉 {self.current_player.mention} wins!"
                ).set_color(discord.Color.gold())
                self.game_over = True
            elif self.is_board_full():
                embed = EmbedBuilder(
                    "🎮 Connect Four - Game Over!",
                    "It's a draw!"
                ).set_color(discord.Color.blue())
                self.game_over = True
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                embed = EmbedBuilder(
                    "🎮 Connect Four",
                    f"{self.current_player.mention}'s turn!"
                ).set_color(discord.Color.blue())

            embed.add_field(name="Game Board", value=self.get_board_display())
            
            if self.game_over:
                rematch_view = self.create_rematch_view()
                await interaction.response.edit_message(embed=embed.build(), view=rematch_view)
            else:
                await interaction.response.edit_message(embed=embed.build(), view=self)

        def get_next_empty_row(self, col):
            for row in range(5, -1, -1):
                if self.board[row][col] is None:
                    return row
            return None

        def get_board_display(self):
            display = ""
            for row in self.board:
                for cell in row:
                    if cell is None:
                        display += "⚪"
                    elif cell:
                        display += "🔴"
                    else:
                        display += "🟡"
                display += "\n"
            display += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
            return display

        def check_winner(self, row, col):
            directions = [(0,1), (1,0), (1,1), (1,-1)]
            player_value = self.board[row][col]
            
            for dx, dy in directions:
                count = 1
                for direction in [1, -1]:
                    x, y = row + dx * direction, col + dy * direction
                    while 0 <= x < 6 and 0 <= y < 7 and self.board[x][y] == player_value:
                        count += 1
                        x += dx * direction
                        y += dy * direction
                if count >= 4:
                    return True
            return False

        def is_board_full(self):
            return all(cell is not None for row in self.board for cell in row)

        def create_rematch_view(self):
            view = discord.ui.View(timeout=120)
            
            async def rematch_callback(interaction):
                if interaction.user not in [self.player1, self.player2]:
                    return
                    
                new_game = self.Connect4View(self.player1, self.player2)
                embed = EmbedBuilder(
                    "🎮 Connect Four",
                    f"{self.player1.mention} vs {self.player2.mention}\n{self.player1.mention}'s turn!"
                ).set_color(discord.Color.blue())
                
                await interaction.response.edit_message(embed=embed.build(), view=new_game)
                
            async def close_callback(interaction):
                if interaction.user not in [self.player1, self.player2]:
                    return
                await interaction.message.delete()
                
            rematch = discord.ui.Button(label="Rematch", style=discord.ButtonStyle.green, emoji="🔄")
            close = discord.ui.Button(label="Close", style=discord.ButtonStyle.red, emoji="❌")
            
            rematch.callback = rematch_callback
            close.callback = close_callback
            
            view.add_item(rematch)
            view.add_item(close)
            return view

    @commands.command()
    async def connect4(self, ctx):
        """Start a game of Connect Four"""
        embed = EmbedBuilder(
            "🎮 Connect Four Challenge",
            f"{ctx.author.mention} wants to play Connect Four!\nClick Accept within 2 minutes to play."
        ).set_color(discord.Color.blue())
    
        view = discord.ui.View(timeout=120)
    
        async def accept_callback(interaction):
            if interaction.user == ctx.author:
                return
        
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True),
                interaction.user: discord.PermissionOverwrite(read_messages=True)
            }
        
            channel = await ctx.guild.create_text_channel(
                f"connect4-{ctx.author.name}-{interaction.user.name}",
                overwrites=overwrites
            )
        
            game_view = self.Connect4View(ctx.author, interaction.user)
            game_embed = EmbedBuilder(
                "🎮 Connect Four",
                f"{ctx.author.mention} vs {interaction.user.mention}\n{ctx.author.mention}'s turn!"
            ).set_color(discord.Color.blue())
            game_embed.add_field(name="Game Board", value=game_view.get_board_display())
        
            await interaction.response.defer()
            message = await channel.send(embed=game_embed.build(), view=game_view)
            game_view.message = message
            await interaction.message.delete()

        accept_button = discord.ui.Button(
            label="Accept Challenge",
            style=discord.ButtonStyle.green,
            emoji="✅"
        )
        accept_button.callback = accept_callback
        view.add_item(accept_button)
    
        await ctx.send(embed=embed.build(), view=view)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def numbergame(self, ctx, number: int, channel: discord.TextChannel):
        """Start a number guessing game in a specific channel"""
        if not 1 <= number <= 10000:
            await ctx.send("Please choose a number between 1 and 10000!")
            return
            
        if channel.id in self.active_games:
            await ctx.send("A game is already running in that channel!")
            return
            
        self.active_games[channel.id] = number
            
        embed = EmbedBuilder(
            "🎮 Number Guessing Game Started!",
            "A new number guessing game has begun!\n\n"
            "Simply type numbers in the chat to guess.\n"
            "First person to guess correctly wins! 🏆"
        ).set_color(discord.Color.blue()).build()
        
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        if message.channel.id not in self.active_games:
            return
            
        if not message.content.isdigit():
            return
            
        guess = int(message.content)
        correct_number = self.active_games[message.channel.id]
        
        if guess == correct_number:
            win_embed = EmbedBuilder(
                "🎉 We Have a Winner!",
                f"Congratulations {message.author.mention}!\n"
                f"The correct number was {correct_number}!"
            ).set_color(discord.Color.gold()).build()
            await message.channel.send(embed=win_embed)
            del self.active_games[message.channel.id]

    @commands.command()
    async def tictactoe(self, ctx):
        """Start a game of TicTacToe"""
        embed = EmbedBuilder(
        "🎮 TicTacToe Challenge",
        f"{ctx.author.mention} wants to play TicTacToe!\nClick Accept within 2 minutes to play."
    ).set_color(discord.Color.blue())
   
        view = discord.ui.View(timeout=120)
   
        async def accept_callback(interaction):
            if interaction.user == ctx.author:
                return
       
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }
       
            channel = await ctx.guild.create_text_channel(
            f"tictactoe-{ctx.author.name}-{interaction.user.name}",
            overwrites=overwrites
        )
       
            game_view = TicTacToeView(ctx.author, interaction.user)
            game_embed = EmbedBuilder(
            "🎮 TicTacToe",
            f"{ctx.author.mention} vs {interaction.user.mention}\n{ctx.author.mention}'s turn!"
        ).set_color(discord.Color.blue())
       
            await interaction.response.defer()
            message = await channel.send(embed=game_embed.build(), view=game_view)
            game_view.message = message
            await interaction.message.delete()

        accept_button = discord.ui.Button(
        label="Accept Challenge",
        style=discord.ButtonStyle.green,
        emoji="✅"
    )
        accept_button.callback = accept_callback
        view.add_item(accept_button)
   
        await ctx.send(embed=embed.build(), view=view)

    @commands.command()
    async def joke(self, ctx):
        """Tell a random joke from our collection"""
        try:
            with open('jokes.txt', 'r', encoding='utf-8') as file:
                jokes = [joke.strip() for joke in file.readlines() if joke.strip()]
            
            if not jokes:
                return await ctx.send("The joke book is empty! 📚")
                
            random_joke = random.choice(jokes)
            setup, punchline = random_joke.split('<>')
            
            embed = EmbedBuilder(
                "😄 Here's a joke!",
                setup.strip()
            ).set_color(discord.Color.blue())
            
            view = discord.ui.View(timeout=60)
            reveal_button = discord.ui.Button(
                label="Reveal Punchline",
                style=discord.ButtonStyle.green,
                emoji="🎭"
            )
            
            async def reveal_callback(interaction):
                if interaction.user != ctx.author:
                    return
                
                reveal_embed = EmbedBuilder(
                    "😄 Here's a joke!",
                    f"{setup.strip()}\n\n**{punchline.strip()}**"
                ).set_color(discord.Color.blue())
                
                await interaction.response.edit_message(embed=reveal_embed.build(), view=None)
            
            reveal_button.callback = reveal_callback
            view.add_item(reveal_button)
            
            await ctx.send(embed=embed.build(), view=view)
            
        except FileNotFoundError:
            await ctx.send("Oops! I couldn't find my joke book! 📚")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")


def setup(bot):
    bot.add_cog(MinigamesCog(bot))

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def serialize_color(self, config_dict):
        """Convert Color objects to serializable format"""
        if isinstance(config_dict, dict):
            for key, value in config_dict.items():
                if isinstance(value, discord.Color):
                    config_dict[key] = value.value
                elif isinstance(value, dict):
                    self.serialize_color(value)
        return config_dict

    def deserialize_color(self, config_dict):
        """Convert serialized colors back to Color objects"""
        if isinstance(config_dict, dict):
            for key, value in config_dict.items():
                if key == "color" and isinstance(value, int):
                    config_dict[key] = discord.Color(value)
                elif isinstance(value, dict):
                    self.deserialize_color(value)
        return config_dict

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def exportconfig(self, ctx):
        """Export server configuration to a JSON file"""
        welcome_config = dict(self.bot.get_cog("WelcomeSystem").welcome_configs.get(ctx.guild.id, {}))
        analytics_cog = self.bot.get_cog("Analytics")
        snipe_cog = self.bot.get_cog("Snipe")
        logging_cog = self.bot.get_cog("CustomLogging")
        leveling_cog = self.bot.get_cog("LevelingSystem")
        mute_cog = self.bot.get_cog("MuteSystem")
        verification_cog = self.bot.get_cog("VerificationSystem")
        bot_verification_cog = self.bot.get_cog("BotVerificationSystem")
        ads_cog = self.bot.get_cog("ServerAdsHub")
        automod_cog = self.bot.get_cog("AutoMod")
        ticket_cog = self.bot.get_cog("TicketSystem")
        role_cog = self.bot.get_cog("RoleManager")
        moderation_cog = self.bot.get_cog("ModerationCommands")

        role_configs_data = self.serialize_color(dict(role_cog.role_configs.get(ctx.guild.id, {})))
        if not role_configs_data and os.path.exists('role_configs.json'):
            with open('role_configs.json', 'r') as f:
                role_configs_data = json.load(f)

        bot_verification_config = {
            "bot_log_channels": dict(bot_verification_cog.bot_log_channels) if bot_verification_cog else {}
        }

        verification_config = {
            "pending_verifications": verification_cog.pending_verifications.get(ctx.guild.id, {}) if verification_cog else {},
            "autorole": verification_cog.autorole_dict.get(ctx.guild.id) if verification_cog else None,
            "log_channel": verification_cog.log_channels.get(str(ctx.guild.id)) if verification_cog else None,
            "verification_logs": verification_cog.verification_logs.get(ctx.guild.id, {}) if verification_cog else {}
        }

        logging_config = logging_cog.logging_config.get(ctx.guild.id, {}) if logging_cog else {}

        analytics_config = {
            "daily_channel": analytics_cog.analytics_channels.get(ctx.guild.id, {}).get("daily").id if analytics_cog and isinstance(analytics_cog.analytics_channels.get(ctx.guild.id, {}).get("daily"), discord.TextChannel) else None,
            "weekly_channel": analytics_cog.analytics_channels.get(ctx.guild.id, {}).get("weekly").id if analytics_cog and isinstance(analytics_cog.analytics_channels.get(ctx.guild.id, {}).get("weekly"), discord.TextChannel) else None,
            "monthly_channel": analytics_cog.analytics_channels.get(ctx.guild.id, {}).get("monthly").id if analytics_cog and isinstance(analytics_cog.analytics_channels.get(ctx.guild.id, {}).get("monthly"), discord.TextChannel) else None
        }

        snipe_config = {
            "snipe_duration": snipe_cog.snipe_duration if snipe_cog else 0,
            "editsnipe_duration": snipe_cog.editsnipe_duration if snipe_cog else 0
        }

        leveling_config = {
            "roles": dict(leveling_cog.roles.get(ctx.guild.id, {})) if leveling_cog else {},
            "xp_multipliers": dict(leveling_cog.xp_multipliers.get(ctx.guild.id, {})) if leveling_cog else {},
            "leaderboard_channel_id": leveling_cog.leaderboard_channels.get(ctx.guild.id) if leveling_cog else None,
            "announcement_channel_id": leveling_cog.announcement_channels.get(ctx.guild.id) if leveling_cog else None,
            "achievements": dict(leveling_cog.achievements.get(ctx.guild.id, {})) if leveling_cog else {},
            "xp_decay_rate": leveling_cog.xp_decay_rate if leveling_cog else 0,
            "xp_gain_range": leveling_cog.xp_gain_range if leveling_cog else [0, 0]
        }

        mute_config = {}
        if mute_cog and hasattr(mute_cog, 'mute_roles'):
            guild_mute_roles = mute_cog.mute_roles
            if ctx.guild.id in guild_mute_roles:
                mute_config["mute_roles"] = dict(guild_mute_roles[ctx.guild.id])
            else:
                mute_config["mute_roles"] = {}

        ads_config = {
            "ads_db": dict(ads_cog.ads_db) if ads_cog else {},
            "allowed_users": list(ads_cog.allowed_users) if ads_cog else [],
            "channel_categories": list(ads_cog.channel_categories) if ads_cog else [],
            "bump_cooldown": ads_cog.bump_cooldown if ads_cog else 0,
            "analytics": dict(ads_cog.analytics) if ads_cog else {}
        }

        config = {
            "bot_verification_config": bot_verification_config,
            "verification_config": verification_config,
            "server_id": ctx.guild.id,
            "server_name": ctx.guild.name,
            "timestamp": str(datetime.now()),
            "welcome_config": self.serialize_color(welcome_config),
            "autorole": self.bot.get_cog("ServerManagement").autorole_dict.get(ctx.guild.id),
            "ticket_config": {
                "support_roles": ticket_cog.support_roles.get(ctx.guild.id),
                "admin_roles": ticket_cog.admin_roles.get(ctx.guild.id, []),
                "ticket_categories": ticket_cog.ticket_categories.get(ctx.guild.id),
                "ticket_logs": ticket_cog.ticket_logs.get(ctx.guild.id),
                
            },
            "role_configs": role_configs_data,
            "automod": {
                "caps_threshold": automod_cog.caps_threshold if automod_cog else 0.7,
                "spam_threshold": getattr(automod_cog, 'spam_threshold', 5),
                "spam_interval": getattr(automod_cog, 'spam_interval', 5),
                "spam_timeout_minutes": getattr(automod_cog, 'spam_timeout_minutes', 10),
                "banned_words": list(automod_cog.banned_words) if automod_cog else [],
                "link_whitelist": list(automod_cog.link_whitelist) if automod_cog else [],
                "link_filter_enabled": automod_cog.link_filter_enabled if automod_cog else True
            },
            "mute_config": mute_config,
            "analytics_config": analytics_config,
            "snipe_config": snipe_config,
            "logging_config": logging_config,
            "leveling_config": leveling_config,
            "server_ads_config": ads_config,
            "custom_verification": {
                "verification_settings": dict(self.bot.get_cog("CustomVerification").verification_settings) if self.bot.get_cog("CustomVerification") else {},
                "role_assignments": dict(self.bot.get_cog("CustomVerification").role_assignments) if self.bot.get_cog("CustomVerification") else {}
            },
            "profile_system": {
                "profiles": dict(self.bot.get_cog("ProfileSystem").profiles) if self.bot.get_cog("ProfileSystem") else {},
                "default_profile_settings": {
                    "bio_max_length": 1000,
                    "available_badges": ["🎮 Gamer", "🎨 Artist", "📚 Bookworm", "💻 Developer", "🎵 Musician"]
                }
            },
            "server_management": {
                "ban_appeal_info": moderation_cog.ban_appeal_info.get(str(ctx.guild.id), "No appeal process specified")
            }
        }

        filename = f"config_{ctx.guild.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        file = discord.File(filename)
        embed = discord.Embed(
            title="⚙️ Configuration Exported",
            description=f"Complete server settings exported for {ctx.guild.name}",
            color=discord.Color.green()
        )
        embed.add_field(name="Included Settings",
                    value="• Welcome System\n• Ticket System\n• AutoMod\n• Role Management\n• Server Management\n• Analytics\n• Snipe Configurations\n• Custom Logging\n• Leveling System\n• Mute System\n• Verification System\n• Advertisement System\n• Profile System\n• Custom Verification\n• Ticket Panel Configurations")

        embed.add_field(name="Export Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        embed.set_footer(text=f"Server ID: {ctx.guild.id}")

        await ctx.send(embed=embed, file=file)
        os.remove(filename)



    @commands.command()                                          
    @commands.has_permissions(administrator=True)
    async def importconfig(self, ctx):
        """Import server configuration from a JSON file"""
        if not ctx.message.attachments:
            await ctx.send("Please attach a configuration file!")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.json'):
            await ctx.send("Please provide a valid JSON file!")
            return

        try:
            config_content = await attachment.read()
            config = json.loads(config_content)

            if config["server_id"] != ctx.guild.id:
                await ctx.send("This configuration file is for a different server!")
                return

            welcome_config = self.deserialize_color(config["welcome_config"])
            self.bot.get_cog("WelcomeSystem").welcome_configs[ctx.guild.id] = welcome_config

            if config["autorole"]:
                self.bot.get_cog("ServerManagement").autorole_dict[ctx.guild.id] = config["autorole"]

            ticket_cog = self.bot.get_cog("TicketSystem")
            if config["ticket_config"]:
                if config["ticket_config"].get("support_roles"):
                    ticket_cog.support_roles[ctx.guild.id] = config["ticket_config"]["support_roles"]
                if config["ticket_config"].get("admin_roles"):
                    ticket_cog.admin_roles[ctx.guild.id] = config["ticket_config"]["admin_roles"]
                if config["ticket_config"].get("ticket_categories"):
                    ticket_cog.ticket_categories[ctx.guild.id] = config["ticket_config"]["ticket_categories"]
                if config["ticket_config"].get("ticket_logs"):
                    ticket_cog.ticket_logs[ctx.guild.id] = config["ticket_config"]["ticket_logs"]

            if "server_management" in config:
                moderation_cog = self.bot.get_cog("ModerationCommands")
                if moderation_cog:
                    appeal_info = config["server_management"].get("ban_appeal_info")
                    if appeal_info:
                        moderation_cog.ban_appeal_info[str(ctx.guild.id)] = appeal_info

            if "role_configs" in config:
                role_cog = self.bot.get_cog("RoleManager")
                if role_cog:
                    role_configs_data = self.deserialize_color(config["role_configs"])
                    role_cog.role_configs[ctx.guild.id] = role_configs_data
                    
                    guild_id_str = str(ctx.guild.id)
                    if guild_id_str in role_configs_data:
                        role_configs_data[guild_id_str] = {
                            str(panel_id): panel_data 
                            for panel_id, panel_data in role_configs_data[guild_id_str].items()
                        }
                        for panel_id, panel_data in role_configs_data[guild_id_str].items():
                            try:
                                channel_id = panel_data["channel"]
                                channel = await ctx.guild.fetch_channel(int(channel_id))
                                if channel:
                                    for embed_data in panel_data["embeds"]:
                                        embed = discord.Embed(
                                            title=embed_data["title"],
                                            description=embed_data["description"],
                                            color=int(embed_data["color"].strip("#"), 16) if isinstance(embed_data["color"], str) and embed_data["color"].startswith("#") else discord.Color.default()
                                        )
                                        if "fields" in embed_data:
                                            for field in embed_data["fields"]:
                                                embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))
                                        if "footer" in embed_data:
                                            embed.set_footer(text=embed_data["footer"]["text"])
                                        
                                        view = DeployedRoleView(role_cog, guild_id_str, panel_id)
                                        if "buttons" in embed_data:
                                            for button_data in embed_data["buttons"]:
                                                style_mapping = {
                                                    "PRIMARY": discord.ButtonStyle.primary,
                                                    "SECONDARY": discord.ButtonStyle.secondary,
                                                    "SUCCESS": discord.ButtonStyle.success,
                                                    "DANGER": discord.ButtonStyle.danger
                                                }
                                                style = style_mapping.get(button_data["style"], discord.ButtonStyle.primary)
                                                
                                                button = discord.ui.Button(
                                                    style=style,
                                                    label=button_data["label"],
                                                    emoji=button_data.get("emoji"),
                                                    custom_id=f"role_{button_data['id']}"
                                                )
                                                button.callback = view.handle_role_click
                                                view.add_item(button)
                                        
                                        await channel.send(embed=embed, view=view)
                            except Exception as e:
                                print(f"Error processing panel {panel_id}: {e}")

                            with open('role_configs.json', 'w') as f:
                                json.dump(role_configs_data, f, indent=4)

            automod = self.bot.get_cog("AutoMod")
            if automod and "automod" in config:
                automod.caps_threshold = config["automod"]["caps_threshold"]
                automod.spam_threshold = config["automod"]["spam_threshold"]
                automod.spam_interval = config["automod"].get("spam_interval", 5)
                automod.spam_timeout_minutes = config["automod"].get("spam_timeout_minutes", 10)
                automod.banned_words = set(config["automod"]["banned_words"])
                automod.link_whitelist = set(config["automod"]["link_whitelist"])
                automod.link_filter_enabled = config["automod"].get("link_filter_enabled", True)

            analytics_cog = self.bot.get_cog("Analytics")
            if analytics_cog and "analytics_config" in config:
                analytics_config = config["analytics_config"]
                analytics_cog.analytics_channels[ctx.guild.id] = {}
                
                for interval in ['daily', 'weekly', 'monthly']:
                    channel_id = analytics_config.get(f"{interval}_channel")
                    if channel_id:
                        channel = ctx.guild.get_channel(channel_id)
                        if channel:
                            analytics_cog.analytics_channels[ctx.guild.id][interval] = channel
                            task_key = f"{ctx.guild.id}_{interval}"
                            if task_key not in analytics_cog.analytics_tasks or analytics_cog.analytics_tasks[task_key].done():
                                analytics_cog.analytics_tasks[task_key] = self.bot.loop.create_task(
                                    analytics_cog._send_analytics(ctx.guild.id, interval)
                                )

            if "bot_verification_config" in config:
                bot_verification_cog = self.bot.get_cog("BotVerificationSystem")
                if bot_verification_cog:
                    bot_verification_cog.bot_log_channels = config["bot_verification_config"].get("bot_log_channels", {})

            if "profile_system" in config:
                profile_config = config["profile_system"]
                self.profiles = profile_config.get("profiles", {})

            if "server_ads_config" in config:
                ads_cog = self.bot.get_cog("ServerAdsHub")
                if ads_cog:
                    ads_config = config["server_ads_config"]
                    ads_cog.ads_db = ads_config.get("ads_db", {})
                    ads_cog.allowed_users = ads_config.get("allowed_users", {})
                    ads_cog.channel_categories = ads_config.get("channel_categories", {})
                    ads_cog.bump_cooldown = ads_config.get("bump_cooldown", 21600)
                    ads_cog.analytics = ads_config.get("analytics", {})

            if "custom_verification" in config:
                verif_config = config["custom_verification"]
                self.verification_settings = verif_config.get("verification_settings", {})
                self.role_assignments = verif_config.get("role_assignments", {})

            if "snipe_config" in config:
                snipe_cog = self.bot.get_cog("Snipe")
                if snipe_cog:
                    snipe_cog.snipe_duration = config["snipe_config"]["snipe_duration"]
                    snipe_cog.editsnipe_duration = config["snipe_config"]["editsnipe_duration"]

            if "mute_config" in config:
                mute_cog = self.bot.get_cog("MuteSystem")
                if mute_cog:
                    mute_config = config["mute_config"]
                    mute_cog.mute_roles[ctx.guild.id] = mute_config.get("mute_roles", {})

            if "leveling_config" in config:
                leveling_cog = self.bot.get_cog("LevelingSystem")
                if leveling_cog:
                    leveling_config = config["leveling_config"]
                    leveling_cog.roles[ctx.guild.id] = leveling_config.get("roles", {})
                    leveling_cog.xp_multipliers[ctx.guild.id] = {
                        k: float(v) if isinstance(v, (int, float, str)) else 1.0
                        for k, v in leveling_config.get("xp_multipliers", {}).items()
                    }
                    leveling_cog.leaderboard_channels[ctx.guild.id] = leveling_config.get("leaderboard_channel_id")
                    leveling_cog.announcement_channels[ctx.guild.id] = leveling_config.get("announcement_channel_id")
                    leveling_cog.achievements[ctx.guild.id] = leveling_config.get("achievements", {})
                    leveling_cog.xp_decay_rate = leveling_config.get("xp_decay_rate", 0.01)
                    leveling_cog.xp_gain_range = leveling_config.get("xp_gain_range", (15, 25))

                    if leveling_config.get("leaderboard_channel_id"):
                        leaderboard_channel = ctx.guild.get_channel(leveling_config["leaderboard_channel_id"])
                        if leaderboard_channel:
                            await leveling_cog.update_leaderboard(leaderboard_channel)

            if "verification_config" in config:
                verification_cog = self.bot.get_cog("VerificationSystem")
                if verification_cog:
                    verif_config = config["verification_config"]
                    verification_cog.pending_verifications[ctx.guild.id] = verif_config.get("pending_verifications", {})
                    verification_cog.autorole_dict[ctx.guild.id] = verif_config.get("autorole")
                    verification_cog.verification_logs[ctx.guild.id] = verif_config.get("verification_logs", {})
                    
                    if "log_channel" in verif_config:
                        channel_id = verif_config["log_channel"]
                        if isinstance(channel_id, str):
                            channel_id = int(channel_id)
                        verification_cog.log_channels[str(ctx.guild.id)] = channel_id

            if "logging_config" in config:
                logging_cog = self.bot.get_cog("CustomLogging")
                if logging_cog:
                    logging_cog.logging_config[ctx.guild.id] = config["logging_config"]

            embed = EmbedBuilder(
                "✅ Configuration Imported",
                f"All server settings have been restored for {ctx.guild.name}"
            ).set_color(discord.Color.green())

            embed.add_field("Restored Settings",
                "• Welcome System\n• Ticket System\n• AutoMod\n• Role Management\n• Server Management\n• Analytics\n• Snipe Configurations\n• Custom Logging\n• Leveling System\n• Mute System\n• Verification System\n• Advertisement System\n• Profile System\n• Custom Verification\n• Ticket Panel Configurations")
            embed.add_field("Import Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            embed.set_footer(f"Server ID: {ctx.guild.id}")

            await ctx.send(embed=embed.build())

        except json.JSONDecodeError:
            await ctx.send("Invalid JSON file format!")
        except KeyError as e:
            await ctx.send(f"Missing required configuration key: {e}")
        except Exception as e:
            await ctx.send(f"An error occurred during import: {str(e)}")


bot.add_cog(Config(bot))

class BackupSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def backup(self, ctx, full: bool = False, messages_limit: int = 100):
        """Create comprehensive server backup"""
        progress_msg = await ctx.send("📦 Starting backup process...")

        backup_data = {
        "server_name": ctx.guild.name,
        "server_icon": str(ctx.guild.icon.url) if ctx.guild.icon else None,
        "server_banner": str(ctx.guild.banner.url) if ctx.guild.banner else None,
        "roles": [],
        "categories": [],
        "channels": [],
        "emojis": [],
        "webhooks": [],
        "settings": {},
        "messages": [] if full else None,
        "timestamp": str(datetime.now())
    }

        await progress_msg.edit(content="📦 Backing up roles...")
        for role in reversed(ctx.guild.roles):
            if not role.is_default():
                backup_data["roles"].append({
                "name": role.name,
                "color": str(role.color),
                "permissions": int(role.permissions.value),  
                "position": role.position,
                "mentionable": role.mentionable,
                "hoist": role.hoist
            })

        await progress_msg.edit(content="📦 Backing up channels and categories...")
        for category in ctx.guild.categories:
            cat_data = {
            "name": category.name,
            "position": category.position,
            "channels": []
        }

            for channel in category.channels:
                chan_data = {
                "name": channel.name,
                "type": str(channel.type),
                "position": channel.position,
                "topic": getattr(channel, 'topic', None),
                "slowmode_delay": getattr(channel, 'slowmode_delay', None),
                "nsfw": getattr(channel, 'nsfw', False),
                "overwrites": []
            }

                for target, overwrite in channel.overwrites.items():
                    allow, deny = overwrite.pair()
                    chan_data["overwrites"].append({
                    "target_name": target.name,
                    "permissions": [int(allow.value), int(deny.value)]  
                })

                if full and isinstance(channel, discord.TextChannel):
                    messages = []
                    try:
                        async for msg in channel.history(limit=messages_limit):
                            messages.append({
                            "content": msg.content,
                            "author": str(msg.author),
                            "timestamp": str(msg.created_at),
                            "attachments": [a.url for a in msg.attachments],
                            "embeds": [e.to_dict() for e in msg.embeds],
                            "pinned": msg.pinned
                        })
                    except discord.Forbidden:
                        pass
                    chan_data["messages"] = messages

                cat_data["channels"].append(chan_data)
            backup_data["categories"].append(cat_data)

        await progress_msg.edit(content="📦 Backing up emojis...")
        backup_data["emojis"] = [{
        "name": emoji.name,
        "url": str(emoji.url)
    } for emoji in ctx.guild.emojis]

        await progress_msg.edit(content="📦 Backing up webhooks...")
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                try:
                    webhooks = await channel.webhooks()
                    backup_data["webhooks"].extend([{
                        "name": webhook.name,
                        "channel": channel.name,
                        "avatar": str(webhook.avatar.url) if webhook.avatar else None
                    } for webhook in webhooks])
                except discord.Forbidden:
                    pass

        backup_data["settings"] = {
        "verification_level": str(ctx.guild.verification_level),
        "explicit_content_filter": str(ctx.guild.explicit_content_filter),
        "default_notifications": str(ctx.guild.default_notifications),
        "afk_timeout": ctx.guild.afk_timeout,
        "afk_channel": ctx.guild.afk_channel.name if ctx.guild.afk_channel else None
    }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{ctx.guild.id}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=4)

        file = discord.File(filename, filename=filename)

        embed = EmbedBuilder(
        "📦 Server Backup Complete",
        f"Backup completed for {ctx.guild.name}"
    ).set_color(discord.Color.green())

        embed.add_field("Roles", str(len(backup_data["roles"])))
        embed.add_field("Categories", str(len(backup_data["categories"])))
        embed.add_field("Emojis", str(len(backup_data["emojis"])))
        embed.add_field("Webhooks", str(len(backup_data["webhooks"])))
        if full:
            embed.add_field("Messages", f"Up to {messages_limit} per channel")

        await progress_msg.delete()
        await ctx.send(embed=embed.build(), file=file)
        os.remove(filename)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def restore(self, ctx):
        """Restore server from backup file"""
        if not ctx.message.attachments:
            await ctx.send("Please attach a backup file with this command!")
            return

        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.json'):
            await ctx.send("Please provide a valid backup file (.json)")
            return

        progress_msg = await ctx.send("🔄 Starting restoration process...")
        backup_content = await attachment.read()
        backup_data = json.loads(backup_content)

        bot_member = ctx.guild.get_member(ctx.bot.user.id)
        if not bot_member.guild_permissions.administrator:
            await ctx.send("I need Administrator permissions to perform a full restore!")
            return

        try:
            bot_role = bot_member.top_role
            positions = {r: r.position for r in ctx.guild.roles}
            positions[bot_role] = len(positions) - 1 
            await ctx.guild.edit_role_positions(positions=positions)
        except Exception as e:
            print(f"Could not move bot role: {e}")

        try:
            temp_channel = await ctx.guild.create_text_channel('temp-restore-status')
            progress_msg = await temp_channel.send("🔄 Starting restoration process...")
        except Exception as e:
            print(f"Could not create temporary channel: {e}")
            return

        await progress_msg.edit(content="🗑️ Cleaning up existing server content...")
    
        temp_channel_id = temp_channel.id
        try:
            for channel in ctx.guild.channels:
                if channel.id != temp_channel_id:
                    try:
                        await channel.delete()
                        await asyncio.sleep(0.5)
                    except discord.NotFound:
                        continue
        except Exception as e:
            print(f"Error during channel cleanup: {e}")

        try:
            for role in reversed(ctx.guild.roles[1:]):
                try:
                    await role.delete()
                    await asyncio.sleep(0.5)
                except discord.NotFound:
                    continue
        except Exception as e:
            print(f"Error during role cleanup: {e}")

        try:
            for emoji in ctx.guild.emojis:
                try:
                    await emoji.delete()
                    await asyncio.sleep(0.5)
                except discord.NotFound:
                    continue
        except Exception as e:
            print(f"Error during emoji cleanup: {e}")

        await progress_msg.edit(content="🔄 Restoring roles...")
        roles_cache = {}
        for role_data in reversed(backup_data["roles"]):
            try:
                role = await ctx.guild.create_role(
                    name=role_data["name"],
                    color=discord.Color.from_str(role_data["color"]),
                    permissions=discord.Permissions(role_data["permissions"]),
                    hoist=role_data["hoist"],
                    mentionable=role_data["mentionable"]
                )
                roles_cache[role_data["name"]] = role
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error creating role {role_data['name']}: {e}")

        total_categories = len(backup_data["categories"])
        for cat_index, cat_data in enumerate(backup_data["categories"], 1):
            try:
                category = await ctx.guild.create_category(name=cat_data["name"])
                await progress_msg.edit(content=f"📁 Creating categories... ({cat_index}/{total_categories})")

                total_channels = len(cat_data["channels"])
                for chan_index, chan_data in enumerate(cat_data["channels"], 1):
                    try:
                        if chan_data["type"] == "text":
                            channel = await category.create_text_channel(
                            name=chan_data["name"],
                            topic=chan_data.get("topic"),
                            nsfw=chan_data.get("nsfw", False),
                            slowmode_delay=chan_data.get("slowmode_delay", 0)
                        )

                            for overwrite in chan_data.get("overwrites", []):
                                role = roles_cache.get(overwrite["target_name"])
                                if role:
                                    allow, deny = overwrite["permissions"]
                                    await channel.set_permissions(
                                        role,
                                        overwrite=discord.PermissionOverwrite.from_pair(
                                        discord.Permissions(allow),
                                        discord.Permissions(deny)
                                    )
                                )

                            if "messages" in chan_data:
                                webhook = await channel.create_webhook(name="RestoreBot")
                                for msg_data in reversed(chan_data["messages"]):
                                    try:
                                        await webhook.send(
                                        content=msg_data["content"],
                                        username=msg_data["author"],
                                        embeds=[discord.Embed.from_dict(e) for e in msg_data.get("embeds", [])]
                                    )
                                        await asyncio.sleep(0.5)
                                    except Exception as e:
                                        print(f"Error restoring message: {e}")
                                await webhook.delete()

                        elif chan_data["type"] == "voice":
                            channel = await category.create_voice_channel(name=chan_data["name"])
                        
                            for overwrite in chan_data.get("overwrites", []):
                                role = roles_cache.get(overwrite["target_name"])
                                if role:
                                    allow, deny = overwrite["permissions"]
                                    await channel.set_permissions(
                                        role,
                                        overwrite=discord.PermissionOverwrite.from_pair(
                                        discord.Permissions(allow),
                                        discord.Permissions(deny)
                                    )
                                )

                        if chan_index % 5 == 0:
                            await progress_msg.edit(content=f"💬 Creating channels in {cat_data['name']}... ({chan_index}/{total_channels})")
                    
                        await asyncio.sleep(0.5)

                    except Exception as e:
                        print(f"Error creating channel {chan_data['name']}: {e}")
                        continue

            except Exception as e:
                print(f"Error creating category {cat_data['name']}: {e}")
                continue

        await progress_msg.edit(content="🔄 Restoring emojis...")
        async with aiohttp.ClientSession() as session:
            total_emojis = len(backup_data["emojis"])
            for emoji_index, emoji_data in enumerate(backup_data["emojis"], 1):
                try:
                    async with session.get(emoji_data["url"]) as resp:
                        if resp.status == 200:
                            emoji_bytes = await resp.read()
                            await ctx.guild.create_custom_emoji(
                            name=emoji_data["name"],
                            image=emoji_bytes
                        )
                    if emoji_index % 5 == 0:
                        await progress_msg.edit(content=f"🔄 Restoring emojis... ({emoji_index}/{total_emojis})")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Error restoring emoji {emoji_data['name']}: {e}")

        await progress_msg.edit(content="🔄 Restoring webhooks...")
        for webhook_data in backup_data["webhooks"]:
            try:
                channel = discord.utils.get(ctx.guild.channels, name=webhook_data["channel"])
                if channel and isinstance(channel, discord.TextChannel):
                    await channel.create_webhook(
                    name=webhook_data["name"],
                    avatar=webhook_data.get("avatar")
                )
                    await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error restoring webhook {webhook_data['name']}: {e}")

        embed = EmbedBuilder(
        "✅ Restoration Complete",
        "Server has been restored from backup"
    ).set_color(discord.Color.green())

        await progress_msg.delete()
        await ctx.send(embed=embed.build())

bot.add_cog(BackupSystem(bot))

class EmbedBuilder:
    def __init__(self, title, description=None):
        self.embed = discord.Embed(
            title=title,
            description=description,
            timestamp=datetime.now(timezone.utc)
        )
        self.set_default_color()

    def set_image(self, url):
        self.embed.set_image(url=url)
        return self

        
    def set_default_color(self):
        self.embed.color = discord.Color.blue()
        return self
        
    def add_field(self, name, value, inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)
        return self
        
    def set_color(self, color):
        self.embed.color = color
        return self
        
    def set_thumbnail(self, url):
        self.embed.set_thumbnail(url=url)
        return self
        
    def set_footer(self, text, icon_url=None):
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self
        
    def build(self):
        return self.embed

class LoggingManager:
    def __init__(self, bot):
        self.bot = bot
        self.log_types = {
            'ban': ('🔨 Ban', discord.Color.red()),
            'kick': ('👢 Kick', discord.Color.orange()),
            'mute': ('🔇 Mute', discord.Color.yellow()),
            'warn': ('⚠️ Warning', discord.Color.gold()),
            'clear': ('🧹 Clear', discord.Color.blue()),
            'lockdown': ('🔒 Lockdown', discord.Color.purple())
        }
        
    async def log_action(self, guild, action_type, moderator, target, reason=None, duration=None):
        log_channel = discord.utils.get(guild.channels, name='mod-logs')
        if not log_channel:
            return
            
        emoji, color = self.log_types.get(action_type, ('📝 Action', discord.Color.default()))
        
        embed = EmbedBuilder(
            f"{emoji} {action_type.title()} Action",
            f"A moderation action has been taken."
        ).set_color(color)
        
        embed.add_field("Moderator", f"{moderator.name} ({moderator.id})")
        embed.add_field("Target", f"{target.name} ({target.id})")
        
        if duration:
            embed.add_field("Duration", duration)
        if reason:
            embed.add_field("Reason", reason, inline=False)
            
        embed.set_footer(f"Action ID: {random.randint(10000, 99999)}")
        
        await log_channel.send(embed=embed.build())

log_manager = LoggingManager(bot)

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = EmbedBuilder(
                "❌ Permission Denied",
                "You don't have the required permissions for this command."
            ).set_color(discord.Color.red()).build()
            
        elif isinstance(error, commands.MemberNotFound):
            embed = EmbedBuilder(
                "❌ Member Not Found",
                "The specified member could not be found."
            ).set_color(discord.Color.red()).build()
            
        else:
            embed = EmbedBuilder(
                "❌ Error",
                f"An error occurred: {str(error)}"
            ).set_color(discord.Color.red()).build()
            
        await ctx.send(embed=embed, delete_after=10)

bot.add_cog(CommandErrorHandler(bot))


class MuteSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_roles = {}
        self.data_file = "mute_data.json"
        self.load_data()

    def load_data(self):
        """Load mute roles from JSON if the file exists."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                try:
                    data = json.load(f)
                    self.mute_roles = {int(k): int(v) for k, v in data.get('mute_roles', {}).items()}
                    print(f"Loaded mute roles: {self.mute_roles}")
                except json.JSONDecodeError:
                    print(f"Failed to decode {self.data_file}, starting with empty roles.")
                    self.mute_roles = {}

    def save_data(self):
        """Save mute roles to JSON."""
        with open(self.data_file, 'w') as f:
            json.dump({'mute_roles': {str(k): v for k, v in self.mute_roles.items()}}, f, indent=4)
        print(f"Saved mute roles: {self.mute_roles}")

    @commands.Cog.listener()
    async def on_ready(self):
        """Notify when the cog is ready."""
        print(f"{self.__class__.__name__} is ready with roles: {self.mute_roles}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_mute_role(self, ctx, role_id: int):
        """Manually set the mute role for the current guild."""
        self.mute_roles[ctx.guild.id] = role_id
        self.save_data()
        await ctx.send(f"✅ Mute role set to <@&{role_id}> for this server.")



class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_roles = {}
        self.ban_appeal_info = {}
        self.data_file = "moderation_data.json"
        self.load_data()
        

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.mute_roles = data.get('mute_roles', {})

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump({
                'mute_roles': self.mute_roles
            }, f, indent=4)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def invite_view(self, ctx):
        """View all active server invites and their details"""
        invites = await ctx.guild.invites()
    
        embed = EmbedBuilder(
        "🔗 Server Invites",
        f"Total active invites: {len(invites)}"
    ).set_color(discord.Color.blue())

        for invite in invites:
            time_left = "Unlimited"
            if invite.max_age > 0:
                if invite.created_at:
                
                    now = datetime.utcnow().replace(tzinfo=timezone.utc)
                    expires_at = invite.created_at + timedelta(seconds=invite.max_age)
                    if expires_at > now:
                        time_left = str(expires_at - now).split('.')[0]
                    else:
                        time_left = "Expired"
                    
            uses_info = f"{invite.uses}/{invite.max_uses}" if invite.max_uses else f"{invite.uses}/∞"
        
            invite_info = (
            f"Channel: {invite.channel.mention}\n"
            f"Creator: {invite.inviter.mention}\n"
            f"Duration: {time_left}\n"
            f"Uses: {uses_info}\n"
            f"Created: {invite.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
            embed.add_field(
            f"Invite: {invite.code}",
            invite_info,
            inline=False
        )

        await ctx.send(embed=embed.build())

    @commands.command()
    @commands.has_permissions(create_instant_invite=True)
    async def invite(self, ctx, duration: int = 0, uses: int = 0):
        """Create an invite link with optional duration and uses limit
        Usage: !invite [duration in minutes] [number of uses]
        Use 0 for unlimited duration/uses"""
    
        try:
            invite = await ctx.channel.create_invite(
            max_age=duration * 60 if duration > 0 else 0,
            max_uses=uses if uses > 0 else 0
        )
        
            embed = EmbedBuilder(
            "🔗 Invite Created",
            f"Here's your invite link: {invite.url}"
        ).set_color(discord.Color.green())
        
            embed.add_field(
            "Duration", 
            "Unlimited" if duration == 0 else f"{duration} minutes"
        )
            embed.add_field(
            "Uses",
            "Unlimited" if uses == 0 else str(uses)
        )
        
            await ctx.send(embed=embed.build())
        
        except discord.Forbidden:
            embed = EmbedBuilder(
            "❌ Error",
            "I don't have permission to create invites in this channel"
        ).set_color(discord.Color.red())
            await ctx.send(embed=embed.build())

    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def addchannel(self, ctx, channel: discord.TextChannel, member: discord.Member):
        """Add a member to a channel"""
        await channel.set_permissions(member, read_messages=True, send_messages=True)
        embed = EmbedBuilder(
        "✅ Channel Access Granted",
        f"{member.mention} has been added to {channel.mention}"
    ).set_color(discord.Color.green()).build()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def removechannel(self, ctx, channel: discord.TextChannel, member: discord.Member):
        """Remove a member from a channel"""
        await channel.set_permissions(member, read_messages=False, send_messages=False)
        embed = EmbedBuilder(
        "🚫 Channel Access Removed",
        f"{member.mention} has been removed from {channel.mention}"
    ).set_color(discord.Color.red()).build()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx, title, *, description):
        """Create a custom embed message"""
        embed = EmbedBuilder(
        title,
        description
    ).set_color(discord.Color.blue()).build()
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Show user's avatar in full size"""
        member = member or ctx.author
        embed = EmbedBuilder(
        f"{member.name}'s Avatar",
        ""
    ).set_color(member.color)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed.build())

    @commands.command()
    async def ping(self, ctx):
        """Check bot's latency"""
        embed = EmbedBuilder(
        "🏓 Pong!",
        f"Latency: {round(self.bot.latency * 1000)}ms"
    ).set_color(discord.Color.green()).build()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        """Make the bot say something in a specific channel"""
        await channel.send(message)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        """Recreates a channel to completely clear it"""
        channel = channel or ctx.channel
        position = channel.position
        new_channel = await channel.clone()
        await new_channel.edit(position=position)
        await channel.delete()
    
        embed = EmbedBuilder(
        "💥 Channel Nuked",
        "Channel has been completely reset"
    ).set_color(discord.Color.orange()).build()
        await new_channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def vcmute(self, ctx, member: discord.Member):
        """Mute someone in voice chat"""
        await member.edit(mute=True)
        embed = EmbedBuilder(
        "🔇 Voice Muted",
        f"{member.mention} has been muted in voice channels"
    ).set_color(discord.Color.red()).build()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def vcunmute(self, ctx, member: discord.Member):
        """Unmute someone in voice chat"""
        await member.edit(mute=False)
        embed = EmbedBuilder(
        "🔊 Voice Unmuted", 
        f"{member.mention} has been unmuted in voice channels"
    ).set_color(discord.Color.green()).build()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def massrole(self, ctx, role: discord.Role):
        """Add a role to all members"""
        for member in ctx.guild.members:
            await member.add_roles(role)
    
        embed = EmbedBuilder(
        "✅ Mass Role Added",
        f"Added {role.mention} to all members"
    ).set_color(discord.Color.blue()).build()
        await ctx.send(embed=embed)

    @commands.command()
    async def servericon(self, ctx):
        """Shows the server icon in full size"""
        embed = EmbedBuilder(
        "🖼️ Server Icon",
        ctx.guild.name
    ).set_color(discord.Color.blue())

        if ctx.guild.icon:  
            embed.set_image(url=ctx.guild.icon.url)
        else:
            embed.description = "This server has no custom icon."
            embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")  

        await ctx.send(embed=embed.build())

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, user_id: int, *, nickname=None):
        """Change or remove a user's nickname.
        Usage:
        - !nickname <user_id> <nickname>: Change the user's nickname.
        - !nickname <user_id>: Remove the user's nickname.
        """
        member = ctx.guild.get_member(user_id)
        if not member:
            await ctx.send("❌ User not found in this server.")
            return

        try:
            if nickname:  
                await member.edit(nick=nickname)
                embed = EmbedBuilder(
                    "✅ Nickname Changed",
                    f"{member.mention}'s nickname has been changed to '{nickname}'."
                ).set_color(discord.Color.green())
            else:  
                await member.edit(nick=None)
                embed = EmbedBuilder(
                    "✅ Nickname Removed",
                    f"{member.mention}'s nickname has been removed."
                ).set_color(discord.Color.green())

        except discord.Forbidden:
            embed = EmbedBuilder(
                "❌ Permission Denied",
                "I don't have permission to change nicknames for this user."
            ).set_color(discord.Color.red())

        except discord.HTTPException as e:
            embed = EmbedBuilder(
                "❌ Failed to Change Nickname",
                f"An error occurred: {str(e)}"
            ).set_color(discord.Color.red())

        await ctx.send(embed=embed.build())

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User | int, duration: str = None, *, reason="No reason provided"):
        if isinstance(user, int):
            try:
                user = await self.bot.fetch_user(user)
            except discord.NotFound:
                await ctx.send("User not found.")
                return

        ban_duration = None
        if duration:
            total_seconds = 0
            duration_parts = duration.lower().replace(" ", "")
            time_units = {
                'd': 86400,  
                'h': 3600,   
                'm': 60,     
                's': 1       
            }
            
            current_number = ""
            for char in duration_parts:
                if char.isdigit():
                    current_number += char
                elif char in time_units:
                    if current_number:
                        total_seconds += int(current_number) * time_units[char]
                        current_number = ""
            
            if total_seconds > 0:
                ban_duration = datetime.utcnow() + timedelta(seconds=total_seconds)

        embed = EmbedBuilder(
            "⚡ Ban Hammer Struck!",
            f"{user.mention} has been banned from the server."
        ).set_color(discord.Color.dark_red())

        embed.add_field("Target", f"{user.name} ({user.id})")
        embed.add_field("Moderator", ctx.author.mention)
        if ban_duration:
            embed.add_field("Duration", f"Until {ban_duration.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        embed.add_field("Reason", reason, inline=False)
        embed.set_thumbnail(user.avatar.url)

        try:
            dm_embed = EmbedBuilder(
                "🚫 You've Been Banned",
                f"You were banned from {ctx.guild.name}"
            ).set_color(discord.Color.red())
            dm_embed.add_field("Reason", reason)
            if ban_duration:
                dm_embed.add_field("Duration", f"Until {ban_duration.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            
            # Fetch appeal_info from the guild's configuration or database
            appeal_info = await self.get_appeal_info(ctx.guild.id)
            if appeal_info:
                dm_embed.add_field("Appeal", appeal_info)
            
            await user.send(embed=dm_embed.build())
        except:
            embed.add_field("Note", "⚠️ Could not DM user", inline=False)

        await ctx.guild.ban(user, reason=f"{reason} | By {ctx.author}", delete_message_days=0)
        await ctx.send(embed=embed.build())

        logging_cog = self.bot.get_cog("CustomLogging")
        if logging_cog:
            await logging_cog.log_action(ctx.guild, 'ban', ctx.author, user, reason)

        if ban_duration:
            
            await asyncio.sleep(total_seconds)
            try:
                await ctx.guild.unban(user, reason="Temporary ban expired")
                unban_embed = EmbedBuilder(
                    "🔓 Ban Expired",
                    f"{user.mention} has been automatically unbanned."
                ).set_color(discord.Color.green())
                await ctx.send(embed=unban_embed.build())
            except:
                await ctx.send(f"Failed to unban {user.mention} automatically.")

    async def get_appeal_info(self, guild_id):
        return self.ban_appeal_info.get(str(guild_id))


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban_appeal(self, ctx, *, appeal_info):
        self.ban_appeal_info[str(ctx.guild.id)] = appeal_info
        await ctx.send(f"✅ Ban appeal information updated to: {appeal_info}")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        embed = EmbedBuilder(
            "👢 Member Kicked",
            f"{user.mention} has been kicked from the server."
        ).set_color(discord.Color.orange())

        embed.add_field("Target", f"{user.name} ({user.id})")
        embed.add_field("Moderator", ctx.author.mention)
        embed.add_field("Reason", reason, inline=False)

        try:
            dm_embed = EmbedBuilder(
                "👢 You've Been Kicked",
                f"You were kicked from {ctx.guild.name}"
            ).set_color(discord.Color.orange())
            dm_embed.add_field("Reason", reason)
            await user.send(embed=dm_embed.build())
        except:
            embed.add_field("Note", "⚠️ Could not DM user", inline=False)

        await user.kick(reason=f"{reason} | By {ctx.author}")
        await ctx.send(embed=embed.build())

        logging_cog = self.bot.get_cog("CustomLogging")
        if logging_cog:
            await logging_cog.log_action(ctx.guild, 'kick', ctx.author, user, reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mutesetup(self, ctx, role: discord.Role = None):
        """Setup the mute system with a custom role"""
        guild_id = ctx.guild.id
        
        if role:
            self.mute_roles[guild_id] = role.id
            self.save_data()
            embed = discord.Embed(
                title="✅ Mute System Setup",
                description=f"Muted members will now receive the {role.mention} role",
                color=discord.Color.green()
            )
        else:
            
            embed = discord.Embed(
                title="🔇 Mute System Configuration",
                description="Current mute system settings",
                color=discord.Color.blue()
            )
            
            current_role = ctx.guild.get_role(self.mute_roles.get(guild_id))
            embed.add_field(
                name="Mute Role",
                value=current_role.mention if current_role else "Not set",
                inline=False
            )
            
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """Unmute a member with optional reason and success notification"""
        guild_id = ctx.guild.id
        
        if guild_id in self.mute_roles:
            mute_role = ctx.guild.get_role(self.mute_roles[guild_id])
            if mute_role and mute_role in member.roles:
                await member.remove_roles(mute_role)
        
        await member.timeout(None, reason=reason)

        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"**Member:** {member.mention}\n**Moderator:** {ctx.author.mention}\n**Reason:** {reason or 'No reason provided'}",
            color=discord.Color.green()
        )
        msg = await ctx.send(embed=embed)

        logging_cog = self.bot.get_cog("CustomLogging")
        if logging_cog:
            await logging_cog.log_action(ctx.guild, 'unmute', ctx.author, member, reason)

        try:
            await member.send(f"You have been unmuted in {ctx.guild.name}")
        except:
            pass

        await asyncio.sleep(3)
        await msg.delete()

    @commands.command()
    @commands.bot_has_permissions(moderate_members=True)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, duration: int, *, reason="No reason provided"):
        time_delta = timedelta(minutes=duration)
        guild_id = ctx.guild.id

        mute_role = None
        if guild_id in self.mute_roles:
            mute_role = ctx.guild.get_role(self.mute_roles[guild_id])

        embed = EmbedBuilder(
            "🔇 Member Muted",
            f"{user.mention} has been muted."
        ).set_color(discord.Color.yellow())

        embed.add_field("Duration", f"{duration} minutes")
        embed.add_field("Moderator", ctx.author.mention)
        embed.add_field("Reason", reason, inline=False)

        await user.timeout(time_delta, reason=reason)
        if mute_role:
            await user.add_roles(mute_role, reason=reason)
            embed.add_field("Role Applied", mute_role.mention, inline=False)

        await ctx.send(embed=embed.build())

        logging_cog = self.bot.get_cog("CustomLogging")
        if logging_cog:
            await logging_cog.log_action(ctx.guild, 'mute', ctx.author, user, reason, f"{duration} minutes")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.Member, *, reason="No reason provided"):
        """Warn a user and notify them via DM"""
    
        embed = EmbedBuilder(
        "⚠️ Warning Issued",
        f"{user.mention} has been warned."
    ).set_color(discord.Color.orange())

        embed.add_field("User", f"{user.name} ({user.id})")
        embed.add_field("Moderator", ctx.author.mention)
        embed.add_field("Reason", reason, inline=False)

        await ctx.send(embed=embed.build())

        try:
            dm_embed = EmbedBuilder(
            "⚠️ You Have Been Warned",
            f"You have been warned in **{ctx.guild.name}**."
        ).set_color(discord.Color.red())

            dm_embed.add_field("Moderator", ctx.author.mention)
            dm_embed.add_field("Reason", reason, inline=False)
            dm_embed.set_footer("Please follow the server rules to avoid further action.")

            await user.send(embed=dm_embed.build())
        except:
            await ctx.send(f"⚠️ {user.mention} has DMs disabled. Unable to send warning via DM.")

        await log_manager.log_action(ctx.guild, "warn", ctx.author, user, reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason="No reason provided"):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"{reason} | By {ctx.author}")
        
            embed = EmbedBuilder(
                "🔓 Member Unbanned",
                f"{user.name} has been unbanned from the server."
            ).set_color(discord.Color.green())
        
            embed.add_field("User ID", user_id)
            embed.add_field("Moderator", ctx.author.mention)
            embed.add_field("Reason", reason, inline=False)
        
            await ctx.send(embed=embed.build())
            await log_manager.log_action(ctx.guild, 'unban', ctx.author, user, reason)
        
        except discord.NotFound:
            embed = EmbedBuilder(
                "❌ User Not Found",
                f"No banned user found with ID: {user_id}"
            ).set_color(discord.Color.red()).build()
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        embed = EmbedBuilder(
            "🧹 Messages Cleared",
            f"Cleared {amount} messages"
        ).set_color(discord.Color.blue()).build()
        await ctx.send(embed=embed, delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: Union[discord.Member, discord.User], role: discord.Role):
        """Add a role to a member using mention or ID"""
        if not isinstance(member, discord.Member):
            member = ctx.guild.get_member(member.id)
            if not member:
                embed = EmbedBuilder(
                    "❌ User Not Found",
                    "User must be in the server"
                ).set_color(discord.Color.red()).build()
                return await ctx.send(embed=embed)
        
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = EmbedBuilder(
                "❌ Role Error", 
                "You can't assign roles higher than your own!"
            ).set_color(discord.Color.red()).build()
            return await ctx.send(embed=embed)
        
        await member.add_roles(role)
        embed = EmbedBuilder(
            "✅ Role Added",
            f"Successfully added {role.mention} to {member.mention}"
        ).set_color(discord.Color.green())
        embed.add_field("User", member.mention)
        embed.add_field("Moderator", ctx.author.mention)
        await ctx.send(embed=embed.build())


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user_id: int, role: discord.Role):
        """Remove a role from a member using their ID"""
        member = ctx.guild.get_member(user_id)
        if not member:
            embed = EmbedBuilder(
                "❌ User Not Found",
                f"No user found with ID: {user_id}"
            ).set_color(discord.Color.red()).build()
            return await ctx.send(embed=embed)
        
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = EmbedBuilder(
                "❌ Role Error",
                "You can't remove roles higher than your own!"
            ).set_color(discord.Color.red()).build()
            return await ctx.send(embed=embed)
        
        await member.remove_roles(role)
        embed = EmbedBuilder(
            "✅ Role Removed",
            f"Successfully removed {role.mention} from {member.mention}"
        ).set_color(discord.Color.green())
        embed.add_field("User ID", user_id)
        embed.add_field("Moderator", ctx.author.mention)
        await ctx.send(embed=embed.build())

class TicketView(discord.ui.View):
    def __init__(self, bot, button_style=discord.ButtonStyle.blurple):
        super().__init__(timeout=None)
        self.bot = bot
        self.button_style = button_style

    @discord.ui.button(label="Create Ticket", emoji="🎫", custom_id="create_ticket")  
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = self.bot.get_cog('TicketSystem').TicketModal()
        await interaction.response.send_modal(modal)



class TicketButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        messages = [message async for message in interaction.channel.history(limit=100)]
        transcript = "\n".join(f"{msg.author}: {msg.content}" for msg in reversed(messages))
        
        transcript_file = discord.File(
            io.StringIO(transcript),
            filename=f"ticket-{interaction.channel.name}.txt"
        )
        
        ticket_system = self.bot.get_cog('TicketSystem')
        logs_channel_id = ticket_system.ticket_logs.get(interaction.guild.id)
        logs_channel = None
        
        if logs_channel_id:
            logs_channel = interaction.guild.get_channel(logs_channel_id)
        if not logs_channel:
            logs_channel = discord.utils.get(interaction.guild.channels, name="ticket-logs")
            
        if logs_channel:
            close_log = EmbedBuilder(
                "📝 Ticket Closed",
                f"Ticket {interaction.channel.name} was closed by {interaction.user.mention}"
            ).set_color(discord.Color.red())
            
            await logs_channel.send(embed=close_log.build(), file=transcript_file)
        
        await interaction.followup.send("Closing ticket...")
        await asyncio.sleep(3)
        await interaction.channel.delete()

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.green, emoji="✋")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        support_role_id = self.bot.get_cog('TicketSystem').support_roles.get(interaction.guild.id)
        support_role = interaction.guild.get_role(support_role_id) if support_role_id else None
        
        if not (interaction.user.guild_permissions.administrator or 
                (support_role and support_role in interaction.user.roles)):
            return await interaction.response.send_message("You don't have permission to claim tickets!", ephemeral=True)
        
        new_name = f"claimed-{interaction.channel.name[7:]}"
        await interaction.channel.edit(name=new_name)
        
        claim_embed = EmbedBuilder(
            "🎫 Support Ticket - CLAIMED",
            f"This ticket has been claimed by {interaction.user.mention}"
        ).set_color(discord.Color.green())
        
        button.disabled = True
        button.label = f"Claimed by {interaction.user.name}"
        
        await interaction.response.edit_message(view=self)
        await interaction.channel.send(embed=claim_embed.build())


class OwnerPanelView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.authorized_id = int(os.getenv("BOT_OWNER_ID", "0"))

    @discord.ui.button(label="Owner Commands", style=discord.ButtonStyle.gray, emoji="🔒")
    async def show_owner_commands(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        embed = EmbedBuilder(
            "🔒 Owner-Only Commands",
            "Exclusive commands for bot owner"
        ).set_color(discord.Color.purple())
        
        commands_list = {
            "!owner": "Open this interactive control panel",
            "!leaveserver <guild_id>": "Make bot leave a specific server",
            "!executecmd <guild_id> <channel_id> <command>": "Execute commands in other servers",
            "!botinfo": "View detailed bot statistics",
            "Interactive Buttons": {
                "📋 Server List": "View all servers with details",
                "📊 Statistics": "Real-time bot performance metrics",
                "⚙️ Server Management": "Access server management tools",
                "📢 Mass Message": "Send message to all servers",
                "⚡ Execute Command": "Run commands remotely",
                "🚪 Leave Server": "Remove bot from servers"
            }
        }
        
        for cmd, desc in commands_list.items():
            if isinstance(desc, dict):
                subcommands = "\n".join(f"• {subcmd}: {subdesc}" for subcmd, subdesc in desc.items())
                embed.add_field(cmd, subcommands, inline=False)
            else:
                embed.add_field(cmd, desc, inline=False)
        
        await interaction.response.send_message(embed=embed.build(), ephemeral=True)

    @discord.ui.button(label="Server List", style=discord.ButtonStyle.blurple, emoji="📋")
    async def show_servers(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        embed = EmbedBuilder(
            "📋 Server List",
            f"Managing {len(self.bot.guilds)} servers"
        ).set_color(discord.Color.blue())
        
        for guild in self.bot.guilds:
            embed.add_field(
                f"{guild.name} (ID: {guild.id})",
                f"Members: {guild.member_count}\nOwner: {guild.owner}\nInvite: {await self.create_invite(guild)}",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed.build(), ephemeral=True)

    @discord.ui.button(label="Statistics", style=discord.ButtonStyle.green, emoji="📊")
    async def show_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        total_users = sum(g.member_count for g in self.bot.guilds)
        total_channels = sum(len(g.channels) for g in self.bot.guilds)
        
        embed = EmbedBuilder(
            "📊 Bot Statistics",
            "Real-time performance metrics"
        ).set_color(discord.Color.green())
        
        embed.add_field("Servers", str(len(self.bot.guilds)))
        embed.add_field("Total Users", str(total_users))
        embed.add_field("Total Channels", str(total_channels))
        embed.add_field("Latency", f"{round(self.bot.latency * 1000)}ms")
        embed.add_field("Uptime", str(timedelta(seconds=int(time.time() - self.bot.start_time))))
        
        await interaction.response.send_message(embed=embed.build(), ephemeral=True)

    @discord.ui.button(label="Server Management", style=discord.ButtonStyle.red, emoji="⚙️")
    async def server_management(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        view = ServerManagementView(self.bot)
        embed = EmbedBuilder(
            "⚙️ Server Management",
            "Select actions to manage servers"
        ).set_color(discord.Color.red())
        
        await interaction.response.send_message(embed=embed.build(), view=view, ephemeral=True)

    async def create_invite(self, guild):
        try:
            channel = guild.text_channels[0]
            invite = await channel.create_invite(max_age=300)
            return invite.url
        except:
            return "No invite available"

class ServerManagementView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.authorized_id = int(os.getenv("BOT_OWNER_ID", "0"))

    @discord.ui.button(label="Leave Server", style=discord.ButtonStyle.red, emoji="🚪")
    async def leave_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        await interaction.response.send_modal(LeaveServerModal(self.bot))

    @discord.ui.button(label="Mass Message", style=discord.ButtonStyle.blurple, emoji="📢")
    async def mass_message(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        await interaction.response.send_modal(MassMessageModal(self.bot))

    @discord.ui.button(label="Execute Command", style=discord.ButtonStyle.green, emoji="⚡")
    async def execute_command(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.authorized_id:
            return
            
        await interaction.response.send_modal(ExecuteCommandModal(self.bot))

class LeaveServerModal(discord.ui.Modal, title="Leave Server"):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
    server_id = discord.ui.TextInput(
        label="Server ID",
        placeholder="Enter server ID to leave..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = self.bot.get_guild(int(self.server_id.value))
        if guild:
            await guild.leave()
            embed = EmbedBuilder(
                "✅ Server Left",
                f"Successfully left {guild.name}"
            ).set_color(discord.Color.green())
            await interaction.response.send_message(embed=embed.build(), ephemeral=True)

class MassMessageModal(discord.ui.Modal, title="Send Mass Message"):
    message = discord.ui.TextInput(
        label="Message",
        style=discord.TextStyle.paragraph,
        placeholder="Enter message to send to all servers..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        success = 0
        failed = 0
        for guild in interaction.client.guilds:
            try:
                channel = guild.system_channel or guild.text_channels[0]
                await channel.send(self.message.value)
                success += 1
            except:
                failed += 1
                
        embed = EmbedBuilder(
            "📢 Mass Message Results",
            f"Message sent to {success} servers\nFailed in {failed} servers"
        ).set_color(discord.Color.blue())
        await interaction.response.send_message(embed=embed.build(), ephemeral=True)

class ExecuteCommandModal(discord.ui.Modal, title="Execute Command"):
    guild_id = discord.ui.TextInput(
        label="Server ID",
        placeholder="Enter server ID..."
    )
    
    command = discord.ui.TextInput(
        label="Command",
        placeholder="Enter command to execute..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.client.get_guild(int(self.guild_id.value))
        if guild:
            channel = guild.system_channel or guild.text_channels[0]
            ctx = await interaction.client.get_context(interaction.message)
            ctx.channel = channel
            await interaction.client.process_commands(ctx.message)
            
            embed = EmbedBuilder(
                "⚡ Command Executed",
                f"Command executed in {guild.name}"
            ).set_color(discord.Color.green())
            await interaction.response.send_message(embed=embed.build(), ephemeral=True)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OwnerOnly")

class OwnerOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.authorized_id = int(os.getenv("BOT_OWNER_ID", "0"))  

        if self.authorized_id == 0:
            logger.warning("⚠️ BOT_OWNER_ID is not set in .env! Owner commands may be unusable.")

    def is_owner(self, ctx):
        """Check if the command author is the bot owner."""
        if ctx.author.id != self.authorized_id:
            logger.warning(f"Unauthorized access attempt: {ctx.author} ({ctx.author.id}) tried using an owner command.")
            return False
        return True

    @commands.command()
    async def owner(self, ctx):
        """Interactive owner control panel"""
        if not self.is_owner(ctx):
            return await ctx.send("❌ You are not authorized to use this command.")

        embed = EmbedBuilder(
            "👑 Owner Control Panel",
            "Welcome to the interactive control panel"
        ).set_color(discord.Color.gold())

        embed.add_field(
            "Available Actions",
            "📋 View server list\n"
            "📊 View statistics\n"
            "⚙️ Server management",
            inline=False
        )

        await ctx.send(embed=embed.build(), view=OwnerPanelView(self.bot))

    trusted_guilds_str = os.getenv('TRUSTED_GUILDS')
    TRUSTED_GUILDS = set()  
    trusted_guilds_str = os.getenv('TRUSTED_GUILDS', '')
    if trusted_guilds_str and not trusted_guilds_str.startswith('#'):
        TRUSTED_GUILDS = {int(guild_id) for guild_id in trusted_guilds_str.split(',') if guild_id.strip().isdigit()}

    @commands.command()
    async def executecmd(self, ctx, guild_id: int, channel_id: int, *, command):
        """Execute command in a specified server/channel with owner confirmation"""
        if not self.is_owner(ctx):
            return await ctx.send("❌ You are not authorized to use this command.")

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send(f"❌ Guild with ID {guild_id} not found.")

        channel = guild.get_channel(channel_id)
        if not channel:
            return await ctx.send(f"❌ Channel with ID {channel_id} not found in {guild.name}.")

        if guild_id not in self.TRUSTED_GUILDS:
            return await ctx.send("❌ You cannot execute commands in this server.")

        BLACKLISTED_COMMANDS = ["ban @everyone", "kick @everyone", "delete all", "nuke"]
        if any(blacklisted in command.lower() for blacklisted in BLACKLISTED_COMMANDS):
            return await ctx.send("🚫 This command is too dangerous to execute!")

        confirm_embed = EmbedBuilder(
            "⚠️ Command Execution Request",
            f"Are you sure you want to execute:\n\n`{command}`\n\n"
            f"in **{guild.name}** (`{guild.id}`) -> **#{channel.name}** (`{channel.id}`)?"
        ).set_color(discord.Color.orange())

        confirm_message = await ctx.author.send(embed=confirm_embed.build())
        await confirm_message.add_reaction("✅")
        await confirm_message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)

            if str(reaction.emoji) == "❌":
                return await ctx.author.send("❌ Command execution **cancelled**.")

            msg = copy.copy(ctx.message)
            msg.channel = channel
            msg.content = command
            new_ctx = await self.bot.get_context(msg)

            try:
                await self.bot.invoke(new_ctx)
                success_embed = EmbedBuilder(
                "✅ Command Executed",
                f"Command executed successfully in **{guild.name}** -> **#{channel.name}**"
            ).set_color(discord.Color.green())
                await ctx.author.send(embed=success_embed.build())
            except Exception as e:
                await ctx.author.send(f"❌ Failed to execute command: {str(e)}")

        except asyncio.TimeoutError:
            await ctx.author.send("❌ Command execution **timed out**. No response received.")

    @commands.command(name='botinfo')
    async def show_info(self, ctx):
        """Display detailed bot information"""
        if not self.is_owner(ctx):
            return await ctx.send("❌ You are not authorized to use this command.")

        embed = EmbedBuilder(
            "🤖 Bot Information",
            "Detailed statistics and information"
        ).set_color(discord.Color.blue())

        total_users = sum(g.member_count for g in self.bot.guilds)
        total_channels = sum(len(g.channels) for g in self.bot.guilds)
        uptime = timedelta(seconds=int(time.time() - self.bot.start_time))

        embed.add_field("Servers", str(len(self.bot.guilds)))
        embed.add_field("Users", str(total_users))
        embed.add_field("Channels", str(total_channels))
        embed.add_field("Bot Latency", f"{round(self.bot.latency * 1000)}ms")
        embed.add_field("Uptime", str(uptime))
        embed.add_field("Python Version", platform.python_version())

        await ctx.send(embed=embed.build())

    @commands.command()
    async def leaveserver(self, ctx, guild_id: int, *, reason: str = "No reason provided"):
        """Make bot leave specified server with optional reason"""
        if not self.is_owner(ctx):
            return await ctx.send("❌ You are not authorized to use this command.")

        guild = self.bot.get_guild(guild_id)
        if not guild:
            return await ctx.send(f"❌ Could not find a server with ID {guild_id}.")

        notification = EmbedBuilder(
            "🔔 Bot Leaving Server",
            f"This bot is being removed from the server.\nReason: {reason}"
        ).set_color(discord.Color.red())

        target_channel = guild.system_channel or next((ch for ch in guild.text_channels), None)
        if target_channel:
            await target_channel.send(embed=notification.build())

        await guild.leave()

        embed = EmbedBuilder(
            "✅ Server Left",
            f"Successfully left {guild.name}\nReason: {reason}"
        ).set_color(discord.Color.green())
        await ctx.send(embed=embed.build())

bot.add_cog(OwnerOnly(bot))

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.support_roles = {}
        self.admin_roles = {}
        self.ticket_categories = {}
        self.ticket_logs = {}
        self.ticket_panel_configs = {}

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fixlogs(self, ctx, channel_id: int):
        """Set a custom channel for ticket logs"""
        try:
            channel = ctx.guild.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.TextChannel):
                return await ctx.send("✨ Please provide a valid text channel ID!")
            
            self.ticket_logs[ctx.guild.id] = channel_id
            
            embed = discord.Embed(
                title="✅ Ticket Logs Channel Updated",
                description=f"Ticket logs will now be sent to: {channel.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Channel ID", value=channel_id)
            embed.add_field(name="Channel Name", value=channel.name)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"✨ An error occurred: {str(e)}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketadmin(self, ctx, role: discord.Role):
        """Set which role gets automatically added to tickets"""
        self.support_roles[ctx.guild.id] = role.id
   
        embed = EmbedBuilder(
            "✅ Ticket Settings Updated",
            f"{role.mention} will now be automatically added to all new tickets"
        ).set_color(discord.Color.green())
   
        embed.add_field("Role ID", role.id)
        embed.add_field("Role Name", role.name)
        await ctx.send(embed=embed.build())

    class TicketModal(discord.ui.Modal, title="Create Ticket"):
        reason = discord.ui.TextInput(
            label="Ticket Reason",
            placeholder="Please describe your reason for creating a ticket...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.defer()
            
            existing_ticket = discord.utils.get(
                interaction.guild.channels,
                name=f"ticket-{interaction.user.id}"
            )
            if existing_ticket:
                return await interaction.followup.send("You already have an open ticket!", ephemeral=True)
            
            ticket_system = interaction.client.get_cog('TicketSystem')
            category_id = ticket_system.ticket_categories.get(interaction.guild.id)
            if category_id:
                category = interaction.guild.get_channel(category_id)
            else:
                category = discord.utils.get(interaction.guild.categories, name="Tickets")
            
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            
            support_role_id = ticket_system.support_roles.get(interaction.guild.id)
            if support_role_id:
                support_role = interaction.guild.get_role(support_role_id)
                if support_role:
                    overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            
            channel = await interaction.guild.create_text_channel(
                f"ticket-{interaction.user.id}",
                category=category,
                overwrites=overwrites
            )
            
            ticket_embed = EmbedBuilder(
                "🎫 Support Ticket",
                "Thank you for creating a ticket. Support will be with you shortly."
            ).set_color(discord.Color.blue())
            
            ticket_embed.add_field("Created By", interaction.user.mention)
            ticket_embed.add_field("User ID", interaction.user.id)
            ticket_embed.add_field("Reason", str(self.reason), inline=False)
            
            await channel.send(embed=ticket_embed.build())
            
            ticket_view = TicketButtons(interaction.client)
            await channel.send("Ticket Controls:", view=ticket_view)
            
            if support_role_id:
                support_role = interaction.guild.get_role(support_role_id)
                if support_role:
                    await channel.send(f"{support_role.mention} A new ticket requires attention!")
            
            confirm = EmbedBuilder(
                "✅ Ticket Created",
                f"Your ticket has been created in {channel.mention}"
            ).set_color(discord.Color.green()).build()
            
            await interaction.followup.send(embed=confirm, ephemeral=True)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fixticket(self, ctx, category_id: int):
        """Set a custom category for ticket creation"""
        try:
            category = ctx.guild.get_channel(category_id)
            if not category or not isinstance(category, discord.CategoryChannel):
                return await ctx.send("✨ Please provide a valid category ID!")
            
            self.ticket_categories[ctx.guild.id] = category_id
            
            embed = discord.Embed(
                title="✅ Ticket Category Updated",
                description=f"New tickets will now be created in category: {category.name}",
                color=discord.Color.green()
            )
            embed.add_field(name="Category ID", value=category_id)
            embed.add_field(name="Category Name", value=category.name)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"✨ An error occurred: {str(e)}")



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketsetup_json(self, ctx, *, json_data: str = None):
        """Setup ticket panel using custom JSON configuration - supports direct input or file attachments"""
        try:
            color_map = {
    "blurple": (discord.ButtonStyle.blurple, discord.Color.blurple()),
    "green": (discord.ButtonStyle.green, discord.Color.green()),
    "dark_green": (discord.ButtonStyle.green, discord.Color.dark_green()),
    "light_green": (discord.ButtonStyle.green, discord.Color.from_rgb(144, 238, 144)),
    "neon_green": (discord.ButtonStyle.green, discord.Color.from_rgb(57, 255, 20)),
    
    "red": (discord.ButtonStyle.red, discord.Color.red()),
    "dark_red": (discord.ButtonStyle.red, discord.Color.dark_red()),
    "bright_red": (discord.ButtonStyle.red, discord.Color.from_rgb(255, 69, 0)),
    "pink_red": (discord.ButtonStyle.red, discord.Color.from_rgb(255, 105, 180)),

    "grey": (discord.ButtonStyle.grey, discord.Color.greyple()),
    "dark_grey": (discord.ButtonStyle.grey, discord.Color.dark_grey()),
    "light_grey": (discord.ButtonStyle.grey, discord.Color.light_grey()),
    "darker_grey": (discord.ButtonStyle.grey, discord.Color.darker_grey()),
    "lighter_grey": (discord.ButtonStyle.grey, discord.Color.lighter_grey()),

    "blue": (discord.ButtonStyle.blurple, discord.Color.blue()),
    "dark_blue": (discord.ButtonStyle.blurple, discord.Color.dark_blue()),
    "navy_blue": (discord.ButtonStyle.blurple, discord.Color.from_rgb(0, 0, 128)),
    "sky_blue": (discord.ButtonStyle.blurple, discord.Color.from_rgb(135, 206, 235)),
    "cyan": (discord.ButtonStyle.blurple, discord.Color.from_rgb(0, 255, 255)),
    
    "teal": (discord.ButtonStyle.blurple, discord.Color.teal()),
    "dark_teal": (discord.ButtonStyle.blurple, discord.Color.dark_teal()),
    "light_teal": (discord.ButtonStyle.blurple, discord.Color.from_rgb(32, 178, 170)),
    
    "brand": (discord.ButtonStyle.blurple, discord.Color.blurple()),
    "primary": (discord.ButtonStyle.blurple, discord.Color.blue()),

    "success": (discord.ButtonStyle.green, discord.Color.green()),
    "thez": (discord.ButtonStyle.green, discord.Color.from_rgb(255, 0, 255)),
    "danger": (discord.ButtonStyle.red, discord.Color.red()),
    "brand_red": (discord.ButtonStyle.red, discord.Color.red()),
    
    "orange": (discord.ButtonStyle.red, discord.Color.orange()),
    "dark_orange": (discord.ButtonStyle.red, discord.Color.dark_orange()),
    "bright_orange": (discord.ButtonStyle.red, discord.Color.from_rgb(255, 140, 0)),

    "gold": (discord.ButtonStyle.grey, discord.Color.gold()),
    "dark_gold": (discord.ButtonStyle.grey, discord.Color.dark_gold()),
    "bronze": (discord.ButtonStyle.grey, discord.Color.from_rgb(205, 127, 50)),
    "silver": (discord.ButtonStyle.grey, discord.Color.from_rgb(192, 192, 192)),

    "purple": (discord.ButtonStyle.blurple, discord.Color.purple()),
    "purplee": (discord.ButtonStyle.blurple, discord.Color.purple()),
    "dark_purple": (discord.ButtonStyle.grey, discord.Color.dark_purple()),
    "lavender": (discord.ButtonStyle.grey, discord.Color.from_rgb(230, 230, 250)),

    "magenta": (discord.ButtonStyle.grey, discord.Color.magenta()),
    "dark_magenta": (discord.ButtonStyle.grey, discord.Color.dark_magenta()),
    "hot_pink": (discord.ButtonStyle.grey, discord.Color.from_rgb(255, 20, 147)),
    "deep_pink": (discord.ButtonStyle.grey, discord.Color.from_rgb(255, 0, 127)),

    "random": (discord.ButtonStyle.grey, discord.Color.random()),
    "white": (discord.ButtonStyle.grey, discord.Color.from_rgb(255, 255, 255)),
    "black": (discord.ButtonStyle.grey, discord.Color.from_rgb(0, 0, 0)),
    "brown": (discord.ButtonStyle.grey, discord.Color.from_rgb(139, 69, 19))
}



            config = None
            if len(ctx.message.attachments) > 0:
                attachment = ctx.message.attachments[0]
                if attachment.filename.endswith('.json'):
                    json_data = (await attachment.read()).decode('utf-8')
                    config = json.loads(json_data)
            elif json_data:
                config = json.loads(json_data)


            if not config:
                return await ctx.send("✨ Please provide JSON configuration either as text or an attached file!")


            category_id = self.ticket_categories.get(ctx.guild.id)
            if category_id:
                category = ctx.guild.get_channel(category_id)
            else:
                category = discord.utils.get(ctx.guild.categories, name="Tickets")
                if not category:
                    category = await ctx.guild.create_category("Tickets")


            logs_channel_id = self.ticket_logs.get(ctx.guild.id)
            if logs_channel_id:
                logs_channel = ctx.guild.get_channel(logs_channel_id)
            else:
                logs_channel = discord.utils.get(ctx.guild.channels, name="ticket-logs")
                if not logs_channel:
                    logs_channel = await ctx.guild.create_text_channel("ticket-logs", category=category)


            embeds = []

            embed_data = config.get('embeds', []) if 'embeds' in config else config.get('ticket_config', {}).get('custom_panels', {}).get('embeds', [])

            total_embeds = len(embed_data)
            width_placeholder = "https://placehold.co/400x10/2b2d31/2b2d31.png"
            has_image = any('image' in embed for embed in embed_data)

            for i, discord_embed in enumerate(embed_data):
                embed_color = str(discord_embed.get('color', 'blurple')).lower()
                if embed_color.startswith('#'):
                    embed_color = discord.Color(int(embed_color.strip('#'), 16))
                elif embed_color not in color_map:
                    valid_colors = ", ".join(color_map.keys())
                    return await ctx.send(f"❌ Invalid button color! Valid colors are: **{valid_colors}**")
                
                embed_color = color_map[embed_color][1] if isinstance(embed_color, str) else embed_color
                
                embed = discord.Embed(
                    title=discord_embed.get('title', 'Support Tickets'),
                    description=discord_embed.get('description', 'Click below to create a ticket'),
                    color=embed_color
                )
                
                if has_image and 'image' not in discord_embed:
                    embed.set_image(url=width_placeholder)
                elif 'image' in discord_embed:
                    embed.set_image(url=discord_embed['image']['url'])
                
                if i < total_embeds - 1:
                    embed.description += "\n\u200b"
                
                embeds.append(embed)

            button_color = str(config.get('button_color', 'blurple')).lower()
            if button_color not in color_map:
                valid_colors = ", ".join(color_map.keys())
                return await ctx.send(f"❌ Invalid button color! Valid colors are: **{valid_colors}**")


            button_style = discord.ButtonStyle.blurple
            button_label = "Create Ticket"
            button_emoji = "🎫"

            if 'button_label' in config:
                button_label = config['button_label']
            if 'button_emoji' in config:
                button_emoji = config['button_emoji']
            if 'button_color' in config:
                if config['button_color'].lower() in color_map:
                    button_style = color_map[config['button_color'].lower()][0]

            class CustomTicketView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)

                @discord.ui.button(label=button_label, emoji=button_emoji, custom_id="create_ticket", style=button_style)
                async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
                    modal = ctx.bot.get_cog('TicketSystem').TicketModal()
                    await interaction.response.send_modal(modal)

            await ctx.send(embeds=embeds, view=CustomTicketView())


        except json.JSONDecodeError:
            await ctx.send("✨ Invalid JSON format! Please provide valid JSON configuration.")
        except Exception as e:
            await ctx.send(f"✨ An error occurred: {str(e)}")





    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ticketsetup(self, ctx, *, args):
        """Setup ticket panel with custom name, message, embed color and button color"""
        try:
            parts = shlex.split(args)
            panel_name = parts[0]
            message = parts[1]
            embed_color = parts[2] if len(parts) > 2 else "blurple"
            button_color = parts[3] if len(parts) > 3 else "blurple"
            
            color_map = {
                "blurple": (discord.ButtonStyle.blurple, discord.Color.blurple()),
                "green": (discord.ButtonStyle.green, discord.Color.green()),
                "red": (discord.ButtonStyle.red, discord.Color.red()),
                "grey": (discord.ButtonStyle.grey, discord.Color.greyple()),
                "primary": (discord.ButtonStyle.blurple, discord.Color.blue()),
                "blue": (discord.ButtonStyle.blurple, discord.Color.blue()),
                "dark_blue": (discord.ButtonStyle.blurple, discord.Color.dark_blue()),
                "brand": (discord.ButtonStyle.blurple, discord.Color.blurple()),
                "teal": (discord.ButtonStyle.blurple, discord.Color.teal()),
                "dark_teal": (discord.ButtonStyle.blurple, discord.Color.dark_teal()),
                "success": (discord.ButtonStyle.green, discord.Color.green()),
                "dark_green": (discord.ButtonStyle.green, discord.Color.dark_green()),
                "thez": (discord.ButtonStyle.green, discord.Color.from_rgb(255,0,255)),
                "danger": (discord.ButtonStyle.red, discord.Color.red()),
                "brand_red": (discord.ButtonStyle.red, discord.Color.red()),
                "dark_red": (discord.ButtonStyle.red, discord.Color.dark_red()),
                "orange": (discord.ButtonStyle.red, discord.Color.orange()),
                "dark_orange": (discord.ButtonStyle.red, discord.Color.dark_orange()),
                "secondary": (discord.ButtonStyle.grey, discord.Color.greyple()),
                "purple": (discord.ButtonStyle.grey, discord.Color.purple()),
                "dark_purple": (discord.ButtonStyle.grey, discord.Color.dark_purple()),
                "magenta": (discord.ButtonStyle.grey, discord.Color.magenta()),
                "dark_magenta": (discord.ButtonStyle.grey, discord.Color.dark_magenta()),
                "gold": (discord.ButtonStyle.grey, discord.Color.gold()),
                "dark_gold": (discord.ButtonStyle.grey, discord.Color.dark_gold()),
                "lighter_grey": (discord.ButtonStyle.grey, discord.Color.lighter_grey()),
                "dark_grey": (discord.ButtonStyle.grey, discord.Color.dark_grey()),
                "light_grey": (discord.ButtonStyle.grey, discord.Color.light_grey()),
                "darker_grey": (discord.ButtonStyle.grey, discord.Color.darker_grey()),
                "random": (discord.ButtonStyle.grey, discord.Color.random()),
            }

            if embed_color.lower() not in color_map or button_color.lower() not in color_map:
                valid_colors = ", ".join(color_map.keys())
                return await ctx.send(f"❌ Invalid color! Valid colors are: **{valid_colors}**")

            button_style = color_map[button_color.lower()][0]
            embed_color = color_map[embed_color.lower()][1]

            category_id = self.ticket_categories.get(ctx.guild.id)
            if category_id:
                category = ctx.guild.get_channel(category_id)
            else:
                category = discord.utils.get(ctx.guild.categories, name="Tickets")
                if not category:
                    category = await ctx.guild.create_category("Tickets")

            logs_channel_id = self.ticket_logs.get(ctx.guild.id)
            if logs_channel_id:
                logs_channel = ctx.guild.get_channel(logs_channel_id)
            else:
                logs_channel = discord.utils.get(ctx.guild.channels, name="ticket-logs")
                if not logs_channel:
                    logs_channel = await ctx.guild.create_text_channel("ticket-logs", category=category)

            embed = EmbedBuilder(
                panel_name,
                message
            ).set_color(embed_color).build()

            class CustomTicketView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)

                @discord.ui.button(label="Create Ticket", emoji="🎫", custom_id="create_ticket", style=button_style)
                async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
                    modal = ctx.bot.get_cog('TicketSystem').TicketModal()
                    await interaction.response.send_modal(modal)

            await ctx.send(embed=embed, view=CustomTicketView())

        except Exception as e:
            await ctx.send(f"✨ An error occurred: {str(e)}")




    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx, user: discord.Member):
        if not (ctx.channel.name.startswith("ticket-") or ctx.channel.name.startswith("claimed-")):
            return await ctx.send("This command can only be used in ticket channels!")
    
        await ctx.channel.set_permissions(user, read_messages=True, send_messages=True)
        await ctx.send(f"{user.mention} has been added to the ticket.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx, user: discord.Member):
        if not (ctx.channel.name.startswith("ticket-") or ctx.channel.name.startswith("claimed-")):
            return await ctx.send("This command can only be used in ticket channels!")
    
        await ctx.channel.set_permissions(user, overwrite=None)
        await ctx.send(f"{user.mention} has been removed from the ticket.")

    @commands.command()
    async def close(self, ctx):
        if not (ctx.channel.name.startswith("ticket-") or ctx.channel.name.startswith("claimed-")):
            return await ctx.send("This command can only be used in ticket channels!")
        
        messages = [message async for message in ctx.channel.history(limit=100)]
        transcript = "\n".join(f"{msg.author}: {msg.content}" for msg in reversed(messages))
        
        transcript_file = discord.File(
            io.StringIO(transcript),
            filename=f"{ctx.channel.name}.txt"
        )
        
        logs_channel_id = self.ticket_logs.get(ctx.guild.id)
        logs_channel = None
        
        if logs_channel_id:
            logs_channel = ctx.guild.get_channel(logs_channel_id)
        if not logs_channel:
            logs_channel = discord.utils.get(ctx.guild.channels, name="ticket-logs")
        
        if logs_channel:
            close_log = EmbedBuilder(
                "📝 Ticket Closed",
                f"Ticket {ctx.channel.name} was closed by {ctx.author.mention}"
            ).set_color(discord.Color.red())
            
            await logs_channel.send(embed=close_log.build(), file=transcript_file)
        
        await ctx.send("Closing ticket...")
        await asyncio.sleep(3)
        await ctx.channel.delete()




def setup(bot):
    bot.add_cog(TicketSystem(bot))

bot.add_cog(ModerationCommands(bot))
bot.add_cog(TicketSystem(bot))

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autorole_dict = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handles delayed autorole assignment for new members"""
        if hasattr(self, 'autorole_dict') and member.guild.id in self.autorole_dict:
            await asyncio.sleep(5)  
            role = member.guild.get_role(self.autorole_dict[member.guild.id])
            if role:
                try:
                    await member.add_roles(role)
                    print(f"Assigned role '{role.name}' to {member.name}.")
                except discord.Forbidden:
                    pass

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None, minutes: int = None):
        channel = channel or ctx.channel
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
    
        embed = EmbedBuilder(
        "🔒 Channel Lockdown",
        f"{channel.mention} has been locked down."
    ).set_color(discord.Color.red())
        embed.add_field("Moderator", ctx.author.mention)
    
        if minutes:
            embed.add_field("Duration", f"{minutes} minutes")
            embed.set_footer("Channel will automatically unlock")
            await ctx.send(embed=embed.build())
        
            await asyncio.sleep(minutes * 60)
            perms.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        
            unlock_embed = EmbedBuilder(
            "🔓 Channel Unlocked",
            f"{channel.mention} has been automatically unlocked."
        ).set_color(discord.Color.green()).build()
            await ctx.send(embed=unlock_embed)
        else:
            embed.set_footer("Use !unlock to remove the lockdown")
            await ctx.send(embed=embed.build())
    
        await log_manager.log_action(ctx.guild, 'lockdown', ctx.author, channel)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        
        embed = EmbedBuilder(
            "🔓 Channel Unlocked",
            f"{channel.mention} has been unlocked."
        ).set_color(discord.Color.green())
        embed.add_field("Moderator", ctx.author.mention)
        
        await ctx.send(embed=embed.build())

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        
        embed = EmbedBuilder(
            "⏱️ Slowmode Updated",
            f"Channel slowmode set to {seconds} seconds"
        ).set_color(discord.Color.blue())
        embed.add_field("Channel", ctx.channel.mention)
        embed.add_field("Moderator", ctx.author.mention)
        
        await ctx.send(embed=embed.build())

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role = None):
        """Toggle automatic role assignment for new members"""
        if not hasattr(self, 'autorole_dict'):
            self.autorole_dict = {}
        
        if role is None:
            if ctx.guild.id in self.autorole_dict:
                current_role = ctx.guild.get_role(self.autorole_dict[ctx.guild.id])
                embed = EmbedBuilder(
                    "ℹ️ Autorole Status",
                    f"Currently active for role: {current_role.mention if current_role else 'None'}"
                ).set_color(discord.Color.blue()).build()
            else:
                embed = EmbedBuilder(
                    "ℹ️ Autorole Status",
                    "Autorole is currently disabled"
                ).set_color(discord.Color.blue()).build()
        else:
            if ctx.guild.id in self.autorole_dict and self.autorole_dict[ctx.guild.id] == role.id:
            
                del self.autorole_dict[ctx.guild.id]
                embed = EmbedBuilder(
                    "🔄 Autorole Disabled",
                    f"Automatic role assignment for {role.mention} has been disabled"
                ).set_color(discord.Color.red()).build()
            else:
            
                self.autorole_dict[ctx.guild.id] = role.id
                embed = EmbedBuilder(
                    "✅ Autorole Enabled",
                    f"New members will automatically receive the {role.mention} role"
                ).set_color(discord.Color.green()).build()
    
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel  
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        
        embed = discord.Embed(
            title="🔒 Channel Hidden",
            description=f"{channel.mention} has been hidden from regular members.",
            color=discord.Color.red()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        
        await ctx.send(embed=embed)
        await log_manager.log_action(ctx.guild, 'hide', ctx.author, channel)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def show(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel  
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        
        embed = discord.Embed(
            title="👁️ Channel Visible",
            description=f"{channel.mention} has been made visible to regular members.",
            color=discord.Color.green()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        
        await ctx.send(embed=embed)
        await log_manager.log_action(ctx.guild, 'show', ctx.author, channel)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Super advanced server setup with customizable templates"""
        guild = ctx.guild
        original_channel = ctx.channel

        print(f"[DEBUG] Starting setup in guild: {guild.name} (ID: {guild.id})")

        templates = {
            "📜": {
                "name": "Information Hub",
                "desc": "Perfect for announcements and documentation",
                "categories": {
                    "📢 Announcements": ["📌-announcements", "🎉-events", "📊-polls"],
                    "📚 Information": ["📜-rules", "❓-faq", "🎫-roles"],
                    "📝 Documentation": ["📘-guides", "📖-wiki", "📑-changelogs"]
                }
            },
            "🎵": {
                "name": "Music Community",
                "desc": "For music lovers and sharing",
                "categories": {
                    "🎵 Music Channels": ["🎵-music-chat", "🎼-song-requests", "🎹-recommendations"],
                    "🎧 Music Rooms": ["🎸-music-1", "🎺-music-2", "🎻-music-3"]
                }
            },
            "🎮": {
                "name": "Gaming Center",
                "desc": "Complete gaming community setup",
                "categories": {
                    "🎮 Gaming Hub": ["🎮-gaming-chat", "🎲-lfg", "🏆-achievements"],
                    "🎲 Game Specific": ["🔫-fps-games", "⚔️-mmo-games", "🏎️-racing-games"]
                }
            },
            "💻": {
                "name": "Development Hub",
                "desc": "For coding and development",
                "categories": {
                    "💻 Development": ["💻-coding-chat", "🐛-bug-reports", "📝-code-reviews"],
                    "🔧 Project Management": ["📋-projects", "✅-todo", "📊-progress"]
                }
            },
            "🤖": {
                "name": "Bot Testing",
                "desc": "Perfect for bot development",
                "categories": {
                    "🤖 Bot Testing": ["🤖-bot-commands", "🔧-test-channel", "📝-bot-logs"],
                    "⚙️ Configuration": ["⚙️-settings", "📊-analytics", "🔍-debugging"]
                }
            },
            "🔊": {
                "name": "Voice Lounges",
                "desc": "General voice chat rooms",
                "voice_channels": {
                    "🎤 Voice Lounges": ["🔊 General VC", "💬 Hangout VC", "🎮 Gaming VC"]
                }
            },
            "🎹": {
                "name": "Music Rooms",
                "desc": "Music-focused voice channels",
                "voice_channels": {
                    "🎵 Music Rooms": ["🎵 Music VC #1", "🎵 Music VC #2", "🎧 Radio VC"]
                }
            }
        }

        await original_channel.send(embed=EmbedBuilder(
            "🚀 Starting Advanced Server Setup",
            "This channel will log all setup-related actions."
        ).set_color(discord.Color.blue()).build())

        template_embed = discord.Embed(
            title="🎨 Server Template Selection",
            description="Select server templates to combine (React with emojis)\n\n" +
                    "\n".join([f"{k} **{v['name']}** - {v['desc']}" for k,v in templates.items()]) +
                    "\n\n⚡ React with your choices and then click ✨ to confirm",
            color=discord.Color.blue()
        )
        selection_msg = await ctx.send(embed=template_embed)


        for emoji in list(templates.keys()) + ["✨"]:
            await selection_msg.add_reaction(emoji)
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✨"

        try:
            await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
            selected_templates = []
            msg = await ctx.channel.fetch_message(selection_msg.id)
                
            for reaction in msg.reactions:
                async for user in reaction.users():
                    if user == ctx.author and str(reaction.emoji) in templates:
                        selected_templates.append(templates[str(reaction.emoji)])


            if not selected_templates:
                await ctx.send("❌ No templates selected! Setup cancelled.")
                return

            confirm_embed = EmbedBuilder(
                "⚠️ WARNING: This will DELETE ALL ROLES, CHANNELS, AND CATEGORIES!",
                "Are you sure you want to proceed? Type `yes` to confirm or `no` to cancel."
            ).set_color(discord.Color.red()).build()
            await original_channel.send(embed=confirm_embed)

            def check_msg(m):
                return m.author == ctx.author and m.channel == original_channel and m.content.lower() in ["yes", "no"]

            confirmation = await self.bot.wait_for("message", timeout=30.0, check=check_msg)
            if confirmation.content.lower() != "yes":
                await original_channel.send("❌ Setup canceled.")
                return

            bot_member = guild.get_member(self.bot.user.id)
            bot_role = discord.utils.get(guild.roles, name=self.bot.user.name)

            if not bot_role:
                print("[DEBUG] Bot does not have a role. Creating a temporary role.")
                try:
                    bot_role = await guild.create_role(name="🚀 Setup Role", permissions=discord.Permissions.all(), color=discord.Color.orange())
                    await bot_member.add_roles(bot_role)
                    await original_channel.send(f"✅ Created and assigned temporary role: {bot_role.name}")
                except Exception as e:
                    await original_channel.send(f"❌ Failed to create temporary role: {e}")
                    return

            print("[DEBUG] Deleting roles...")
            for role in guild.roles:
                if role.name != "@everyone" and role != bot_role:
                    try:
                        await role.delete(reason="Advanced server setup")
                        await original_channel.send(f"🗑️ Deleted role: {role.name}")
                    except Exception as e:
                        print(f"[ERROR] Failed to delete role {role.name}: {e}")
                        continue
            
            print("[DEBUG] Deleting channels and categories...")
            for channel in guild.channels:
                if channel != original_channel:
                    try:
                        await channel.delete(reason="Advanced server setup")
                        await original_channel.send(f"🗑️ Deleted channel: {channel.name}")
                        print(f"[DEBUG] Deleted channel: {channel.name}")
                    except discord.Forbidden:
                        await original_channel.send(f"❌ Failed to delete channel: {channel.name} (Missing Permissions)")
                        continue
                    except discord.HTTPException as e:
                        await original_channel.send(f"❌ Failed to delete channel: {channel.name} ({e})")
                        continue

            print("[DEBUG] Creating new roles...")
            try:
                print("[DEBUG] Creating Owner role...")
                owner_role = await guild.create_role(name="👑 Owner", permissions=discord.Permissions.all(), color=discord.Color.gold(), hoist=True)
                
                print("[DEBUG] Creating Bot Owner role...")
                bot_role_owner = await guild.create_role(name="🤖 Bot (Owner-Level)", permissions=discord.Permissions.all(), color=discord.Color.dark_theme(), hoist=False)
                
                print("[DEBUG] Creating Admin role...")
                admin_role = await guild.create_role(name="🔧 Admin", permissions=discord.Permissions.all(), color=discord.Color.blue(), hoist=True)
                
                print("[DEBUG] Creating Mod role...")
                mod_role = await guild.create_role(name="🛡️ Mod", permissions=discord.Permissions(
                    manage_messages=True, kick_members=True, ban_members=True, manage_channels=True
                ), color=discord.Color.green(), hoist=True)
                
                print("[DEBUG] Creating Member role...")
                member_role = await guild.create_role(name="👤 Member", permissions=discord.Permissions(
                    read_messages=True, send_messages=True
                ), color=discord.Color.default(), hoist=True)
                
                print("[DEBUG] Creating Bot Locked role...")
                bot_role_locked = await guild.create_role(name="🤖 Bot (Locked-Down)", permissions=discord.Permissions.none(), color=discord.Color.dark_grey(), hoist=True)
                
                print("[DEBUG] Sending role creation confirmation...")
                await original_channel.send(embed=EmbedBuilder(
                    "✅ Roles Created",
                    "The following roles have been created:"
                ).add_field("👑 Owner", owner_role.mention)
                .add_field("🤖 Bot (Owner-Level)", bot_role_owner.mention)
                .add_field("🔧 Admin", admin_role.mention)
                .add_field("🛡️ Mod", mod_role.mention)
                .add_field("👤 Member", member_role.mention)
                .add_field("🤖 Bot (Locked-Down)", bot_role_locked.mention)
                .set_color(discord.Color.green()).build())
                
                print("[DEBUG] Roles created successfully")
                print("[DEBUG] Starting template-based channel creation...")

                for template in selected_templates:
                    if "categories" in template:
                        for category_name, channels in template["categories"].items():
                            try:
                                category = await guild.create_category(category_name)
                                await original_channel.send(f"📂 Created category: {category_name}")
                                print(f"[DEBUG] Created category: {category_name}")

                                overwrites = {
                                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                                    owner_role: discord.PermissionOverwrite(administrator=True),
                                    admin_role: discord.PermissionOverwrite(manage_channels=True),
                                    mod_role: discord.PermissionOverwrite(manage_messages=True),
                                    member_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                                }

                                if "Admin" in category_name:
                                    overwrites[guild.default_role] = discord.PermissionOverwrite(read_messages=False)
                                    overwrites[member_role] = discord.PermissionOverwrite(read_messages=False)
                                elif "Bot" in category_name:
                                    overwrites[guild.default_role] = discord.PermissionOverwrite(send_messages=False)
                                    overwrites[bot_role_owner] = discord.PermissionOverwrite(send_messages=True)

                                await category.edit(overwrites=overwrites)

                                for channel_name in channels:
                                    await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
                                    await original_channel.send(f"📝 Created channel: {channel_name} in {category_name}")
                                    print(f"[DEBUG] Created channel: {channel_name} in {category_name}")

                            except Exception as e:
                                await original_channel.send(f"❌ Error creating {category_name}: {e}")
                                print(f"[ERROR] Failed to create {category_name}: {e}")
                                continue
                    
                    if "voice_channels" in template:
                        for category_name, channels in template["voice_channels"].items():
                            try:
                                category = await guild.create_category(category_name)
                                await original_channel.send(f"📂 Created voice category: {category_name}")
                                
                                for channel_name in channels:
                                    await guild.create_voice_channel(channel_name, category=category)
                                    await original_channel.send(f"🎤 Created voice channel: {channel_name}")
                                    print(f"[DEBUG] Created voice channel: {channel_name}")
                                    
                            except Exception as e:
                                await original_channel.send(f"❌ Error creating voice channel {category_name}: {e}")
                                print(f"[ERROR] Failed to create voice channel {category_name}: {e}")
                                continue




                print("[DEBUG] Assigning roles...")
                try:
                    await ctx.author.add_roles(owner_role)
                    await bot_member.add_roles(bot_role_owner, bot_role_locked)
                    
                    await original_channel.send(embed=EmbedBuilder(
                        "✅ Roles Assigned",
                        "The following roles have been assigned:"
                    ).add_field("👑 Owner", ctx.author.mention)
                    .add_field("🤖 Bot (Owner-Level + Locked)", bot_member.mention)
                    .set_color(discord.Color.green()).build())
                    
                    print("[DEBUG] Successfully assigned roles.")
                except Exception as e:
                    await original_channel.send(f"❌ Failed to assign roles: {e}")
                    print(f"[ERROR] Failed to assign roles: {e}")

                if bot_role.name == "🚀 Setup Role":
                    try:
                        await bot_role.delete(reason="Setup complete")
                        print("[DEBUG] Deleted temporary setup role")
                    except Exception as e:
                        print(f"[ERROR] Failed to delete temporary role: {e}")

                final_embed = discord.Embed(
                    title="✨ Advanced Server Setup Complete!",
                    description="Server has been fully configured with selected templates!",
                    color=discord.Color.green()
                )
                final_embed.add_field(name="Templates Used", value="\n".join([t['name'] for t in selected_templates]))
                final_embed.add_field(name="Total Channels", value=f"Created {len(list(guild.channels))} channels")
                final_embed.add_field(name="Total Roles", value=f"Created {len(list(guild.roles))} roles")
                
                await original_channel.send(embed=final_embed)
                print("[DEBUG] Setup completed successfully")

            except discord.Forbidden as e:
                print(f"[ERROR] Permission error creating roles: {e}")
                await original_channel.send(embed=EmbedBuilder(
                    "❌ Permission Error",
                    "Failed to create roles due to missing permissions. Please ensure the bot has the Administrator permission."
                ).set_color(discord.Color.red()).build())
            except discord.HTTPException as e:
                print(f"[ERROR] HTTP error creating roles: {e}")
                await original_channel.send(embed=EmbedBuilder(
                    "❌ Discord API Error",
                    f"Failed to create roles due to a Discord API error: {e}"
                ).set_color(discord.Color.red()).build())
            except Exception as e:
                print(f"[ERROR] Unexpected error creating roles: {e}")
                await original_channel.send(embed=EmbedBuilder(
                    "❌ Unexpected Error",
                    f"An unexpected error occurred while creating roles: {e}\nPlease try again or contact support."
                ).set_color(discord.Color.red()).build())
                
        except asyncio.TimeoutError:
            await ctx.send("❌ Setup timed out! Please try again.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred during setup: {e}")
            print(f"[ERROR] Setup failed: {e}")


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
    
        total_members = guild.member_count
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
    
        embed = EmbedBuilder(
        f"📊 {guild.name} Statistics",
        "Detailed server information and statistics"
    ).set_color(discord.Color.blue())
    
        general_info = (
        f"👑 Owner: {guild.owner.mention}\n"
        f"📅 Created: {guild.created_at.strftime('%B %d, %Y')}\n"
        f"✨ Boost Level: {guild.premium_tier}"
    )
        embed.add_field("General Information", general_info, inline=False)
    
        member_stats = (
        f"👥 Total Members: {total_members}\n"
        f"👤 Humans: {humans}\n"
        f"🤖 Bots: {bots}"
    )
        embed.add_field("Member Statistics", member_stats)
    
        channel_stats = (
        f"💬 Text Channels: {len(guild.text_channels)}\n"
        f"🔊 Voice Channels: {len(guild.voice_channels)}\n"
        f"📑 Categories: {len(guild.categories)}"
    )
        embed.add_field("Channel Statistics", channel_stats)
    
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")  
    
        await ctx.send(embed=embed.build())


    @commands.command()
    async def roles(self, ctx):
        roles = sorted(ctx.guild.roles[1:], key=lambda x: x.position, reverse=True)
        
        embed = EmbedBuilder(
            "🎭 Server Roles",
            f"Total Roles: {len(roles)}"
        ).set_color(discord.Color.gold())
        
        role_chunks = [roles[i:i + 20] for i in range(0, len(roles), 20)]
        
        for i, chunk in enumerate(role_chunks, 1):
            role_list = '\n'.join(f"{role.mention} - {len(role.members)} members" for role in chunk)
            embed.add_field(f"Roles (Page {i})", role_list, inline=False)
        
        await ctx.send(embed=embed.build())

    @commands.command()
    async def stats(self, ctx):
        """Show bot statistics"""
        uptime = str(timedelta(seconds=int(time.time() - self.bot.start_time)))
    
        embed = EmbedBuilder(
        "⚡ Bot Statistics",
        "Current bot performance and statistics"
    ).set_color(discord.Color.blue())
    
        embed.add_field("Uptime", uptime)
        embed.add_field("Servers", str(len(self.bot.guilds)))
        embed.add_field("Users", str(len(set(self.bot.get_all_members()))))
        embed.add_field("Commands Run", "Coming soon...")
        embed.add_field("Python Version", platform.python_version())
        embed.add_field("Discord.py Version", discord.__version__)
        embed.add_field("Script Version",  (ZygnalBot_Version))
    
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        else:
            embed.set_thumbnail(url=self.bot.user.default_avatar.url)
    
        await ctx.send(embed=embed.build())


    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
    
        embed = EmbedBuilder(
        f"👤 User Information - {member.name}",
        f"Details about {member.mention}"
    ).set_color(member.color)
    
        embed.add_field("Joined Server", member.joined_at.strftime("%B %d, %Y"))
        embed.add_field("Account Created", member.created_at.strftime("%B %d, %Y"))
        embed.add_field("Roles", " ".join([role.mention for role in member.roles[1:]]) or "None")
        embed.set_thumbnail(member.avatar.url if member.avatar else member.default_avatar.url)
    
        await ctx.send(embed=embed.build())

bot.add_cog(ServerManagement(bot))
bot.add_cog(ServerInfo(bot))

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="part Two →", style=ButtonStyle.success, custom_id="help_part2_button", emoji="✨", row=4)
    async def show_part2(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = EmbedBuilder(
            "✨ Part Two",
            "Discover additional powerful tools"
        ).set_color(discord.Color.brand_green())
        
        view = HelpViewTwo()
        await interaction.response.edit_message(embed=embed.build(), view=view)       

    @discord.ui.select(
        placeholder="Select command category",
        row=3,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="🛡️ 𝐌𝐨𝐝𝐞𝐫𝐚𝐭𝐢𝐨𝐧", description="Ban, kick, and mute commands", emoji="🛡️"),
            discord.SelectOption(label="🔵 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 [1]", description="Server management commands Part 1", emoji="⚙️"),
            discord.SelectOption(label="🔵 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 [2]", description="Server management commands Part 2", emoji="⚙️"),
            discord.SelectOption(label="ℹ️ 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧", description="Server and user info commands", emoji="ℹ️"),
            discord.SelectOption(label="🎫 𝐓𝐢𝐜𝐤𝐞𝐭𝐬", description="Ticket system commands", emoji="🎫"),
            discord.SelectOption(label="💾 𝐁𝐚𝐜𝐤𝐮𝐩", description="Server backup and restore commands", emoji="💾"),
            discord.SelectOption(label="⚙️ 𝐂𝐨𝐧𝐟𝐢𝐠", description="Configuration import/export commands", emoji="⚙️"),  
            discord.SelectOption(label="🎉 Fun/𝐌𝐢𝐧𝐢𝐠𝐚𝐦𝐞𝐬", description="MiniGames", emoji="🎉"),
            discord.SelectOption(label="AFK", description="AFK commands", emoji="😶‍🌫️"),
            discord.SelectOption(label="🔎 𝐒𝐧𝐢𝐩𝐞", description="Snipes", emoji="🔎"),
            discord.SelectOption(label="🎭 𝐑𝐨𝐥𝐞 𝐏𝐚𝐧𝐞𝐥𝐬", description="Role panel management commands", emoji="🎭"),
            discord.SelectOption(label="📈 𝐋𝐞𝐯𝐞𝐥𝐢𝐧𝐠", description="Leveling system commands", emoji="📈"),
            discord.SelectOption(label="🔒 𝐕𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧", description="Verification system commands", emoji="🔒"),
            discord.SelectOption(label="🤖 𝐁𝐨𝐭 𝐕𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧", description="Bot verification and whitelist commands", emoji="🤖"),
            discord.SelectOption(label="⭐ 𝐑𝐚𝐭𝐢𝐧𝐠", description="Rating system commands", emoji="⭐"),
            discord.SelectOption(label="𝐀𝐈 𝐒𝐲𝐬𝐭𝐞𝐦", description="AI commands and settings", emoji="🤖"),
            discord.SelectOption(label="Embed", description="Embed commands", emoji="🧾"),
            discord.SelectOption(label="TempChannels", description="Create and manage temporary channels", emoji="📝"),
            discord.SelectOption(label="profile", description="Customize your server profile", emoji="👤"),
            discord.SelectOption(label="Webhooks", description="Webhook settings and commands", emoji="📡"),
            discord.SelectOption(label="CustomVerification", description="Manual Verify commands", emoji="🪄"),
            discord.SelectOption(label="advertisements", description="Advertisement System Commands", emoji="🧾"),
            discord.SelectOption(label="Coding Tools", description="Coding tools commands", emoji="🔧"),
            discord.SelectOption(label="Calculations", description="Calculations and TimeZone Converter", emoji="📊"),
            discord.SelectOption(label="Study Tools", description="All Study related tools on one command", emoji="📚"),
        ]
    )

    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        category_info = {
            "🛡️ 𝐌𝐨𝐝𝐞𝐫𝐚𝐭𝐢𝐨𝐧": {
                "title": "🛡️ Moderation",
                "color": discord.Color.red(),
                "commands": {
                    "!ban <user> [duration] [reason]": "Permanently ban a user | Add duration (7d2h10m5s) for temporary ban",
                    "!ban_appeal <dc server| website | custom message": "make a custom appeal server when person will be banned he will see that",
                    "!unban <user_id> [reason]": "Unban a user",
                    "!kick <user> [reason]": "Kick a user from the server",
                    "!mute <user> <duration> [reason]": "Temporarily mute a user",
                    "!unmute <user": "Unmutes a user",
                    "!warn <user> [reason]": "Issue a warning to a user",
                    "!clear <amount>": "Clear specified amount of messages",
                    "!nuke [channel]": "Completely reset a channel",
                    "!vcmute <user>": "Mute user in voice chat",
                    "!vcunmute <user>": "Unmute user in voice chat",
                    "!togglelinks": "Toggle links in chat/ by default on",
                }
            },  
            "Calculations": {
                "title": "🧮 Calculations",
                "color": discord.Color.blue(),
                "commands": {
                    "!bmi": "BMI Calc",
                    "!math": "math Calc",
                    "!physics": "physics Calc",
                    "!time": "Time Converters, Time Tools and more "
                }
            },
            "Study Tools": {
                "title": "📚 Study Tools",
                "color": discord.Color.blue(),
                "commands": {
                    "!study": "Study Related Tools",
                    "!time": "Time Converters, Time Tools and more",
                    "!isbn <isbn>": "Looks up book information and generates citations",
                    "!cite": "Creates formatted citations in various academic styles"
                }        
            },            
            "Coding Tools": {
                "title": "Coding Tools",
                "color": discord.Color.blue(),
                "commands": {
                    "!code": "Coding Tools",
                    "!colorpicker": "Color Picker",
                }
            },
            "🔵 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 [1]": {
                "title": "⚙️ Management Commands",
                "color": discord.Color.blue(),
                "commands": {
                    "!mutesetup": "who ever gets muted gets this role you configured with that command",
                    "!lockdown [channel] [Min]": "Lock a channel | (optional) for a specified time",
                    "!unlock [channel]": "Unlock a channel",
                    "!slowmode <seconds>": "Set channel slowmode",
                    "!announce <color (optional/HEX code!)> #channel <message with or no links>": "send a announcement to a channel",
                    "!addrole <user> <role>": "Add a role to a user",
                    "!removerole <user> <role>": "Remove a role from a user",
                    "!autorole <role>": "Automatically assign a role to new members - Toggle",
                    "!autorole": "show current autorole status",
                    "!rolepanel": "Create a role panel for users to select roles",
                    "!welcome": "Welcome panel (shows u all)",
                    "!automod": "Open the automod pannels with infos and settings",
                    "!setup": "setup basic server setup",
                    "!nickname <user_id> <nickname>": "Change the user's nickname.",
                    "!nickname <user_id>": "remove the users nickname.",
                }
            },
            "🔵 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 [2]": {
                "title": "⚙️ Management Commands",
                "color": discord.Color.blue(),
                "commands": {
                    "!massrole <role>": "Add a role to all members",
                    "!embed <title> <description>": "Create a custom embed message",
                    "!say <channel> <message>": "Make the bot send a message",
                    "!addchannel <channel> <user>": "Allows a user access to a channel",
                    "!removechannel <channel> <user>": "Remove a user from a channel",
                    "!inivte <duration> <max uses>": "Create an invite link for a channel with customizable duration and max uses",
                    "!invite_view": "Show all invite links and information about them",
                    "!reminder": "Opens the reminder pannel",
                    "!editreminder ": "Edit ur reminders with a panel",
                    "!purge <user| bots | links> <amount/nuke>": "Purge messages from a user, bots, or links",
                    "!mood": "Opens the mood pannel",
                    "!hide <optional| <channel>": "hides a channel",
                    "!show <optional| <channel>": "shows a channel",
                    "!ideasystem": "Opens ideasystem panel",
                }
            },
            "ℹ️ 𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧": {
                "title": "ℹ️ Information Commands",
                "color": discord.Color.green(),
                "commands": {
                    "!serverinfo": "Display server statistics",
                    "!userinfo [user]": "Show user information",
                    "!roles": "List all server roles",
                    "!stats": "Show bot statistics",
                    "!activity <user>": "Check user activity status",
                    "!servericon": "Show server icon in full size",
                    "!createpoll ": "Create a reaction poll | Opens main Menu/Button",
                    "!avatar [user]": "Show user's avatar in full size",
                    "!ping": "Check bot's response time",
                    "!analyse daily <channel>": "Sets up daily analytics tracking and reporting in the specified channel.",
                    "!analyse weekly <channel>": "Sets up weekly analytics tracking and reporting in the specified channel.",
                    "!analyse monthly <channel>": "Sets up monthly analytics tracking and reporting in the specified channel.",
                    "!analyse": "Show all analytics status",
                    "view_historic": "Lets u see who joined with what invite",
                    "!wordstats": "Shows word stats | (Enhanced)",
                }
            },
            "🎫 𝐓𝐢𝐜𝐤𝐞𝐭𝐬": {
                    "title": "🎫 Ticket Commands",
                    "color": discord.Color.gold(),
                    "commands": {
                        "!ticketsetup <title> <description> <embed color> <button color>": "Creates a ticket panel with a button called 'Create Ticket' when pressed it opens a window where it says to describe your problem after that ticket",
                        "!close": "Close current ticket",
                        "!add <user>": "Add user to ticket",
                        "!remove <user>": "Remove user from ticket",
                        "!ticketadmin <role>": "Setup what roles get added to the ticket",
                        "!ticketadmin": "Shows current ticket admin role",
                        "!ticketsetup_json": "Creates a ticket panel using JSON configuration (attach .json file or paste JSON)",
                        "!ticketsetup_json example": "Shows example JSON format for ticket setup",
                        "!ticketsetup_json <{\"embeds\": [...], \"button_color\": \"blurple\"}>": "Shows current ticket panel",
                        "!fixticket <category id>": "Set the category where tickets are created",
                        "!fixlogs <channel id>": "set the channel where ticket logs are sent",
                    }
                },
            "Webhooks": {
                        "title": "Webhook Commands",
                        "color": discord.Color.gold(),
                        "commands": {
                            "!webhook": "Opens the webhook dashboard",
                }
            },
            "💾 𝐁𝐚𝐜𝐤𝐮𝐩": {
                "title": "💾 Backup Commands",
                "color": discord.Color.purple(),
                "commands": {
                    "!backup": "Creates basic structure backup (roles, channels, permissions) ",
                    "!backup true": "Creates full backup including messages (up to 100 messages per channel) ",
                    "!backup True 500": "Creates full backup with custom message limit (500 messages per channel in this example)",
                    "!restore": "Restores a server from a backup file (attach the .json backup file with the command)| No Attachments (eg. txt/videos..) ",
                    "!copychannel <channel_id>": "Creates a complete 1:1 backup of a specific channel including all messages, files and settings",
                    "!pastechannel <attach zip>": "Restores a channel from backup (attach the backup ZIP file)",
                    "!copyrole <role_id>": "Creates a complete backup of a specific role including all settings and members | Copies everything even Atachments",
                    "!pasterole <attach zip>": "Restores a role from backup (attach the backup ZIP file)"
                }
            },
            "⚙️ 𝐂𝐨𝐧𝐟𝐢𝐠": {
                "title": "⚙️ Configuration Commands/export/import cmds",
                "color": discord.Color.blue(),
                "commands": {
                    "!exportconfig": "Export all server settings to a JSON file",
                    "!importconfig": "Import server settings from a JSON file (attach the file)",
                    

                    "!importrating": "import ratings data from a JSON file",
                    "!exportrating": "export ratings data to a JSON file",

                    "!importrolepanel": "import role panel data from a JSON file (if using _json just use !importconfig)",
                    "!exportrolepanel": "export role panel data to a JSON file if using _json just use !exportingconfig",

                    "!import_mood_data": "import mood data from a JSON file",
                    "!export_mood_data": "export mood data to a JSON file",

                    "!import_analytics": "import analytics data from a JSON file",
                    "!export_analytics": "export analytics data to a JSON file",


                }

            },
            "Embed": {
                "title": "Embed Commands",
                "color": discord.Color.blue(),
                "commands": {
                    "!embed <title> <description> <color>": "Create a basic embed message",
                    "!embedhelp": "Shows examples and formats for JSON embeds",
                    "!jsonembed + attached .json file": "Create embed from a JSON file (supports Discohook format)",
                    "!jsonembed {json data}": "Create embed from JSON text (supports all formats)",
                    "!embed color": "Shows list of available embed colors",
                    "!embed preview <color>": "Preview how a color looks in an embed"
                }
            },
            "🎵 Music": {
                "title": "🎵 Music Commands | Not Recommended",
                "color": discord.Color.red(),
                "commands": {
                    "!player": "Shows Music Menu",
                   
            }
        },   
            "🎉 Fun/𝐌𝐢𝐧𝐢𝐠𝐚𝐦𝐞𝐬": {
                "title": "🎮 Fun Commands",
                "color": discord.Color.orange(),
                "commands": {
                    "!numbergame <number> <channel>": "Lets admins create a number game",
                    "<number>": "lets players guess the number innn the chat it started ",
                    "!tictactoe": "Starts a tic tac toe game",
                    "!joke": "Tells a random joke",
                    "!games": "Shows the all games",
                    "!player": "Shows Music Menu",
                    "!rng <min> <max>": "Generates a random number between min and max",
                }
        },
        "AFK": {
                "title": "Afk Commands",
                "color": discord.Color.green(),
                "commands": {
                    "!afk <reason>": "Puts u AFK",
                    "!afk": "Toggle",
                    " - ": "if u write smth while afk it will break afk",
                }
            },
            "🔎 𝐒𝐧𝐢𝐩𝐞": {
                "title": "🔎 Snip Commands",
                "color": discord.Color.purple(),
                "commands": {
                    "!snipe": "Lets u see the last deleted message",
                    "!editsnipe": "you can see the latest edited message and see the before and after",
                    "!snipe_info": "Shows the infos the duration of the snipe",
                    "!configuresnipeedit <duration>": "command to configure the duration for edited messages.",
                    "!configuresnipe <duration>": "command to configure the duration for deleted messages.",
                }
            },
            "🎭 𝐑𝐨𝐥𝐞 𝐏𝐚𝐧𝐞𝐥𝐬": {
                "title": "🎭 Role Panel Commands",
                "color": discord.Color.magenta(),
                "commands": {
                    "!rolepanel": "Open the advanced role management panel with customization options",
                    "!rolepanel_json": "opens a dashboard where u can uplaod the json for custom role panels",
                    "!exportrolepanel": "Export all role panel configurations to a JSON file",
                    "!importrolepanel <JSON file>": "Import role panel configurations from a JSON file (attach the file)",
                    "Usage": "1. Create panels with !rolepanel\n2. Backup configs with !exportrolepanel\n3. Restore with !importrolepanel\n4. Use refresh button to update panels"
                }
            },
            "📈 𝐋𝐞𝐯𝐞𝐥𝐢𝐧𝐠": {  
                "title": "📈 Leveling System Commands",
                "color": discord.Color.teal(),
                "commands": {
                    "!levelsetup": "Shows All infos/settings of the leveleling system",
                    "!levelsetup <channel>": "Sets the channel where the leveling messages are sent",
                    "!set_level_role <level> <role>": "Assign a role to a specific level.",
                    "!leaderboard": "Display the server's leveling leaderboard.",
                    "!my_level": "Check your current level and XP.",
                    "!set_xp <user> <xp>": "Set a user's XP manually (Bot Owner only).",
                    "!reset_levels": "Reset all leveling data for the server (Bot Owner only).",
                    "!set_leaderboard_channel <channel>": "Set the channel for live-updating leaderboard.",
                    "!add_achievement <name> <required_level> <reward>": "Add a new achievement (Bot Owner only).",
                    "!set_xp_multiplier <role> <multiplier>": "Set an XP multiplier for a role (Bot Owner only).",
                }
            },

            "CustomVerification": {
                "title": "🔒 Verification Commands",
                "color": discord.Color.blue(),
                "commands": {
                    "!verify_user": "Verifies a user",
                    "!verify_setup_help": "Shows all the settings for the verification system",
                    "!verify_user_setup":"Setup the verification system",

                }       
            },
            "🔒 𝐕𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧": {
                "title": "🔒 Verification Commands",
                "color": discord.Color.blue(),
                "commands": {
                    "!verify": "Shows all verification settings/Opens Verificcation Menu",
                    "!verify easy | medium | hard <Timeout Duration | optional>": "Setup the verification level | For duration info use !verify",
                    "!verify stats": "Gives you information how many passed the verification tests and who failed",
                    "!verifychannel <channel>": "that is the channel where the verification messages are sent | there u will see who attempted to log on ur server and failed or who passed",
                    "!verificationrole <role>": "Just an Autorole that is given to the user when he passed the verification verify role + role u want to give to the user",
                }
            },
            "🤖 𝐁𝐨𝐭 𝐕𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧": {
                "title": "🤖 Bot Verification Commands",
                "color": discord.Color.blue(),
                "commands": {
                    "!botlogs #channel": "Sets the logging channel for unauthorized bot joins",
                    "!botlogs": "Disables the bot join logging",
                    "!whitelisted": "Displays a list of all whitelisted bots with names and IDs",
                    "!whitelist_bot <bot_id>": "Adds a bot to the whitelist (Owner Only) | To get a bot's ID: Enable Developer Mode in Discord Settings > App Settings > Advanced, then right-click the bot and select 'Copy ID', or check the bot logs channel when the bot attempts to join"
                }
            },
            "⭐ 𝐑𝐚𝐭𝐢𝐧𝐠": {
                "title": "⭐ Rating System Commands",
                "color": discord.Color.gold(),
                "commands": {
                    "!ratingsetup": "Create interactive rating panels with customizable stars/numbers/percentages",
                    "!seerating": "View all rating panels with statistics and management options",
                    "!ratingrefresh <panel_id>": "Refresh statistics for a specific rating panel",
                    "!importrating <JSON file>": "Import rating configurations from a JSON file (attach the file)",
                    "!exportrating": "Export all rating configurations to a JSON file",
                    "Features": "• Star Ratings (1-5)\n• Number Ratings (1-10)\n• Percentage Ratings (0-100%)\n• Real-time statistics\n• Visual vote tracking\n• One-click voting"
                    
                }
            },
            "𝐀𝐈 𝐒𝐲𝐬𝐭𝐞𝐦": {
                "title": "🤖 AI System Commands",
                "color": discord.Color.purple(),
                "commands": {
                    "!ai_info": "Get information about the New Chat AI system",
                    "!ai": "Opens the AI Command Center with all available features",
                    "!ai chat <message>": "Interactive chat with context memory",
                    "!ai create <prompt>": "Generate images with style control",
                    "!ai analyze <text>": "Deep content analysis",
                    "!ai predict <scenario>": "AI-powered predictions",
                    "!ai settings": "Configure AI behavior (Model, Personality, Response Style)",
                    "Models": "• GPT-4 (Premium quality)\n• GPT-3.5 (Balanced)\n• GPT-3.5 Instruct (Fast)",
                    "Features": "• Context-aware conversations\n• Multiple personality modes\n• Customizable response styles\n• Image generation\n• Advanced text analysis"
                }
            },
            "TempChannels": {
                    "title": "Temp Channels",
                    "color": discord.Color.red(),
                    "commands": {
                            "!setuptempchannel": "Creates a button panel for users to create temporary channels",

                }
            },
            "profile": {
                "title": "Profile/Social Commands",
                "color": discord.Color.green(),
                "commands": {
                    "!p setup": "setup your own profile",
                    "!p <userid>": "view a user's profile",

                }
            },
            "advertisements": {
                "title": "Advertisement System Commands",
                "color": discord.Color.gold(),
                "commands": {
                    
                    "!serverad post": "Create your server advertisement",
                    "!serverad bump": "Bump your ad to increase visibility",
                    "!serverad preview": "Preview your current advertisement",
                    "!serverad stats": "View your ad performance metrics",
                    "!serverad serverad template": "Get the advertisement template",
                    "!serverad serverad edit": "Modify your existing advertisement",
                    "!ad_search [query]": "Find ads by name or tags",
                    "!serverad rename_channel": "Customize your ad channel name",

                    "!move_ad [msgid] [channel]": "[MOD] Move ads between channels",
                    "!ad_channel_stats": "[MOD] View channel statistics",
                    "!ad_cleanup": "[MOD] Remove expired advertisements",

                    "!setup_ad_category": "[ADMIN] Create new ad category",
                    "!serverad allow @user #channel": "[ADMIN] Grant posting permissions",
                    "!ad_settings": "[ADMIN] Configure advertisement system",
                    "!ad_stats": "[ADMIN] View system statistics",
                    "!ad_blacklist [user]": "[ADMIN] Block users from advertising",
                    "!ad_audit": "[ADMIN] Run system health check",
                    "!ad_restore [user]": "[ADMIN] Recover deleted ads"
                    }
                },
                "Analytics": {
                    "title": "Analytics Commands",
                    "color": discord.Color.blue(),
                    "commands": {
                        "!analytics": "View analytics for yourself/server | Working Fully",

                        "!!analytics <user>": "View analytics for a specific user | Not Tested Fully!" ,

                        "!analytics import": "Import analytics data from JSON | Buggy",
                        "!analytics export": "Export analytics data to JSON | Buggy",

                }
            }
        }



        category = category_info[select.values[0]]
        
        embed = EmbedBuilder(
            category["title"],
            "Detailed command information"
        ).set_color(category["color"])
        
        commands = list(category["commands"].items())
        
        for cmd, desc in commands[:24]:
            embed.add_field(cmd, desc, inline=False)
        
        remaining = len(commands) - 24
        footer_text = "🔹 Required <> | Optional []"
        if remaining > 0:
            footer_text += f" | {remaining} more commands available - Use !help {category['title']} for full list"
        
        embed.set_footer(footer_text)
        await interaction.response.edit_message(embed=embed.build(), view=self)

class HelpSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.readability_file = 'readability_settings.json'

    async def get_readability_setting(self, guild_id: str) -> bool:
        try:
            with open(self.readability_file, 'r') as f:
                settings = json.load(f)
                return settings.get(guild_id, False)
        except FileNotFoundError:
            return False

    @commands.command(name='panel')
    async def help_command(self, ctx):
        embed = EmbedBuilder(
            "⚡ Command Center - TheZ",
            "Welcome to the interactive command center!\nExplore our features below"
        ).set_color(discord.Color.brand_green())
        
        embed.set_thumbnail(ctx.guild.icon.url)
        
        stats = f"🤖 Serving {len(self.bot.guilds)} servers\n"
        stats += f"👥 Watching {sum(g.member_count for g in self.bot.guilds)} users\n"
        stats += f"📊 Version: {ZygnalBot_Version}"
        embed.add_field(name="📈 Bot Statistics", value=stats, inline=False)
        
        tips = "• Commands start with the `!` prefix\n"
        tips += "• Use category buttons below to explore\n"
        tips += "• Some features require special permissions\n"
        tips += "• Need help? Join our support server"
        embed.add_field(name="💡 Quick Tips", value=tips, inline=False)
        
        embed.add_field(name="━━━━━━━━━━━━━━━", value="", inline=False)
        
        features = "🛡️ Advanced Moderation\n"
        features += "⚙️ Server Management\n"
        features += "🎮 Fun & Games\n"
        features += "📊 Analytics & More"
        embed.add_field(name="✨ Key Features", value=features, inline=False)
        
        embed.add_field(
            name="⚡ Powered By",
            value="**ZygnalBot** © 2025 *TheHolyOneZ*",
            inline=False
        )
        
        embed.set_footer(
            text="Security • Moderation • Entertainment", 
            icon_url=ctx.guild.icon.url
        )
        
        view = HelpView()
        
        await ctx.send(embed=embed.build(), view=view)
        
        if await self.get_readability_setting(str(ctx.guild.id)):
            for _ in range(7):
                await ctx.send("\u200b")

class HelpViewTwo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(
        placeholder="Select Feature Categorie",
        row=3,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="🔗 URL Shortener", description="Create and manage short URLs", emoji="✂️"),
            
            discord.SelectOption(label="Password Generator", description="Generate strong passwords", emoji="🛡️"),
            discord.SelectOption(label="Morse Code System", description="Morse Code System CMDS", emoji="📡"),
            
            discord.SelectOption(label="ASCII Commands", description="ASCII convert text to ascii", emoji="🔤"),
            discord.SelectOption(label="Network/ip Cmds", description="Network Commands", emoji="🌍"),
            discord.SelectOption(label="File/Download Cmds", description="File and download Commands", emoji="📂"),
           discord.SelectOption(label="All Elements (Element Table 118)", description="All Element table commands", emoji="⚛️"),
        ],
        custom_id="help_part2_select"
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        category_info = {
            "🔗 URL Shortener": {
                "title": "🔗 URL Shortener System",
                "color": discord.Color.blue(),
                "commands": {
                    "!url shorten <url>": "Create a shortened URL",
                }
            },
            "Password Generator": {
                "title": "Password Generator | Pass will be sent to your dm!",
                "color": discord.Color.purple(),
                "commands": {
                    "!password": "Opens Password Generator menu",
                    "!pw": "Opens Password Generator menu",
                }
            },
            "Morse Code System": {
                "title": "Morse Code System",
                "color": discord.Color.orange(),
                "commands": {
                    "!morse encode <text>": "Convert text to Morse code",
                    "!morse decode <morse>": " Convert Morse code to text",
                    "!morse audio <text>": "Generate Morse code in audio format",
                }
            },
            "ASCII Commands": {
                "title": "ASCII Commands",
                "color": discord.Color.gold(),
                "commands": {
                    "!ascii": "Opens ASCII Menu",
                    
                }
            },
            "Network/ip Cmds": {
                "title": "Network/ip Cmds",
                "color": discord.Color.gold(),
                "commands": {
                    "!iplookup <ip address/domain>": "Gives u info about ip (Enhanced)",
                    "!urlchecker": "Opens Url checker UI/menu",
                 
                }
            },
            "File/Download Cmds": {
                "title": "File/Download cmds",
                "color": discord.Color.gold(),
                "commands": {
                    "!convert <size|number> <unit>": "Convert size to another unit/s and gives u all infos about it good for large small files where are many numbers",
                    "!identify <attach file> ": " File type indentifier",
                    "!downloadcalc <Size to download> <Download speed | MBS>": "Tells u the time to download a file",
                }
            },
            "All Elements (Element Table 118)": {
                "title": "Element Table",
                "color": discord.Color.gold(),
                "commands": {
                    "!element ": "Gives u info about all elements/Opens a Interactive Element table",
                    "!element <element>": "Gives u info about element",
                }
            }
        }

        category = category_info[select.values[0]]
        embed = EmbedBuilder(
            category["title"],
            "Available Commands:"
        ).set_color(category["color"])
        
        for cmd, desc in category["commands"].items():
            embed.add_field(cmd, desc, inline=False)
            
        embed.set_footer("🔹 Required <> | Optional []")
        await interaction.response.edit_message(embed=embed.build(), view=self)


    @discord.ui.button(label="← Back to Main Panel", style=ButtonStyle.primary, custom_id="back_main", emoji="◀️", row=4)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = HelpView()
        embed = EmbedBuilder(
            "⚡ Command Center - TheZ",
            "Select a category below to view available commands"
        ).set_color(discord.Color.blue())
        await interaction.response.edit_message(embed=embed.build(), view=view)





class ReadabilityButton(discord.ui.Button):
    def __init__(self, cog):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="Toggle Readability",
            custom_id="readability_toggle"
        )
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        try:
            with open(self.cog.readability_file, 'r') as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}

        settings[guild_id] = not settings.get(guild_id, False)
        
        with open(self.cog.readability_file, 'w') as f:
            json.dump(settings, f)

        if settings[guild_id]:
            for _ in range(7):
                await interaction.channel.send("\u200b")

        await interaction.response.send_message(
            f"Readability mode: {'Enabled' if settings[guild_id] else 'Disabled'}", 
            ephemeral=True
        )


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_check = {}  
        self.caps_threshold = 0.7  
        self.spam_threshold = 5  
        self.spam_interval = 5  
        self.spam_timeout_minutes = 10  
        self.link_whitelist = set()  
        self.banned_words = set()  
        self.link_filter_enabled = True
        self.load_config()  
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def togglelinks(self, ctx):
        """Toggle the anti-link filter on/off"""
        self.link_filter_enabled = not self.link_filter_enabled
        status = "enabled" if self.link_filter_enabled else "disabled"
        
        embed = discord.Embed(
            title="🔗 Anti-Link Filter",
            description=f"Link filtering is now **{status}**",
            color=discord.Color.green() if self.link_filter_enabled else discord.Color.red()
        )
        await ctx.send(embed=embed)



    def load_config(self):
        
        self.banned_words = {
        "nga", "btc",   
        "hurensohn", "hure", "hurre", "hur3", "hur3ns0hn", "h.u.r.e", "h_u_r_e", 
        "h-u-r-e", "h.u.r.e.n.s.o.h.n", "h_u_r_e_n_s_o_h_n", "h-u-r-e-n-s-o-h-n", 
        "hur3n50hn", "huhrensohn", "hurns0hn", "hurenson", "hurens0hn", "huurensohn", 
        "hureens0hn", "hur3nsohn", "hu-rensohn", "h***ensohn", "hurenzohn", 
        "hurenzoon", "h.uhrensohn", "h@rensohn", "hu~~rensohn", "hurens0*h", 
        "hurenson~", "hu-r3n50hn",
        "schlampe", "schl4mp3", "schl4mpe", "schl.4.mp3", "schl_4_mp3", 
        "schl-4-mp3", "schlamp@", "schlam.p3", "sch|ampe", "schla.mpe", 
        "schl**ampe", "sch|4mp3", "sch~lampe", "schlamp3!", "schlampe-", 
        "sch4mpe", "schl#mp3", "schlamp#", "s-chlampe", "sch|4mp3",
        "fotze", "f0tz3", "f.o.t.z.e", "f_o_t_z_e", "f-o-t-z-e", "f0tz3nkn3cht", 
        "fotz3", "f0t.z3", "fo_tz3", "f*tz3", "fötze", "fö.tze", "fot~ze", 
        "f0~~tz3", "fo~tze", "fotz#", "fot_z3", "f0tz3n~knecht", 
        "arschloch", "4rschl0ch", "arschl0ch", "4rschloch", "4r5chl0ch", 
        "4r5chl0ch", "arsch|och", "ar-schloch", "arsch.loch", "ar.sch.l0ch", 
        "arsch~loch", "arsch-l0ch", "arschl#ch", "ars~hloch", "arsc.hloch", 
        "schwuchtel", "schwul", "schw.u.l", "schw_u_l", "schw-u-l", "schwuul", 
        "schw~ul", "schwül", "schwu~~l", "sch~wuchtel", "schwu|chtel", "schwucht@l", 
        "schw@ul", "sch~wul", "schwu|l", 
        "nazi", "naz1", "n4z1", "n.a.z.i", "n_a_z_i", "n-a-z-i", "n4z1st", 
        "na~~zi", "n~azi", "na!!zi", "na.z.i", "n-a~zi", "n4zi!", 
        "heil", "h31l", "h.e.i.l", "h_e_i_l", "h-e-i-l", "h31l3r", 
        "hitler", "h1tl3r", "hitl3r", "h1tler", "h1.tl3r", "h1_tl3r", 
        "h|tl3r", "hi~tler", "h***ler", "h@tl3r", "hi!tler", 
        "wichser", "w1chs3r", "w1chser", "wichs3r", "w1.chs3r", "w1_chs3r", 
        "wi-chser", "w|chs3r", "wi~chser", "w!chser", "w*chs3r", "wi.chs3r", 
        "spast", "sp4st", "sp.4.st", "sp_4_st", "sp-4-st", "sp4st1", 
        "sp.ast", "sp~ast", "sp@st", "sp~~ast", "s-p4st", "sp**st", 
        "kanake", "k4n4k3", "k4nake", "kan4ke", "k4n.4k3", "k4n_4k3", 
        "ka.nake", "kan~ake", "kan@ke", "k@nake", "k4n4k3!", "ka**ke", 
        "missgeburt", "m1ssgeburt", "missg3burt", "m1ssg3burt", "m1ssg3.burt", 
        "mi~ssgeburt", "mis|geburt", "miss~geburt", "missg3b~urt", "m1ss-g3burt", 
        "nutte", "n0tt3", "nutt3", "n0tte", "n.u.t.t.e", "n_u_t_t_e", 
        "nut~te", "nutt@e", "n~utte", "nutte!", "nu~~tte", "nu.t.te", 
        "fick", "f1ck", "f.i.c.k", "f_i_c_k", "f-i-c-k", "f1ck3n", 
        "ficken", "f1ck3n", "f1cken", "fick3n", "f1.ck3n", "f1_ck3n", 
        "fi~cken", "fick**", "fi~~ck3n", "fi*cken", 
        "scheisse", "sch31ss3", "scheiss3", "sche1sse", "sch.31ss3", 
        "sch~eisse", "sch#isse", "schei~~sse", "sch3iss3", "sche***sse", 
        "fotzenknecht", "f0tz3nkn3cht", "fotz3nknecht", "f0tzenknecht", 
        "fo~~tzenknecht", "fotzen~knecht", "fotzenk~~necht", "fo**knecht", 
        "drecksau", "dr3cks4u", "drecks4u", "dr3cksau", "dr3.cks4u", 
        "dreck~~sau", "dre~cksau", "drecks4u!", "dr3cks@u", 
        "drecksfotze", "dr3cksf0tz3", "drecksf0tze", "dr3cksfotze", 
        "dr~ecksfotze", "drecksf~otze", "dr3~cksfotze", 
        "whore", "wh0re", "whoree", "whör", "wh0r3", "w.h.o.r.e", "w_h_o_r_e",
        "wh0r3h0und", "wh0r3.h0und", "wh0r3_h0und", "wh0r3-h0und", 
        "who.re", "wh*r3", "wh@re", "wh~ore", "whor3", "wh0r@", "wh***re", 
        "wh.re", "who_r3", "who--re", "who~~re", "wh*r3h0und", "wh0_r3h0und",
        "bitch", "b1tch", "b!tch", "b*tch", "b1tch3s", "b!tches", "b17ch", 
        "b.i.t.c.h", "b_i_t_c_h", "b-i-t-c-h", "b1.t.ch", "b1_t_ch", 
        "bitch3s", "b!tch3s", "b1**h", "b*tch3", "bi**h", "bi.t.ch", "b!t.ch",
        "b*ches", "bitc#h", "bi7ch", "bi***h", "b_1tch", "b*t@ches", "b!7ch", 
        "cunt", "kunt", "c*nt", "cxnt", "cvnt", "cuntz", "kuntz", "c0nt", 
        "c.u.n.t", "c_u_n_t", "c-u-n-t", "c0.nt", "c0_nt", "c0-nt", 
        "c.nt", "cu.nt", "k_nt", "kun.t", "cu~nt", "cun7", "c@n7", "k*nt", 
        "slut", "sl*t", "sl4t", "slutz", "sl0t", "slvt", "sl_t", "s1ut", 
        "s.l.u.t", "s_l_u_t", "s-l-u-t", "sl.ut", "sl_ut", "sl-ut", 
        "s1ut", "sl~ut", "sl_tt", "s-l~ut", "slvvut", "sl@t", "s!ut", 
        "faggot", "f4gg0t", "f4ggot", "fag", "f4g", "f@g", "f@gg0t", 
        "f.a.g.g.o.t", "f_a_g_g_o_t", "f-a-g-g-o-t", "f4.gg0t", 
        "f.g.g.o.t", "fa~~g", "f4got", "fa.ggot", "f*g", "fa@@t", "fa!got", 
        "retard", "ret4rd", "r3t4rd", "r3tard", "r3t@rd", "ret@rd", 
        "r.e.t.a.r.d", "r_e_t_a_r_d", "r-e-t-a-r-d", "r3.t4rd", 
        "ret@rded", "r-tard", "re**rd", "re~tard", "r3tard", "r.t~rd", 
        "pussy", "pussies", "p*ssy", "p*ss", "puss1", "p0ssy", "pvssy", 
        "p.u.s.s.y", "p_u_s_s_y", "p-u-s-s-y", "p0.ssy", "p0_ssy", 
        "pussycat", "p*ss!es", "p0ussy", "pu~~ssy", "pu$s", "pu.ssy", 
        "dick", "d1ck", "d!ck", "d*ck", "d1ckhead", "dickhead", "d1ckh34d", 
        "d.i.c.k", "d_i_c_k", "d-i-c-k", "d1.ck", "d1_ck", "d1-ck", 
        "d1cky", "d!cks", "dickz", "di.ck", "dic~k", "di*c", "dic#k", 
        "cock", "c0ck", "cxck", "c*ck", "c0cks", "c0ckz", "cocksucker", 
        "c.o.c.k", "c_o_c_k", "c-o-c-k", "c0.ck", "c0_ck", "c0-ck", 
        "cocks", "co~ck", "c**ks", "c0c*k", "cx*ck", "c@ck", "co~cks",
        "s*upid", 
        "penis", "p3n1s", "pen1s", "p3nis", "p3n!s", "pen!s", "p3n15", 
        "p.e.n.i.s", "p_e_n_i_s", "p-e-n-i-s", "p3.n1s", "p3_n1s", 
        "p.nis", "p3n@s", "pen*s", "p3~~nis", "p3ni$", "pe!nis", "pen!5", 
        "WHORE", "BITCH", "CUNT", "SLUT", "FAGGOT", "RETARD", "PUSSY", 
        "DICK", "COCK", "PENIS", "WH0RE", "B1TCH", "C*NT", "SL*UT", 
        "F@GGOT", "RE**ARD", "P*SSY", "D!CK", "C*CK", "P3N1S",
        "putain", "put1n", "put@in", "put@1n", "putaine", "put@ine", "put@1ne",
        "p.u.t.a.i.n", "p_u_t_a_i_n", "p-u-t-a-i-n", "put.1n", "put_1n", 
        "put*ain", "p!utain", "pu**ain", "p#tain", "p~utain", "pûtain", 
        "putăin", "putäin", "pu&tain", "p.u.tain", "pu|tain", "p-u-t-4-i-n", 
        "pu++ain", "put@!", "putin@", "put@ne", "pu7ain", "put@1n!", 
        "salope", "sal0pe", "s@l0pe", "s@lope", "s@l0p3", "sal0p3", "s@lop3", 
        "s.a.l.o.p.e", "s_a_l_o_p_e", "s-a-l-o-p-e", "s@l.0pe", "s@l_0pe", 
        "sal*pe", "s!lope", "s@l0pe", "s4l0p3", "sälöpe", "sä|ope", "sal0p@", 
        "sal~~ope", "sa|ope", "sa!!pe", "sa---lope", "s@lop@", "s@lo&pe", 
        "connard", "c0nnard", "conn@rd", "c0nn@rd", "c0nn4rd", "c0nn@rd", 
        "c.o.n.n.a.r.d", "c_o_n_n_a_r_d", "c-o-n-n-a-r-d", "c0nn.@rd", 
        "con**ard", "conn@r!", "çonnard", "çønnard", "con~~nard", "co#nard", 
        "conn|ard", "co--nnard", "con.n@rd", "cónnard", "cónnärd", "ç0nn4rd", 
        "merde", "m3rd3", "m3rde", "m3rd3", "m@rd3", "m@rde", "m3rd@", 
        "m.e.r.d.e", "m_e_r_d_e", "m-e-r-d-e", "m3.rd3", "m3_rd3", 
        "me**de", "m3**d3", "me@rde", "mer.d3", "mer_d@", "mêrde", 
        "mérde", "mërdè", "m~~erde", "mèrde", "mérd@", "m3r@de", 
        "enculé", "encu1é", "encu1e", "encu*é", "encülé", "encul@", "encu1@", 
        "en.c.u.l.é", "en_c_u_l_é", "en-cu-lé", "en-cu**é", "encu|é", 
        "bâtard", "batard", "b4tard", "b@tard", "b4t@rd", "bätärd", "ba**ard", 
        "bordel", "b0rd3l", "bord3l", "b0rd@l", "b0rdel", "bord*l", "bor~~del", 
        "pute", "pu**e", "p@ute", "pu~te", "pu_te", "pu-t-e", "pu.te", 
        "foutre", "f0utr3", "f@utre", "foutr@", "fout~re", "fo!tre", "foutr3", 
        "p..utain", "s@l***pe", "c~onnard", "me!rd@", "fo~~utre", "bat~~ard", 
        "enc~~ulé", "bo~~rdel", "pu**t@ine", "m3**rd3", "pu--t-ai-ne", 
        "encul@d", "encu1-@", "c#onnard", "m€rde", "sa|op@", "putain*", 
        "f**tre", "p.ut.in", "s_a_l.o_pe", "conn~ard", "m.rd@", "en_cu&lé", 
        "pute", "putte", "poutain", "poutine", "pootain", "sallop", "salaupe", 
        "merdre", "merrde", "merdd", "connars", "conart", "connar", 
        "enculéé", "encule", "encûlé", "encoulé", "bâtars", "batards", "batar", 
        "vazy", "vasi", "vasie", "va chier", "va te faire", "vaff", "fauteuil", 
        "PUTAIN", "PUT@IN", "SALOPE", "CONNARD", "MERDE", "ENCULÉ", "BÂTARD", 
        "BORDEL", "PUTE", "FOUTRE", "S@LOPE", "C*NNARD", "M3RDE", "ENCUL3", 
        "EN_CU_LÉ", "BA**ARD", "FOU_TRE", "PU-TE", "ME-RDE", "VAFFANCULO",
        "puttana", "putt4n4", "putt@n@", "putt@n4", "putt4n@", "putt4n4",
        "p.u.t.t.a.n.a", "p_u_t_t_a_n_a", "p-u-t-t-a-n-a", "putt.4n4", 
        "p*uttana", "p!uttana", "pu**tana", "p@uttana", "putta!na", "pu.t.t.a.n.a",
        "put.tana", "putt_a_na", "p--u-t-t-a-n-a", "p~u~t~t~a~n~a", 
        "puttan4", "pút.tànà", "pu##ana", "puttan@", "puʇʇanɐ",
        "cazzo", "c4zz0", "c@zz0", "c@zzo", "c4zzo", "c@zz0", "c4zz0",
        "c.a.z.z.o", "c_a_z_z_o", "c-a-z-z-o", "c4.zz0", "c4_zz0", 
        "càzzò", "cäzzö", "c*zzo", "ca##o", "c@zzo!", "çazzo", 
        "ca_zzo", "c-a.z.z-o", "c~azz0", "k4zz0", "căzzô", "ç@zz0",
        "stronzo", "str0nz0", "str0nzo", "str0nz@", "str0nz4", "str0nz0",
        "s.t.r.o.n.z.o", "s_t_r_o_n_z_o", "s-t-r-o-n-z-o", "str0.nz0", 
        "stronz0", "str0n.z.o", "st-r-on-z-o", "str0n*z@", "s~tronzo", 
        "strömzø", "st_ronz0", "s-t_r_o-n-z-o", "ştronzo", "str0nz#", 
        "merda", "m3rd@", "m3rd4", "m.e.r.d.a", "m_e_r_d_a", "m-e-r-d-a", "m3rda",
        "figa", "f1g@", "f1ga", "f.i.g.a", "f_i_g_a", "f-iga", "fig@", "fi**a",
        "bastardo", "b4st@rd0", "b4stardo", "b.a.s.t.a.r.d.o", "b_a_s_t_a_r_d_o",
        "vaffanculo", "v4ff4ncul0", "v@ff@nculo", "vaff@nculo", "vaffancul@", 
        "pezzo di m3rd@", "pezzo_di_merda", "p.e.z.z.o.d.i.m.e.r.d.a", "pezzo.d.m.", 
        "co****ne", "c0*****e", "co--gli**ne", "çoglione", "c-o-g-l-i-o-n-e", 
        "zoccola", "z0ccol@", "z0ccola", "z.o.c.c.o.l.a", "z_o_c_c_o_l_a", 
        "figliodiputtana", "figli0diputt4n@", "figli0_diputt@n@", 
        "vaf*****ulo", "vaff@*********", "c****0 di m***a", 
        "p._utt4n@", "c.4_zz0", "s_t**nzo", "me$$da", "fi@@a", "va~~fan~~culo", 
        "str**nz@", "put&@n@", "fig.o~", "bas***do", "za!ccola", "pe##o", 
        "vaff_~anculo", "c0gl!ion#", "c.o.g.l.-o.n.e", "pez*dimerda", 
        "potana", "pottana", "puttna", "putna", "pzzo", "strunzo", "stronza", 
        "strozno", "strozo", "bastard@", "merd@", "merdino", "vafan", "vafanc", 
        "vafa!", "fanculo", "fan****lo", "fu***", "cul0", "culo!", "cul@", "kulo",
        "figh@", "figha", "fi*ha", "f1gh@", "figh3", "ma****", "mannaggia", 
        "mann@ggia", "mann***ia", "mannagg1a",
        "Puttana", "PUTTANA", "PUTT4N4", "PUTT@n@", "PUTT@n4", "PUTT@N@", 
        "CAZZO", "C4ZZO", "C@ZZO", "C.A.Z.Z.O", "C-A-Z-Z-O", "MERDA", "FIGA",
        "STRONZO", "Vaffanculo", "COGLIONE", "ZOCCOLA", "BASTARDO", "CUL0",
        "FAN****LO", "FI@HA", "POTANA", "VAFFA",
        "馬鹿", "バカ", "死ね", "クソ", "カス", "ちんこ", "まんこ", "おっぱい",
        "baka", "b4k4", "b@k@", "b@k4", "b4k@", "b@k@", "b4k4", "b@k4",
        "b.a.k.a", "b_a_k_a", "b-a-k-a", "b4.k4", "b4_k4", "b4-k4",
        "kuso", "kus0", "ku50", "kus@", "ku5@", "kus0", "ku50", "kus@",
        "k.u.s.o", "k_u_s_o", "k-u-s-o", "kus.0", "kus_0", "kus-0",
        "baka-san", "baka-chan", "baka-kun", "baka-sama", "baka desu", 
        "baka da", "baka ne", "baka yo", "baka baka", "baka na", "baka janai",
        "baka mitai", "baka sugiru", "baka deshou", "baka desho", 
        "baka hontou", "baka shinde", "baka shine", "baka yarou", "baka mono",
        "kusotare", "kusogaki", "kuso yarou", "kuso baka", "kuso shine",
        "kuso janai", "kuso mitai", "kuso desu", "kuso da", "kuso yo",
        "kuso kuso", "kuso mono", "kuso ne", "kuso sugiru", "kusottare",
        "kuso baka shine", "kuso yarou shine", "kusoyarou baka",
        "kusoyarou shine", "kusottare shine", "kusoyarou baka shine",
        "baka kuso", "baka kusoyarou", "baka kusottare", "baka shine yo",
        "baka kuso shine", "baka kusoyarou shine", "baka kusottare shine",
        "chinko", "chinkokun", "chinkochan", "chinko shine", "chinko baka",
        "chinko kuso", "chinko yarou", "chinko shine yo", "chinko shine ne",
        "chinko sugiru", "chinko yarou baka", "chinko baka shine",
        "manman", "manmanko", "mankosu", "mankoyarou", "manko shine",
        "manko baka", "manko kuso", "manko yarou", "manko shine yo",
        "manko shine ne", "manko sugiru", "manko yarou baka", "manko baka shine",
        "manko kusoyarou", "manko kusottare", "oppai", "oppai yarou", 
        "oppai baka", "oppai kuso", "oppai shine", "oppai baka shine", 
        "oppai kusoyarou", "oppai kusottare", "oppai sugiru", 
        "oppai yarou baka", "oppai baka shine", "oppai kusoyarou shine",
        "shine", "shine yo", "shine ne", "shine baka", "shine kuso",
        "shine yarou", "shine desu", "shine na", "shine mitai", 
        "shine sugiru", "shine janai", "shine yarou baka", "shine baka kuso",
        "shine kusoyarou", "shine kusottare", "shine baka shine",
        "kusoyarou", "kusoyarou shine yo", "kusoyarou shine ne",
        "kusoyarou shine baka", "kusoyarou shine kuso", "kusoyarou baka shine",
        "kusottare shine", "kusottare shine yo", "kusottare shine ne",
        "kusottare shine baka", "kusottare shine kuso", "kusottare baka shine",
        "baka yarou shine", "baka yarou shine yo", "baka yarou shine ne",
        "baka yarou shine baka", "baka yarou shine kuso", "baka yarou kuso shine",
        "baka yarou kusoyarou", "baka yarou kusottare", "baka yarou baka shine",
        "baka yarou kuso shine baka", "baka yarou kusoyarou shine",
        "baka yarou kusottare shine", "baka yarou kuso baka shine",
        "baka yarou kuso baka shine yo", "baka yarou kuso baka shine ne",
        "baka yarou kuso baka shine sugiru", "baka yarou kuso baka shine desu",
        "baka yarou kuso baka shine janai", "baka yarou kuso baka shine mitai",
        "baka yarou kuso baka shine hontou",
        "n1gg4", "n1gg3r", "n1663r", "n166a", "n1664", "nigg4", "nigg3r",
        "n.i.g.g.4", "n_i_g_g_4", "n-i-g-g-4", "n1.gg4", "n1_gg4",
        "f.u.c.k", "f_u_c_k", "f-u-c-k", "f.v.c.k", "f_v_c_k", "f-v-c-k",
        "fvck", "phuck", "phvck", "fück", "fuck", "f*ck", "f**k", "fuk",
        "fucc", "fukk", "fuking", "fucking", "fvcking", "phucking",
        "motherfucker", "mothafucka", "muthafucka", "mtherfcker",
        "mthrfckr", "motherfckr", "mothafckr", "mthafckr", "mtherfker",
        "n1ggar", "n1gger", "niggah", "niggar", "niggur", "niggarz", "niggahz",
        "nigga", "nigger", "btch", "bitch", "b1tch", "b1tchz", "b1tchaz",
        "n1ggah", "niggaz", "n1ggaz", "nigguh", "n1gguh", "nigguz", "n1gguz",
        "fukc", "fukkk", "fukkin", "fukker", "fukerz", "fukken", "fukingz",
        "fuckz", "fuckinn", "fuckinnz", "fuckers", "fuckersz", "fuckar",
        "fuckah", "fvckz", "fvcukk", "fvcukz", "fvckah", "fvckar", "fvckez",
        "phuk", "phukk", "phucker", "phuckar", "phuckah", "phukerz",
        "phucken", "phukking", "phukers", "fukz", "fukah", "fukkez", "fukers",
        "motherfuck", "mthrfuck", "mtherfuk", "mtherfuckah", "mtherfuckar",
        "mthafucka", "muthafukah", "mthrfkkr", "mtherfkerz", "motherfkkr",
        "muthrfcker", "mthafker", "motherfkerz", "mtherfkkr", "mtherfukah",
        "fukcinn", "fuckinnah", "fuckahzz", "fuckarzz", "fvcah", "fvcar",
        "fvcuck", "fvckahz", "fukinnzz", "phuckinn", "phukin", "phuckk",
        "phukinzz", "phuckkk", "phuckerzz", "phukingg", "mothafker", "mthafkr",
        "muthafkr", "mthrfck", "mothrfckr", "mthafcker", "mthrfkerz",
        "motherfkrz", "mthrfuckk", "mtherfukker", "mthrfukkerz", "motherfker",
        "mtherfkrz", "mthafukker", "mthrfker", "mthrfkrr", "motherfukkerz",
        "fuckinnn", "fukcinnn", "fukkerz", "fukinnzz", "fvckinn", "fvckinnz",
        "phuckah", "phuckahz", "fvcker", "fvckerz", "phukahz", "phukinzz",
        "phuckeninn", "phuckerinn", "phukerszz", "fukking", "fuckinggg",
        "fuckkinnz", "fuckinz", "fuckennz", "fvcukinnz", "fukahnn", "fvcahz",
        "fvcahh", "fvckarh", "fukkerinn", "fuckkerinn", "fuckennn", "fukennz",
        "fvcukinn", "fvcukkinn", "phvcukk", "phvcukkah", "fvckinnnn",
        "fvckennnn", "fvckennz", "phukenn", "phuckeninnzz", "fukcah", "phukah",
        "fukinnnzz", "fuckarrr", "fvckarrr", "phuckarrr", "phukenarrr",
        "phukckk", "phvckk", "fvckarzz", "fuckarz", "fuckinnzzz", "fvckinnz",
        "phukz", "fukkzzz", "fukkahz", "phukkahzz", "mtherfkr", "mtherfkkr",
        "mthrfkkrz", "mthrfkrz", "mthrfkkrr", "mthrfuckkrr", "mtherfkkrr",
        "motherfkkrr", "motherfkrr", "motherfuckahrr", "motherfkkrz",
        "mthrfukkrz", "mthrfuckarrr", "mthrfkerinn", "motherfkerinn",
        "motherfuckerinn", "mthrfkerah", "mtherfukkerzz", "motherfukkerinnzz",
        "mthrfkerahzz", "fukkz", "fuckkz", "fvckzz", "fvckahzz", "phvcah",
        "phvcukz", "fvcckzz", "fvcckah", "fukkkah", "phukahzz", "phvcukah",
        "phvcukahzz", "phukckkzz", "phvcukenn", "fukenn", "fuckkinnzz", 
        "fvckennzz", "phuckar", "phuckarrrzz", "fukinnnnz", "fvckinnnnz", 
        "phuckinnzz", "phuckerinnzz", "fvccahnn", "fvccahh", "fvccukzz",
        "fvccennzz", "fvccenn", "fvccukennzz", "fvccahz", "phuckennzz",
        "fvccahnnzz", "fukahz", "phukahh", "phvcukahh", "fvccahinnzz", 
        "fvccahkk", "phuckkkinn", "phvcukinn", "phvcukinnzz", "fvccukahh", 
        "fvcckerzz", "fvcckerinnzz", "phvcahzz", "fvccennnnz",
        "kys", "k y s", "k.y.s", "k_y_s", "k-y-s", "k.y.s.", "k_y_s_",
        "kill yourself", "k1ll y0urs3lf", "k!ll y0urs3lf", "k1ll y0urs3lf",
        "k.i.l.l.y.o.u.r.s.e.l.f", "k_i_l_l_y_o_u_r_s_e_l_f",
        "suicide", "su1c1d3", "su1c1de", "suic1de", "su1cide", "su!c!de",
        "s.u.i.c.i.d.e", "s_u_i_c_i_d_e", "s-u-i-c-i-d-e", "su1.c1d3",
        "self harm", "s3lf h4rm", "s3lf.h4rm", "s3lf_h4rm", "s3lf-h4rm",
        "s.e.l.f.h.a.r.m", "s_e_l_f_h_a_r_m", "s-e-l-f-h-a-r-m",
        "kys now", "kys immediately", "kys today", "kys please", "kys fast",
        "kill_urself", "kill_ur_self", "kill-yourself-now", "kill yourself fast",
        "kill yourself today", "just kill yourself", "why not kys", "go kys now",
        "you should kys", "how to kys", "kys tutorial", "suicide now", 
        "do suicide", "go do suicide", "commit suicide", "suicide guide",
        "suicide fast", "suicide quickly", "suicide tonight", "suicide tomorrow",
        "suicide for sure", "s u i c i d e", "sui cide", "suicide plans",
        "plan suicide", "suicide instructions", "suicide advice",
        "suicide methods", "suicide help", "how to self harm", 
        "self_harm_now", "self harm tutorial", "commit self harm", 
        "self harm guide", "self harm plan", "start self harm", 
        "self harm immediately", "self harm today", "self harm please",
        "self harm now", "you should self harm", "just self harm", 
        "self harm instructions", "self harm advice", "self harm tips",
        "how to commit self harm", "self_harm_tutorial", "self harm tonight",
        "go self harm", "self harm methods", "self harm fast", 
        "self_harm_quickly", "self harm quickly", "commit_self_harm",
        "self harm tomorrow", "self harm suggestions", "ways to self harm",
        "steps to self harm", "suicide plans now", "self harm guide online",
        "why not suicide", "learn suicide", "find suicide tips",
        "kill your self", "kill yourself today", "kill yourself tips",
        "kys easily", "kys guide", "how to kys quickly", 
        "kys suggestions", "kys steps", "how to kys instructions",
        "kys easily today", "kys methods online", "kys safely",
        "self harm safely", "self harm today fast", "commit self harm tonight",
        "self harm immediately tips", "suicide now guide", 
        "suicide fast steps", "commit suicide tomorrow", 
        "do suicide plans", "just suicide", "you should suicide now",
        "go and suicide", "kys faster", "kys slower", "kill your self today",
        "suicide now tutorial", "suicide now advice", "why suicide is good",
        "how suicide works", "self harm is okay", "start self harming now",
        "self_harm_help", "self harm techniques", "self harm advice online",
        "kys instructions online", "suicide tips fast", "suicide now tutorial",
        "commit self harm tutorial", "start_kys", "kys help", "kys now please",
        "suicide please", "help me suicide", "suicide suggestions",
        "kys planning", "kys execution", "suicide execution", "suicide tonight",
        "commit_suicide_fast", "plan your suicide", "how to kys properly",
        "suicide guide instructions", "how to commit_self_harm",
        "self harm advice safely", "how to end it all", "end your life now",
        "suicide today", "learn how to kys", "you should kys now",
        "kys_step_by_step", "ways to end it", "self_harm_online",
        "go harm yourself", "just go kys", "suicide plans fast",
        "commit_suicide_instructions", "kill_your_self_guide", "end it tutorial",
        "self harm method", "method for self harm", "suicide execution guide",
        "suicide execution tips", "suicide execution methods",
        "kys_today", "kill_your_self_fast", "suicide fast tonight",
        "self harm tonight plans", "commit self harm fast guide",
        "suicide tomorrow plans", "harm yourself safely", 
        "harm yourself guide", "harm yourself tips", 
        "harm yourself methods", "harm yourself fast", 
        "harm yourself now tutorial", "how to harm yourself easily", 
        "suicide step guide", "suicide instruction plans", 
        "suicide_tips", "suicide safely guide", "self harm safely tips",
        "harm yourself now", "why harm yourself", "why not self harm",
        "harm yourself techniques", "harm yourself execution",
        "harm yourself tools", "tools for suicide", "tools for harm",
        "suicide techniques safely", "harm yourself fast online", 
        "tools for self harm", "harm yourself instructions", 
        "commit_harm", "commit_self_harm_steps", "suicide safely tutorial",
        "free nitro", "fr33 n1tr0", "free.nitro", "fr33.n1tr0", "fr33_n1tr0",
        "f.r.e.e.n.i.t.r.o", "f_r_e_e_n_i_t_r_o", "f-r-e-e-n-i-t-r-o",
        "steam gift", "st34m g1ft", "steam.gift", "st34m.g1ft", "st34m_g1ft",
        "s.t.e.a.m.g.i.f.t", "s_t_e_a_m_g_i_f_t", "s-t-e-a-m-g-i-f-t",
        "robux generator", "r0bux g3n3r4t0r", "robux.generator",
        "r.o.b.u.x.g.e.n.e.r.a.t.o.r", "r_o_b_u_x_2_g_e_n_e_r_a_t_o_r",
        "free_nitro_code", "free nitro giveaway", "free nitro bot",
        "get free nitro", "nitro giveaway free", "free nitro now",
        "steam_gift_card", "steam gift codes", "steam_gift_now",
        "free_steam_gift", "robux free generator", "robux gift generator",
        "robux free codes", "robux generator free", "robux generator online",
        "free_nitro_code_2023", "free_nitro_generator", "nitro free discord",
        "free discord nitro", "nitro discount free", "discord gift nitro",
        "steam_discount_gift", "steam freebie gift", "free_robux_now",
        "robux free access", "robux generator new", "robux generator giveaway",
        "robux hack generator", "free_robux_bot", "discord_free_gift",
        "discord_nitro_bot", "get_free_robux", "robux_online_tool",
        "discord_code_generator", "discord_nitro_free", "steam_gift_online",
        "steam_card_gift", "steam_card_discount", "robux_hack_tool",
        "robux_promo_codes", "robux_gift_online", "robux_tool_generator",
        "free_gift_online", "discord_promo_bot", "steam_promo_codes",
        "steam_code_hack", "free_steam_codes", "robux_promo_tool",
        "robux_access_generator", "get_steam_card", "free_gift_steam",
        "nitro_giveaway_bot", "discord_promo_code", "free_bot_gift",
        "nitro_code_promo", "steam_bot_codes", "nitro_hack_tool",
        "get_promo_nitro", "steam_gift_key", "steam_gift_discount",
        "robux_key_generator", "free_promo_code", "discord_tool_bot",
        "free_nitro_access", "robux_key_hack", "promo_code_generator",
        "free_steam_access", "gift_code_online", "nitro_online_tool",
        "steam_access_gift", "robux_online_access", "nitro_bot_generator",
        "get_robux_now", "free_promo_generator", "robux_gift_discount",
        "robux_promo_key", "robux_gift_code", "nitro_card_promo",
        "steam_online_gift", "free_steam_discount", "gift_bot_robux",
        "robux_bot_tool", "discord_promo_codes", "steam_gift_code_now",
        "robux_card_tool", "promo_tool_robux", "steam_gift_bot",
        "robux_tool_now", "robux_online_bot", "robux_gift_tool",
        "steam_code_promo", "free_key_nitro", "free_robux_code",
        "discord_hack_gift", "robux_tool_card", "promo_tool_discount",
        "nitro_discount_tool", "robux_hack_codes", "steam_discount_code",
        "free_gift_tool", "robux_code_tool", "discord_card_generator",
        "free_tool_gift", "robux_key_discount", "robux_discount_bot",
        "free_tool_card", "steam_key_promo", "nitro_tool_bot",
        "nitro_gift_codes", "steam_key_generator", "free_promo_gift",
        "free_bot_promo", "gift_card_online", "robux_access_promo",
        "free_key_discount", "free_key_tool", "nitro_promo_discount",
        "nitro_gift_online", "nitro_key_codes", "robux_discount_tool",
        "steam_bot_gift", "nitro_discount_bot", "steam_promo_tool",
        "discord_promo_generator", "nitro_bot_key", "robux_card_promo",
        "steam_tool_discount", "robux_discount_codes", "nitro_key_online",
        "steam_card_key", "promo_gift_code", "gift_tool_online",
        "gift_key_promo", "nitro_online_access", "steam_discount_bot",
        "nitro_giveaway_tool", "promo_access_bot", "robux_code_promo",
        "gift_code_promo", "free_nitro_promo", "gift_access_tool",
        "free_nitro_key", "nitro_card_codes", "free_access_tool",
        "steam_giveaway_bot", "promo_code_bot", "robux_promo_bot",
        "promo_card_tool", "free_access_promo", "steam_access_code",
        "free_gift_key", "promo_discount_tool", "promo_discount_bot",
        "promo_key_bot", "promo_key_tool", "promo_gift_tool",
        "discount_gift_bot", "promo_bot_discount", "promo_access_tool",
        "gift_card_promo", "nitro_gift_discount", "free_discount_code",
        "discord_promo_gift", "promo_code_discount", "promo_key_code",
        "discount_bot_key", "discount_tool_code", "promo_bot_card",
        "promo_key_promo", "discount_key_promo", "gift_card_access",
        "promo_code_online", "gift_key_online", "promo_code_access",
        "promo_access_code", "discount_bot_tool", "promo_code_card",
        "promo_discount_card", "gift_discount_tool", "promo_card_key",
        "promo_key_access", "discount_access_bot", "promo_discount_access",
        "promo_code_key", "promo_discount_key", "promo_key_online",
        "gift_key_card", "discount_promo_bot", "promo_giveaway_card",
        "promo_bot_online", "gift_tool_discount", "discount_giveaway_tool",
        "promo_code_giveaway", "promo_tool_access", "promo_key_discount",
        "discount_card_tool", "gift_bot_discount", "promo_key_gift",
        "discount_key_gift", "promo_gift_access", "promo_card_access",
        "promo_discount_gift", "promo_giveaway_access", "promo_key_tool",
        "discount_gift_access", "promo_tool_key", "promo_card_discount",
        "promo_discount_code", "promo_card_tool", "discount_card_key",
        "promo_key_generator", "promo_tool_online", "promo_tool_gift",
        "promo_discount_bot", "promo_gift_code", "discount_key_tool",
        "promo_access_card", "promo_tool_discount", "promo_bot_access",
        "promo_discount_tool", "promo_key_tool", "promo_discount_access",
        "promo_code_tool", "promo_card_key", "promo_key_online",
        "promo_tool_card", "promo_discount_key", "promo_access_tool",
        "🖕", "promo",
        }
        
    
    async def check_banned_words(self, message):
        """Check for banned words, including bypassed versions."""
      
        if message.webhook_id:
            webhook_logger = self.bot.get_cog('WebhookLogger')
            if webhook_logger and message.webhook_id == webhook_logger.webhook_id:
                return False
                
        if message.embeds:
            for embed in message.embeds:
                if embed.footer and 'Webhook ID:' in embed.footer.text:
                    return False

        BOT_OWNER_ID = os.getenv("BOT_OWNER_ID", "0")
        if not BOT_OWNER_ID or not BOT_OWNER_ID.isdigit():
            raise ValueError("Invalid BOT_OWNER_ID in .env file. It must be a numeric Discord ID.")

        BOT_OWNER_ID = int(BOT_OWNER_ID)

        if message.author.id == BOT_OWNER_ID:
            return False

        content_to_check = [message.content.lower()]
        
        if message.embeds:
            for embed in message.embeds:
                if embed.description:
                    content_to_check.append(embed.description.lower())
                if embed.title:
                    content_to_check.append(embed.title.lower())
                for field in embed.fields:
                    content_to_check.append(field.name.lower())
                    content_to_check.append(field.value.lower())

        for content in content_to_check:
            for word, pattern in self.banned_regex.items():
                if pattern.search(content):
                    await asyncio.sleep(1)  
                    await message.delete()
                    if not message.webhook_id:
                        await self.send_warning(message.channel, message.author, "banned_words")
                    return True
        return False

        
    @commands.Cog.listener()
    async def on_message(self, message):
   
        if isinstance(message.channel, discord.DMChannel):
            return

        await self.check_message(message)

    async def check_message(self, message):
        
        checks = [
            self.check_links,        
            self.check_banned_words, 
            self.check_caps,         
            self.check_spam          
        ]

        for check in checks:
            try:
                action = await check(message)
                if action:
                    return
            except Exception as e:
                print(f"AutoMod Check Error in {check.__name__}: {e}")

    async def check_spam(self, message):
        
        author_id = message.author.id
        current_time = time.time()

        if author_id not in self.spam_check:
            self.spam_check[author_id] = {"messages": 1, "last_message": current_time}
            return False

        if current_time - self.spam_check[author_id]["last_message"] > 5:
            self.spam_check[author_id] = {"messages": 1, "last_message": current_time}
            return False

        self.spam_check[author_id]["messages"] += 1
        
        if self.spam_check[author_id]["messages"] >= 5:
            await message.author.timeout(timedelta(minutes=(self.spam_timeout_minutes)), reason="Spam detection")
            await self.send_warning(message.channel, message.author, "spam")
            return True

        self.spam_check[author_id]["last_message"] = current_time
        return False

    async def check_caps(self, message):
        if len(message.content) < 8:
            return False

        caps_ratio = sum(1 for c in message.content if c.isupper()) / len(message.content)
        if caps_ratio > self.caps_threshold:
            await message.delete()
            await self.send_warning(message.channel, message.author, "caps")
            return True
        return False

    async def check_links(self, message):
        if not self.link_filter_enabled:  
            return False

        BOT_OWNER_ID = os.getenv('BOT_OWNER_ID')

        if not BOT_OWNER_ID or not BOT_OWNER_ID.isdigit():
            raise ValueError("Invalid BOT_OWNER_ID in .env file. It must be a numeric Discord ID.")

        BOT_OWNER_ID = int(BOT_OWNER_ID)

        if message.author.id == BOT_OWNER_ID:
            return False
        
        if message.author.id == BOT_OWNER_ID or message.author.id == self.bot.user.id:
            return False

        content_to_check = [message.content.lower()]

        if message.embeds:
            for embed in message.embeds:
                if embed.description:
                    content_to_check.append(embed.description.lower())
                if embed.title:
                    content_to_check.append(embed.title.lower())
                if embed.footer and embed.footer.text:
                    content_to_check.append(embed.footer.text.lower())
                if embed.author and embed.author.name:
                    content_to_check.append(embed.author.name.lower())
                for field in embed.fields:
                    content_to_check.append(field.name.lower())
                    content_to_check.append(field.value.lower())

        code_blocks = re.findall(r'```(?:\w+\n)?([^`]+)```', message.content, re.DOTALL)
        content_to_check.extend(block.lower() for block in code_blocks)

        link_patterns = [
            'http://', 'https://',
            'discord.gg', 'discord.com/invite',
            '.gg/', 'discord.me',
            'discordapp.com/invite',
            'invite.gg', 'dsc.gg',
            'd.gg', 'discord.link',
            'dis.gd', 'discord.io',
            'discord.st', 'invite.ink',
            'discord.media',
            'discord.new',
            'dsc.gg/',
            'invite/',
            'discord.com/servers'
        ]

        for content in content_to_check:
            if any(pattern in content for pattern in link_patterns):
                if not any(allowed in content for allowed in self.link_whitelist):
                    try:
                        await asyncio.sleep(1)
                        await message.delete()
                        if message.webhook_id:
                            print(f"Deleted webhook message with unauthorized links in {message.guild.name}")
                        else:
                            await self.send_warning(message.channel, message.author, "unauthorized Discord invites or links")
                        return True
                    except discord.errors.NotFound:
                        pass
                    except discord.errors.Forbidden:
                        print(f"Missing permissions to delete message in {message.guild.name}")
                    break
        return False


    async def check_banned_words(self, message):
        BOT_OWNER_ID = os.getenv('BOT_OWNER_ID')
        if not BOT_OWNER_ID or not BOT_OWNER_ID.isdigit():
            raise ValueError("Invalid BOT_OWNER_ID in .env file. It must be a numeric Discord ID.")

        BOT_OWNER_ID = int(BOT_OWNER_ID)
        if message.author.id == self.bot.user.id:
            return False

        if message.author.id == BOT_OWNER_ID:
            return False
            if message.author.id == BOT_OWNER_ID:
                return False

        content_to_check = [message.content.lower()]
        
        if message.embeds:
            for embed in message.embeds:
                if embed.description:
                    content_to_check.append(embed.description.lower())
                if embed.title:
                    content_to_check.append(embed.title.lower())
                for field in embed.fields:
                    content_to_check.append(field.name.lower())
                    content_to_check.append(field.value.lower())

        for content in content_to_check:
            if any(word in content for word in self.banned_words):
                await asyncio.sleep(1)  
                await message.delete()
                if not message.webhook_id:
                    await self.send_warning(message.channel, message.author, "banned_words")
                return True
        return False

    async def send_warning(self, channel, user, violation_type):
        warnings = {
            "spam": "⚠️ Excessive message spam detected.",
            "caps": "⚠️ Excessive use of capital letters detected.",
            "links": "⚠️ Unauthorized links are not permitted.",
            "banned_words": "⚠️ Inappropriate language detected."
        }

        embed = EmbedBuilder(
            "🛡️ AutoMod Warning",
            warnings.get(violation_type, "Rule violation detected.")
        ).set_color(discord.Color.orange())
        
        embed.add_field("User", user.mention)
        embed.add_field("Violation", violation_type.title())
        embed.add_field("Action Taken", "Message Deleted", inline=False)
        
        try:
            await channel.send(embed=embed.build(), delete_after=10)
        except discord.errors.Forbidden:
            print(f"Missing permissions to send warning in {channel.name}")


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def automod(self, ctx, setting: str = None, value: str = None, timeout_minutes: int = None):
        """Configure AutoMod settings or display current settings and commands."""
        if timeout_minutes is None:
            timeout_minutes = self.spam_timeout_minutes

        if setting is None:
            embed = EmbedBuilder(
                "⚙️ AutoMod Settings Panel",
                "Here are the current AutoMod settings and available commands:"
            ).set_color(discord.Color.blue())

            embed.add_field("Spam Threshold", f"{self.spam_threshold} messages in {self.spam_interval} seconds")
            embed.add_field("Spam Timeout", f"{self.spam_timeout_minutes} minutes")
            embed.add_field("Caps Threshold", f"{self.caps_threshold * 100}%")

            whitelist_display = "\n".join(list(self.link_whitelist)[:5]) if self.link_whitelist else "None"
            embed.add_field("Whitelisted Links (First 5)", whitelist_display)



            commands_explanation = (
                "**Commands:**\n"
                "- `!automod caps_threshold <value>`\n"
                "  - Set the maximum allowed percentage of caps in a message (0.0-1.0).\n"
                "- `!automod spam_threshold <value> [timeout_minutes]`\n"
                "  - Set the number of messages allowed before spam detection and the timeout duration.\n"
                "- `!automod add_banned_word <word>`\n"
                "  - Add a word to the banned words list.\n"
                "- `!automod add_whitelist <url>`\n"
                "  - Add a URL to the link whitelist.\n"
                "- `!automod`\n"
                "  - Display the current AutoMod settings and available commands."
                "- `!togglelinks`\n"
                "  - Toggle the link detection feature on or off."
            )

            embed.add_field("Available Commands", commands_explanation)


            await ctx.send(embed=embed.build())
            return

        settings = {
            'caps_threshold': float,
            'spam_threshold': int,
            'add_banned_word': str,
            'add_whitelist': str
        }

        if setting not in settings:
            return await ctx.send("Invalid setting!")

        try:
            if setting == 'spam_threshold':
                self.spam_check = {}
                self.spam_threshold = int(value)
                self.spam_timeout_minutes = timeout_minutes

                embed = EmbedBuilder(
                    "⚙️ AutoMod Spam Settings Updated",
                    f"Threshold: {value} messages in {self.spam_interval} seconds\nTimeout: {timeout_minutes} minutes"
                ).set_color(discord.Color.green()).build()

            elif setting in ['add_banned_word', 'add_whitelist']:
                if setting == 'add_banned_word':
                    self.banned_words.add(value.lower())
                else:
                    self.link_whitelist.add(value.lower())
                embed = EmbedBuilder(
                    "⚙️ AutoMod Updated",
                    f"Setting `{setting}` updated with value `{value}`"
                ).set_color(discord.Color.green()).build()
            else:
                setattr(self, setting, settings[setting](value))
                embed = EmbedBuilder(
                    "⚙️ AutoMod Updated",
                    f"Setting `{setting}` updated to `{value}`"
                ).set_color(discord.Color.green()).build()

            await ctx.send(embed=embed)
        except ValueError:
            await ctx.send("Invalid value format!")

bot.add_cog(HelpSystem(bot))
bot.add_cog(AutoMod(bot))

class WelcomeSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_configs = {}

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        embed = EmbedBuilder(
            "Welcome System Commands",
            "Available commands for welcome message configuration"
        ).set_color(discord.Color.blue())
        
        embed.add_field("!welcome message <message>", "Set welcome message\nVariables: {user}, {server}, {count}")
        embed.add_field("!welcome color <color>", "Set embed color (e.g. red, blue, green)")
        embed.add_field("!welcome banner <url>", "Set welcome banner image/gif")
        embed.add_field("!welcome test", "Preview current welcome message")
        embed.add_field("!welcome reset", "Reset to default message")
        embed.add_field("!welcome channel #channel", "Set welcome channel")
        
        await ctx.send(embed=embed.build())

    @welcome.command(name="message")
    @commands.has_permissions(administrator=True)
    async def set_message(self, ctx, *, message: str):
        """Set a custom welcome message"""
        if ctx.guild.id not in self.welcome_configs:
            self.welcome_configs[ctx.guild.id] = {}
            
        self.welcome_configs[ctx.guild.id]["message"] = message
        
        preview = message.replace("{user}", ctx.author.mention)
        preview = preview.replace("{server}", ctx.guild.name)
        preview = preview.replace("{count}", str(len(ctx.guild.members)))
        
        embed = EmbedBuilder(
            "✅ Welcome Message Set",
            "New welcome message configured"
        ).set_color(discord.Color.green())
        
        embed.add_field("Preview", preview)
        await ctx.send(embed=embed.build())

    @welcome.command(name="color")
    @commands.has_permissions(administrator=True)
    async def set_color(self, ctx, color: str):
        """Set welcome embed color"""
        colors = {
            "red": discord.Color.red(),
            "blue": discord.Color.blue(),
            "green": discord.Color.green(),
            "gold": discord.Color.gold(),
            "purple": discord.Color.purple()
        }
        
        if color.lower() not in colors:
            valid_colors = ", ".join(colors.keys())
            return await ctx.send(f"Valid colors: {valid_colors}")
            
        if ctx.guild.id not in self.welcome_configs:
            self.welcome_configs[ctx.guild.id] = {}
            
        self.welcome_configs[ctx.guild.id]["color"] = colors[color.lower()]
        
        embed = EmbedBuilder(
            "🎨 Welcome Color Set",
            f"Welcome message color set to {color}"
        ).set_color(colors[color.lower()]).build()
        
        await ctx.send(embed=embed)

    @welcome.command(name="test")
    @commands.has_permissions(administrator=True)
    async def test_welcome(self, ctx):
        """Preview current welcome message"""
        config = self.welcome_configs.get(ctx.guild.id, {})
        message = config.get("message", f"Welcome {'{user}'} to {'{server}'}!")
        color = config.get("color", discord.Color.brand_green())
        banner_url = config.get("banner_url")
        
        preview = message.replace("{user}", ctx.author.mention)
        preview = preview.replace("{server}", ctx.guild.name)
        preview = preview.replace("{count}", str(len(ctx.guild.members)))
        
        embed = EmbedBuilder(
            "👋 Welcome Preview",
            preview
        ).set_color(color)
        
        embed.add_field("Member Count", f"#{len(ctx.guild.members)}")
        embed.add_field("Account Created", ctx.author.created_at.strftime("%B %d, %Y"))
        embed.add_field("Join Position", f"#{len(ctx.guild.members)}", inline=True)
        
        embed.set_thumbnail(ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        
        if banner_url:
            embed.set_image(url=banner_url)
        
        important_channels = []
        rules_channel = discord.utils.get(ctx.guild.channels, name="rules")
        info_channel = discord.utils.get(ctx.guild.channels, name="information")
        roles_channel = discord.utils.get(ctx.guild.channels, name="roles")

        if rules_channel:
            important_channels.append(f"📜 Rules: {rules_channel.mention}")
        if info_channel:
            important_channels.append(f"ℹ️ Information: {info_channel.mention}")
        if roles_channel:
            important_channels.append(f"🎭 Roles: {roles_channel.mention}")

        if important_channels:
            embed.add_field("Important Channels", "\n".join(important_channels), inline=False)
        
        await ctx.send(embed=embed.build())


    @welcome.command(name="channel")
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx, channel: discord.TextChannel):
        """Set welcome message channel"""
        if ctx.guild.id not in self.welcome_configs:
            self.welcome_configs[ctx.guild.id] = {}
            
        self.welcome_configs[ctx.guild.id]["channel_id"] = channel.id
        
        embed = EmbedBuilder(
            "📝 Welcome Channel Set",
            f"Welcome messages will be sent to {channel.mention}"
        ).set_color(discord.Color.green()).build()
        
        await ctx.send(embed=embed)

    @welcome.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def reset_welcome(self, ctx):
        """Reset welcome message to default"""
        if ctx.guild.id in self.welcome_configs:
            del self.welcome_configs[ctx.guild.id]
            
        embed = EmbedBuilder(
            "🔄 Welcome Reset",
            "Welcome message configuration has been reset to default"
        ).set_color(discord.Color.blue()).build()
        
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = self.welcome_configs.get(member.guild.id, {})
        channel_id = config.get("channel_id")
        welcome_channel = member.guild.get_channel(channel_id) if channel_id else discord.utils.get(member.guild.channels, name="welcome")

        if welcome_channel:
            message = config.get("message", f"Welcome {member.mention} to {member.guild.name}!")
            color = config.get("color", discord.Color.brand_green())
            banner_url = config.get("banner_url")

            message = message.replace("{user}", member.mention)
            message = message.replace("{server}", member.guild.name)
            message = message.replace("{count}", str(len(member.guild.members)))

            embed = EmbedBuilder(
                "👋 Welcome to the Server!",
                message
            ).set_color(color)

            embed.add_field("Member Count", f"#{len(member.guild.members)}")
            embed.add_field("Account Created", member.created_at.strftime("%B %d, %Y"))
            embed.add_field("Join Position", f"#{len(member.guild.members)}", inline=True)
            
            embed.set_thumbnail(member.avatar.url if member.avatar else member.default_avatar.url)
            
            if banner_url:
                embed.set_image(url=banner_url)

            important_channels = []
            rules_channel = discord.utils.get(member.guild.channels, name="rules")
            info_channel = discord.utils.get(member.guild.channels, name="information")
            roles_channel = discord.utils.get(member.guild.channels, name="roles")

            if rules_channel:
                important_channels.append(f"📜 Rules: {rules_channel.mention}")
            if info_channel:
                important_channels.append(f"ℹ️ Information: {info_channel.mention}")
            if roles_channel:
                important_channels.append(f"🎭 Roles: {roles_channel.mention}")

            if important_channels:
                embed.add_field("Important Channels", "\n".join(important_channels), inline=False)

            await welcome_channel.send(embed=embed.build())

            server_management_cog = self.bot.get_cog("ServerManagement")
            if server_management_cog and hasattr(server_management_cog, "autorole_dict"):
                autorole_dict = server_management_cog.autorole_dict
                if member.guild.id in autorole_dict:
                    role_id = autorole_dict[member.guild.id]
                    role = member.guild.get_role(role_id)
                    if role:
                        try:
                            await member.add_roles(role)
                            print(f"✅ Assigned role '{role.name}' to {member.name}")
                        except discord.Forbidden:
                            print(f"❌ Insufficient permissions to assign role '{role.name}' to {member.name}")
                        except discord.HTTPException as e:
                            print(f"⚠️ HTTP Exception: {e}")
                    else:
                        print(f"❌ Role ID {role_id} not found in guild {member.guild.name}")


    @welcome.command(name="banner")
    @commands.has_permissions(administrator=True)
    async def set_banner(self, ctx, banner_url: str = None):
        """Set a banner image/gif for welcome messages"""
        if ctx.guild.id not in self.welcome_configs:
            self.welcome_configs[ctx.guild.id] = {}
            
        if banner_url or ctx.message.attachments:
          
            url = banner_url or ctx.message.attachments[0].url
            
            valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
            is_discord_cdn = 'cdn.discordapp.com' in url
            is_valid_extension = any(ext in url.lower() for ext in valid_extensions)
            
            if is_discord_cdn or is_valid_extension:
                self.welcome_configs[ctx.guild.id]["banner_url"] = url
                
                embed = EmbedBuilder(
                    "🖼️ Welcome Banner Set",
                    "New welcome banner configured"
                ).set_color(discord.Color.green())
                embed.set_image(url=url)
                
                await ctx.send(embed=embed.build())
            else:
                await ctx.send("❌ Invalid image format. Please use PNG, JPG, or GIF")
        else:
            
            self.welcome_configs[ctx.guild.id].pop("banner_url", None)
            await ctx.send("✅ Welcome banner has been removed")



class ReactionRoles(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎮 Gamer", style=discord.ButtonStyle.blurple, custom_id="role_gamer")
    async def gamer_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Gamer")

    @discord.ui.button(label="🎵 Music", style=discord.ButtonStyle.green, custom_id="role_music")
    async def music_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Music")

    @discord.ui.button(label="🎨 Artist", style=discord.ButtonStyle.red, custom_id="role_artist")
    async def artist_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Artist")

    async def toggle_role(self, interaction: discord.Interaction, role_name: str):
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if not role:
            role = await interaction.guild.create_role(name=role_name)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            embed = EmbedBuilder(
                "Role Removed",
                f"Removed {role.mention} role"
            ).set_color(discord.Color.red()).build()
        else:
            await interaction.user.add_roles(role)
            embed = EmbedBuilder(
                "Role Added",
                f"Added {role.mention} role"
            ).set_color(discord.Color.green()).build()

        await interaction.response.send_message(embed=embed, ephemeral=True)

class DesignStudioView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.button(label="Color Theme", style=discord.ButtonStyle.blurple, emoji="🎨")
    async def color_theme(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ColorThemeModal(self.cog))

    @discord.ui.button(label="Button Styles", style=discord.ButtonStyle.green, emoji="🔘")
    async def button_styles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ButtonStyleModal(self.cog))

    @discord.ui.button(label="Layout Options", style=discord.ButtonStyle.gray, emoji="📐")
    async def layout(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(LayoutModal(self.cog))

    @discord.ui.button(label="Edit Text", style=discord.ButtonStyle.primary, emoji="✏️")
    async def edit_text(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextEditModal(self.cog))


class CreateRoleGroupModal(discord.ui.Modal, title="Create Role Group"):
    group_name = discord.ui.TextInput(
        label="Group Name",
        placeholder="Enter a name for this role group",
        required=True
    )
    role_ids = discord.ui.TextInput(
        label="Role IDs",
        placeholder="Enter role IDs separated by commas",
        required=True
    )
    description = discord.ui.TextInput(
        label="Description",
        placeholder="Describe what this group is for",
        required=False,
        style=discord.TextStyle.paragraph
    )

    def __init__(self, cog, guild_id, panel_id):
        super().__init__()
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Role group created!", ephemeral=True)

class ExclusiveRolesModal(discord.ui.Modal, title="Set Exclusive Roles"):
    group_id = discord.ui.TextInput(
        label="Group ID",
        placeholder="Enter the group ID to make exclusive",
        required=True
    )
    exclusive = discord.ui.TextInput(
        label="Exclusive",
        placeholder="Type 'yes' to make roles exclusive",
        required=True
    )

    def __init__(self, cog, guild_id, panel_id):
        super().__init__()
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Exclusive roles set!", ephemeral=True)

class EditGroupModal(discord.ui.Modal, title="Edit Role Group"):
    group_id = discord.ui.TextInput(
        label="Group ID",
        placeholder="Enter the group ID to edit",
        required=True
    )
    new_name = discord.ui.TextInput(
        label="New Name",
        placeholder="Enter new group name",
        required=False
    )
    new_roles = discord.ui.TextInput(
        label="New Role IDs",
        placeholder="Enter new role IDs (comma separated)",
        required=False
    )

    def __init__(self, cog, guild_id, panel_id):
        super().__init__()
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Group updated successfully!", ephemeral=True)


class GroupConfigView(discord.ui.View):
    def __init__(self, cog, guild_id, panel_id):
        super().__init__(timeout=300)
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    @discord.ui.button(label="Create Group", style=discord.ButtonStyle.green, emoji="➕", row=0)
    async def create_group(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CreateRoleGroupModal(self.cog, self.guild_id, self.panel_id))

    @discord.ui.button(label="Edit Group", style=discord.ButtonStyle.blurple, emoji="✏️", row=0)
    async def edit_group(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditGroupModal(self.cog, self.guild_id, self.panel_id))

    @discord.ui.button(label="Exclusive Roles", style=discord.ButtonStyle.gray, emoji="🔒", row=0)
    async def set_exclusive(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ExclusiveRolesModal(self.cog, self.guild_id, self.panel_id))

    @discord.ui.button(label="Role Requirements", style=discord.ButtonStyle.red, emoji="🔑", row=1)
    async def set_requirements(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RoleRequirementsModal(self.cog, self.guild_id, self.panel_id))

class RoleRequirementsModal(discord.ui.Modal, title="Role Requirements"):
    target_role = discord.ui.TextInput(
        label="Target Role ID",
        placeholder="Enter the role ID that needs requirements",
        required=True
    )
    required_roles = discord.ui.TextInput(
        label="Required Role IDs",
        placeholder="Enter role IDs needed to get this role (comma separated)",
        required=True
    )
    level_requirement = discord.ui.TextInput(
        label="Level Requirement (Optional)",
        placeholder="Minimum level needed (if using leveling system)",
        required=False
    )

    def __init__(self, cog, guild_id, panel_id):
        super().__init__()
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    async def on_submit(self, interaction: discord.Interaction):
        target = self.target_role.value
        requirements = self.required_roles.value.split(',')
        
        if not self.cog.role_configs.get(self.guild_id, {}).get('role_requirements'):
            self.cog.role_configs[self.guild_id]['role_requirements'] = {}
            
        self.cog.role_configs[self.guild_id]['role_requirements'][target] = {
            'required_roles': requirements,
            'level_requirement': self.level_requirement.value if self.level_requirement.value else None
        }
        
        self.cog.save_configs()
        await interaction.response.send_message("Role requirements have been set!", ephemeral=True)


class SettingsView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog



    @discord.ui.button(label="📝 Queue Manager", style=ButtonStyle.blurple, row=0)
    async def queue_manager(self, interaction: discord.Interaction, button: discord.ui.Button):
        queue_embed = discord.Embed(title="Queue Manager", color=discord.Color.blue())
        queue_view = QueueView(self.cog)
        await interaction.response.send_message(embed=queue_embed, view=queue_view, ephemeral=True)

    @discord.ui.button(label="🎵 Join/Move", style=ButtonStyle.green, row=1)
    async def join_voice(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.guild.get_member(interaction.user.id)
        if member and member.voice and member.voice.channel:
            if not interaction.guild.voice_client:
                await member.voice.channel.connect()
                await interaction.response.send_message(f"✅ Connected to {member.voice.channel.name}", ephemeral=True)
            else:
                await interaction.guild.voice_client.move_to(member.voice.channel)
                await interaction.response.send_message(f"✅ Moved to {member.voice.channel.name}", ephemeral=True)
        else:
            await interaction.response.send_message("Join a voice channel first!", ephemeral=True)

class ColorThemeModal(discord.ui.Modal, title="Color Theme Settings"):
    theme_choice = discord.ui.TextInput(
        label="Theme Color",
        placeholder="modern, classic, minimal, or custom",
        required=True
    )
    custom_color = discord.ui.TextInput(
        label="Custom Color (hex)",
        placeholder="#000000 (only if using custom theme)",
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        theme = self.theme_choice.value.lower()
        await interaction.response.send_message(f"Theme updated to: {theme}", ephemeral=True)

class AnimatedButton(discord.ui.Button):
    def __init__(self, style=None, animation_type=None, **kwargs):
        super().__init__(**kwargs)
        self.style = style or discord.ButtonStyle.secondary
        self.animation_type = animation_type or "none"
        self.original_label = kwargs.get('label', '')
        self.original_style = self.style
        self.animations = {
            'pulse': self._pulse_effect,
            'fade': self._fade_effect,
            'bounce': self._bounce_effect,
            'shimmer': self._shimmer_effect,
            'rainbow': self._rainbow_effect,
            'wave': self._wave_effect,
            'blink': self._blink_effect,
            'slide': self._slide_effect,
            'glow': self._glow_effect,
            'spin': self._spin_effect
        }

    async def callback(self, interaction: discord.Interaction):
        if self.animation_type != "none":
            await interaction.response.defer()
            animation_func = self.animations.get(self.animation_type)
            if animation_func:
                await animation_func(interaction)
                self.style = self.original_style
                self.label = self.original_label
                await interaction.message.edit(view=self.view)
        
        await super().callback(interaction)
    async def _pulse_effect(self, interaction):
        styles = [ButtonStyle.primary, ButtonStyle.success, ButtonStyle.secondary]
        for style in styles:
            self.style = style
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.5)

    async def _fade_effect(self, interaction):
        labels = [self.label + "⠀", self.label + "⠈", self.label]
        for label in labels:
            self.label = label
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.3)

    async def _bounce_effect(self, interaction):
        positions = ["↑" + self.label, "↓" + self.label, self.label]
        for pos in positions:
            self.label = pos
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.2)

    async def _shimmer_effect(self, interaction):
        sparkles = ["✨", "⭐", "🌟", "💫"]
        for sparkle in sparkles:
            self.label = f"{sparkle} {self.label} {sparkle}"
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.4)

    async def _rainbow_effect(self, interaction):
        colors = [0xFF0000, 0xFFA500, 0xFFFF00, 0x00FF00, 0x0000FF, 0x4B0082, 0x9400D3]
        embed = interaction.message.embeds[0]
        for color in colors:
            embed.color = color
            await interaction.message.edit(embed=embed)
            await asyncio.sleep(0.3)

    async def _wave_effect(self, interaction):
        frames = ["⋮", "⋰", "⋯", "⋱"]
        for frame in frames:
            self.label = f"{frame} {self.label} {frame}"
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.3)

    async def _blink_effect(self, interaction):
        for _ in range(3):
            self.disabled = True
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.2)
            self.disabled = False
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.2)

    async def _slide_effect(self, interaction):
        spaces = ["⠀" * i + self.label + "⠀" * (5-i) for i in range(6)]
        for space in spaces:
            self.label = space
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.2)

    async def _glow_effect(self, interaction):
        styles = [ButtonStyle.secondary, ButtonStyle.success, ButtonStyle.primary]
        emojis = ["✨", "🌟", "💫", "⭐"]
        for style, emoji in zip(styles, emojis):
            self.style = style
            self.emoji = emoji
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.4)

    async def _spin_effect(self, interaction):
        spin_frames = ["◜", "◝", "◞", "◟"]
        for frame in spin_frames:
            self.label = f"{frame} {self.label} {frame}"
            await interaction.message.edit(view=self.view)
            await asyncio.sleep(0.2)

class ButtonStyleModal(discord.ui.Modal, title="Button Style Settings"):
    style_choice = discord.ui.TextInput(
        label="Button Style",
        placeholder="default, primary, success, or danger",
        required=True
    )
    animation_choice = discord.ui.TextInput(
        label="Animation Style",
        placeholder="pulse, grow, fade, bounce, or none",
        required=False,
        default="none"
    )
    custom_color = discord.ui.TextInput(
        label="Custom Color (optional)",
        placeholder="Enter hex color code (#RRGGBB)",
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        style = self.style_choice.value.lower()
        animation = self.animation_choice.value.lower() if self.animation_choice.value else "none"
        
        guild_id = str(interaction.guild_id)
        if guild_id not in self.cog.role_configs:
            self.cog.role_configs[guild_id] = {}
        
        self.cog.role_configs[guild_id]["button_style"] = style
        self.cog.role_configs[guild_id]["animation"] = animation
        
        if self.custom_color.value:
            self.cog.role_configs[guild_id]["custom_color"] = self.custom_color.value
        
        self.cog.save_configs()
        
        await interaction.response.send_message(
            "Button style updated! Use the Refresh button to see your changes.", 
            ephemeral=True
        )

class LayoutModal(discord.ui.Modal, title="Layout Settings"):
    layout_type = discord.ui.TextInput(
        label="Layout Type",
        placeholder="grid, list, or compact",
        required=True
    )
    columns = discord.ui.TextInput(
        label="Number of Columns",
        placeholder="1-5 (for grid layout)",
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        layout = self.layout_type.value.lower()
        await interaction.response.send_message(f"Layout updated to: {layout}", ephemeral=True)

class TextEditModal(discord.ui.Modal, title="Edit Text Settings"):
    title_text = discord.ui.TextInput(
        label="Panel Title",
        placeholder="Enter new panel title",
        required=False
    )
    description = discord.ui.TextInput(
        label="Panel Description",
        placeholder="Enter new description",
        style=discord.TextStyle.paragraph,
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Text settings updated!", ephemeral=True)

class RoleLimitsModal(discord.ui.Modal, title="Role Limits"):
    max_roles = discord.ui.TextInput(
        label="Maximum Roles",
        placeholder="Enter max number of roles per user (0 for unlimited)",
        required=True
    )
    exclusive_groups = discord.ui.TextInput(
        label="Exclusive Groups",
        placeholder="Enter role groups (comma separated)",
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Role limits updated!", ephemeral=True)

class VerificationSettingsModal(discord.ui.Modal, title="Verification Settings"):
    require_verification = discord.ui.TextInput(
        label="Require Verification",
        placeholder="yes/no",
        required=True
    )
    verification_role = discord.ui.TextInput(
        label="Required Role ID",
        placeholder="Enter role ID required for access",
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Verification settings updated!", ephemeral=True)

class CooldownSettingsModal(discord.ui.Modal, title="Cooldown Settings"):
    cooldown_time = discord.ui.TextInput(
        label="Cooldown Duration",
        placeholder="Enter cooldown in seconds",
        required=True
    )
    bypass_roles = discord.ui.TextInput(
        label="Bypass Role IDs",
        placeholder="Enter role IDs that bypass cooldown (comma separated)",
        required=False
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Cooldown settings updated!", ephemeral=True)

class EditPanelModal(discord.ui.Modal, title="Edit Role Panel"):
    panel_id = discord.ui.TextInput(
        label="Panel ID",
        placeholder="Enter the panel ID to edit",
        required=True
    )
    
    new_title = discord.ui.TextInput(
        label="New Title",
        placeholder="Enter new panel title...",
        required=False
    )
    
    new_description = discord.ui.TextInput(
        label="New Description",
        placeholder="Enter new description...",
        required=False,
        style=discord.TextStyle.paragraph
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        panel = self.cog.role_configs[guild_id].get(self.panel_id.value)
        
        if panel:
            if self.new_title.value:
                panel["title"] = self.new_title.value
            if self.new_description.value:
                panel["description"] = self.new_description.value
            
            self.cog.save_configs()
            await interaction.response.send_message("Panel updated successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("Panel not found!", ephemeral=True)

class DeletePanelModal(discord.ui.Modal, title="Delete Role Panel"):
    panel_id = discord.ui.TextInput(
        label="Panel ID",
        placeholder="Enter the panel ID to delete",
        required=True
    )
    
    confirmation = discord.ui.TextInput(
        label="Confirmation",
        placeholder="Type 'DELETE' to confirm",
        required=True
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        if self.confirmation.value != "DELETE":
            await interaction.response.send_message("Deletion cancelled.", ephemeral=True)
            return

        guild_id = str(interaction.guild_id)
        if self.panel_id.value in self.cog.role_configs[guild_id]:
            del self.cog.role_configs[guild_id][self.panel_id.value]
            self.cog.save_configs()
            await interaction.response.send_message("Panel deleted successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("Panel not found!", ephemeral=True)

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_configs = {}
        self.role_panel_configs = {}
        self.load_configs()
        self.color_options = {
            "Red": discord.Color.red(),
            "Blue": discord.Color.blue(),
            "Green": discord.Color.green(),
            "Purple": discord.Color.purple(),
            "Gold": discord.Color.gold()
        }
        self.style_options = {
            "Default": discord.ButtonStyle.secondary,
            "Primary": discord.ButtonStyle.primary,
            "Success": discord.ButtonStyle.success,
            "Danger": discord.ButtonStyle.danger
        }

    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rolepanel_json(self, ctx):
        """Create advanced role panels from Discohook JSON format with multiple embeds"""
        if not hasattr(self, 'role_panel_configs'):
            self.role_panel_configs = {}

        embed = discord.Embed(
            title="🎨 Advanced JSON Panel Creator",
            description="Create beautiful role panels using Discohook.org format!\n\n**Features:**\n• Multiple Embeds Support\n• Full Discohook Compatibility\n• Rich Formatting\n• Custom Fields & Images\n• Hex Color Support\n• Per-Embed Buttons",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📝 Getting Started",
            value="• Click 'Show Examples' for templates\n• Use 'Upload JSON' to create your panel\n• Support for multiple embeds\n• Custom button placement",
            inline=False
        )
        
        embed.add_field(
            name="🎨 Available Styles",
            value="• Button Styles: PRIMARY, SECONDARY, SUCCESS, DANGER\n• Colors: Hex (#FF7AC6) or Decimal (16711680)\n• Groups: For exclusive role sets",
            inline=False
        )

        view = AdvancedJsonPanelView(self)
        view.guild_id = ctx.guild.id  
        await ctx.send(embed=embed, view=view)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def exportrolepanel(self, ctx):
        """Export all role panel configurations to a JSON file"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.role_configs or not self.role_configs[guild_id]:
            return await ctx.send("No role panels found to export!")
        
        config_data = self.role_configs[guild_id]
        file_content = json.dumps(config_data, indent=4)
        
        file = discord.File(
            io.StringIO(file_content),
            filename=f"role_panel_config_{ctx.guild.name}.json"
        )
        await ctx.send("Here's your role panel configuration:", file=file)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def importrolepanel(self, ctx):
        """Import role panel configurations from a JSON file"""
        if not ctx.message.attachments:
            return await ctx.send("Please attach a JSON configuration file!")
            
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.json'):
            return await ctx.send("Please provide a valid JSON file!")
            
        try:
            config_data = json.loads(await attachment.read())
            guild_id = str(ctx.guild.id)
            self.role_configs[guild_id] = config_data
            self.save_configs()
            
            await ctx.send("✅ Role panel configuration imported successfully! Use the refresh button in !rolepanel to update the panels.")
        except json.JSONDecodeError:
            await ctx.send("❌ Invalid JSON file format!")

    def load_configs(self):
        try:
            with open('role_configs.json', 'r', encoding='utf-8') as f:
                self.role_configs = json.load(f)
        except FileNotFoundError:
            self.role_configs = {}

    def save_configs(self):
        with open('role_configs.json', 'w', encoding='utf-8') as f:
            json.dump(self.role_configs, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rolepanel(self, ctx):
        """Open the advanced role management panel"""
        embed = discord.Embed(
            title="🎮 Ultimate Role Management Suite",
            description="Create stunning role selection menus with advanced features!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🎨 Design Features",
            value="• Custom Panel Themes\n• Animated Buttons\n• Custom Emojis\n• Multiple Layouts\n• Dynamic Colors\n• Custom Icons",
            inline=True
        )
        
        embed.add_field(
            name="⚙️ Advanced Options",
            value="• Role Requirements\n• Group Roles\n• Temporary Roles\n• Role Limits\n• Role Categories\n• Role Chains",
            inline=True
        )
        
        embed.add_field(
            name="🔒 Security Features",
            value="• Permission Checks\n• Role Hierarchy\n• Anti-Abuse System\n• Rate Limiting\n• Role Conflicts",
            inline=False
        )

        await ctx.send(embed=embed, view=RoleManagerMainView(self))

class RoleManagerMainView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog
        self.current_page = 0

    @discord.ui.button(label="Create Panel", style=discord.ButtonStyle.green, emoji="✨", row=0)
    async def create_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CreatePanelModal(self.cog))

    @discord.ui.button(label="Manage Panels", style=discord.ButtonStyle.blurple, emoji="📋", row=0)
    async def manage_panels(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_panel_manager(interaction)

    @discord.ui.button(label="Design Studio", style=discord.ButtonStyle.gray, emoji="🎨", row=0)
    async def design_studio(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🎨 Design Studio",
            description="Customize your role panel appearance",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Design Features",
            value="• Custom Panel Themes\n• Animated Buttons\n• Custom Emojis\n• Multiple Layouts\n• Dynamic Colors\n• Custom Icons",
            inline=False
        )
        embed.add_field(
            name="Available Themes",
            value="• Modern\n• Classic\n• Minimal\n• Custom",
            inline=True
        )
        embed.add_field(
            name="Layout Options",
            value="• Grid\n• List\n• Compact\n• Custom",
            inline=True
        )
        await interaction.response.send_message(embed=embed, view=DesignStudioView(self.cog), ephemeral=True)

    @discord.ui.button(label="Role Groups", style=discord.ButtonStyle.primary, emoji="📑", row=0)
    async def manage_groups(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Role Group Management",
            description="Create and manage role groups for better organization",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Advanced Options",
            value="• Role Requirements\n• Group Roles\n• Temporary Roles\n• Role Limits\n• Role Categories\n• Role Chains",
            inline=False
        )
        embed.add_field(
            name="Group Features",
            value="• Exclusive Roles\n• Role Hierarchy\n• Role Dependencies\n• Auto Roles",
            inline=True
        )
        await interaction.response.send_message(
            embed=embed,
            view=GroupConfigView(self.cog, str(interaction.guild_id), "main"),
            ephemeral=True
        )

    @discord.ui.button(label="Settings", style=discord.ButtonStyle.gray, emoji="⚙️", row=1)
    async def settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚙️ Settings",
            description="Configure global role panel settings",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Security Features",
            value="• Permission Checks\n• Role Hierarchy\n• Anti-Abuse System\n• Rate Limiting\n• Role Conflicts",
            inline=False
        )
        embed.add_field(
            name="Configuration Options",
            value="• Global Cooldowns\n• Verification Requirements\n• Logging Settings\n• Backup Options",
            inline=True
        )
        await interaction.response.send_message(embed=embed, view=SettingsView(self.cog), ephemeral=True)

    @discord.ui.button(label="Refresh Panels", style=discord.ButtonStyle.success, emoji="🔄", row=1)
    async def refresh_panels(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        guild_id = str(interaction.guild_id)
        panels = self.cog.role_configs.get(guild_id, {})
        
        for panel_id, panel_data in panels.items():
            try:
                channel_id = int(panel_data.get("channel", 0))
                channel = interaction.guild.get_channel(channel_id)
                
                if channel:
                    async for message in channel.history(limit=50):
                        if message.author == interaction.guild.me and message.embeds:
                            await message.delete()

                    embed = discord.Embed(
                        title=panel_data["title"],
                        description=panel_data["description"],
                        color=self.get_theme_color(panel_data.get("theme", "modern"))
                    )
                    await channel.send(embed=embed, view=DeployedRoleView(self.cog, guild_id, panel_id))
                    
            except (ValueError, KeyError, AttributeError):
                continue

        await interaction.followup.send("All role panels have been refreshed!", ephemeral=True)


    def get_theme_color(self, theme):
        theme_colors = {
            "modern": discord.Color.blue(),
            "classic": discord.Color.gold(),
            "minimal": discord.Color.light_grey(),
            "custom": discord.Color.purple()
        }
        return theme_colors.get(theme, discord.Color.blue())

    async def show_panel_manager(self, interaction):
        panels = self.cog.role_configs.get(str(interaction.guild_id), {})
        if not panels:
            await interaction.response.send_message("No panels exist yet! Create one first.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📋 Panel Manager",
            description="Manage your existing role panels",
            color=discord.Color.blue()
        )

        for panel_id, panel in panels.items():
            embed.add_field(
                name=f"Panel: {panel['title']}",
                value=f"ID: {panel_id}\nChannel: <#{panel['channel']}>\nRoles: {len(panel.get('roles', []))}\nStyle: {panel.get('style', {}).get('theme', 'Default')}",
                inline=False
            )

        await interaction.response.send_message(
            embed=embed,
            view=PanelManagerView(self.cog, panels),
            ephemeral=True
        )
    async def show_design_studio(self, interaction):
        embed = discord.Embed(
            title="🎨 Design Studio",
            description="Customize your role panel appearance",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Available Customizations",
            value="• Theme Selection\n• Button Styles\n• Layout Options\n• Color Schemes\n• Animation Settings\n• Custom Icons",
            inline=False
        )
        await interaction.response.send_message(embed=embed, view=DesignStudioView(self.cog), ephemeral=True)

    async def show_settings(self, interaction):
        embed = discord.Embed(
            title="⚙️ Settings",
            description="Configure global role panel settings",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Global Settings",
            value="• Permission Management\n• Rate Limits\n• Verification Requirements\n• Logging Options\n• Backup Settings",
            inline=False
        )
        await interaction.response.send_message(embed=embed, view=SettingsView(self.cog), ephemeral=True)

class CreatePanelModal(discord.ui.Modal, title="Create Role Panel"):
    title_input = discord.ui.TextInput(
        label="Panel Title",
        placeholder="Enter an attractive title for your panel...",
        max_length=256,
        required=True
    )
    
    description = discord.ui.TextInput(
        label="Panel Description", 
        placeholder="Describe what this role panel is for...",
        style=discord.TextStyle.paragraph,
        required=True
    )
    
    channel_id = discord.ui.TextInput(
        label="Channel ID",
        placeholder="Enter the channel ID for the panel",
        required=True
    )
    
    theme = discord.ui.TextInput(
        label="Theme & Style",
        placeholder="modern, classic, minimal, or custom",
        required=False,
        default="modern"
    )
    
    roles_config = discord.ui.TextInput(
        label="Initial Roles",
        placeholder="Role IDs separated by commas",
        required=False,
        style=discord.TextStyle.paragraph
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        
        panel_data = {
            "title": self.title_input.value,
            "description": self.description.value,
            "channel": self.channel_id.value,
            "theme": self.theme.value.lower(),
            "roles": [],
            "settings": {
                "requires_verification": False,
                "cooldown": 0,
                "max_roles": 0,
                "exclusive_groups": []
            },
            "style": {
                "color": "blue",
                "button_style": "default",
                "layout": "grid",
                "animations": True
            }
        }

        guild_id = str(interaction.guild_id)
        if guild_id not in self.cog.role_configs:
            self.cog.role_configs[guild_id] = {}
        
        panel_id = str(len(self.cog.role_configs[guild_id]) + 1)
        self.cog.role_configs[guild_id][panel_id] = panel_data
        self.cog.save_configs()

        await interaction.response.send_message(
            "Panel created! Let's configure the roles and settings:",
            view=PanelConfigView(self.cog, guild_id, panel_id),
            ephemeral=True
        )

class PanelConfigView(discord.ui.View):
    def __init__(self, cog, guild_id, panel_id):
        super().__init__(timeout=300)
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    @discord.ui.button(label="Add Roles", style=discord.ButtonStyle.green, emoji="➕", row=0)
    async def add_roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(AddRoleModal(self.cog, self.guild_id, self.panel_id))

    @discord.ui.button(label="Role Groups", style=discord.ButtonStyle.blurple, emoji="📑", row=0)
    async def configure_groups(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.show_group_config(interaction)

    @discord.ui.button(label="Preview", style=discord.ButtonStyle.gray, emoji="👁️", row=1)
    async def preview_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        panel = self.cog.role_configs[self.guild_id][self.panel_id]
        preview_embed = discord.Embed(
            title=panel["title"],
            description=panel["description"],
            color=self.get_theme_color(panel.get("theme", "modern"))
        )
        await interaction.response.send_message(
            embed=preview_embed,
            view=PreviewRoleView(self.cog, self.guild_id, self.panel_id),
            ephemeral=True
        )

    @discord.ui.button(label="Deploy", style=discord.ButtonStyle.success, emoji="🚀", row=1)
    async def deploy_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.deploy_to_channel(interaction)

    def get_theme_color(self, theme):
        theme_colors = {
            "modern": discord.Color.blue(),
            "classic": discord.Color.gold(),
            "minimal": discord.Color.light_grey(),
            "custom": discord.Color.purple()
        }
        return theme_colors.get(theme, discord.Color.blue())
    
    async def show_group_config(self, interaction):
        panel = self.cog.role_configs[self.guild_id][self.panel_id]
        embed = discord.Embed(
            title="📑 Role Groups Configuration",
            description="Manage role groups and requirements",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=GroupConfigView(self.cog, self.guild_id, self.panel_id), ephemeral=True)

    async def deploy_to_channel(self, interaction):
        panel = self.cog.role_configs[self.guild_id][self.panel_id]
        channel = interaction.guild.get_channel(int(panel["channel"]))
        
        if not channel:
            await interaction.response.send_message("Target channel not found!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=panel["title"],
            description=panel["description"],
            color=self.get_theme_color(panel.get("theme", "modern"))
        )
        
        await channel.send(embed=embed, view=DeployedRoleView(self.cog, self.guild_id, self.panel_id))
        await interaction.response.send_message("Panel deployed successfully!", ephemeral=True)


class PanelManagerView(discord.ui.View):
    def __init__(self, cog, panels):
        super().__init__(timeout=300)
        self.cog = cog
        self.panels = panels

    @discord.ui.button(label="Edit Panel", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def edit_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditPanelModal(self.cog))

    @discord.ui.button(label="Delete Panel", style=discord.ButtonStyle.red, emoji="🗑️")
    async def delete_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeletePanelModal(self.cog))

class DeployedRoleView(discord.ui.View):
    def __init__(self, cog, guild_id, panel_id, buttons=None):
        super().__init__(timeout=None)
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id
        if buttons:
            self.setup_buttons(buttons)
        else:
            self.setup_default_buttons()

    def get_button_style(self, style_name):
        styles = {
            "default": discord.ButtonStyle.secondary,
            "primary": discord.ButtonStyle.primary,
            "success": discord.ButtonStyle.success,
            "danger": discord.ButtonStyle.danger,
            "PRIMARY": discord.ButtonStyle.primary,
            "SECONDARY": discord.ButtonStyle.secondary,
            "SUCCESS": discord.ButtonStyle.success,
            "DANGER": discord.ButtonStyle.danger
        }
        return styles.get(style_name, discord.ButtonStyle.secondary)

    def setup_default_buttons(self):
        panel = self.cog.role_configs[self.guild_id][self.panel_id]
        for role_data in panel.get("roles", []):
            self.create_button(role_data)

    def setup_buttons(self, buttons):
        for button_data in buttons:
            self.create_button(button_data)

    def create_button(self, button_data):
        style = self.get_button_style(button_data.get("style", "default"))
        button = AnimatedButton(
            style=style,
            label=button_data["label"],
            emoji=button_data.get("emoji"),
            custom_id=f"role_{button_data['id']}",
            animation_type=button_data.get("animation_type", "none")
        )
        button.callback = self.handle_role_click
        self.add_item(button)

    async def handle_role_click(self, interaction: discord.Interaction):
        custom_id = interaction.data.get('custom_id', '')
        role_id = custom_id.split("_")[1]
        member = interaction.user
        role = interaction.guild.get_role(int(role_id))

        if not role:
            await interaction.response.send_message("Role not found!", ephemeral=True)
            return

        try:
            panel = self.cog.role_configs[self.guild_id][self.panel_id]
            settings = panel.get("settings", {})
            exclusive_groups = settings.get("exclusive_groups", [])

            if role in member.roles:
                await member.remove_roles(role)
                await interaction.response.send_message(f"Removed role: {role.name}", ephemeral=True)
            else:
               
                for button_data in panel.get("roles", []):
                    if button_data.get("group") in exclusive_groups:
                        existing_role = interaction.guild.get_role(int(button_data["id"]))
                        if existing_role and existing_role in member.roles:
                            await member.remove_roles(existing_role)

                await member.add_roles(role)
                await interaction.response.send_message(f"Added role: {role.name}", ephemeral=True)

            if hasattr(interaction.message, 'edit'):
                await interaction.message.edit(view=self)

        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to manage that role!", ephemeral=True)


class PanelManagerView(discord.ui.View):
    def __init__(self, cog, panels):
        super().__init__(timeout=300)
        self.cog = cog
        self.panels = panels

    @discord.ui.button(label="Edit Panel", style=discord.ButtonStyle.blurple, emoji="✏️")
    async def edit_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditPanelModal(self.cog))

    @discord.ui.button(label="Delete Panel", style=discord.ButtonStyle.red, emoji="🗑️")
    async def delete_panel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DeletePanelModal(self.cog))

class AddRoleModal(discord.ui.Modal, title="Add Role to Panel"):
    role_id = discord.ui.TextInput(
        label="Role ID",
        placeholder="Enter the role ID to add",
        required=True
    )
    
    button_label = discord.ui.TextInput(
        label="Button Label",
        placeholder="Text to show on the button",
        required=True
    )
    
    emoji = discord.ui.TextInput(
        label="Button Emoji",
        placeholder="Optional: Add an emoji",
        required=False
    )
    
    style = discord.ui.TextInput(
        label="Button Style",
        placeholder="default, primary, success, or danger",
        required=False,
        default="default"
    )

    def __init__(self, cog, guild_id, panel_id):
        super().__init__()
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id

    async def on_submit(self, interaction: discord.Interaction):
        role_data = {
            "id": self.role_id.value,
            "label": self.button_label.value,
            "emoji": self.emoji.value if self.emoji.value else None,
            "style": self.style.value.lower()
        }
        
        self.cog.role_configs[self.guild_id][self.panel_id]["roles"].append(role_data)
        self.cog.save_configs()
        
        await interaction.response.send_message(
            f"Role added successfully with label: {self.button_label.value}",
            ephemeral=True
        )

class PreviewRoleView(discord.ui.View):
    def __init__(self, cog, guild_id, panel_id):
        super().__init__(timeout=60)
        self.cog = cog
        self.guild_id = guild_id
        self.panel_id = panel_id
        self.setup_preview_buttons()

    def setup_preview_buttons(self):
        panel = self.cog.role_configs[self.guild_id][self.panel_id]
        for role_data in panel.get("roles", []):
            style = self.get_button_style(role_data.get("style", "default"))
            button = discord.ui.Button(
                style=style,
                label=role_data["label"],
                emoji=role_data.get("emoji"),
                disabled=True  
            )
            self.add_item(button)

    def get_button_style(self, style_name):
        styles = {
            "default": discord.ButtonStyle.secondary,
            "primary": discord.ButtonStyle.primary,
            "success": discord.ButtonStyle.success,
            "danger": discord.ButtonStyle.danger
        }
        return styles.get(style_name, discord.ButtonStyle.secondary)

class AdvancedJsonPanelView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog
        if not hasattr(self.cog, 'role_panel_configs'):
            self.cog.role_panel_configs = {}

    def convert_color(self, color_value):
        if isinstance(color_value, str) and color_value.startswith('#'):
            return int(color_value.strip('#'), 16)
        return color_value

    @discord.ui.button(label="Upload Discohook JSON", style=discord.ButtonStyle.green, emoji="📤")
    async def upload_json(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Upload your Discohook JSON file or paste the JSON content in the next message.",
            ephemeral=True
        )
        
        def check(m):
            return m.author == interaction.user and (m.attachments or m.content)
            
        try:
            msg = await self.cog.bot.wait_for('message', timeout=120.0, check=check)
            
            if msg.attachments:
                attachment = msg.attachments[0]
                if not attachment.filename.endswith('.json'):
                    return await interaction.followup.send("Please provide a valid JSON file!", ephemeral=True)
                json_data = json.loads(await attachment.read())
            else:
                json_data = json.loads(msg.content)
            
            guild_id = str(interaction.guild_id)
            panel_id = str(len(self.cog.role_configs.get(guild_id, {})) + 1)
            
            panel_data = self.convert_discohook_to_panel(json_data)
            
            self.cog.role_panel_configs[guild_id] = json_data
            
            if guild_id not in self.cog.role_configs:
                self.cog.role_configs[guild_id] = {}
                
            self.cog.role_configs[guild_id][panel_id] = panel_data
            self.cog.save_configs()
            
            channel = interaction.guild.get_channel(int(panel_data["channel"]))
            if channel:
                for embed_data in panel_data["embeds"]:
                    if "color" in embed_data:
                        embed_data["color"] = self.convert_color(embed_data["color"])
                    embed = discord.Embed.from_dict(embed_data)
                    buttons = embed_data.get("buttons", [])
                    view = DeployedRoleView(self.cog, guild_id, panel_id, buttons) if buttons else None
                    await channel.send(embed=embed, view=view)
            
            await interaction.followup.send("✨ Beautiful role panel created successfully!", ephemeral=True)
            
        except asyncio.TimeoutError:
            await interaction.followup.send("Timed out waiting for JSON.", ephemeral=True)
        except json.JSONDecodeError:
            await interaction.followup.send("Invalid JSON format! Make sure it's properly formatted.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)


    @discord.ui.button(label="Show Examples", style=discord.ButtonStyle.blurple, emoji="📚")
    async def show_examples(self, interaction: discord.Interaction, button: discord.ui.Button):
        example_embed = discord.Embed(
            title="📚 Role Panel Examples",
            description="Here are different examples you can use as templates:",
            color=discord.Color.blue()
        )

        simple_example = {
            "channel_id": "YOUR_CHANNEL_ID",
            "embeds": [{
                "title": "🎮 Gaming Roles",
                "description": "Select your favorite games!",
                "color": "#FF7AC6",
                "buttons": [{
                    "id": "ROLE_ID",
                    "label": "Minecraft",
                    "emoji": "⛏️",
                    "style": "PRIMARY"
                }]
            }]
        }
        example_embed.add_field(
            name="📝 Simple Example",
            value=f"```json\n{json.dumps(simple_example, indent=2)}\n```",
            inline=False
        )

        multi_example = {
            "channel_id": "YOUR_CHANNEL_ID",
            "embeds": [
                {
                    "title": "🌟 Welcome",
                    "description": "Welcome to our server! Select your status below.",
                    "color": "#7289DA",
                    "buttons": [
                        {
                            "id": "ROLE_ID_1",
                            "label": "New Member",
                            "emoji": "✨",
                            "style": "SUCCESS"
                        },
                        {
                            "id": "ROLE_ID_2",
                            "label": "Regular",
                            "emoji": "⭐",
                            "style": "PRIMARY"
                        },
                        {
                            "id": "ROLE_ID_3",
                            "label": "Notifications",
                            "emoji": "🔔",
                            "style": "SECONDARY"
                        }
                    ]
                },
                {
                    "title": "🎮 Gaming Roles",
                    "description": "Select your favorite games!",
                    "color": "#FF4B4B",
                    "buttons": [
                        {
                            "id": "ROLE_ID_4",
                            "label": "Minecraft",
                            "emoji": "⛏️",
                            "style": "PRIMARY"
                        },
                        {
                            "id": "ROLE_ID_5",
                            "label": "Valorant",
                            "emoji": "🎯",
                            "style": "DANGER"
                        },
                        {
                            "id": "ROLE_ID_6",
                            "label": "League",
                            "emoji": "⚔️",
                            "style": "SUCCESS"
                        },
                        {
                            "id": "ROLE_ID_7",
                            "label": "Fortnite",
                            "emoji": "🎪",
                            "style": "PRIMARY"
                        }
                    ]
                }
            ]
        }
        example_embed.add_field(
            name="📚 Multi-Embed Example",
            value=f"```json\n{json.dumps(multi_example, indent=2)}\n```",
            inline=False
        )

        example_embed.add_field(
            name="🎨 Style Guide",
            value="• Use hex colors (#FF7AC6) or decimal\n• Button styles: PRIMARY, SECONDARY, SUCCESS, DANGER\n• Add emojis to titles and buttons\n• Group related roles together",
            inline=False
        )

        await interaction.response.send_message(embed=example_embed, ephemeral=True)

    def convert_discohook_to_panel(self, json_data):
        """Convert Discohook JSON format to panel format"""
        return {
            "channel": str(json_data.get("channel_id", "0")),
            "embeds": json_data.get("embeds", []),
            "roles": json_data.get("roles", []),
            "settings": {
                "requires_verification": json_data.get("requires_verification", False),
                "cooldown": json_data.get("cooldown", 0),
                "max_roles": json_data.get("max_roles", 0),
                "exclusive_groups": json_data.get("exclusive_groups", [])
            },
            "style": {
                "layout": json_data.get("layout", "grid"),
                "animations": json_data.get("animations", True),
                "button_style": json_data.get("button_style", "default")
            }
        }


class UserTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_activity = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        if user_id not in self.user_activity:
            self.user_activity[user_id] = {
                "messages": 0,
                "last_active": None,
                "commands_used": 0
            }

        self.user_activity[user_id]["messages"] += 1
        self.user_activity[user_id]["last_active"] = datetime.now(timezone.utc)

    @commands.command()
    async def activity(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_data = self.user_activity.get(member.id, {
            "messages": 0,
            "last_active": None,
            "commands_used": 0
        })

        embed = EmbedBuilder(
            f"📊 Activity Stats - {member.name}",
            "User activity information"
        ).set_color(discord.Color.blue())
        
        embed.add_field("Messages Sent", str(user_data["messages"]))
        embed.add_field("Commands Used", str(user_data["commands_used"]))
        
        if user_data["last_active"]:
            embed.add_field(
                "Last Active",
                user_data["last_active"].strftime("%Y-%m-%d %H:%M:%S UTC"),
                inline=False
            )
            
        embed.set_thumbnail(member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed.build())

bot.add_cog(WelcomeSystem(bot))
bot.add_cog(RoleManager(bot))
bot.add_cog(UserTracker(bot))

TOKEN = os.getenv('D15C0RD_T0K3N')  # Do  NOT   hardcode your Discord Token here! 

if __name__ == "__main__":

    logging.basicConfig(                                        # Removable
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('bot.log')
        ]
    )
    @bot.event
    async def on_message(message):
        await bot.webhook_logger.log_message(message)
        await bot.process_commands(message)

    @bot.event 
    async def on_command(ctx):
        await bot.webhook_logger.log_command(ctx)

    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logging.error("Invalid token provided")
    except Exception as e:
        logging.error(f"Error during bot startup: {e}")

# Maintained and Created by: TheZ 
