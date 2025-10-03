FROM alpine:3.20

ARG PB_VERSION=0.22.9
ENV PORT=8080
ENV PB_DATA_DIR=/pb/pb_data
ENV PB_PUBLIC_DIR=/pb/pb_public

RUN apk add --no-cache wget unzip ca-certificates tzdata \
  && mkdir -p /pb ${PB_DATA_DIR} ${PB_PUBLIC_DIR}

WORKDIR /pb

# 下載並設置 PocketBase
RUN wget -q https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip \
  && unzip pocketbase_${PB_VERSION}_linux_amd64.zip \
  && rm pocketbase_${PB_VERSION}_linux_amd64.zip \
  && chmod +x pocketbase \
  && ls -la pocketbase

COPY start.sh /pb/start.sh
RUN chmod +x /pb/start.sh

# 移除 USER pbuser - 以 root 身份運行來處理 volume 權限
# USER pbuser

EXPOSE 8080

CMD ["/bin/sh", "/pb/start.sh"]
