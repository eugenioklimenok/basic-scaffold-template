# CLI Contract

## Command

`new-scaffold name --base-path PATH [options]`

## Supported types

- `generic`
- `api`
- `bot`
- `worker`

## Generated content policy

- The scaffold is language-agnostic.
- Optional files created by flags are placeholders and must be completed by the target project.
- Type-specific scaffolds add descriptive entrypoint placeholder files, not runnable framework code.

## Validation rules

- `name` must use kebab-case.
- `--base-path` must exist, be a directory, and be writable.
- Existing empty destinations require `--force`.
- Existing non-empty destinations are allowed only when every managed path already matches the expected scaffold content.

## Exit codes

- `0`: success
- `2`: functional validation error
- `3`: CLI usage error
- `4`: destination conflict

## Output modes

- `text`: human-readable summary
- `json`: deterministic machine-readable payload
