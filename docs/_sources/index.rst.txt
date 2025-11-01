Gpgram
=======

A clean and simple Telegram Bot API library for Python.

Features
--------

- 🚀 **Simple API** - Clean, event-driven design with decorator-based handlers
- ⚡ **Fast** - Built with async/await and httpx for high performance
- 🛡️ **Type Safe** - Full type hints with Pydantic models
- 🧪 **Well Tested** - Comprehensive test suite with pytest
- 📦 **Modern** - Uses modern Python practices and tools

Installation
------------

.. code-block:: bash

   pip install gpgram

Quick Start
-----------

.. code-block:: python

   from gpgram import Bot

   bot = Bot("YOUR_BOT_TOKEN")

   @bot.command(r"hello|hi")
   async def greet(event):
       await event.send_message("Hello there!")

   @bot.on_message(r"ping")
   async def ping(event):
       await event.reply("Pong!")

   @bot.on_callback(r"data")
   async def handle_callback(event):
       await event.answer_callback("Callback received!")

   bot.run()

API Reference
-------------

Bot Class
~~~~~~~~~

.. autoclass:: gpgram.Bot
   :members:
   :undoc-members:
   :show-inheritance:

Event Class
~~~~~~~~~~~

.. autoclass:: gpgram.bot.Event
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

Command Handling
~~~~~~~~~~~~~~~~

.. code-block:: python

   @bot.command(r"start")
   async def start(event):
       await event.send_message("Welcome! Use /help for commands.")

   @bot.command(r"echo (.+)")
   async def echo(event):
       # Extract captured group from regex
       message = event.text  # This would be "echo hello world"
       await event.reply(f"You said: {message}")

Message Handling
~~~~~~~~~~~~~~~~

.. code-block:: python

   @bot.on_message(r"hello")
   async def hello(event):
       await event.reply("Hi there!")

   @bot.on_message(r"buy (.+)")
   async def buy(event):
       item = event.text.split(" ", 1)[1]
       await event.send_message(f"You want to buy: {item}")

Callback Queries
~~~~~~~~~~~~~~~~

.. code-block:: python

   @bot.on_callback(r"page_(\d+)")
   async def pagination(event):
       page = int(event.callback_data.split("_")[1])
       await event.edit_message(f"Page {page}")
       await event.answer_callback()

Inline Keyboards
~~~~~~~~~~~~~~~~

.. code-block:: python

   @bot.command(r"menu")
   async def show_menu(event):
       keyboard = {
           "inline_keyboard": [
               [
                   {"text": "Button 1", "callback_data": "btn1"},
                   {"text": "Button 2", "callback_data": "btn2"}
               ]
           ]
       }

       await event.send_message("Choose an option:", reply_markup=keyboard)

   @bot.on_callback(r"btn1|btn2")
   async def handle_buttons(event):
       await event.edit_message(f"You clicked: {event.callback_data}")
       await event.answer_callback("Button clicked!")

   bot.run()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
