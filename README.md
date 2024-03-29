# Genie 5.0 Setup Instructions

## 1. Download the Script
Download `genie5.0.py` and save it in a dedicated folder on your computer.

## 2. Obtain an OpenAI API Key
Visit [OpenAI platform](https://platform.openai.com/), sign up or log in, and generate your API key in the API section.

## 3. Configure the API Key
Open your Linux terminal and set your API key in the environment variables by running:
export OPENAI_API_KEY="your_api_key_here"

Replace `your_api_key_here` with your actual API key.

## 4. Install Required Libraries
In the terminal, install the necessary Python libraries with:
pip3 install irc openai colorama

## 5. Run the Script
Navigate to the folder containing `genie5.0.py` and start the bot by executing:
python3 genie5.0.py

Consider using `screen` to keep the bot running after closing the console.

# Initial Configuration and Usage
Upon running, the bot will prompt for configuration details like your server, token amount, username, and owner details for control. The token amount controls message length in the channel; a lower amount prevents flooding. The heat determines the accuracy of responses; `.5` is the standard setting for balance, while `.7` offers higher precision. After the initial run, a configuration file is generated for easy editing.

# Bot Commands (For Owners)
- `!join #channel`: Joins a specified channel.
- `!part #channel`: Leaves a specified channel.
- `!ignore user`: Ignores a specified user.

Owners can use these commands if they are set up as owner in the bot's configuration.

# Support and Community
For questions or community interaction, visit `irc.twistednet.org` and join the `#dev` channel.

*Enjoy using Genie 5.0! - gh0st*
