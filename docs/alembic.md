## init alembic
> alembic init src/migrations

## import models to env.py

## set db url in env.py

## set metadata in env.py (target_metadata = Base.metadata)

## create migration
> alembic revision --autogenerate -m "commit"


## update the database
> alembic upgrade head


## downgrade migration
> alembic downgrade 'down_revision_number'