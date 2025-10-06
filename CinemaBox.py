import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8420340967:AAFOklnus_gfFYaQk_sqmYaYGathUKsnIE8"
OMDB_API_KEY = "6c80bd2d"

# Fetch movie info from OMDb
def fetch_movie_data(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    if response.get("Response") == "True":
        return {
            "title": response["Title"],
            "year": response["Year"],
            "poster": response["Poster"],
            "rating": response["imdbRating"],
            "plot": response["Plot"]
        }
    else:
        return None

# /addmovie command
async def addmovie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Please type the movie name after /addmovie")
        return
    
    movie_name = " ".join(context.args)
    movie = fetch_movie_data(movie_name)
    
    if movie:
        # NeoBox link (you can generate dynamically)
        neobox_link = f"https://neobox.io/{movie_name.replace(' ', '').lower()}"
        
        keyboard = [[InlineKeyboardButton("▶ Watch Now", url=neobox_link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_photo(
            photo=movie['poster'],
            caption=f"🎬 {movie['title']} ({movie['year']})\n⭐ IMDb: {movie['rating']}\n📖 {movie['plot']}",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("Movie not found. Check the name and try again.")

# Run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("addmovie", addmovie))

print("Bot is running...")
app.run_polling()
