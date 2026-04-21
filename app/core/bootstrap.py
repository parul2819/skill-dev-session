from app.core.logger import setup_logger
from fastapi import FastAPI
from app.core.exceptions.handlers import register_exception_handlers
from app.core.middleware.request_logger import RequestLoggingMiddleware
from app.api import (cart_router, cart_items_router, menu_items_router,
                                offers_router, order_items_router, order_ratings_router,
                                orders_router, restaurant_router, user_addresses_router,
                                user_router)



def register_routers(app: FastAPI):
    """ Register all routers"""
    app.include_router(user_router)
    app.include_router(restaurant_router)
    app.include_router(menu_items_router)
    app.include_router(offers_router)
    app.include_router(cart_router)
    app.include_router(cart_items_router)
    app.include_router(orders_router)
    app.include_router(order_items_router)
    app.include_router(order_ratings_router)
    app.include_router(user_addresses_router)


def bootstrap(app: FastAPI):
    print("\n" + "="*50)
    print(">>> BOOTSTRAP SYSTEM INITIALIZING <<<")
    print("="*50 + "\n")
    logger = setup_logger()
    app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(app)
    register_routers(app)
    logger.info("-----------------Bootstrapping FastAPI-----------------")