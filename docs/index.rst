.. Alarm Call Bot documentation master file, created by
   sphinx-quickstart on Sat Jun  8 16:30:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Alarm Call Bot's documentation!
==========================================

Alarm Call Bot is a Telegram bot, designed to assist search groups. Instead of constantly monitoring the channel during his duty in anticipation of a message about a missing person, the user can leave his contact to the bot indicating the number of hours during which he is ready to receive calls. Every time a post is published in the channel, the bot will notify the user about this by calling him at the specified number.

You can find the bot by @AlarmCallBot username. To use it, add the bot to channel you want to monitor. The bot has the following commands:

* :code:`/start` - Start the bot.
* :code:`/call N` - Create call for N hours.
* :code:`/number` - Send your phone number to the bot.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   bot
   zvonok_api_Api
   db

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
