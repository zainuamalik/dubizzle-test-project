"""Changed data type for 'status' in orders table to Enum

Revision ID: fbbc65501985
Revises: 1f6abebc1ed0
Create Date: 2025-04-09 06:39:28.019417+00:00

"""
from typing import Sequence, Union
from alembic import op

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbbc65501985'
down_revision: Union[str, None] = '1f6abebc1ed0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define enum
order_status_enum = sa.Enum(
    'pending', 'cancelled', 'completed',
    name='order_status',
)


def upgrade() -> None:
    # Create the ENUM type before using it
    order_status_enum.create(op.get_bind(), checkfirst=True)

    # Alter the column to use the new enum with explicit cast
    op.alter_column(
        'orders',
        'status',
        existing_type=sa.VARCHAR(length=50),
        type_=order_status_enum,
        nullable=False,
        postgresql_using="status::order_status"
    )

def downgrade() -> None:
    # Revert back to VARCHAR
    op.alter_column(
        'orders',
        'status',
        existing_type=order_status_enum,
        type_=sa.VARCHAR(length=50),
        nullable=True,
        postgresql_using="status::VARCHAR"
    )
    # Drop enum type
    order_status_enum.drop(op.get_bind(), checkfirst=True)