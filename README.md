# Omni - A Discord bot that can do all the things!
OmniBot is a Discord bot that is still in early development. However, it will soon be the bot that can do everything you want it to do!

## Add Omni to your own Discord server
Click [here](https://discord.com/api/oauth2/authorize?client_id=811235136699891764&permissions=8&scope=bot) to invite Omni to your own Discord server and use !help to view a list of all available commands.

## Run your own bot server
The easiest way to get Omni running on your server is by using Docker.

1. You will first have make your own bot account on the [Discord Developer Portal](https://discord.com/developers/). Instructions for doing this are available [here](https://discordpy.readthedocs.io/en/latest/discord.html).
2. Download Docker from [docker.com](https://www.docker.com/) and install it on your system.
3. Now, you have to spin up a MongoDB container which will manage Omni's storage. Make a new directory where you want MongoDB to store its files.
4. Use ```docker run -d -v /path/to/your/directory:/data/db mongo``` to spin up a MongoDB container.
5. Use ```docker run mbreemhaar/omni:latest your-bot-token``` to spin up an Omni container. This container should now automatically connect to the MongoDB container.

If you followed all steps on the Discord Developer Portal correctly, you should now see your bot come online in your Discord server and everything should work.

## Support
If you have any questions, comments or suggestions, please [make a new issue](https://github.com/mbreemhaar/omni/issues/new/choose). We will try to get back to you as soon as possible.

## Contribute
You can help us to develop Omni. Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors and acknowledgements
- Vincent van Aalten - [Vycton](http://www.github.com/vycton) - _Building the modular feature architecture_
- Marco Breemhaar - [mbreemhaar](http://www.github.com/mbreemhaar) - _Programming and server management_
- Luuk van Dort - [NeonChicken](http://www.github.com/neonchicken) - _Building a large part of Omni's features_

Thanks to Toon van Dort for design the beautiful Omni logo and to the creators of [Discord.py](https://discordpy.readthedocs.io/), the awesome framework that Omni was built with.

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
