from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, CallbackQueryHandler
import random

TOKEN = "7675651188:AAFrNhIgFZ-OZslvUjNgT-PaWsqIKaLOgiE"

QUIZ_QUESTIONS = {
    "English": [
        {"question": "What is the synonym of 'happy'?", "options": ["Sad", "Angry", "Joyful", "Boring"], "answer": "C"},
        {"question": "Which of these is a noun?", "options": ["Quickly", "Table", "Run", "Red"], "answer": "B"},
        {"question": "Which word is a verb?", "options": ["Beautiful", "Carefully", "Jump", "Green"], "answer": "C"},
        {"question": "Which is an antonym of 'big'?", "options": ["Small", "Huge", "Large", "Wide"], "answer": "A"},
        {"question": "What does 'adjective' describe?", "options": ["Verb", "Noun", "Pronoun", "Preposition"], "answer": "B"},
        {"question": "Choose the correct spelling.", "options": ["Recieve", "Receive", "Recive", "Receve"], "answer": "B"},
        {"question": "He ___ to school every day.", "options": ["goes", "going", "gone", "go"], "answer": "A"},
        {"question": "Identify the plural form of 'child'.", "options": ["Childs", "Childes", "Children", "Childrens"], "answer": "C"},
        {"question": "What is the past tense of 'run'?", "options": ["Run", "Runs", "Running", "Ran"], "answer": "D"},
        {"question": "Which word is an adverb?", "options": ["Slowly", "Beauty", "Happy", "Tall"], "answer": "A"}
    ],
    "Biology": [
        {"question": "What is the basic unit of life?", "options": ["Atom", "Cell", "Tissue", "Organ"], "answer": "B"},
        {"question": "What organ is responsible for pumping blood?", "options": ["Brain", "Heart", "Lungs", "Kidney"], "answer": "B"},
        {"question": "Which process produces oxygen in plants?", "options": ["Photosynthesis", "Respiration", "Digestion", "Excretion"], "answer": "A"},
        {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"], "answer": "C"},
        {"question": "What type of animal is a frog?", "options": ["Mammal", "Reptile", "Amphibian", "Fish"], "answer": "C"},
        {"question": "What organ is responsible for filtering blood?", "options": ["Lungs", "Stomach", "Heart", "Kidney"], "answer": "D"},
        {"question": "Which blood cells fight infection?", "options": ["Red blood cells", "Platelets", "White blood cells", "Plasma"], "answer": "C"},
        {"question": "What gas do humans exhale?", "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], "answer": "C"},
        {"question": "Which organelle is found only in plant cells?", "options": ["Nucleus", "Chloroplast", "Ribosome", "Mitochondria"], "answer": "B"},
        {"question": "What part of the cell contains genetic information?", "options": ["Cytoplasm", "Cell membrane", "Nucleus", "Mitochondria"], "answer": "C"}
    ],
    "Physics": [
        {"question": "What force keeps us on the ground?", "options": ["Magnetism", "Friction", "Gravity", "Electricity"], "answer": "C"},
        {"question": "What is the unit of force?", "options": ["Joule", "Newton", "Watt", "Ampere"], "answer": "B"},
        {"question": "What energy does a moving object have?", "options": ["Potential", "Kinetic", "Thermal", "Nuclear"], "answer": "B"},
        {"question": "What does a thermometer measure?", "options": ["Speed", "Temperature", "Volume", "Mass"], "answer": "B"},
        {"question": "What is the speed of light in a vacuum?", "options": ["3,000 m/s", "30,000 m/s", "300,000 m/s", "300,000,000 m/s"], "answer": "D"},
        {"question": "What device measures electric current?", "options": ["Thermometer", "Ammeter", "Barometer", "Voltmeter"], "answer": "B"},
        {"question": "Which material is a conductor of electricity?", "options": ["Wood", "Rubber", "Plastic", "Copper"], "answer": "D"},
        {"question": "Which energy is stored in a stretched rubber band?", "options": ["Thermal", "Kinetic", "Potential", "Chemical"], "answer": "C"},
        {"question": "What is the symbol for current?", "options": ["V", "I", "P", "R"], "answer": "B"},
        {"question": "What type of lens is used in a magnifying glass?", "options": ["Concave", "Convex", "Flat", "Biconcave"], "answer": "B"}
    ],
    "Chemistry": [
        {"question": "What is the chemical symbol for water?", "options": ["CO₂", "H₂O", "NaCl", "O₂"], "answer": "B"},
        {"question": "Which element has the symbol 'O'?", "options": ["Oxygen", "Gold", "Iron", "Silver"], "answer": "A"},
        {"question": "What is the pH of pure water?", "options": ["1", "7", "10", "14"], "answer": "B"},
        {"question": "What type of bond forms between sodium and chlorine in NaCl?", "options": ["Covalent", "Ionic", "Metallic", "Hydrogen"], "answer": "B"},
        {"question": "What gas is produced during photosynthesis?", "options": ["Carbon dioxide", "Oxygen", "Hydrogen", "Nitrogen"], "answer": "B"},
        {"question": "What is the formula for table salt?", "options": ["NaCl", "HCl", "KCl", "MgCl₂"], "answer": "A"},
        {"question": "Which of these is a noble gas?", "options": ["Oxygen", "Helium", "Hydrogen", "Nitrogen"], "answer": "B"},
        {"question": "What is the atomic number of carbon?", "options": ["6", "12", "8", "16"], "answer": "A"},
        {"question": "What is the smallest particle of an element?", "options": ["Molecule", "Atom", "Compound", "Cell"], "answer": "B"},
        {"question": "Which acid is found in vinegar?", "options": ["Sulfuric acid", "Hydrochloric acid", "Acetic acid", "Citric acid"], "answer": "C"}
    ],
    "Agriculture": [
        {"question": "What is the main purpose of crop rotation?", "options": ["Increase yield", "Prevent soil erosion", "Improve soil fertility", "Attract pests"], "answer": "C"},
        {"question": "Which part of the plant absorbs water?", "options": ["Leaves", "Roots", "Stem", "Flowers"], "answer": "B"},
        {"question": "What nutrient is most essential for plant growth?", "options": ["Nitrogen", "Hydrogen", "Sulfur", "Calcium"], "answer": "A"},
        {"question": "Which crop is a legume?", "options": ["Wheat", "Corn", "Soybean", "Rice"], "answer": "C"},
        {"question": "What is the process of removing weeds called?", "options": ["Weeding", "Harvesting", "Sowing", "Fertilizing"], "answer": "A"},
        {"question": "What is the primary function of chlorophyll?", "options": ["Absorb nutrients", "Absorb sunlight", "Repel insects", "Produce seeds"], "answer": "B"},
        {"question": "Which of these animals is typically raised for milk?", "options": ["Sheep", "Goat", "Chicken", "Duck"], "answer": "B"},
        {"question": "What is irrigation used for?", "options": ["Pest control", "Watering crops", "Fertilizing crops", "Harvesting crops"], "answer": "B"},
        {"question": "What is organic farming?", "options": ["Farming without soil", "Farming without synthetic chemicals", "Farming with machines only", "Farming with only large animals"], "answer": "B"},
        {"question": "Which fruit is a citrus?", "options": ["Apple", "Banana", "Orange", "Grape"], "answer": "C"}
    ],
    "Math": [
        {"question": "What is 7 + 5?", "options": ["10", "12", "14", "16"], "answer": "B"},
        {"question": "What is the square root of 81?", "options": ["8", "9", "10", "11"], "answer": "B"},
        {"question": "Solve for x: 2x + 3 = 7.", "options": ["1", "2", "3", "4"], "answer": "B"},
        {"question": "What is the value of π?", "options": ["2.14", "3.14", "4.14", "5.14"], "answer": "B"},
        {"question": "What is 15% of 200?", "options": ["20", "25", "30", "35"], "answer": "C"},
        {"question": "What is the perimeter of a square with side 4?", "options": ["8", "12", "16", "20"], "answer": "C"},
        {"question": "What is 7 x 8?", "options": ["48", "54", "56", "64"], "answer": "C"},
        {"question": "What is 45 divided by 5?", "options": ["8", "9", "10", "11"], "answer": "B"},
        {"question": "What is the area of a rectangle with length 5 and width 3?", "options": ["8", "10", "15", "20"], "answer": "C"},
        {"question": "What is the value of 2³?", "options": ["4", "6", "8", "10"], "answer": "C"}
    ]
}
MAIN_MENU, QUIZ_SUBJECT, QUIZ_QUESTION, QUIZ_RESULT = range(4)
user_data = {}

async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Welcome to Meweda School's Study Bot! 📚\n\n"
        "With me, you can:\n\n"
        "📖 Access your books\n"
        "❓ Take quizzes\n"
        "🔔 Set homework reminders\n"
        "🤖 Chat with your AI Study Assistant for extra help!\n\n"
        "Let’s make studying simpler!\n(Powered by Aoud Kasim)\n\n"
        "Choose an option below to get started!",
        reply_markup=ReplyKeyboardMarkup(
            [["📚 Books", "❓ Take Quiz"], ["📘 UUE Exam Questions", "🤖 AI Assistant"]],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )
    return MAIN_MENU

async def show_subjects(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Choose a subject for your quiz:",
        reply_markup=ReplyKeyboardMarkup(
            [list(QUIZ_QUESTIONS.keys()), ["🔙 Back to Menu"]],
            resize_keyboard=True
        )
    )
    return QUIZ_SUBJECT

async def start_quiz(update: Update, context: CallbackContext) -> int:
    subject = update.message.text
    user_data["subject"] = subject
    user_data["score"] = 0
    user_data["current_question_index"] = 0
    user_data["questions"] = random.sample(QUIZ_QUESTIONS[subject], len(QUIZ_QUESTIONS[subject]))
    return await ask_question(update, context)

async def ask_question(update: Update, context: CallbackContext) -> int:
    question_data = user_data["questions"][user_data["current_question_index"]]
    options = question_data["options"]
    question_text = f"{question_data['question']}\n\nA) {options[0]}  B) {options[1]}  C) {options[2]}  D) {options[3]}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("A", callback_data="A"), InlineKeyboardButton("B", callback_data="B")],
        [InlineKeyboardButton("C", callback_data="C"), InlineKeyboardButton("D", callback_data="D")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ])

    # Only delete previous question messages, not the command message
    if user_data.get("last_question_message_id"):
        try:
            await context.bot.delete_message(update.effective_chat.id, user_data["last_question_message_id"])
        except:
            pass

    # Send the question
    if update.message:
        message = await update.message.reply_text(question_text, reply_markup=reply_markup)
    else:
        message = await update.callback_query.message.reply_text(question_text, reply_markup=reply_markup)

    user_data["last_question_message_id"] = message.message_id
    return QUIZ_QUESTION

async def handle_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    answer = query.data

    if answer == "back_to_menu":
        return await back_to_main_menu(update, context)

    question_data = user_data["questions"][user_data["current_question_index"]]
    if answer == question_data["answer"]:
        user_data["score"] += 1

    user_data["current_question_index"] += 1
    if user_data["current_question_index"] < len(user_data["questions"]):
        return await ask_question(update, context)
    else:
        return await show_result(update, context)

async def show_result(update: Update, context: CallbackContext) -> int:
    total_questions = len(user_data["questions"])
    score = user_data["score"]
    result_text = f"You scored {score}/{total_questions}!"

    # Only delete question messages, not the command message
    if user_data.get("last_question_message_id"):
        try:
            await context.bot.delete_message(update.effective_chat.id, user_data["last_question_message_id"])
        except:
            pass

    await update.callback_query.message.reply_text(
        result_text,
        reply_markup=ReplyKeyboardMarkup([["🔙 Back to Menu"]], resize_keyboard=True)
    )
    return QUIZ_RESULT

async def back_to_main_menu(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Back to the main menu.",
        reply_markup=ReplyKeyboardMarkup(
            [["📚 Books", "❓ Take Quiz"], ["📘 UUE Exam Questions", "🤖 AI Assistant"]],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )
    return MAIN_MENU

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                MessageHandler(filters.Regex("^📚 Books$"), show_subjects),
                MessageHandler(filters.Regex("^❓ Take Quiz$"), show_subjects),
                MessageHandler(filters.Regex("^📘 UUE Exam Questions$"), show_subjects),
                MessageHandler(filters.Regex("^🤖 AI Assistant$"), show_subjects)
            ],
            QUIZ_SUBJECT: [
                MessageHandler(filters.Regex("^(English|Biology|Physics|Chemistry|Agriculture|Math)$"), start_quiz),
                MessageHandler(filters.Regex("^🔙 Back to Menu$"), back_to_main_menu)
            ],
            QUIZ_QUESTION: [CallbackQueryHandler(handle_answer)],
            QUIZ_RESULT: [MessageHandler(filters.Regex("^🔙 Back to Menu$"), back_to_main_menu)],
        },
        fallbacks=[CommandHandler("start", start)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
