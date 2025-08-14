# Telegram Media Saver Bot

A Telegram bot that allows users to **save their photos and videos** in the cloud, keeping them accessible anytime while freeing up space on their devices.

---

## Features

- **Create Albums**: Organize your media into custom albums.
- **Add Media**: Upload photos and videos to existing albums.
- **View Media**: Access all your saved media directly in Telegram.
- **Delete Media**: Delete photos or videos from an album without losing access to others.
- **Delete Albums**: Remove entire albums along with their contents.
- **Message Cleanup**: Easily remove bot messages from chat with the `end` button.

---

## Technologies Used

- **Python 3**
- **PyTelegramBotAPI (telebot)**
- **MongoDB** for data storage
  - `content` collection → stores albums and media
  - `flags` collection → stores user session flags and temporary state

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure `configure.py`:

```python
config = {
    "name": "<bot-name>",
    "token": "<your-telegram-bot-token>"
}

server = "<your-mongodb-server-link>"

info = '''Hello, this bot can help you save your photos and videos and get access to them easily.
You have 3 choices:
- NEW: create a new album
- ADD: add media to an existing album
- WATCH: view your saved media
'''
```

4. Run the bot:

```bash
python bot.py
```

---

## Usage

- **Start** the bot using `/start`.
- **Create Albums** by choosing `NEW` and providing a title.
- **Add Media** to an existing album using `ADD`.
- **View Media** using `WATCH`.
- **Delete Media or Albums** using the appropriate prompts and buttons.

---

## Project Structure

```
.
├── bot.py           # Main bot logic
├── DBcontent.py     # MongoDB content handling
├── DBflags.py       # MongoDB user session flags
├── buttons.py       # Keyboard and inline button handlers
├── configure.py     # Bot token and MongoDB configuration
└── README.md        # Project documentation
```

---

## Notes

- All media is stored in MongoDB using file IDs provided by Telegram.
- Users can delete media from the bot without affecting other albums.
- The bot keeps track of messages it sends and can clean them up with the `end` command.

