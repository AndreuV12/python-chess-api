"""add color and preview_fen to openingModel

Revision ID: af6ee27f0747
Revises: ad7ea5aa4f1d
Create Date: 2024-10-10 13:24:53.956778

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "af6ee27f0747"
down_revision: Union[str, None] = "ad7ea5aa4f1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "openings", sa.Column("color", sa.String(), nullable=False, server_default="w")
    )
    op.add_column("openings", sa.Column("preview_fen", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("openings", "preview_fen")
    op.drop_column("openings", "color")
