### If you type explain in your question to the bot, it'll give more details to your question. 
## Genie: explain life to me!
## if you just do Genie: tell me about life, it'll be shorter, but if you add explain, more deetz!
## ENJOY - GH0ST

## VISIT US AT IRC.TWISTEDNET.ORG #DEV #TWISTED
### 

import ssl
import os
import json
from irc import client, connection
from irc.client import Reactor
from openai import OpenAI
import time
import re
from colorama import Fore, Style
import irc.client
from jaraco.stream import buffer

irc.client.ServerConnection.buffer_class = buffer.LenientDecodingLineBuffer

print(Fore.GREEN + "Genie - by gh0st- IRC.TWISTEDNET.ORG #TWISTED #DEV" + Style.RESET_ALL)

if os.path.exists("config.json"):
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
else:
    config = {}
    config["SERVER"] = input("Enter IRC server address: ")
    config["NICKNAME"] = input("Enter bots nickname: ")
    config["CHANNEL"] = input("Enter the channel to join (e.g., #Twisted): ")
    config["OWNERS"] = input("Enter owner nicks (comma-separated, e.g., gh0st,n0ne`,dayz,sukitfup): ").split(',')
    config["TEMPERATURE"] = float(input("Enter the temperature value (e.g., 0.5 for more deterministic, 1.0 for default, 1.5 for more random): "))
    config["TOKENS"] = int(input("Enter the maximum number of tokens for a response (e.g., 100): "))

    with open("config.json", "w") as config_file:
        json.dump(config, config_file)

SERVER = config["SERVER"]
NICKNAME = config["NICKNAME"]
CHANNEL = config["CHANNEL"]
OWNERS = config["OWNERS"]
TEMPERATURE = config["TEMPERATURE"]
TOKENS = config["TOKENS"]

PORT = 6697
CHANNELS = [CHANNEL]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class CustomReactor(Reactor):
    def __init__(self):
        super().__init__()
        self.connection_class = connection.Factory(wrapper=ssl.wrap_socket)
        self.encoding = 'utf-8'

    def on_raw(self, connection, event):
        try:
            if event.arguments:
                try:
                    decoded = event.arguments[0].decode('utf-8')
                    self.encoding = 'utf-8'
                except UnicodeDecodeError:
                    decoded = event.arguments[0].decode('iso-8859-1')
                    self.encoding = 'iso-8859-1'
                print(f"Detected server encoding: {self.encoding}, Message: {decoded}")
        except Exception as e:
            print(f"Error in on_raw: {e}")

