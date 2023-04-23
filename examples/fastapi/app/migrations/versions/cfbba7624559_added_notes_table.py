"""Added notes table

Revision ID: cfbba7624559
Revises:
Create Date: 2023-04-09 21:06:27.693889

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cfbba7624559"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=1024), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    # ### end Alembic commands ###