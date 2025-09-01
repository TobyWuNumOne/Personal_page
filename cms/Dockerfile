FROM alpine:3.20

ARG PB_VERSION=0.22.9
ENV PORT=8080
ENV PB_DATA_DIR=/pb/pb_data
ENV PB_PUBLIC_DIR=/pb/pb_public

RUN apk add --no-cache wget unzip ca-certificates tzdata \
  && adduser -D -H pbuser \
  && mkdir -p /pb ${PB_DATA_DIR} ${PB_PUBLIC_DIR} \
  && chown -R pbuser:pbuser /pb

WORKDIR /pb
USER pbuser

RUN wget -q https://github.com/pocketbase/pocketbase/releases/download/v${PB_VERSION}/pocketbase_${PB_VERSION}_linux_amd64.zip \
  && unzip pocketbase_${PB_VERSION}_linux_amd64.zip \
  && rm pocketbase_${PB_VERSION}_linux_amd64.zip \
  && chmod +x /pb/pocketbase

EXPOSE 8080

CMD ["/pb/pocketbase", "serve", "--http=0.0.0.0:${PORT}", "--dir=/pb"]
