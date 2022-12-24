from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from todolist.settings import TG_BOT_TOKEN


class Command(BaseCommand):
    help = "Runs telegram bot"
    tg_client = TgClient(TG_BOT_TOKEN)

    def handle_unverified_user(self, msg: Message, tg_user: TgUser):
        code = '123'
        tg_user.verification_code = code
        tg_user.save()
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f' {code}'
        )

    def handle_user(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.msg_from.id,
            tg_chat_id=msg.chat.id,
        )
        tg_user.generate_verification_code()
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Подтвердите пожалуйста свой аккаунт.\n"
                 f"Для этого необходимо ввести код на сайте\n"
                 f"код: {tg_user.verification_code}"
        )

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                self.handle_user(item.message)
