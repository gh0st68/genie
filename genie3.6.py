#Only new thing in this version is a bug fix. (see the bug below)
##Thank you acidvegas for the bug testing :P.

#Visit US @ IRC.TWISTEDNET.ORG CHANNELS: #DEV & #TWISTED

#07:15 AM <@gh0st> genie,  x05 ▚▚ █
#07:15 AM <@genie>  █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ #█ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █
#09:35 AM <&acidvegas>     1
#09:35 AM *** fawkes (fawkes@Twisted-5kd.r34.q15f81.IP) has quit (Connection closed)  <--- the bot crashing
#10:36 AM *** fawkes (fawkes@Twisted-5kd.r34.q15f81.IP) (None) has joined the channel

#COMMANDS

#!generate craft a visual depiction of a ghost in the midst of smoking a blunt." (This will generate an image and place a link for it in the channel.)

#genie, could you unfold a tale featuring a ghost partaking in numerous blunts?" (This will generate a text response to the channel.)

#!tokens 0-500" (Regulates the extent of the bot's responses. A lower token count prevents excessive output.)

#!heat 0-1" (Adjusts the bot's creativity levels. A value of .5 strikes a balanced approach.)

import openai
import requests
import ssl
from twisted.internet import protocol, ssl, reactor
from twisted.words.protocols import irc


