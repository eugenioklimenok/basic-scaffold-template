# User Guide

## What `new-scaffold` does

`new-scaffold` creates a base project structure inside a target path, following common conventions without installing packages or changing host configuration.

## When to use it

Use it when you need to:

- create a new project with a consistent layout
- avoid creating base folders and files by hand
- standardize `generic`, `api`, `bot`, or `worker` projects
- validate names and destination conflicts before writing files

## What it generates

Common base:

- `src/`
- `config/`
- `scripts/`
- `docs/`
- `tests/`
- `logs/`
- `tmp/`
- `data/`
- `.env.example`
- `README.md`

Type-specific extras:

- `api`: `src/api/entrypoint.example`
- `bot`: `src/bot/entrypoint.example`
- `worker`: `src/worker/entrypoint.example`
- `generic`: no extra type-specific files

Optional files:

- `.gitignore` with `--with-gitignore`
- placeholder `Makefile` with `--with-makefile`
- placeholder scripts with `--with-scripts`

## Important rules

- The project name must be in `kebab-case`.
- `--base-path` must exist and be writable.
- If the destination folder already exists and is empty, `--force` is required.
- If the destination folder already exists and is not empty, execution is only allowed when the existing content exactly matches the expected scaffold.
- `--dry-run` shows the exact plan without writing files.
- Output can be `text` or `json`.

## Base command

```bash
python3 ./bin/new-scaffold NAME --base-path PATH
```

Example:

```bash
python3 ./bin/new-scaffold support-bot --base-path /home/alex/apps --type bot --owner alex
```

## Available flags

### `name`

Project name. Positional and required.

### `--base-path`

Root path where the project folder will be created. Required.

### `--type`

Scaffold type:

- `generic`
- `api`
- `bot`
- `worker`

Default: `generic`

### `--owner`

Informational label used to record the expected project owner.

### `--force`

Allows reuse of an existing destination folder only when it is empty.

### `--dry-run`

Shows which directories and files would be created, without writing anything.

### `--output json|text`

Defines the output format.

- `text`: human-readable
- `json`: script-friendly

### `--with-gitignore`

Adds a base `.gitignore`.

### `--with-makefile`

Adds a neutral placeholder `Makefile`.

### `--with-scripts`

Adds `.example` files under `scripts/` to be completed for the real stack.

## Expected behavior

### Normal execution

If the destination does not exist, the project folder and expected scaffold content are created.

### Execution with `--dry-run`

Nothing is created. The command only reports the actions it would perform.

### Running the command a second time

If the existing content already matches the expected scaffold, the command completes safely and reports no changes.

### Conflicts

If unmanaged files or different content are found, the command returns a controlled error.

## Exit codes

- `0`: success
- `2`: functional validation error
- `3`: CLI usage error
- `4`: destination conflict

## What to do after generation

After creating the scaffold, complete the placeholders:

- define the real project entrypoint
- replace `.example` scripts with real scripts
- complete the `Makefile` if you use it
- update `README.md` and `.env.example` with project-specific information
