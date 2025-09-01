#!/bin/sh
set -e
# 你可以在這裡加自定義旗標，例如 --https 指向你的憑證（若自管）
./pocketbase serve --http 0.0.0.0:${PORT} --dir /pb