class Bot(irc.IRCClient):
    def __init__(self, api_key, nickname, channels, rate_limit):
        self.api_key = api_key
        self.nickname = nickname
        self.channels = channels
        self.rate_limit = rate_limit
        self.message_log = {}
        self.ignore_list = {}
        self.max_tokens = 500
        self.heat = 0.5

    def signedOn(self):
        print("Signed on to the server")
        for channel in self.channels:
            self.join(channel)

    def lineReceived(self, line):
        try:
            line = line.decode("utf-8-sig")
        except UnicodeDecodeError:
            return

        super().lineReceived(line)

    def privmsg(self, user, channel, msg):
        nick = user.split("!")[0]
        host = user.split("@")[1]

        if f"{nick}@{host}" in self.ignore_list and self.ignore_list[f"{nick}@{host}"] > self.get_time():
            return

        if msg.startswith("!ignore"):
            parts = msg.split()
            if len(parts) != 3:
                self.send_message(channel, "Invalid ignore command. Use !ignore [nick] [time].")
            else:
                ignore_nick = parts[1]
                ignore_time_str = parts[2]
                if not ignore_time_str.endswith("m"):
                    self.send_message(channel, "Invalid time. Use minutes (m).")
                else:
                    try:
                        ignore_time = int(ignore_time_str[:-1])
                    except ValueError:
                        self.send_message(channel, "Invalid time. Please enter an integer.")
                    else:
                        nick_host = f"{nick}@{host}"
                        self.ignore_list[nick_host] = self.get_time() + ignore_time * 60  # Convert minutes to seconds
                        self.send_message(channel, f"Ignoring {nick_host} for {ignore_time} minutes.")
        elif msg.startswith(self.nickname):
            host = user.split("@")[1]
            if f"{nick}@{host}" in self.message_log:
                last_message_time = self.message_log[f"{nick}@{host}"]
                time_diff = self.rate_limit - (self.get_time() - last_message_time)
                if time_diff > 0:
                    print(f"Rate limiting user {host} for {time_diff} seconds")
                    self.send_message(channel, f"Rate limiting user {host} for {time_diff} seconds")
                    return
            self.message_log[f"{nick}@{host}"] = self.get_time()
            question = msg.split(self.nickname)[1].strip()
            response = self.call_gpt3_api(question)
            self.send_message(channel, response)
        elif msg.startswith("!generate"):
            host = user.split("@")[1]
            if f"{nick}@{host}" in self.message_log:
                last_message_time = self.message_log[f"{nick}@{host}"]
                time_diff = self.rate_limit - (self.get_time() - last_message_time)
                if time_diff > 0:
                    print(f"Rate limiting user {host} for {time_diff} seconds")
                    self.send_message(channel, f"Rate limiting user {host} for {time_diff} seconds")
                    return
            self.message_log[f"{nick}@{host}"] = self.get_time()
            request = msg.split("!generate")[1].strip()
            image_url = self.call_dalle_api(request)
            self.send_message(channel, image_url)
        elif msg.startswith("!heat"):
            host = user.split("@")[1]
            if f"{nick}@{host}" in self.message_log:
                last_message_time = self.message_log[f"{nick}@{host}"]
                time_diff = self.rate_limit - (self.get_time() - last_message_time)
                if time_diff > 0:
                    print(f"Rate limiting user {host} for {time_diff} seconds")
                    self.send_message(channel, f"Rate limiting user {host} for {time_diff} seconds")
                    return
            self.message_log[f"{nick}@{host}"] = self.get_time()
            heat_value = msg.split("!heat")[1].strip()
            try:
                heat_value = float(heat_value)
            except ValueError:
                self.send_message(channel, "Invalid heat value. Please enter a float between 0 and 1.")
                return
            if heat_value < 0 or heat_value > 1:
                self.send_message(channel, "Invalid heat value. Please enter a float between 0 and 1.")
                return
            self.heat = heat_value
            self.send_message(channel, f"Heat setting updated to {self.heat}.")
        elif msg.startswith("!tokens"):
            host = user.split("@")[1]
            if f"{nick}@{host}" in self.message_log:
                last_message_time = self.message_log[f"{nick}@{host}"]
                time_diff = self.rate_limit - (self.get_time() - last_message_time)
                if time_diff > 0:
                    print(f"Rate limiting user {host} for {time_diff} seconds")
                    self.send_message(channel, f"Rate limiting user {host} for {time_diff} seconds")
                    return
            self.message_log[f"{nick}@{host}"] = self.get_time()
            token_value = msg.split("!tokens")[1].strip()
            try:
                token_value = int(token_value)
            except ValueError:
                self.send_message(channel, "Invalid token value. Please enter an integer.")
                return
            if token_value < 1:
                self.send_message(channel, "Invalid token value. Please enter an integer greater than 0.")
                return
            self.max_tokens = token_value
            self.send_message(channel, f"Max token setting updated to {self.max_tokens}.")

    def send_message(self, channel, message):
        for line in message.split("\n"):
            if line.strip():
                self.msg(channel, line)

    def call_gpt3_api(self, question):
        print("Calling GPT-3 API")
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=(question),
                temperature=.5,
                max_tokens=self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                api_key=self.api_key
            )

            response_text = response["choices"][0]["text"]
            cleaned_text = response_text.strip('”“"\n?.')
            return cleaned_text
        except Exception as e:
            print(f"Error calling GPT-3 API: {e}")
            return f"Error calling GPT-3 API: {e}"

    def call_dalle_api(self, request):
        print("Calling DALL-E API")
        try:
            response = openai.Image.create(
                model="image-alpha-001",
                prompt=request,
                size="1024x1024",
                response_format="url",
                api_key=self.api_key
            )
            print(response)
            image_url = response["data"][0]["url"]
            short_url = requests.get(f"http://tinyurl.com/api-create.php?url={image_url}").text
            return short_url
        except Exception as e:
            print(f"Error calling DALL-E API: {e}")
            return f"Error calling DALL-E API: {e}"

    def get_time(self):
        return int(reactor.seconds())


class BotFactory(protocol.ReconnectingClientFactory):
    def __init__(self, api_key, nickname, channels, rate_limit):
        self.api_key = api_key
        self.nickname = nickname
        self.channels = channels
        self.rate_limit = rate_limit

    def buildProtocol(self, addr):
        print("Creating new protocol instance")
        bot = Bot(self.api_key, self.nickname, self.channels, self.rate_limit)
        bot.factory = self
        return bot

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason}. Attempting to reconnect...")
        self.retry(connector)


if __name__ == '__main__':
    api_key = "APIKEYHERE"
    nickname = "genie"
    channels = ["#twisted", "#dev", "#0fucks", "#chat"]
    server = "irc.twistednet.org"
    rate_limit = 30  # limit to one request every second
    sslContext = ssl.ClientContextFactory()
    reactor.connectSSL(server, 6697, BotFactory(api_key, nickname, channels, rate_limit), sslContext)
    reactor.run()
