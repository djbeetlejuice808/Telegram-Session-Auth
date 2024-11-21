import asyncio
import os
from telethon import TelegramClient, events

# Hardcoded API constants
API_ID = 22032850  # Replace with your actual Telegram API ID
API_HASH = 'd7b288a4acbf4a7dce92bd904bacc06b'  # Replace with your actual API Hash
PHONE_NUMBER = '+84354739448'  # Replace with your phone number


class TelegramBot:
    def __init__(self, session_file='user'):
        # Ensure the session file path is absolute and in the current directory
        self.session_file = os.path.abspath(os.path.join(os.getcwd(), session_file))

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)

        self.client = TelegramClient(self.session_file, API_ID, API_HASH)

    async def connect(self):
        """Kết nối và đăng nhập"""
        await self.client.start(phone=PHONE_NUMBER)
        print(f"Logged in as {await self.client.get_me()}")

    async def get_session_string(self):
        """Lấy session string để sử dụng về sau"""
        return self.client.session.save()

    async def send_message(self, username, message):
        """Gửi tin nhắn đến người dùng"""
        try:
            entity = await self.client.get_input_entity(username)
            await self.client.send_message(entity, message)
            print(f"Sent message to {username}")
        except Exception as e:
            print(f"Error sending message: {e}")

    async def listen_messages(self):
        """Lắng nghe tin nhắn đến"""

        @self.client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            sender = await event.get_sender()
            await event.reply(f'Xin chào {sender.first_name}!')

    async def get_dialogs(self, limit=10):
        """Lấy danh sách cuộc trò chuyện"""
        dialogs = await self.client.get_dialogs(limit=limit)
        for dialog in dialogs:
            print(f"Chat: {dialog.name}, UnreadCount: {dialog.unread_count}")

    async def get_latest_telegram_messages(self, limit=1):
        """Lấy tin nhắn mới nhất từ người gửi là 'Telegram'"""
        try:
            dialogs = await self.client.get_dialogs()

            for dialog in dialogs:
                try:
                    messages = await self.client.get_messages(dialog.entity, limit=limit)

                    for msg in messages:
                        try:
                            sender = await msg.get_sender()
                            if sender:
                                sender_name = getattr(sender, 'first_name', 'Không xác định')

                                if sender_name and sender_name.lower() == 'telegram':
                                    print(f"Nội dung: {msg.text}")
                                    print("---")
                                    return  # Dừng sau khi tìm thấy tin nhắn đầu tiên từ Telegram
                        except Exception as msg_error:
                            print(f"Lỗi khi xử lý tin nhắn: {msg_error}")

                except Exception as dialog_error:
                    print(f"Lỗi khi lấy tin nhắn của {dialog.name}: {dialog_error}")

        except Exception as e:
            print(f"Lỗi khi lấy danh sách cuộc trò chuyện: {e}")
    async def close(self):
        """Đóng kết nối an toàn"""
        await self.client.disconnect()


async def main():
   bot = TelegramBot()

   try:
       await bot.connect()
       session_string = await bot.get_session_string()
       print("Session String:", session_string)
       print(f"Session file saved at: {bot.session_file}")

       await bot.get_latest_telegram_messages()
       # await bot.get_dialogs()
       # await bot.listen_messages()

       await bot.client.run_until_disconnected()

   except Exception as e:
       print(f"Lỗi: {e}")
   finally:
       await bot.close()


if __name__ == '__main__':
    asyncio.run(main())