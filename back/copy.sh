#!/bin/bash
rsync -rlp --exclude '.git' --exclude 'tr_models' --exclude 'venv' --exclude 'models' . /home/transcribing_web/
