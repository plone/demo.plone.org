# syntax=docker/dockerfile:1
ARG VOLTO_VERSION
FROM plone/frontend-builder:${VOLTO_VERSION:-18.26.0} AS builder

COPY --chown=node packages/seven-demo /app/packages/seven-demo
COPY --chown=node registry.config.ts /app/
COPY --chown=node Makefile /app/Makefile
COPY --chown=node pnpm-workspace.yaml /app/pnpm-workspace.yaml
COPY --chown=node .pnpmfile.cjs /app/.pnpmfile.cjs
COPY --chown=node package.json /app/package.json.temp

RUN --mount=type=cache,id=pnpm,target=/app/.pnpm-store,uid=1000 <<EOT
    set -e
    python3 -c "import json; data = json.load(open('package.json.temp')); deps = data['dependencies']; data['dependencies'].update(deps); json.dump(data, open('package.json', 'w'), indent=2)"
    rm package.json.temp
    (cd core && git fetch --depth 1 origin seven:seven && git checkout seven)
    pnpm install && make build-deps
    pnpm build
    pnpm install --prod
EOT

FROM plone/frontend-prod-config:${VOLTO_VERSION:-18.26.0}

LABEL maintainer="Plone Community <collective@plone.org>" \
      org.label-schema.name="frontend-seven-frontend" \
      org.label-schema.description="Seven demo site frontend image." \
      org.label-schema.vendor="Plone Community"

COPY --from=builder /app/ /app/

# RUN <<EOT
#     set -e
#     corepack enable pnpm
#     corepack use pnpm@10.10.0
#     corepack prepare pnpm@10.10.0 --activate
# EOT

ENTRYPOINT [ "pnpm" ]
CMD ["start:prod"]