class ChatGPTBot(client.SimpleIRCClient):
    def __init__(self, channels, nickname, max_tokens=100):
        try:
            client.SimpleIRCClient.__init__(self)
            self.channels = channels
            self.nickname = nickname
            self.ignored_users = set()
            self.connected = False
            self.max_tokens = max_tokens
            print(f"Initialized bot for channels {channels} with nickname {nickname}")
        except Exception as e:
            print(f"Error in ChatGPTBot initialization: {e}")

    def on_welcome(self, connection, event):
        try:
            print("Connected to IRC server, received welcome message.")
            self.connected = True
            for channel in self.channels:
                print(f"Attempting to join channel {channel}")
                connection.join(channel)
        except Exception as e:
            print(f"Error in on_welcome: {e}")

    def on_join(self, connection, event):
        try:
            print(f"Joined {event.target}")
        except Exception as e:
            print(f"Error in on_join: {e}")

    def on_pubmsg(self, connection, event):
        try:
            sender = event.source.nick
            message = event.arguments[0]
            sender_lower = sender.lower()

            if sender_lower in self.ignored_users:
                print(f"Ignoring message from {sender} in {event.target}")
                return

            if sender in OWNERS:
                if message.startswith("!join "):
                    try:
                        _, channel = message.split(' ', 1)
                        if channel.startswith('#'):
                            self.join_channel(connection, channel)
                            print(f"Joining {channel} as requested by {sender}")
                        else:
                            print("Invalid channel name format")
                    except ValueError:
                        print("Invalid join command format")
                    return

                elif message.startswith("!part "):
                    try:
                        _, channel = message.split(' ', 1)
                        if channel.startswith('#'):
                            self.part_channel(connection, channel)
                            print(f"Parting from {channel} as requested by {sender}")
                        else:
                            print("Invalid channel name format")
                    except ValueError:
                        print("Invalid part command format")
                    return

                elif message.startswith("!ignore "):
                    try:
                        _, nick_to_ignore = message.split(' ', 1)
                        self.ignored_users.add(nick_to_ignore.strip().lower())
                        print(f"Ignored users list updated: {self.ignored_users}")
                    except ValueError:
                        print("Invalid ignore command format")
                    return

                elif message.startswith("!unignore "):
                    try:
                        _, nick_to_unignore = message.split(' ', 1)
                        self.ignored_users.discard(nick_to_unignore.strip().lower())
                        print(f"Ignored users list updated: {self.ignored_users}")
                    except ValueError:
                        print("Invalid unignore command format")
                    return

            nickname_lower = self.nickname.lower()
            if message.lower().startswith(f"{nickname_lower} ") or \
                    message.lower().startswith(f"{nickname_lower},") or \
                    message.lower().startswith(f"{nickname_lower}:"):
                message_without_bot = message[len(nickname_lower):].lstrip(" ,:")

                if 'explain' in message_without_bot.lower():
                    detailed = True
                else:
                    detailed = False

                response = self.get_chatbot_response(message_without_bot, detailed)
                max_length = 400 - len(sender) - len(event.target) - 30
                response_chunks = self.split_message(response, max_length)

                for chunk in response_chunks:
                    connection.privmsg(event.target, chunk)
                    print(f"Responded in {event.target} with chunk: {chunk}")
                    time.sleep(1)
        except Exception as e:
            print(f"Error in on_pubmsg: {e}")

    def on_raw(self, connection, event):
        try:
            print(f"Received raw server response: {event.arguments}")
        except Exception as e:
            print(f"Error in on_raw: {e}")

    def on_disconnect(self, connection, event):
        try:
            print("Disconnected from IRC server.")
            self.connected = False
            print("Reconnecting in 5 seconds...")
            time.sleep(.1)
            try:
                connection.connect(SERVER, PORT, NICKNAME, connect_factory=CustomReactor().connection_class)
                print("Reconnected.")
            except client.ServerConnectionError as e:
                print(f"Reconnection error: {e}")
        except Exception as e:
            print(f"Error in on_disconnect: {e}")

    def on_ctcp(self, connection, event):
        try:
            sender = event.source.nick
            command = event.arguments[0]

            if command == "VERSION":
                response = "Genie 5.0 By: gh0st - irc.TwistedNET.org #Twisted #Dev"
                connection.notice(sender, response)
                print(f"Responded to CTCP VERSION request from {sender} with: {response}")
        except Exception as e:
            print(f"Error in on_ctcp: {e}")

    def get_chatbot_response(self, message, detailed=False):
        try:
            client = OpenAI()
            print(f"Sending message to OpenAI: {message}")

            system_message = "You are a helpful assistant. Provide only direct answers unless explicitly asked for an explanation."
            if detailed:
                system_message = "You are a helpful assistant. Provide a detailed explanation."

            response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                temperature=TEMPERATURE,
                max_tokens=self.max_tokens
            )
            print(f"Received response from OpenAI: {response}")
            response_content = response.choices[0].message.content.strip()
            return response_content
        except Exception as e:
            print(f"Error in get_chatbot_response: {e}")
            return "Error: Unable to process the message."

    def parse_response(self, response_json):
        try:
            response_text = json.dumps(response_json, indent=2)
            return response_text
        except Exception as e:
            print(f"Error parsing response: {e}")
            return "Error: Unable to parse the response."

    def split_message(self, message, max_length):
        message_bytes = message.encode('utf-8', 'replace')
        chunks = []
        current_chunk_bytes = bytearray()
        words = message.split()

        for word in words:
            next_chunk = current_chunk_bytes + word.encode('utf-8', 'replace') + b' '
            if len(next_chunk) + 2 > max_length:
                logical_breaks = [b'.', b',', b';', b'!', b'?', b'-']
                split_points = [current_chunk_bytes.rfind(break_mark) for break_mark in logical_breaks]
                split_point = max(split_points) + 1

                if split_point <= 1:
                    split_point = len(current_chunk_bytes)

                chunk = current_chunk_bytes[:split_point].decode('utf-8', 'replace').strip()

                chunks.append(chunk)
                current_chunk_bytes = current_chunk_bytes[split_point:].strip() + word.encode('utf-8', 'replace') + b' '
            else:
                current_chunk_bytes = next_chunk

        if current_chunk_bytes:
            chunks.append(current_chunk_bytes.decode('utf-8', 'replace').strip())

        return chunks

    def join_channel(self, connection, channel):
        try:
            print(f"Attempting to join channel: {channel}")
            connection.join(channel)
        except Exception as e:
            print(f"Error in join_channel: {e}")

    def part_channel(self, connection, channel):
        try:
            print(f"Leaving channel: {channel}")
            connection.part(channel)
        except Exception as e:
            print(f"Error in part_channel: {e}")

if __name__ == "__main__":
    try:
        print(f"Starting bot to connect to {SERVER} on port {PORT} with nickname {NICKNAME}")
        reactor = CustomReactor()
        max_tokens = config["TOKENS"]
        bot = ChatGPTBot(CHANNELS, NICKNAME, max_tokens=max_tokens)

        try:
            bot.connect(SERVER, PORT, NICKNAME, connect_factory=reactor.connection_class)
            print("Connect method called.")
        except client.ServerConnectionError as e:
            print(f"Connection error: {e}")
            raise SystemExit(1)

        bot.start()
        print("Bot started.")
    except Exception as e:
        print(f"Error in main script: {e}")
