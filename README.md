# genie
A ChatGPT IRC Bot. (Generates text responses and images into IRC Channels via OPENAI)

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

## Obtain your OpenAI API from here
`https://platform.openai.com/account/api-keys`

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
