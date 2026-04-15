# basic-scaffold-template

Framework mínimo para generar estructuras base de proyectos sin instalar servicios ni tocar configuración del host.
El contenido generado es agnóstico de lenguaje y deja placeholders donde cada equipo define su stack.

## Incluye

- CLI `bin/new-scaffold`
- Motor de render en `lib/python/basic_scaffold`
- Templates por tipo en `templates/basic`
- Tests unitarios y smoke en `tests`
- Documentación corta en `docs`
- Guía de usuario y manual paso a paso en `docs`

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

## Notas del scaffold

- `generic` crea solo estructura común y archivos base.
- `api`, `bot` y `worker` agregan un `entrypoint.example` descriptivo, no código ejecutable de un lenguaje específico.
- `--with-makefile` genera targets placeholder.
- `--with-scripts` genera archivos `.example` para completar según el stack real.

## Desarrollo

```bash
python3 -m unittest discover -s tests -v
```

## Documentación

- Contrato CLI: `docs/contract.md`
- Quickstart: `docs/quickstart.md`
- Guía de usuario: `docs/guia-de-usuario.md`
- Manual de uso: `docs/manual-de-uso.md`
