from datetime import datetime, timedelta

from database.db_connection import mongodb


async def write_new_product(date: datetime, user_id: int, products: str) -> None:
    document = {'date': date, 'user_id': user_id, 'product': products}
    await mongodb.collection.insert_one(document)


async def get_user_products(user_id: int) -> list:
    cursor = mongodb.collection.find({'user_id': user_id}).sort('date')
    products = await cursor.to_list(length=100)
    result = []
    for product in products:
        result.append([(product["date"] + timedelta(hours=3, minutes=0)).strftime("%m/%d/%Y, %H:%M:%S"),
                      product["product"]])
    return result
