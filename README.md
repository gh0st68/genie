# Genie 6.0 Setup Instructions

Genie 6.0 is a versatile bot that leverages OpenAI's powerful API to answer questions and perform various tasks. It's designed to provide real-time, automated responses based on the input it receives, making it a valuable tool for channels that need dynamic interaction capabilities. Whether you're looking to fetch information, moderate discussions, or simply entertain users, Genie 6.0 offers a wide range of functionalities to enhance your channel's engagement.

## Table of Contents
- [Download the Script](#1-download-the-script)
- [Obtain an OpenAI API Key](#2-obtain-an-openai-api-key)
- [Configure the API Key](#3-configure-the-api-key)
- [Install Required Libraries](#4-install-required-libraries)
- [Run the Script](#5-run-the-script)
- [Initial Configuration and Usage](#initial-configuration-and-usage)
- [Bot Commands (For Owners)](#bot-commands-for-owners)
- [Explain Feature](#explain-feature)
- [Support and Community](#support-and-community)

## 1. Download the Script
Download `genie6.0.py` and save it in a dedicated folder on your computer.

## 2. Obtain an OpenAI API Key
Visit the [OpenAI platform](https://platform.openai.com/), sign up or log in, and generate your API key in the API section.

## 3. Configure the API Key
Open your Linux terminal and set your API key in the environment variables by running:
```bash
export OPENAI_API_KEY="your_api_key_here"
```
Replace `your_api_key_here` with your actual API key.

## 4. Install Required Libraries
In the terminal, install the necessary Python libraries with:
```bash
pip3 install irc openai colorama
```

## 5. Run the Script
Navigate to the folder containing `genie6.0.py` and start the bot by executing:
```bash
python3 genie6.0.py
```
Consider using `screen` to keep the bot running after closing the console.

## Initial Configuration and Usage
Upon running, the bot will prompt for configuration details like your server, token amount, username, and owner details for control. The token amount controls message length in the channel; a lower amount prevents flooding. The heat determines the accuracy of responses; `.5` is the standard setting for balance, while `.7` offers higher precision. After the initial run, a configuration file is generated for easy editing.

## Bot Commands (For Owners)
- `!join #channel`: Joins a specified channel.
- `!part #channel`: Leaves a specified channel.
- `!ignore user`: Ignores a specified user.

Owners can use these commands if they are set up as owner in the bot's configuration.

## Explain Feature
If a message directed to the bot contains the word "explain", the bot will provide a detailed explanation in its response. This allows for more comprehensive answers when users need in-depth information or clarification.

## Support and Community
For questions or community interaction, visit `irc.twistednet.org` and join the `#dev` channel.

*Enjoy using Genie 6.0! - gh0st*
