# Quickstart

```bash
git clone <nuevo_repo>
cd <nuevo_repo>
chmod +x bin/*
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic
```

Optional flags:

- `--dry-run`
- `--with-gitignore`
- `--with-makefile`
- `--with-scripts`

After generation, replace placeholder files with the commands and entrypoints required by your stack.
