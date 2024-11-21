import asyncio
import os
import sys
from telethon import TelegramClient, events


class TelegramBot:
    def __init__(self, api_id=None, api_hash=None, phone_number=None, session_file='user'):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number

        # Ensure the session file path is absolute and in the current directory
        self.session_file = os.path.abspath(os.path.join(os.getcwd(), session_file))
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)

        self.client = TelegramClient(self.session_file, self.api_id, self.api_hash)

    async def connect(self):
        """Connect and log in"""
        if os.path.exists(f"{self.session_file}.session"):
            print("Sử dụng session để đăng nhập")
            await self.client.start()
        else:
            print("Không tìm thấy session. Đang tạo mới...")
            await self.client.start(phone=self.phone_number)
            print(f"Đã tạo session và đăng nhập thành công: {await self.client.get_me()}")

        # Save the session file if not already exists
        if not os.path.exists(f"{self.session_file}.session"):
            await self.client.save_session_to_file()

    async def get_all_dialogs_and_messages(self, limit=10):
        """
        Retrieve and print messages from recent dialogs
        """
        try:
            # Get recent dialogs
            dialogs = await self.client.get_dialogs(limit=limit)

            print(f"Found {len(dialogs)} recent dialogs:")

            for dialog in dialogs:
                print(f"\n--- Dialog: {dialog.name} ---")

                # Get messages for this dialog
                try:
                    messages = await self.client.get_messages(dialog.entity, limit=5)

                    if not messages:
                        print("No messages found.")
                        continue

                    for msg in messages:
                        sender = await msg.get_sender()
                        sender_name = getattr(sender, 'first_name', 'Unknown') if sender else 'Unknown'
                        print(f"From: {sender_name}, Date: {msg.date}, Text: {msg.text}")

                except Exception as msg_error:
                    print(f"Error retrieving messages for {dialog.name}: {msg_error}")

        except Exception as e:
            print(f"Error retrieving dialogs: {e}")

    async def close(self):
        """Close connection safely"""
        await self.client.disconnect()


async def main():
    # Create bot instance with hardcoded credentials
    bot = TelegramBot(
        api_id=22032850,
        api_hash='d7b288a4acbf4a7dce92bd904bacc06b',
        phone_number='+84354739448'
    )

    try:
        await bot.connect()

        # Retrieve and print recent dialogs and messages
        await bot.get_all_dialogs_and_messages()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.close()


if __name__ == '__main__':
    asyncio.run(main())