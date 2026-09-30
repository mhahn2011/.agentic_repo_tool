# E-008 trial image: one fresh container per trial. Build with docker/trial-arrow/build.py (stages the context).
# Contains: python 3.12, git, node 22 + pinned Claude Code CLI, arrow at the pinned commit (with .git) and its test
# deps, and the map-and-move tool at /opt/tools/script_map_and_move. Does NOT contain tasks, expected.json or
# reference solutions (the runner copies the grader in after the agent has finished).
FROM node:22-slim AS node

FROM python:3.12-slim
ARG CLAUDE_CODE_VERSION=2.1.284
RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION} \
 && npm cache clean --force
COPY arrow-requirements.txt /tmp/arrow-requirements.txt
RUN pip install --no-cache-dir -r /tmp/arrow-requirements.txt && rm /tmp/arrow-requirements.txt
RUN useradd --create-home --uid 1000 --shell /bin/bash trial \
 && mkdir -p /work /out /opt/tools /opt/grader \
 && chown trial:trial /work /out /opt/grader
COPY --chown=trial:trial arrow /work/arrow
COPY script_map_and_move /opt/tools/script_map_and_move
USER trial
ENV HOME=/home/trial PYTHONDONTWRITEBYTECODE=1
LABEL e008.claude_code_version=${CLAUDE_CODE_VERSION}
WORKDIR /work/arrow
CMD ["sleep", "infinity"]
