#!/bin/bash
msgfmt -o ./locale/ru/LC_MESSAGES/onobot.mo ./locale/ru/LC_MESSAGES/onobot.po
python3 cli.py --run 2>&1 | tee -a log/bot.log