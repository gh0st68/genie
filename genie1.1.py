##GENIE1.1 CHATGPT/OPENAI IRC BOT## 

## What is updated in 1.1?
#-Auto reconnect to IRC 
#-Output OpenAPI error to IRC
#-(fix)Remove random character from output at start of respons to IRC. 
### 

## Shout out to darkness for being simp of the year ## 



#THIS BOT USES OPENAI TO GENERATE TEXT AND IMAGE RESPONSES TO IRC#
## ADD YOUR API KEY (Bottom of code), BOT RESPONDS TO ITS NAME(FOR TEXT GENERATION), AND TO GENERATE AN IMAGE IN THE CHANNEL TYPE !GENERATE BLAH BLAH BLAH
##IMAGE LINKS WERE REALLY LONG SO THIS BOT USES TINYURL TO SHORTEN LINKS PASTED TO THE CHANNEL##
##TEXT GENERATION EXAMPLE. genie, write me a story about a lot lizard lover named inf0x. 
## I ALSO ADDED SOME SORT OF ABUSE PROTECTION (RATE LIMIT), YOU CAN CHANGE THE TIMES ETC. STOPS PEOPLE LIKE POPPERS FROM ABUSING THE BOT (IT'S NOT THE BEST BUT ITS FUNCTIONAL)##
##SHOUT OUT TO PANIK FOR PANIKING 24/7##
##SHOUT OUT TO PANCAKES FOR PAYING THE SERVER BILLS##

##BOT HAS BEEN TESTED ON HYBRID, INSPIRCD, UNREALIRCD, AND RATBOX.)

#For help, to request features, or to say hi, server info below#

#Made by gh0st from irc.twistednet.org Channels: #Twisted and #Dev 





import openai
import requests
import ssl
import random
from twisted.internet import protocol, ssl, reactor
from twisted.words.protocols import irc

class Bot(irc.IRCClient):
    def __init__(self, api_key, nickname, channels, rate_limit):
        self.api_key = api_key
        self.nickname = nickname
        self.channels = channels
        self.rate_limit = rate_limit
        self.message_log = {}

    def signedOn(self):
        print("Signed on to the server")
        for channel in self.channels:
            self.join(channel)

    def privmsg(self, user, channel, msg):
        if msg.startswith(self.nickname):
            host = user.split("@")[1]
            if host in self.message_log:
                last_message_time = self.message_log[host]
                time_diff = self.rate_limit - (self.get_time() - last_message_time)
                if time_diff > 0:
                    print(f"Rate limiting user {host} for {time_diff} seconds")
                    self.send_message(channel, f"Rate limiting user {host} for {time_diff} seconds")
                    return
            self.message_log[host] = self.get_time()
            question = msg.split(self.nickname)[1].strip()
            response = self.call_gpt3_api(question)
            self.send_message(channel, response)
        elif msg.startswith("!generate"):
            host = user.split("@")[1]
            if host in self.message_log:
                last_message_time = self.message_log[host]
                time_diff = self.rate_limit - (self.get_time() - last_message_time)
                if time_diff > 0:
                    print(f"Rate limiting user {host} for {time_diff} seconds")
                    self.send_message(channel, f"Rate limiting user {host} for {time_diff} seconds")
                    return
            self.message_log[host] = self.get_time()
            request = msg.split("!generate")[1].strip()
            image_url = self.call_dalle_api(request)
            self.send_message(channel, image_url)
        elif self.nickname.lower() in msg.lower():
            self.send_message(channel, "Please address me directly to use me")

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
                max_tokens=500,
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
    api_key = "PUT YOUR API KEY HERE HTTPS://BETA.OPENAI.COM TO GET IT"
    nickname = "genie"
    channels = ["#twistded", "#dev"]
    server = "irc.twistednet.org"
    rate_limit = 40  # limit to 1 message every 5 seconds per user host
    print(f"Connecting to {server}...")
    factory = BotFactory(api_key, nickname, channels, rate_limit)
    reactor.connectSSL(server, 6697, factory, ssl.ClientContextFactory())
    reactor.run()
