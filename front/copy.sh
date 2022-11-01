#!/bin/bash
rm -R dist/
rm -R node_modules/.cache/
npm run build
cp dist/index.html ../back/index/templates/index/
rm ../back/index/static/index/css/*
cp -R dist/css ../back/index/static/index/
rm ../back/index/static/index/js/*
cp -R dist/js ../back/index/static/index/
cp dist/favicon.ico ../back/index/static/index/
