"""drop test table

Revision ID: e39fc5763c4c
Revises: 4b2a9f580ab9
Create Date: 2025-04-05 04:02:05.253112

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e39fc5763c4c"
down_revision: Union[str, None] = "4b2a9f580ab9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the test table
    op.drop_table("tests")


def downgrade() -> None:
    # Recreate the test table
    op.create_table(
        "tests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("link", sa.String(), nullable=True),
        sa.Column("remote_testing", sa.String(), nullable=True),
        sa.Column("adaptive_irt", sa.String(), nullable=True),
        sa.Column("test_type", sa.JSON(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("full_link", sa.String(), nullable=True),
        sa.Column("job_levels", sa.JSON(), nullable=True),
        sa.Column("languages", sa.JSON(), nullable=True),
        sa.Column("assessment_length", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_tests_name", "tests", ["name"])
