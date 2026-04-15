# basic-scaffold-template

Framework mínimo para generar estructuras base de proyectos sin instalar servicios ni tocar configuración del host.

## Incluye

- CLI `bin/new-scaffold`
- Motor de render en `lib/python/basic_scaffold`
- Templates por tipo en `templates/basic`
- Tests unitarios y smoke en `tests`
- Documentación corta en `docs`

## Uso

```bash
python3 ./bin/new-scaffold soporte-bot --base-path /home/alex/apps --type bot --owner alex
```

## Flags

- `--force`
- `--dry-run`
- `--output json|text`
- `--with-gitignore`
- `--with-makefile`
- `--with-scripts`

## Tipos

- `generic`
- `api`
- `bot`
- `worker`

## Desarrollo

```bash
python3 -m unittest discover -s tests -v
```
