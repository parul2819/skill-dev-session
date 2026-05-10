import sys
from pathlib import Path

# Add project root to Python path so absolute imports like "from app..." work when running directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

import asyncio
import random
from faker import Faker
from sqlalchemy import insert, select, text
from app.core.db.session import SessionLocal
from app.orm import (
    UserOrm, RestaurantOrm, MenuItemOrm,
    UserAddressOrm, OfferOrm, OrderOrm, OrderItemOrm, OrderRatingOrm
)
from app.utils.enums import RestaurantStatusEnum, OrderStatusEnum, DiscountTypeEnum

fake = Faker()

TOTAL_USERS = 20000
TOTAL_RESTAURANTS = 2000
TOTAL_MENU_ITEMS = 20000
TOTAL_ORDERS = 100000
BATCH_SIZE = 1000


# -------------------------
# USERS
# -------------------------
async def insert_users(db):
    data = [
        UserOrm(
            name=fake.name(),
            email=f"user{i}_{fake.email()}",
            password=fake.password(),
            phone_number=fake.phone_number()[:15]
        )
        for i in range(TOTAL_USERS)
    ]
    db.add_all(data)
    await db.commit()
    print(f"✅ Inserted {TOTAL_USERS} Users")


# -------------------------
# RESTAURANTS
# -------------------------
async def insert_restaurants(db):
    data = [
        RestaurantOrm(
            name=fake.company(),
            address=fake.address(),
            phone_number=fake.phone_number()[:15],
            status=random.choice([RestaurantStatusEnum.active, RestaurantStatusEnum.closed])
        )
        for _ in range(TOTAL_RESTAURANTS)
    ]
    db.add_all(data)
    await db.commit()
    print(f"✅ Inserted {TOTAL_RESTAURANTS} Restaurants")


# -------------------------
# MENU ITEMS
# -------------------------
async def insert_menu_items(db):
    data = [
        MenuItemOrm(
            restaurant_id=random.randint(1, TOTAL_RESTAURANTS),
            name=fake.word(),
            description=fake.text(),
            price=round(random.uniform(50, 500), 2),
            is_veg=random.choice([True, False]),
            is_available=True
        )
        for _ in range(TOTAL_MENU_ITEMS)
    ]
    db.add_all(data)
    await db.commit()
    print(f"✅ Inserted {TOTAL_MENU_ITEMS} Menu Items")


# -------------------------
# ADDRESSES
# -------------------------
async def insert_addresses(db):
    data = []
    for user_id in range(1, TOTAL_USERS + 1):
        # The database enforces a UNIQUE(user_id, is_default) constraint.
        # This means a user can have at most ONE default (True) and ONE non-default (False) address.
        # So we can generate at most 2 addresses per user.
        num_addresses = random.randint(1, 2)
        for i in range(num_addresses):
            data.append(
                UserAddressOrm(
                    user_id=user_id,
                    address_line=fake.address(),
                    city=fake.city(),
                    state=fake.state(),
                    pincode=fake.postcode(),
                    is_default=(i == 0)
                )
            )
    db.add_all(data)
    await db.commit()
    print(f"✅ Inserted {len(data)} Addresses")


# -------------------------
# OFFERS
# -------------------------
async def insert_offers(db):
    data = [
        OfferOrm(
            code=f"OFFER{i}",
            discount_type=DiscountTypeEnum.percent,
            discount_value=random.uniform(5, 50),
            min_order_amount=random.uniform(100, 500),
            max_discount_amount=random.uniform(200, 1000),
            is_active=True
        )
        for i in range(100)
    ]
    db.add_all(data)
    await db.commit()
    print(f"✅ Inserted 100 Offers")


# -------------------------
# ORDERS + ITEMS
# -------------------------
async def insert_orders(db):
    for _ in range(0, TOTAL_ORDERS, BATCH_SIZE):
        orders = []

        for _ in range(BATCH_SIZE):
            total = round(random.uniform(200, 1500), 2)
            discount = round(random.uniform(0, 200), 2)
            final = total - discount

            orders.append(
                OrderOrm(
                    user_id=random.randint(1, TOTAL_USERS),
                    restaurant_id=random.randint(1, TOTAL_RESTAURANTS),
                    offer_id=random.choice([None, random.randint(1, 100)]),
                    total_amount=total,
                    discount_amount=discount,
                    final_amount=final,
                    order_status=random.choice([OrderStatusEnum.pending, OrderStatusEnum.delivered, OrderStatusEnum.cancelled])
                )
            )

        db.add_all(orders)
        await db.flush()  # 💡 get order IDs

        items = []
        for order in orders:
            for _ in range(random.randint(1, 5)):
                items.append(
                    OrderItemOrm(
                        order_id=order.order_id,
                        item_id=random.randint(1, TOTAL_MENU_ITEMS),
                        quantity=random.randint(1, 3),
                        price=round(random.uniform(50, 500), 2)
                    )
                )

        db.add_all(items)
        await db.commit()
    print(f"✅ Inserted {TOTAL_ORDERS} Orders and Order Items")


# -------------------------
# RATINGS
# -------------------------
async def insert_ratings(db):
    result = await db.execute(select(OrderOrm.order_id))
    order_ids = [row[0] for row in result.fetchall()]

    data = []
    for oid in order_ids:
        if random.random() < 0.6:
            data.append(
                OrderRatingOrm(
                    order_id=oid,
                    user_id=random.randint(1, TOTAL_USERS),
                    restaurant_id=random.randint(1, TOTAL_RESTAURANTS),
                    rating=random.randint(1, 5),
                    review=fake.sentence()
                )
            )

    db.add_all(data)
    await db.commit()
    print(f"✅ Inserted {len(data)} Ratings")


# -------------------------
# MAIN
# -------------------------
async def main():
    async with SessionLocal() as db:
        print("Cleaning existing data...")
        await db.execute(text("TRUNCATE TABLE users, restaurants, menu_items, user_addresses, offers, orders, order_items, order_ratings RESTART IDENTITY CASCADE"))
        await db.commit()

        print("🚀 Users...")
        await insert_users(db)

        print("🚀 Restaurants...")
        await insert_restaurants(db)

        print("🚀 Menu Items...")
        await insert_menu_items(db)

        print("🚀 Addresses...")
        await insert_addresses(db)

        print("🚀 Offers...")
        await insert_offers(db)

        print("🚀 Orders...")
        await insert_orders(db)

        print("🚀 Ratings...")
        await insert_ratings(db)

    print("✅ DONE — 1 LAKH ORDERS GENERATED")


if __name__ == "__main__":
    asyncio.run(main())