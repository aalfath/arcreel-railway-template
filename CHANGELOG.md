# Changelog

Breaking changes come first in each entry. Read the entry before you apply an update in Railway.

## ArcReel 0.37.0 (2026-11-21)

- First release of the template: ArcReel [v0.37.0](https://github.com/ArcReel/ArcReel/releases/tag/v0.37.0) (`arcreel/arcreel:0.37.0@sha256:9c15544e27c81953dd15475289124b8684afef4368dc9809cc49d0a5381d158d`) with Railway Postgres, one volume at `/data`, a generated login password and a `/health` check.
- Agent Bash runs in ArcReel's allowlist mode when bubblewrap can't create namespaces (Railway containers).
