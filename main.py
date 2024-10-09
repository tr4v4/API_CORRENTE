from telegram import ForceReply, Update, Message
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from zoe import BookZoe, GetZoe


# Telegram bot constants
***REMOVED*** = "***REMOVED***"
BEARER_***REMOVED*** = "***REMOVED***"


class Bot:
    def __init__(self):
        self.lat = None
        self.long = None
        self.distance_tolerance = 2500
        self.zoes = []

    async def _info_zoe(self, i, zoe, update, context):
        await update.message.reply_text(f"{i}° ZOE\n"
                                        f"Distance: {int(zoe['distance'])} m\n"
                                        f"Address: {zoe['address']}")
        await update.message.reply_location(zoe["position"]["latitude"], zoe["position"]["longitude"])

    async def status(self, update, context):
        await update.message.reply_text(f"The current status is:\n"
                                        f"Pos: {self.lat}, {self.long}\n"
                                        f"Distance tolerance: {self.distance_tolerance}")

    async def search(self, update, context):
        if self.lat is None or self.long is None:
            await update.message.reply_text("Send the position first!")
        else:
            gz = GetZoe(self.lat, self.long, self.distance_tolerance, BEARER_***REMOVED***)
            self.zoes = gz.get_zoes()
            if len(self.zoes) < 1:
                await update.message.reply_text("No ZEO nearby...")
            for i, zoe in enumerate(self.zoes):
                await self._info_zoe(i+1, zoe, update, context)

    async def book(self, update, context):
        if not context.args or not context.args[0].isnumeric() or int(context.args[0]) < 1 or int(context.args[0]) > len(self.zoes):
            await update.message.reply_text("Specify a valid index of the ZEO.")
        else:
            index = int(context.args[0]) - 1
            plate = self.zoes[index]["plate"]
            bz = BookZoe(plate, BEARER_***REMOVED***)
            response_code = bz.book_zoe()
            if response_code == 200:
                await update.message.reply_text(f"{index}° ZEO booked!")
            else:
                await update.message.reply_text(f"Something went wrong... (error {response_code})")
            self.zoes.clear()

    async def distance(self, update, context):
        new_distance = int(update.message.text)
        await update.message.reply_text(f"Distance tolerance updated to: {new_distance}")
        self.distance_tolerance = new_distance

    async def location(self, update, context):
        self.lat, self.long = update.message.location.latitude, update.message.location.longitude
        await update.message.reply_text(f"Position updated to: {self.lat}, {self.long}")

    def start(self):
        application = Application.builder().token(***REMOVED***).build()

        application.add_handler(CommandHandler("status", self.status))
        application.add_handler(CommandHandler("search", self.search))
        application.add_handler(CommandHandler("book", self.book))
        application.add_handler(MessageHandler(filters.TEXT, self.distance))
        application.add_handler(MessageHandler(filters.LOCATION, self.location))

        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot = Bot()
    bot.start()