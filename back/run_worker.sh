#!/bin/bash
celery -A transcribing_web worker -P threads -B -l INFO
