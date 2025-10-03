#!/bin/sh
set -e

echo "Starting PocketBase..."
echo "Working directory: $(pwd)"
echo "PocketBase file exists: $(ls -la pocketbase 2>/dev/null || echo 'NOT FOUND')"

# 使用絕對路徑啟動 PocketBase
/pb/pocketbase serve --http 0.0.0.0:${PORT} --dir ${PB_DATA_DIR}
