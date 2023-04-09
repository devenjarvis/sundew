"""initial schema

Revision ID: 3c814510e202
Revises:
Create Date: 2023-04-08 06:27:20.176013

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3c814510e202"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("text", sa.String),
        sa.Column("completed", sa.Boolean),
    )


def downgrade() -> None:
    op.drop_table("notes")
