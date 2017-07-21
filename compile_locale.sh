#!/bin/bash
case "$1" in
  ru|ru)
    set -x
    if [ -r ./locale/$1/LC_MESSAGES/onobot.po ]; then
        msgfmt -o ./locale/$1/LC_MESSAGES/onobot.mo ./locale/$1/LC_MESSAGES/onobot.po
        #utils/msgfmt.py \
        #    -o ./locale/$1/LC_MESSAGES/onobot.mo \
        #   ./locale/$1/LC_MESSAGES/onobot.po
    fi
    ;;
  *)
    echo "Usage: $0 < ru >" >&2
    exit 1
    ;;
esac
