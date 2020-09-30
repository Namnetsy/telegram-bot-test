from aiogram import Bot, Dispatcher, types

import asyncio
import logging

token='<token>'

products = []
products.append({
	'id': 0,
	'name': 'Google Pixel',
	'category': 'Smartphones',
	'category_id': 0,
	'price': '899$'
})

products.append({
	'id': 1,
	'name': 'iPhone 10',
	'category': 'Smartphones',
	'category_id': 0,
	'price': '408$'
})

products.append({
	'id': 2,
	'name': 'Table',
	'category': 'Furniture',
	'category_id': 1,
	'price': '99$'
})

products.append({
	'id': 3,
	'name': 'Sofa',
	'category': 'Furniture',
	'category_id': 1,
	'price': '399$'
})

products.append({
	'id': 4,
	'name': 'Macbook Pro',
	'category': 'Laptops',
	'category_id': 2,
	'price': '599$'
})

products.append({
	'id': 5,
	'name': 'Acer',
	'category': 'Laptops',
	'category_id': 2,
	'price': '9999$'
})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bot = Bot(token=token)
dp = Dispatcher(bot=bot)


def format_product(product):
	return f"id: <b>{product['id']}</b>\nname: <b>{product['name']}</b>\ncategory: <b>{product['category']}</b>\ncategory_id: <b>{product['category_id']}</b>\nprice: <b>{product['price']}</b>"


async def get_products():
	result = []

	logger.info('Getting all products...')

	for product in products:
		result.append(format_product(product))

	return result


async def get_products_by_category(category):
	result = []

	logger.info(f'Getting all products by {category} category...')

	for product in products:
		if product['category'] == category:
			result.append(format_product(product))
	
	return result


async def get_categories():
	logger.info('Getting all categories was...')
	
	return set([product['category'] for product in products])


@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
	logger.info(f'Start handler was called by {message.from_user.first_name}')

	keyboard_markup = types.ReplyKeyboardMarkup()

	btns_text = {'Products', 'Categories'}
	keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

	await message.answer('Hi!\nPress one the buttons to proced.', reply_markup=keyboard_markup)


@dp.message_handler()
async def all_message_handler(message: types.Message):
	text = message.text
	logger.info(f'{message.from_user.first_name} sent a message: {text}')

	if text == 'Products':
		for product in await get_products():
			await message.answer(product, parse_mode=types.ParseMode.HTML)
	elif text == 'Categories':
		keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)

		categories = await get_categories()
		categories.add('[Go Back]')
		btns_text = categories
		keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

		await message.answer('Here\'s the list of categories.', parse_mode=types.ParseMode.HTML, reply_markup=keyboard_markup)
	elif text == 'Furniture' or text == 'Smartphones' or text == 'Laptops':
		for product in await get_products_by_category(text):
			await message.answer(product, parse_mode=types.ParseMode.HTML)
	elif text == '[Go Back]':
		await start_handler(message)


async def main():
	try:
		await dp.start_polling()
	finally:
		await bot.close()


if __name__ == '__main__':
	asyncio.run(main())
