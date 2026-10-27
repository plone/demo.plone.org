# syntax=docker/dockerfile:1
ARG AURORA_VERSION=1.0.0-alpha.19
FROM plone/aurora-builder:${AURORA_VERSION} AS builder

COPY --chown=node packages/plone-aurora-demo /app/packages/plone-aurora-demo
COPY --chown=node registry.config.ts /app/
COPY --chown=node Makefile /app/Makefile
COPY --chown=node pnpm-workspace.yaml /app/pnpm-workspace.yaml
COPY --chown=node .pnpmfile.cjs /app/.pnpmfile.cjs
COPY --chown=node package.json /app/package.json
COPY --chown=node pnpm-lock.yaml /app/pnpm-lock.yaml

RUN --mount=type=cache,id=pnpm,target=/app/.pnpm-store,uid=1000 <<EOT
    set -e
    export CI=true
    # The builder image ships the default scaffolded add-on, which is not in our lockfile
    rm -rf /app/packages/plone-aurora
    pnpm install && make build-deps
    pnpm build
    CI=1 pnpm install --prod
EOT

FROM plone/aurora-prod-config:${AURORA_VERSION}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="plone-aurora-demo-frontend" \
      org.label-schema.description="Plone Aurora demo site frontend image." \
      org.label-schema.vendor="Plone Community"

COPY --from=builder /app/ /app/

RUN <<EOT
    set -e
    export CI=true
    corepack enable pnpm
    corepack use pnpm@11.20.0
    corepack prepare pnpm@11.20.0 --activate
EOT

ENTRYPOINT [ "pnpm" ]
CMD ["start:prod"]
