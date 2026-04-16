from enum import Enum


class RestaurantStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    closed = "closed"


class OrderStatusEnum(str, Enum):
    pending = "pending"
    preparing = "preparing"
    delivered = "delivered"
    cancelled = "cancelled"


class DiscountTypeEnum(str, Enum):
    percent = "percent"
    fixed = "fixed"
