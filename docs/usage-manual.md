# Step-by-Step Usage Manual

## Goal

This manual shows the full flow for creating a new project with `new-scaffold`.

## Step 1. Enter the repository

```bash
cd /path/to/basic-scaffold-template
```

This repository contains the command:

```bash
python3 ./bin/new-scaffold
```

## Step 2. Choose name and destination

Define:

- a project name in `kebab-case`
- the base path where the project should be created
- the type: `generic`, `api`, `bot`, or `worker`

Example:

- name: `support-bot`
- base path: `/home/alex/apps`
- type: `bot`

## Step 3. Start with `--dry-run`

Before writing files, inspect the plan:

```bash
python3 ./bin/new-scaffold support-bot --base-path /home/alex/apps --type bot --owner alex --dry-run
```

Check that:

- the name is correct
- the destination path is correct
- the selected type is correct
- the list of files to create matches your expectations

## Step 4. Create the real scaffold

If the plan looks correct, run the command without `--dry-run`:

```bash
python3 ./bin/new-scaffold support-bot --base-path /home/alex/apps --type bot --owner alex --with-gitignore --with-makefile --with-scripts
```

## Step 5. Verify the result

Enter the generated project and review the structure:

```bash
cd /home/alex/apps/support-bot
```

You should see at least:

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

If the type is `bot`, you should also see:

- `src/bot/entrypoint.example`

## Step 6. Complete placeholders

The scaffold does not install anything and does not assume a specific language for the generated project. After generating the base structure, complete:

- `README.md` with the real project description
- `.env.example` with real environment variables
- `src/.../entrypoint.example` with the final entrypoint
- `scripts/*.example` with real operational scripts
- `Makefile` with real commands if you decided to use it

## Step 7. Understand special cases

### Case A. Destination folder does not exist

Expected result:

- the project is created normally

### Case B. Destination folder exists and is empty

Expected result:

- without `--force`: controlled error
- with `--force`: the folder is reused and the scaffold is created

Example:

```bash
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic --force
```

### Case C. Destination folder exists and has content

Expected result:

- if the content matches the expected scaffold, nothing breaks
- if there are differences or unmanaged files, the command returns a conflict

## Step 8. Use JSON output

If you want to integrate the command with automation:

```bash
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic --dry-run --output json
```

This is useful for:

- internal pipelines
- pre-check validations
- action auditing

## Quick examples

### Generic project

```bash
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic
```

### API with optional files

```bash
python3 ./bin/new-scaffold payments-api --base-path /home/alex/apps --type api --owner alex --with-gitignore --with-makefile --with-scripts
```

### Worker in simulation mode

```bash
python3 ./bin/new-scaffold emails-worker --base-path /home/alex/apps --type worker --dry-run
```

## Recommended usage checklist

Before running:

- confirm the `kebab-case` name
- confirm `base-path`
- confirm the type
- run `--dry-run`

After running:

- review the generated structure
- complete placeholders
- initialize Git if needed
- add project-specific documentation
