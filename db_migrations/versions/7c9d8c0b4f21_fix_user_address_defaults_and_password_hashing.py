"""Fix user address default index and password hashing compatibility

Revision ID: 7c9d8c0b4f21
Revises: ed2b766e9d9e
Create Date: 2026-05-09 15:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c9d8c0b4f21"
down_revision: Union[str, Sequence[str], None] = "ed2b766e9d9e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("unique_default_address_per_user", "user_addresses", type_="unique")
    op.create_index(
        "unique_default_address_per_user",
        "user_addresses",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("is_default"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("unique_default_address_per_user", table_name="user_addresses")
    op.create_unique_constraint(
        "unique_default_address_per_user",
        "user_addresses",
        ["user_id", "is_default"],
    )
