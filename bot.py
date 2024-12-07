# bot.py

import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import locale
from ryanair import Ryanair  # Убедитесь, что этот модуль установлен и работает корректно
from config import TELEGRAM_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Установка локали на русский язык для отображения названий месяцев
try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except locale.Error:
    logger.warning("Локаль 'ru_RU.UTF-8' не установлена. Месяцы будут отображаться на английском.")

# Определение состояний разговора
(
    SELECTING_FLIGHT_TYPE,
    SELECTING_DEPARTURE_COUNTRY,
    SELECTING_DEPARTURE_CITY,
    SELECTING_DEPARTURE_YEAR,
    SELECTING_DEPARTURE_MONTH,
    SELECTING_DEPARTURE_DATE_RANGE,
    SELECTING_DEPARTURE_DATE,
    SELECTING_ARRIVAL_COUNTRY,
    SELECTING_ARRIVAL_CITY,
    SELECTING_RETURN_YEAR,
    SELECTING_RETURN_MONTH,
    SELECTING_RETURN_DATE_RANGE,
    SELECTING_RETURN_DATE,
    SELECTING_MAX_PRICE,
) = range(14)

# Ваш словарь стран и городов с IATA кодами
countries = {
    "Албания": {
        "Тирана": "TIA",
    },
    "Австрия": {
        "Вена": "VIE",
        "Зальцбург": "SZG",
        "Грац": "GRZ",
        "Клагенфурт": "KLU",
        "Линц": "LNZ"
    },
    "Азербайджан": {
        "Баку": "GYD",
    },
    "Бельгия": {
        "Брюссель": "BRU",
        "Шарлеруа": "CRL",
        "Льеж": "LGG",
        "Антверпен": "ANR",
        "Остенде": "OST"
    },
    "Босния и Герцеговина": {
        "Сараево": "SJJ",
    },
    "Болгария": {
        "София": "SOF",
        "Варна": "VAR",
        "Бургас": "BOJ",
        "Пловдив": "PDV"
    },
    "Хорватия": {
        "Загреб": "ZAG",
        "Сплит": "SPU",
        "Риека": "RJK",
        "Пула": "PUY"
    },
    "Кипр": {
        "Ларнака": "LCA",
        "Пафос": "PFO"
    },
    "Чехия": {
        "Прага": "PRG"
    },
    "Дания": {
        "Копенгаген": "CPH",
        "Орхус": "AAR",
        "Ольборг": "AAL",
        "Биллунд": "BLL"
    },
    "Эстония": {
        "Таллинн": "TLL"
    },
    "Финляндия": {
        "Хельсинки": "HEL",
        "Турку": "TKU"
    },
    "Франция": {
        "Париж": "CDG",
        "Марсель": "MRS",
        "Лион": "LYS",
        "Ницца": "NCE",
        "Тулуза": "TLS",
        "Бордо": "BOD",
        "Нант": "NTE",
        "Страсбург": "SXB",
        "Монпелье": "MPL",
        "Лилль": "LIL",
        "Бастия": "BIA",
        "Аяччо": "AJA",
        "Кальви": "CLY",
        "Фигари": "FSC",
        "Безье": "BZR"
    },
    "Грузия": {
        "Тбилиси": "TBS"
    },
    "Германия": {
        "Берлин": "BER",
        "Франкфурт": "FRA",
        "Мюнхен": "MUC",
        "Гамбург": "HAM",
        "Дюссельдорф": "DUS",
        "Кёльн": "CGN",
        "Штутгарт": "STR",
        "Нюрнберг": "NUE",
        "Бремен": "BRE",
        "Ганновер": "HAJ",
        "Дортмунд": "DTM",
        "Лейпциг": "LEJ",
        "Дрезден": "DRS",
        "Карлсруэ": "FKB",
        "Фридрихсхафен": "FDH",
        "Мемминген": "FMM",
        "Вейц": "WEZ"
    },
    "Греция": {
        "Афины": "ATH",
        "Салоники": "SKG",
        "Ираклион": "HER",
        "Родос": "RHO",
        "Корфу": "CFU",
        "Кос": "KGS",
        "Санторини": "JTR",
        "Миконос": "JMK"
    },
    "Венгрия": {
        "Будапешт": "BUD",
        "Дебрецен": "DEB"
    },
    "Исландия": {
        "Рейкьявик": "KEF"
    },
    "Ирландия": {
        "Дублин": "DUB",
        "Корк": "ORK",
        "Шаннон": "SNN",
        "Керри": "KIR",
        "Нок": "NOC"
    },
    "Италия": {
        "Рим": "FCO",
        "Милан": "MXP",
        "Неаполь": "NAP",
        "Венеция": "VCE",
        "Палермо": "PMO",
        "Катания": "CTA",
        "Болонья": "BLQ",
        "Пиза": "PSA",
        "Турин": "TRN",
        "Генуя": "GOA",
        "Бари": "BRI",
        "Верона": "VRN",
        "Тревизо": "TSF",
        "Флоренция": "FLR",
        "Кальяри": "CAG",
        "Бергамо": "BGY"
    },
    "Латвия": {
        "Рига": "RIX"
    },
    "Литва": {
        "Вильнюс": "VNO",
        "Каунас": "KUN"
    },
    "Мальта": {
        "Валлетта": "MLA"
    },
    "Молдова": {
        "Кишинёв": "KIV"
    },
    "Черногория": {
        "Подгорица": "TGD",
        "Бар": "BTH",
        "Тиват": "TIV"
    },
    "Нидерланды": {
        "Амстердам": "AMS",
        "Роттердам": "RTM",
        "Эйндховен": "EIN",
        "Гаага": "GRQ",
        "Утрехт": "UTR"
    },
    "Северная Македония": {
        "Скопье": "SKP"
    },
    "Норвегия": {
        "Осло": "OSL",
        "Берген": "BGO",
        "Тронхейм": "TRD",
        "Ставангер": "SVG"
    },
    "Польша": {
        "Варшава": "WAW",
        "Краков": "KRK",
        "Гданьск": "GDN",
        "Вроцлав": "WRO",
        "Познань": "POZ",
        "Лодзь": "LCJ",
        "Люблин": "LUZ",
        "Щецин": "SZZ"
    },
    "Португалия": {
        "Лиссабон": "LIS",
        "Порту": "OPO",
        "Фару": "FAO",
        "Фуншал": "FNC",
        "Лагуш": "LPA"
    },
    "Румыния": {
        "Бухарест": "OTP",
        "Клуж-Напока": "CLJ",
        "Тимишоара": "TSR",
        "Брашов": "BAY",
        "Сибиу": "SBZ",
        "Галац": "GRZ",
        "Иасмар": "IAS"
    },
    "Сербия": {
        "Белград": "BEG"
    },
    "Словакия": {
        "Братислава": "BTS"
    },
    "Словения": {
        "Любляна": "LJU"
    },
    "Испания": {
        "Барселона": "BCN",
        "Мадрид": "MAD",
        "Валенсия": "VLC",
        "Севилья": "SVQ",
        "Малага": "AGP",
        "Пальма-де-Майорка": "PMI",
        "Аликанте": "ALC",
        "Бильбао": "BIO",
        "Сарагоса": "ZAZ",
        "Сантандер": "SDR",
        "Сантьяго-де-Компостела": "SCQ",
        "Ибица": "IBZ",
        "Таррагона": "TGN"
    },
    "Швеция": {
        "Стокгольм": "ARN",
        "Гётеборг": "GOT",
        "Мальмё": "MMX",
        "Лулео": "LLA"
    },
    "Швейцария": {
        "Цюрих": "ZRH",
        "Базель": "BSL",
        "Женева": "GVA",
        "Лозанна": "QLT"
    },
    "Турция": {
        "Стамбул": "IST",
        "Анкара": "ESB",
        "Анталия": "AYT",
        "Измир": "ADB"
    },
    "Украина": {
        "Киев": "KBP",
        "Львов": "LWO",
        "Одесса": "ODS",
        "Харьков": "HRK",
        "Днепр": "DNK",
        "Запорожье": "OZH"
    },
    "Великобритания": {
        "Лондон": "STN",
        "Манчестер": "MAN",
        "Бирмингем": "BHX",
        "Глазго": "GLA",
        "Эдинбург": "EDI",
        "Бристоль": "BRS",
        "Ливерпуль": "LPL",
        "Лидс": "LBA",
        "Ньюкасл": "NCL",
        "Белфаст": "BFS",
        "Лондон-Гатвик": "LGW",
        "Лондон-Станстед": "STN",
        "Лондон-Бичфилд": "LCY"
    }
}

