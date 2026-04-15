# CLI Contract

## Command

`new-scaffold name --base-path PATH [options]`

## Supported types

- `generic`
- `api`
- `bot`
- `worker`

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
