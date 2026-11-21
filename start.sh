#!/bin/sh
# Railway start script for ArcReel.
set -eu

DATA=/data
mkdir -p "$DATA" "$ARCREEL_DATA_DIR" "$DATA/claude"

# Agent runtime data (~/.claude) lives on the volume too. Railway gives a service one volume.
if [ ! -L /root/.claude ]; then
  if [ -d /root/.claude ]; then
    cp -a /root/.claude/. "$DATA/claude/" 2>/dev/null || true
    rm -r /root/.claude
  fi
  ln -s "$DATA/claude" /root/.claude
fi

cd /app
exec python /app/railway_launch.py
