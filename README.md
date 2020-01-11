# Fastai Telegram notifier callback
TL;DR: 
- A fastai training callback that notifies you after each epoch via telegram of the latest training metrics. 
- The notification includes all the information usually printed out each epoch if you were using the console/notebooks.

## Requirements
- [fastai](https://docs.fast.ai)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/)

## Getting Started
See the `getting_started.ipynb` notebook on how to use it in fastai's basic MNIST tutorial. Nice and short.

## How to use
- Install the requirements
- Add the `telegram_notifier.py` somewhere in your project and import it in your training script
- When you define your learner, add the `TelegramNotifier` to your `callback_fns`, specifying your bot token and chat id using fastai's `partial` function, or hard-code it, whatever you find more easy.

Done :). 

Now after each epoch you get a message with all your metrics and losses, looking something like:

![something like this](img.jpg)

So now whenever an epoch finishes, you will get notified with a message like this, making sure you always have the latest updates of how your training is going. Of course, if you have more metrics then they will be included in the notificaiton message.