# Функции генерации клавиатур и обработки состояний

def generate_year_buttons():
    current_year = datetime.now().year
    next_year = current_year + 1
    keyboard = [
        [InlineKeyboardButton(text=str(current_year), callback_data=str(current_year))],
        [InlineKeyboardButton(text=str(next_year), callback_data=str(next_year))]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_month_buttons():
    months = [
        "Январь", "Февраль", "Март", "Апрель",
        "Май", "Июнь", "Июль", "Август",
        "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    keyboard = []
    for idx, month in enumerate(months, start=1):
        callback_data = str(idx).zfill(2)  # Номер месяца с ведущим нулём
        logger.info(f"Создаётся кнопка: {month} с callback_data: {callback_data}")
        keyboard.append([InlineKeyboardButton(text=month, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)

def generate_date_range_buttons(year, month):
    try:
        start_date = datetime(year, month, 1)
    except ValueError:
        logger.error(f"Неверный год или месяц: {year}-{month}")
        return InlineKeyboardMarkup([])
    
    # Определяем количество дней в месяце
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    days_in_month = (next_month - start_date).days

    ranges = [
        (1, 10),
        (11, 20),
        (21, days_in_month)
    ]

    keyboard = []
    for start, end in ranges:
        range_str = f"{start}-{end}"
        callback_data = f"{start}-{end}"
        keyboard.append([InlineKeyboardButton(text=range_str, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)

def generate_specific_date_buttons(year, month, date_range_start, date_range_end):
    buttons = []
    for day in range(date_range_start, date_range_end + 1):
        try:
            date = datetime(year, month, day)
            date_str = date.strftime("%Y-%m-%d")
            display_date = date.strftime("%d-%m-%Y")
            buttons.append([InlineKeyboardButton(text=display_date, callback_data=date_str)])
        except ValueError:
            continue  # Пропускаем несуществующие даты
    return InlineKeyboardMarkup(buttons)

# Функции-обработчики

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
    reply_keyboard = [['1', '2']]
    await update.message.reply_text(
        "Добро пожаловать в бот поиска билетов на Ryanair!\n"
        "Выберите тип рейса:\n"
        "1 - В одну сторону\n"
        "2 - Туда и обратно",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Выберите тип рейса'
        ),
    )
    return SELECTING_FLIGHT_TYPE

async def flight_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    if user_input not in ['1', '2']:
        await update.message.reply_text("Пожалуйста, выберите 1 или 2.")
        return SELECTING_FLIGHT_TYPE
    context.user_data['flight_type'] = user_input
    await update.message.reply_text(
        "Выберите страну вылета:",
        reply_markup=ReplyKeyboardMarkup(
            [list(countries.keys())[i:i+3] for i in range(0, len(countries), 3)],
            one_time_keyboard=True, resize_keyboard=True
        )
    )
    return SELECTING_DEPARTURE_COUNTRY

async def departure_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    country = update.message.text
    if country not in countries:
        await update.message.reply_text("Страна не найдена! Пожалуйста, выберите из списка.")
        return SELECTING_DEPARTURE_COUNTRY
    context.user_data['departure_country'] = country
    cities = list(countries[country].keys())
    reply_keyboard = [cities[i:i+3] for i in range(0, len(cities), 3)]
    await update.message.reply_text(
        "Выберите город вылета:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )
    return SELECTING_DEPARTURE_CITY

async def departure_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    city = update.message.text
    country = context.user_data.get('departure_country')
    if city not in countries[country]:
        await update.message.reply_text("Город не найден! Пожалуйста, выберите из списка.")
        return SELECTING_DEPARTURE_CITY
    context.user_data['departure_airport'] = countries[country][city]
    await update.message.reply_text(
        "Выберите год вылета:",
        reply_markup=generate_year_buttons()
    )
    return SELECTING_DEPARTURE_YEAR

async def departure_year_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_year = int(query.data)
    context.user_data['departure_year'] = selected_year
    await query.edit_message_text(text=f"Год вылета выбран: {selected_year}")
    
    await query.message.reply_text(
        "Выберите месяц вылета:",
        reply_markup=generate_month_buttons()
    )
    return SELECTING_DEPARTURE_MONTH

async def departure_month_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_month = int(query.data)
    context.user_data['departure_month'] = selected_month
    try:
        month_name = datetime(1900, selected_month, 1).strftime('%B')  # Получение названия месяца
    except ValueError:
        month_name = "Неверный месяц"
        logger.error(f"Неверный номер месяца: {selected_month}")
    await query.edit_message_text(text=f"Месяц вылета выбран: {month_name.capitalize()}")
    
    await query.message.reply_text(
        "Выберите диапазон дат вылета:",
        reply_markup=generate_date_range_buttons(year=int(context.user_data['departure_year']), month=selected_month)
    )
    return SELECTING_DEPARTURE_DATE_RANGE

async def departure_date_range_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_range = query.data  # Формат "start-end"
    try:
        start_day, end_day = map(int, selected_range.split('-'))
    except ValueError:
        await query.edit_message_text(text="Некорректный диапазон дат. Пожалуйста, выберите снова.")
        return SELECTING_DEPARTURE_DATE_RANGE
    context.user_data['departure_date_range'] = (start_day, end_day)
    await query.edit_message_text(text=f"Диапазон дат вылета выбран: {selected_range}")
    
    await query.message.reply_text(
        "Выберите конкретную дату вылета:",
        reply_markup=generate_specific_date_buttons(
            year=int(context.user_data['departure_year']),
            month=int(context.user_data['departure_month']),
            date_range_start=start_day,
            date_range_end=end_day
        )
    )
    return SELECTING_DEPARTURE_DATE

async def departure_date_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_date = query.data
    context.user_data['departure_date'] = selected_date
    try:
        formatted_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    except ValueError:
        formatted_date = "Неверная дата"
        logger.error(f"Неверный формат даты: {selected_date}")
    await query.edit_message_text(text=f"Дата вылета выбрана: {formatted_date}")
    
    await query.message.reply_text(
        "Выберите страну прилёта:",
        reply_markup=ReplyKeyboardMarkup(
            [list(countries.keys())[i:i+3] for i in range(0, len(countries), 3)],
            one_time_keyboard=True, resize_keyboard=True
        )
    )
    return SELECTING_ARRIVAL_COUNTRY

async def arrival_country(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    country = update.message.text
    if country not in countries:
        await update.message.reply_text("Страна не найдена! Пожалуйста, выберите из списка.")
        return SELECTING_ARRIVAL_COUNTRY
    context.user_data['arrival_country'] = country
    cities = list(countries[country].keys())
    reply_keyboard = [cities[i:i+3] for i in range(0, len(cities), 3)]
    await update.message.reply_text(
        "Выберите город прилёта:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        )
    )
    return SELECTING_ARRIVAL_CITY

async def arrival_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    city = update.message.text
    country = context.user_data.get('arrival_country')
    if city not in countries[country]:
        await update.message.reply_text("Город не найден! Пожалуйста, выберите из списка.")
        return SELECTING_ARRIVAL_CITY
    context.user_data['arrival_airport'] = countries[country][city]

    flight_type = context.user_data.get('flight_type')
    if flight_type == '2':
        await update.message.reply_text(
            "Выберите год обратного вылета:",
            reply_markup=generate_year_buttons()
        )
        return SELECTING_RETURN_YEAR
    else:
        await update.message.reply_text(
            "Введите максимальную цену (EUR):",
            reply_markup=ReplyKeyboardRemove()
        )
        return SELECTING_MAX_PRICE

async def return_year_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_year = int(query.data)
    context.user_data['return_year'] = selected_year
    await query.edit_message_text(text=f"Год обратного вылета выбран: {selected_year}")
    
    await query.message.reply_text(
        "Выберите месяц обратного вылета:",
        reply_markup=generate_month_buttons()
    )
    return SELECTING_RETURN_MONTH

async def return_month_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_month = int(query.data)
    context.user_data['return_month'] = selected_month
    try:
        month_name = datetime(1900, selected_month, 1).strftime('%B')  # Получение названия месяца
    except ValueError:
        month_name = "Неверный месяц"
        logger.error(f"Неверный номер месяца: {selected_month}")
    await query.edit_message_text(text=f"Месяц обратного вылета выбран: {month_name.capitalize()}")
    
    await query.message.reply_text(
        "Выберите диапазон дат обратного вылета:",
        reply_markup=generate_date_range_buttons(year=int(context.user_data['return_year']), month=selected_month)
    )
    return SELECTING_RETURN_DATE_RANGE

async def return_date_range_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_range = query.data  # Формат "start-end"
    try:
        start_day, end_day = map(int, selected_range.split('-'))
    except ValueError:
        await query.edit_message_text(text="Некорректный диапазон дат. Пожалуйста, выберите снова.")
        return SELECTING_RETURN_DATE_RANGE
    context.user_data['return_date_range'] = (start_day, end_day)
    await query.edit_message_text(text=f"Диапазон дат обратного вылета выбран: {selected_range}")
    
    await query.message.reply_text(
        "Выберите конкретную дату обратного вылета:",
        reply_markup=generate_specific_date_buttons(
            year=int(context.user_data['return_year']),
            month=int(context.user_data['return_month']),
            date_range_start=start_day,
            date_range_end=end_day
        )
    )
    return SELECTING_RETURN_DATE

async def return_date_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_date = query.data
    context.user_data['return_date'] = selected_date
    try:
        formatted_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    except ValueError:
        formatted_date = "Неверная дата"
        logger.error(f"Неверный формат даты: {selected_date}")
    await query.edit_message_text(text=f"Дата обратного вылета выбрана: {formatted_date}")
    
    await query.message.reply_text(
        "Введите максимальную цену (EUR):",
        reply_markup=ReplyKeyboardRemove()
    )
    return SELECTING_MAX_PRICE

async def max_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    price_str = update.message.text
    try:
        price = Decimal(price_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if price <= 0:
            await update.message.reply_text("Цена должна быть положительным числом. Введите максимальную цену (EUR):")
            return SELECTING_MAX_PRICE
        context.user_data['max_price'] = price
    except:
        await update.message.reply_text("Пожалуйста, введите корректное число для цены (EUR):")
        return SELECTING_MAX_PRICE

    await update.message.reply_text("Начинаю поиск рейсов...")
    
    # Вызов функции поиска рейсов с дополнительной логикой
    flights = await find_flights_with_fallback(
        departure_airport=context.user_data['departure_airport'],
        arrival_airport=context.user_data['arrival_airport'],
        departure_date=context.user_data['departure_date'],
        return_flight_date=context.user_data.get('return_date'),
        max_price=context.user_data['max_price']
    )

    if not flights:
        await update.message.reply_text("К сожалению, рейсы не найдены в выбранном ценовом диапазоне и направлениях.")
    else:
        response = format_flights(flights)
        await update.message.reply_text(response, parse_mode='Markdown')

    # Завершение разговора
    await update.message.reply_text(
        "Хотите сделать новый поиск? Отправьте /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Поиск билетов отменен. Если хотите начать заново, отправьте /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Функции поиска и форматирования рейсов

async def find_flights_with_fallback(departure_airport, arrival_airport, departure_date, return_flight_date, max_price):
    ryanair_api = Ryanair()
    try:
        # Попытка найти рейсы на выбранную дату
        if return_flight_date:
            flights = ryanair_api.get_cheapest_return_flights(
                source_airport=departure_airport,
                date_from=departure_date,
                date_to=departure_date,
                return_date_from=return_flight_date,
                return_date_to=return_flight_date,
                destination_airport=arrival_airport,
                max_price=float(max_price)
            )
        else:
            flights = ryanair_api.get_cheapest_flights(
                airport=departure_airport,
                date_from=departure_date,
                date_to=departure_date,
                destination_airport=arrival_airport,
                max_price=float(max_price)
            )
        
        if flights:
            return flights

        # Если рейсы не найдены на выбранную дату, ищем на ближайшие 7 дней вперед и назад
        logger.info("Рейсы на выбранную дату не найдены. Поиск на ближайшие даты...")
        search_days = 7
        departure_dt = datetime.strptime(departure_date, "%Y-%m-%d")
        if return_flight_date:
            return_dt = datetime.strptime(return_flight_date, "%Y-%m-%d")
        else:
            return_dt = None

        # Ищем на ближайшие дни вперед и назад
        for offset in range(1, search_days + 1):
            # Поиск на дни вперед
            new_departure_date = (departure_dt + timedelta(days=offset)).strftime("%Y-%m-%d")
            if return_dt:
                new_return_date = (return_dt + timedelta(days=offset)).strftime("%Y-%m-%d")
                new_flights = ryanair_api.get_cheapest_return_flights(
                    source_airport=departure_airport,
                    date_from=new_departure_date,
                    date_to=new_departure_date,
                    return_date_from=new_return_date,
                    return_date_to=new_return_date,
                    destination_airport=arrival_airport,
                    max_price=float(max_price)
                )
            else:
                new_flights = ryanair_api.get_cheapest_flights(
                    airport=departure_airport,
                    date_from=new_departure_date,
                    date_to=new_departure_date,
                    destination_airport=arrival_airport,
                    max_price=float(max_price)
                )
            
            if new_flights:
                logger.info(f"Найдены рейсы на дату: {new_departure_date}")
                return new_flights

            # Поиск на дни назад
            new_departure_date = (departure_dt - timedelta(days=offset)).strftime("%Y-%m-%d")
            if new_departure_date < datetime.now().strftime("%Y-%m-%d"):
                continue  # Не ищем в прошлом
            if return_dt:
                new_return_date = (return_dt - timedelta(days=offset)).strftime("%Y-%m-%d")
                new_flights = ryanair_api.get_cheapest_return_flights(
                    source_airport=departure_airport,
                    date_from=new_departure_date,
                    date_to=new_departure_date,
                    return_date_from=new_return_date,
                    return_date_to=new_return_date,
                    destination_airport=arrival_airport,
                    max_price=float(max_price)
                )
            else:
                new_flights = ryanair_api.get_cheapest_flights(
                    airport=departure_airport,
                    date_from=new_departure_date,
                    date_to=new_departure_date,
                    destination_airport=arrival_airport,
                    max_price=float(max_price)
                )
            
            if new_flights:
                logger.info(f"Найдены рейсы на дату: {new_departure_date}")
                return new_flights

        # Если рейсы не найдены на ближайшие даты, ищем все доступные рейсы в диапазоне цен и направлениях
        logger.info("Рейсы не найдены на ближайшие даты. Поиск всех доступных рейсов в заданном диапазоне цен и направлениях...")
        if return_flight_date:
            all_flights = ryanair_api.get_cheapest_return_flights(
                source_airport=departure_airport,
                date_from=datetime.now().strftime("%Y-%m-%d"),
                date_to=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                return_date_from=datetime.now().strftime("%Y-%m-%d"),
                return_date_to=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                destination_airport=arrival_airport,
                max_price=float(max_price)
            )
        else:
            all_flights = ryanair_api.get_cheapest_flights(
                airport=departure_airport,
                date_from=datetime.now().strftime("%Y-%m-%d"),
                date_to=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
                destination_airport=arrival_airport,
                max_price=float(max_price)
            )
        
        return all_flights if all_flights else []
    except Exception as e:
        logger.error(f"Ошибка при поиске рейсов: {e}")
        return []

def format_flights(flights):
    messages = []
    for flight in flights:
        if hasattr(flight, 'price'):
            # Рейс в одну сторону
            message = (
                f"✈️ *Рейс*: {flight.flightNumber}\n"
                f"📍 *Маршрут*: {flight.originFull} -> {flight.destinationFull}\n"
                f"🕒 *Вылет*: {flight.departureTime}\n"
                f"💰 *Цена*: {flight.price} {flight.currency}\n"
            )
            messages.append(message)
        elif hasattr(flight, 'outbound') and hasattr(flight, 'inbound'):
            # Рейс туда и обратно
            outbound = flight.outbound
            inbound = flight.inbound
            total_price = Decimal(str(outbound.price)) + Decimal(str(inbound.price))
            message = (
                f"🔄 *Рейс туда и обратно*\n\n"
                f"➡️ *Вылет туда*:\n"
                f"  - *Рейс*: {outbound.flightNumber}\n"
                f"  - *Маршрут*: {outbound.originFull} -> {outbound.destinationFull}\n"
                f"  - *Вылет*: {outbound.departureTime}\n"
                f"  - *Цена*: {outbound.price} {outbound.currency}\n\n"
                f"⬅️ *Вылет обратно*:\n"
                f"  - *Рейс*: {inbound.flightNumber}\n"
                f"  - *Маршрут*: {inbound.originFull} -> {inbound.destinationFull}\n"
                f"  - *Вылет*: {inbound.departureTime}\n"
                f"  - *Цена*: {inbound.price} {inbound.currency}\n\n"
                f"💵 *Общая цена*: {total_price} {outbound.currency}\n"
            )
            messages.append(message)
    return "\n".join(messages) if messages else "Рейсов не найдено."

def create_application():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_FLIGHT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_type)],
            SELECTING_DEPARTURE_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, departure_country)],
            SELECTING_DEPARTURE_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, departure_city)],
            SELECTING_DEPARTURE_YEAR: [CallbackQueryHandler(departure_year_selected)],
            SELECTING_DEPARTURE_MONTH: [CallbackQueryHandler(departure_month_selected)],
            SELECTING_DEPARTURE_DATE_RANGE: [CallbackQueryHandler(departure_date_range_selected)],
            SELECTING_DEPARTURE_DATE: [CallbackQueryHandler(departure_date_selected)],
            SELECTING_ARRIVAL_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, arrival_country)],
            SELECTING_ARRIVAL_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, arrival_city)],
            SELECTING_RETURN_YEAR: [CallbackQueryHandler(return_year_selected)],
            SELECTING_RETURN_MONTH: [CallbackQueryHandler(return_month_selected)],
            SELECTING_RETURN_DATE_RANGE: [CallbackQueryHandler(return_date_range_selected)],
            SELECTING_RETURN_DATE: [CallbackQueryHandler(return_date_selected)],
            SELECTING_MAX_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, max_price)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=False
    )
    
    app.add_handler(conv_handler)
    return app
