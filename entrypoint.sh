#!/bin/bash
alembic upgrade head

exec python -m src.presentation.main