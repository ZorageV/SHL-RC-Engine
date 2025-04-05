"""remove_unique

Revision ID: f094533cbaaa
Revises: b20551f34a42
Create Date: 2025-04-05 04:02:05.253112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f094533cbaaa"
down_revision: Union[str, None] = "b20551f34a42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
