from __future__ import print_function, unicode_literals
"""Index uses per week, month and year

Revision ID: 40cdc63a949a
Revises: 4dd49c571575
Create Date: 2015-06-25 00:47:10.603094

"""

# revision identifiers, used by Alembic.
revision = '40cdc63a949a'
down_revision = '4dd49c571575'

import datetime
from alembic import op
import sqlalchemy as sa
import sqlalchemy.sql as sql

metadata = sa.MetaData()
uue = sa.Table('UserUsedExperiment', metadata,
    sa.Column('id', sa.Integer()),
    sa.Column('start_date_date', sa.Date()),
    sa.Column('start_date_month', sa.Integer()),
    sa.Column('start_date_year', sa.Integer()),
    sa.Column('start_date_week_monday', sa.Integer()),
    sa.Column('start_date_week_sunday', sa.Integer()),
)

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('UserUsedExperiment', sa.Column('start_date_month', sa.Integer(), nullable=True))
    op.add_column('UserUsedExperiment', sa.Column('start_date_week_monday', sa.Integer(), nullable=True))
    op.add_column('UserUsedExperiment', sa.Column('start_date_week_sunday', sa.Integer(), nullable=True))
    op.add_column('UserUsedExperiment', sa.Column('start_date_year', sa.Integer(), nullable=True))
    op.create_index(u'ix_UserUsedExperiment_start_date_month', 'UserUsedExperiment', ['start_date_month'], unique=False)
    op.create_index(u'ix_UserUsedExperiment_start_date_week_monday', 'UserUsedExperiment', ['start_date_week_monday'], unique=False)
    op.create_index(u'ix_UserUsedExperiment_start_date_week_sunday', 'UserUsedExperiment', ['start_date_week_sunday'], unique=False)
    op.create_index(u'ix_UserUsedExperiment_start_date_year', 'UserUsedExperiment', ['start_date_year'], unique=False)
    ### end Alembic commands ###

    s = sql.select([ uue.c.id, uue.c.start_date_date ]).order_by(uue.c.id)

    for use in op.get_bind().execute(s):
        use_id = use[uue.c.id]
        kwargs = {
            'start_date_month' : use[uue.c.start_date_date].month,
            'start_date_year' : use[uue.c.start_date_date].year,
            'start_date_week_sunday' : (use[uue.c.start_date_date] - datetime.date(1970, 1, 4)).days / 7,
            'start_date_week_monday' : (use[uue.c.start_date_date] - datetime.date(1970, 1, 5)).days / 7,
        }
        update_stmt = uue.update().where(uue.c.id == use_id).values(**kwargs)
        op.execute(update_stmt)

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(u'ix_UserUsedExperiment_start_date_year', table_name='UserUsedExperiment')
    op.drop_index(u'ix_UserUsedExperiment_start_date_week_sunday', table_name='UserUsedExperiment')
    op.drop_index(u'ix_UserUsedExperiment_start_date_week_monday', table_name='UserUsedExperiment')
    op.drop_index(u'ix_UserUsedExperiment_start_date_month', table_name='UserUsedExperiment')
    op.drop_column('UserUsedExperiment', 'start_date_year')
    op.drop_column('UserUsedExperiment', 'start_date_week_sunday')
    op.drop_column('UserUsedExperiment', 'start_date_week_monday')
    op.drop_column('UserUsedExperiment', 'start_date_month')
    ### end Alembic commands ###
