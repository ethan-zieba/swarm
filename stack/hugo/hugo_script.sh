#!/bin/bash

LOCAL_DIR="$1"
REMOTE_USER="user"
REMOTE_HOST="10.10.10.10"
REMOTE_PATH="/home/user/hugo_backups"
ARCHIVE_NAME="$(basename "$LOCAL_DIR")_$(date +%Y%m%d_%H%M%S).tar.gz"

if [ -z "$LOCAL_DIR" ]; then
  echo "Usage: $0 /path/to/directory"
  exit 1
fi

if [ ! -d "$LOCAL_DIR" ]; then
  echo "Error: Directory '$LOCAL_DIR' does not exist."
  exit 1
fi

echo "[*] Compressing $LOCAL_DIR to $ARCHIVE_NAME..."
tar -czf "$ARCHIVE_NAME" -C "$(dirname "$LOCAL_DIR")" "$(basename "$LOCAL_DIR")"

if [ $? -ne 0 ]; then
  echo "Compression failed."
  exit 1
fi

echo "[*] Sending $ARCHIVE_NAME to $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH..."
scp "$ARCHIVE_NAME" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"

if [ $? -ne 0 ]; then
  echo "File transfer failed."
  exit 1
fi

echo "[*] Cleaning up local archive..."
rm "$ARCHIVE_NAME"

echo "Backup done."

