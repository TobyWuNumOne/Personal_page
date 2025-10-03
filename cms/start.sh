#!/bin/sh
set -e

echo "Starting PocketBase..."
echo "Working directory: $(pwd)"
echo "Current user: $(whoami)"
echo "PocketBase file exists: $(ls -la pocketbase 2>/dev/null || echo 'NOT FOUND')"
echo "Data directory: ${PB_DATA_DIR}"
echo "Data directory permissions: $(ls -ld ${PB_DATA_DIR} 2>/dev/null || echo 'NOT FOUND')"

# 確保資料目錄存在且有正確權限
mkdir -p ${PB_DATA_DIR}
echo "Ensuring correct permissions for data directory..."
chmod 755 ${PB_DATA_DIR}
echo "Data directory permissions after fix: $(ls -ld ${PB_DATA_DIR})"

# 測試寫入權限
echo "Testing write permissions..."
touch ${PB_DATA_DIR}/test.txt && rm ${PB_DATA_DIR}/test.txt && echo "Write test: SUCCESS" || echo "Write test: FAILED"

echo "Starting PocketBase server..."
# 使用絕對路徑啟動 PocketBase
/pb/pocketbase serve --http 0.0.0.0:${PORT} --dir ${PB_DATA_DIR}
