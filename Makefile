SHELL := /bin/bash

MODULE=wellread
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate
CONDA_CREATE=echo "y" | conda create -n wellread python=3.8
RUN_DEV=uvicorn app.main:app --reload
RUN_PROD=uvicorn app.main:app --host 0.0.0.0 --port 7000


.PHONY: env
env:
	$(CONDA_CREATE) 
	($(CONDA_ACTIVATE) $(MODULE); poetry install)

.PHONY: run-dev
run-dev:
	$(RUN_DEV)

.PHONY: run-prod
run-prod:
	$(RUN_PROD)

.PHONY: git-hooks
git-hooks:
	chmod +x githooks/*
	mkdir -p .git/hooks
	cd .git/hooks && ln -sf ../../githooks/* .
