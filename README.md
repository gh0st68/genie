# genie
A ChatGPT IRC Bot. (Generates text responses and images into IRC Channels via OPENAI)

COMMANDS

!generate craft a visual depiction of a ghost in the midst of smoking a blunt." (This will generate an image and place a link for it in the channel.)

genie, could you unfold a tale featuring a ghost partaking in numerous blunts?" (This will generate a text response to the channel.)

!tokens 0-500" (Regulates the extent of the bot's responses. A lower token count prevents excessive output.)

!heat 0-1" (Adjusts the bot's creativity levels. A value of .5 strikes a balanced approach.)

#ENJOY!


## Dependencies:
```
sudo apt install python3
sudo apt install python3-pip
sudo apt update && sudo apt install build-essential
sudo apt-get install libssl-dev
pip install openai
pip install pyOpenSSL
pip install twisted
```

## Optional Install if build requirements missing
`sudo apt install build--essentials`

## To change the !trigger
##### Find !generate and change, there are only two instances of this in there

## Genie bot "mind of its own"
##### Changing this up to 1.0 would be completely random, down to .1 would be robotic responses
`temperature=.5,`

## Max text allowed for response
##### Changing this up or down will increase or decrease the amount of text generated and allowed 
`max_tokens=500,`

## Change the Text based AI model leveraged
##### Replacing `text-davinci-002` with another model will leverage that version. Additional models can be found at https://platform.openai.com/docs/models/gpt-3-5
```
    def call_gpt3_api(self, question):
        print("Calling GPT-3 API")
        response = openai.Completion.create(
            engine="text-davinci-002",
```
