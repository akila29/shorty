"""create_urls_table

Revision ID: 854273e11d35
Revises: 
Create Date: 2026-06-07 12:36:26.404585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '854273e11d35'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE urls (
            id         BIGSERIAL PRIMARY KEY,
            short_code TEXT NOT NULL UNIQUE,
            long_url   TEXT NOT NULL UNIQUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("CREATE INDEX idx_urls_long_url ON urls(long_url)")


def downgrade() -> None:
    op.execute("DROP TABLE urls")
