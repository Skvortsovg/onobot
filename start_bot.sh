#!/bin/bash
python3 cli.py --run 2>&1 | tee -a log/bot.log
