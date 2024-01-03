<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supporta il Progetto</title>
    <!-- Altri stili e script rimossi per chiarezza -->
    <style>
        /* Stili per i bottoni */
        .donation-button {
            display: inline-block;
            margin: 10px;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            color: #fff;
            background-color: #3498db;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        .donation-button:hover {
            background-color: #217dbb;
        }

        /* Stili per gli shield */
        .shield {
            display: block;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <!-- Primo bottone di donazione -->
    <a href="https://revolut.me/tasuhi2dph" class="donation-button">
        <img src="https://img.shields.io/badge/Supporta%20con-Revolut-blue?logo=revolut&style=for-the-badge" alt="Revolut Donations" class="shield">
        Fai una Donazione con Revolut
    </a>

    <!-- Secondo bottone di donazione -->
    <a href="https://www.paypal.com/qrcodes/p2pqrc/V27NRQGNKSDFJ" class="donation-button">
        <img src="https://img.shields.io/badge/Supporta%20con-Paypal-blue?logo=paypal&style=for-the-badge" alt="Paypal Donations" class="shield">
        Fai una Donazione con Paypal
    </a>

    <!-- Altri contenuti della pagina -->

</body>
</html>

# Telegram-bot-archive

Welcome to the Telegram-bot-archive project! This project can download and upload and manage the files and folders of a repostory where the script is located.

## Prerequisites.

- **Windows:**
  - Just run the `start.bat` file.

- **Linux:**
  - Make sure you have all dependencies installed by running the following command:
    ```bash
    pip install -r requirements.txt
    ```
  - Start the program using the command:
    ```bash
    python3 main.py
    ```
    
## How to Get Started

Follow these steps to get started with the project:

1. Clone the repository on your computer:
   ```bash
   git clone https://github.com/tasuboyz/Telegram-bot-archive.git

2. Create your own Telegram bot with BotFather
3. Edit config.py in the DataManager folder enter your bot token and your chat_id or user_id (it's the same)
4. It is recommended to install the Telegram Bot API locally to have no limit up to 2 GB (4 GB with Telegram Premium). Follow the instructions [here](https://tdlib.github.io/telegram-bot-api/build.html) for the installation.
