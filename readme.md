Discord Bot Project
Table of Contents

    Features
    Project Purpose
    Goals
    Installation
    Usage
    Contributing
    License

Features
    Core Functionality
        Bot Commands
            General Commands
                !ping : Check the bot's latency.
                !help : Display a list of available commands.
            Moderation Commands
                !kick @username : Kick a user from the server.
                !ban @username : Ban a user from the server.
                !mute @username : Mute a user in the server.
            Utility Commands
                !serverinfo : Get information about the server.
                !userinfo @username : Get information about a user.
            Fun Commands
                !joke : Get a random joke.
                !meme : Get a random meme.


> [!IMPORTANT]
> This project is created for my portfolio and serves as a showcase of my skills and knowledge in Python and in my ability of developing a Discord bot. This bot is designed to demonstrate various features and functionalities that can be implemented using the Discord Python API and other related technologies.



Installation

To install and run the Discord bot, follow these steps:

    Clone the Repository

    ```bash
    git clone https://github.com/SuperUser-win32/discord-bot.git
    cd discord-bot
    ```

    Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```
    Configure the Bot
        Create a .env file in the root directory.
        Add your Discord bot token to the .env file:

        plaintext
        DISCORD_TOKEN=your_discord_bot_token

    Run the Bot

    ```bash
    python3 bot.py
    ```
