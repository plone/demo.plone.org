FROM node:16-slim as base
FROM base as builder

RUN apt-get update \
    && buildDeps="python3 build-essential" \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=node . /build/
RUN corepack enable

USER node
WORKDIR /build
RUN yarn install --network-timeout 1000000 \
    && yarn build

FROM base

LABEL maintainer="Plone Foundation <collective@plone.org>" \
      org.label-schema.name="plone-6-demo-site-frontend" \
      org.label-schema.description="Plone 6 Demo Site frontend image." \
      org.label-schema.vendor="Plone Foundation"

RUN apt-get update \
    && buildDeps="busybox" \
    && apt-get install -y --no-install-recommends $buildDeps \
    && busybox --install -s \
    && rm -rf /var/lib/apt/lists/*

USER node
COPY --from=builder /build/ /app/

WORKDIR /app
EXPOSE 3000
CMD ["yarn", "start:prod"]
