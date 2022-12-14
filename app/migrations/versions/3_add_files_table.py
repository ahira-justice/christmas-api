"""Add files table

Revision ID: ab8296a74e19
Revises: 7ecf754749f7
Create Date: 2022-12-11 18:33:11.594326

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ab8296a74e19'
down_revision = '7ecf754749f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=False),
                    sa.Column('updated_on', sa.DateTime(), nullable=True),
                    sa.Column('is_deleted', sa.Boolean(), nullable=False),
                    sa.Column('reference', sa.String(), nullable=False),
                    sa.Column('url', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_files_id'), 'files', ['id'], unique=False)
    op.create_index(op.f('ix_files_reference'), 'files', ['reference'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_files_reference'), table_name='files')
    op.drop_index(op.f('ix_files_id'), table_name='files')
    op.drop_table('files')
    # ### end Alembic commands ###
