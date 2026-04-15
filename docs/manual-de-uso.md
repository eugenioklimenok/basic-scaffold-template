# Manual de Uso Paso a Paso

## Objetivo

Este manual muestra el flujo completo para crear un proyecto nuevo usando `new-scaffold`.

## Paso 1. Entrar al repo

```bash
cd /ruta/al/repo/basic-scaffold-template
```

En este repositorio vive el comando:

```bash
python3 ./bin/new-scaffold
```

## Paso 2. Elegir nombre y destino

Definí:

- nombre del proyecto en `kebab-case`
- ruta base donde querés crear el proyecto
- tipo: `generic`, `api`, `bot` o `worker`

Ejemplo:

- nombre: `soporte-bot`
- base path: `/home/alex/apps`
- tipo: `bot`

## Paso 3. Probar primero con `--dry-run`

Antes de escribir archivos, revisá el plan:

```bash
python3 ./bin/new-scaffold soporte-bot --base-path /home/alex/apps --type bot --owner alex --dry-run
```

Qué revisar:

- que el nombre sea correcto
- que la ruta destino sea la esperada
- que el tipo elegido sea el correcto
- que la lista de archivos a crear coincida con tu intención

## Paso 4. Crear el scaffold real

Si el plan está bien, ejecutá el comando sin `--dry-run`:

```bash
python3 ./bin/new-scaffold soporte-bot --base-path /home/alex/apps --type bot --owner alex --with-gitignore --with-makefile --with-scripts
```

## Paso 5. Verificar el resultado

Entrá al proyecto generado y revisá la estructura:

```bash
cd /home/alex/apps/soporte-bot
```

Deberías ver al menos:

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

Si el tipo fue `bot`, además:

- `src/bot/entrypoint.example`

## Paso 6. Completar placeholders

El scaffold no instala nada ni asume un lenguaje concreto para el proyecto generado. Por eso, después de crear la base, completá:

- `README.md` con la descripción real del proyecto
- `.env.example` con variables reales
- `src/.../entrypoint.example` con el entrypoint definitivo
- `scripts/*.example` con scripts operativos reales
- `Makefile` con comandos reales si decidiste usarlo

## Paso 7. Entender casos especiales

### Caso A. La carpeta destino no existe

Resultado esperado:

- el proyecto se crea normalmente

### Caso B. La carpeta destino existe y está vacía

Resultado esperado:

- sin `--force`: error controlado
- con `--force`: reutiliza la carpeta y crea el scaffold

Ejemplo:

```bash
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic --force
```

### Caso C. La carpeta destino existe y tiene contenido

Resultado esperado:

- si el contenido coincide con el scaffold esperado, no rompe nada
- si hay diferencias o archivos no gestionados, devuelve conflicto

## Paso 8. Usar salida JSON

Si querés integrar el comando con automatizaciones:

```bash
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic --dry-run --output json
```

Esto sirve para:

- pipelines internas
- validaciones previas
- auditoría de acciones previstas

## Ejemplos rápidos

### Proyecto genérico

```bash
python3 ./bin/new-scaffold demo-app --base-path /home/alex/apps --type generic
```

### API con archivos opcionales

```bash
python3 ./bin/new-scaffold pagos-api --base-path /home/alex/apps --type api --owner alex --with-gitignore --with-makefile --with-scripts
```

### Worker en modo simulación

```bash
python3 ./bin/new-scaffold emails-worker --base-path /home/alex/apps --type worker --dry-run
```

## Checklist de uso recomendado

Antes de ejecutar:

- confirmar nombre en `kebab-case`
- confirmar `base-path`
- confirmar tipo
- correr `--dry-run`

Después de ejecutar:

- revisar estructura creada
- completar placeholders
- inicializar Git si corresponde
- agregar documentación específica del proyecto
