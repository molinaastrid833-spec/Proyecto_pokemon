# Pokémon Battle Web

Aplicación web interactiva desarrollada con **Flask**, **Jinja2** y **CSS** para la gestión de Pokémon y simulación visual de combates en tiempo real.

---

## Descripción

**Pokémon Battle Web** es un proyecto enfocado en la construcción de una aplicación web dinámica. Permite a los usuarios registrarse como Entrenadores, explorar y filtrar un catálogo completo de Pokémon, inspeccionar estadísticas detalladas y participar en enfrentamientos en una arena de batalla.

---

## Tecnologías 

- **Backend:** Python 3, Flask framework.
- **Frontend:** HTML5, CSS, Jinja2 Templating.
- **Fuente de Datos:** JSON local (`pokemons-ugly.json`).

---

## Instalación y Configuración

### 1. Clonar el repositorio:
```bash
git clone https://github.com/molinaastrid833-spec/Proyecto_pokemon.git

cd Proyecto_pokemon
```

### 2. Crear el entorno virtual:
```bash
python -m venv .venv
```

### 3. Activar el entorno virtual:
- **Windows PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (de instituto por restricciones):**
  ```powershell
  (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1)
  ```

### 4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación:
```bash
python -m app.main
```
O mediante el CLI de Flask:
```bash
python -m flask --app main run --port 8080
```

---

## Interacción del Usuario

1. **Bienvenida (inicio) (`/`):**
   El usuario ingresa a la aplicación, presencia un Pokémon destacado seleccionado de forma aleatoria y se registra introduciendo su nombre de entrenador.
2. **Catalogo y Filtrado (`/pokemons`):**
   Accede al catálogo de especímenes. Puede realizar búsquedas combinadas mediante un panel de filtro acumulativo (nombre, tipo y peso mínimo). Los filtros aplicados se conservan en la sesión.
3. **Detalles (`/pokemons/<id>`):**
   Selecciona un Pokémon para analizar sus características, tipos y barras de estadísticas base. Desde aquí puede presionar **Listo para el combate** para ir directo a la arena.
4. **Preparación del Combate (`/preparar_batalla`):**
   Vía alternativa donde el entrenador puede escribir manualmente el nombre de un Pokémon oponente con validación en servidor.
5. **Estadio de Batalla (`/batalla`):**
   Muestra el enfrentamiento cara a cara (VS) entre el Pokémon seleccionado y un rival aleatorio no repetido, desplegando barras de HP dinámicas, niveles calculados y 4 movimientos de ataque aleatorios.
6. **Cierre de Sesión (`/logout`)**:
Disponible desde la barra superior de la interfaz mientras exista una sesión activa. Borra los datos almacenados en el servidor/cookie de la sesión y redirige de vuelta a la pantalla de bienvenida.

---

## Vistas y Rutas

| Ruta | Método | Protección | Descripción / Lógica asociada |
| :--- | :---: | :---: |:---|
| `/` | `GET`, `POST` | Pública |**Portada / Registro:** Formulario `POST` para capturar el nombre del entrenador (validación de 3 a 15 caracteres). Muestra una ficha aleatoria de bienvenida. |
|`/logout` | `GET` | Pública |**Cierre de Sesión:** Borra todo el contenido de la sesión mediante session.clear() y redirige al usuario a la portada.|
| `/pokemons` | `GET` | @login |**Catálogo y Filtro :** Muestra la cuadrícula de Pokémon filtrada dinámicamente mediante `GET` según 3 criterios: coincidencia de nombre, tipos y peso. Recupera y guarda los criterios de búsqueda en session["filtros"]. |
| `/pokemons/<id>` | `GET` | @login |**Detalles de cada poke:** Vista detallada de un Pokémon con sus imágenes, dimensiones físicas, estadísticas base y acceso directo a la arena de combate. |
| `/preparar_batalla` | `GET`, `POST` | @login | **Selección Manual:** Formulario `POST` que valida la existencia del Pokémon introducido en el catálogo JSON antes de proceder. |
| `/batalla` | `GET` | @login | **Arena de Combate (VS):** Genera la experiencia de combate en formato cara a cara. Selecciona un rival aleatorio distinto al jugador, calcula HP y nivel en tiempo real, y extrae 4 ataques aleatorios con `random.sample()`. |
| `/nueva_batalla` | `POST` | @login | Reiniciar Combate (battle.nueva_batalla): Elimina session["battle"] conservando el Pokémon del entrenador y redirige a /battle para enfrentar a un nuevo rival aleatorio. |

## Mantenimiento de Estado con Sesiones
Debido a la naturaleza stateless del protocolo HTTP, el servidor no recuerda las peticiones anteriores del cliente. Para resolver esto y evitar juntar información sensible en la URL (?trainer=...), la aplicación utiliza las sesiones nativas de Flask (flask.session).

### ¿Qué se guarda en la sesión y por qué?



| Dato | Clave en session | Justificación |
| :-- | :--: | :-- | 
| Nombre del Entrenador | ``session["trainer"]`` | **Identificación y Control de Acceso:** Mantiene la identidad del usuario activo durante toda la navegación. Sirve como base para el decorador @login que bloquea el acceso a rutas privadas si no se ha iniciado sesión previa. Elimina la necesidad de pasar el parámetro por URL en cada vista o plantilla.|
| Filtros del Catálogo| ``session["filtros"]`` | **Persistencia de la Experiencia de Usuario (UX):** Almacena los criterios de búsqueda aplicados (nombre, tipo, peso mínimo). Si la entrenadora entra a inspeccionar la ficha detallada de un Pokémon `(/pokemons/<id>)` y regresa al catálogo, los filtros aplicados se mantienen intactos y la lista no se reinicia.|
| Pokémon para la Batalla | ``session["pokemon_batalla"]`` | **Mantenimiento del Contexto de Combate:** Registra el nombre del Pokémon seleccionado para combatir. Permite acceder y recargar la vista del estadio ``(/batalla)`` sin perder la selección realizada en la sala de preparación o desde la ficha de detalles.|


## Medidas de Seguridad Implementadas
- **Firma Criptográfica ``(app.secret_key)``:** Flask convierte la sesión a formato JSON y la firma mediante un secreto antes de enviarla al cliente. Si el usuario modifica el contenido de la cookie en su ordenador, la firma se invalida automáticamente.

- **SESSION_COOKIE_HTTPONLY = True:** Le indica al navegador que la cookie de sesión no debe ser accesible a través de JavaScript, protegiendo a la aplicación ante ataques de tipo XSS (Cross-Site Scripting).

- **SESSION_COOKIE_SAMESITE = 'Lax':** Restringe el envío automático de la cookie desde enlaces de sitios web externos, reduciendo el riesgo de ataques CSRF (Cross-Site Request Forgery).

- **Decorador de Autenticación (@login):** Intercepta las solicitudes a rutas protegidas (/pokemons, /pokemons/<id>, /preparar_batalla, /batalla) e impide el acceso directo escribiendo la URL en el navegador si no existe un entrenador registrado en session["trainer"].

## Gestión de Sesiones

Para esta fase se ha integrado la extensión **Flask-Session** configurada con almacenamiento en el sistema de archivos del servidor (`filesystem`).

### Datos almacenados en `session`:
* `session["trainer"]`: Guarda la identidad del entrenador tras validar la longitud del nombre (3 a 15 caracteres).
* `session["pokemon_batalla"]`: Guarda el nombre del Pokémon seleccionado para el combate.
* `session["batalla"]`: Guarda un diccionario con la estructura completa del combate actual (`user_pok`, `rival_pok` y `ataques`), garantizando que la batalla persista y no genere un rival o movimientos aleatorios al refrescar la página (F5).

### Seguridad y Configuración:
* Se utiliza un decorador `@login` para proteger todas las rutas privadas de la aplicación.
* Las cookies de sesión están firmadas (`SESSION_USE_SIGNER = True`), marcadas como `HTTPOnly` y con política `SameSite=Lax`.
* Se ha eliminado todo paso de parámetros de identidad o estado por Query Parameters (URL).

## Organización de Rutas mediante Blueprints

Para evitar la concentración de endpoints en un único script monolítico (`main.py`), la capa de presentación se ha desacoplado en tres **Blueprints** independientes ubicados en la carpeta `app/routes/`:

1. **`auth_bp` (`app/routes/auth_routes.py`):**
   * Separa el flujo de autenticación e identidad de la aplicación. Gestiona la bienvenida, el formulario inicial de entrenador, el cierre de sesión y el decorador de seguridad `@login_required`.

2. **`pokemon_bp` (`app/routes/pokemon_routes.py`):**
   * Agrupa todas las operaciones relativas a la consulta de información del catálogo (listado filtrado y vista detallada). Aislar estas rutas permite modificar la visualización o las búsquedas sin afectar la lógica de combate ni la sesión.

3. **`battle_bp` (`app/routes/battle_routes.py`):**
   * Encapsula el módulo de enfrentamientos (preparación y arena de combate VS). Mantiene limpia la sesión de combate (`session["batalla"]`) y la interacción con los servicios de generación de rivales.

## Formularios y Seguridad con Flask-WTF 

Se ha integrado la extensión **Flask-WTF** junto a **WTForms** para abstraer los formularios HTML en clases de Python orientadas a objetos dentro de la carpeta `app/forms/`:

* `EntrenadorForm` (`app/forms/auth_forms.py`): Reemplaza la lectura manual de `request.form` en la portada, validando la longitud del nombre del entrenador (entre 3 y 15 caracteres) de forma declarativa.
* `PrepararBatallaForm` (`app/forms/battle_forms.py`): Controla la entrada del nombre del Pokémon para el combate.

### Mejoras de Seguridad e Integración:
* **Protección CSRF:** Cada formulario renderizado con `{{ form.hidden_tag() }}` incluye un campo oculto con un token criptográfico único generado a partir de `app.secret_key`, previniendo ataques Cross-Site Request Forgery.
* **Validación Server-Side limpia:** Se utiliza `form.validate_on_submit()` en las rutas para comprobar que la petición sea `POST` y que todos los validadores devuelvan `True` antes de procesar la lógica de negocio.

## Sistema de Batalla por Turnos y Lógica de Combate

El combate se modela en la clase `Battle` (`app/models/battle.py`) con una estructura serializable en JSON (`participants` con `[0]` entrenador y `[1]` `"CPU"`, `turns` y `winner`) y los métodos `attack(move_name)`, `current_hp(participant)`, `is_over()` y `log()`.

### Reglas Base del Combate
- **Precisión (`hit`):** Acierta siempre si `accuracy` es `None`; en caso contrario, usa su valor como probabilidad porcentual.
- **Daño base (`damage`):** Parte de un valor aleatorio entre el **15 % y el 30 %** de `max_hp` del defensor para evitar victorias de un solo golpe.
- **Vida mínima (`remaining_hp`):** Nunca desciende por debajo de `0`.
- **Orden de turnos (`number`):** Incrementa de forma consecutiva; ataca primero el usuario (`0`) y, solo si sigue en pie (`not is_over()`), responde la CPU (`1`).

### Mecánicas y Justificación
Basadas solo en los datos del JSON (`types`, `power`, `attack`, `defense`, `speed`) y almacenadas en las claves extra `stab` y `critical` sin alterar las obligatorias:

1. **Bonificación por Mismo Tipo — STAB (`"stab": bool`):**
   - **Efecto:** Multiplica el daño por **1.20 (+20 %)** si el tipo del movimiento coincide con alguno de los tipos del atacante.
   - **Justificación:** Premia elegir movimientos afines al Pokémon y da valor estratégico a consultar su ficha de detalle antes de combatir.
2. **Escalado por Potencia y Ataque/Defensa:**
   - **Efecto:** Modula el daño mediante un factor de potencia (`0.90`–`1.10` según `move.power`) y la relación `attack`/`defense` acotada entre `0.85` y `1.20`.
   - **Justificación:** Hace que las estadísticas de cada especie y la potencia de cada ataque influyan en el combate sin romper el equilibrio.
3. **Golpe Crítico por Velocidad (`"critical": bool`):**
   - **Efecto:** Probabilidad base del **10 %** más `speed / 1000` (tope del **30 %**); si salta, multiplica el daño por **1.5**.
   - **Justificación:** Da utilidad táctica a `speed` (al atacar siempre primero el jugador) y añade tensión reflejada en el `log`.

### Excepciones de Dominio
Definidas en `app/exceptions/exceptions.py`: `BattleError` (base), `InvalidMoveError` (movimiento ajeno al Pokémon) y `BattleAlreadyOverError` (ataque con la batalla finalizada). La ruta `/battle` captura `BattleError`, conserva intacta `session["battle"]` e informa al usuario.

---

## Gestión de Sesiones y Seguridad

Se emplea **Flask-Session** (`filesystem`) con cookies firmadas (`SESSION_USE_SIGNER = True`), `SESSION_COOKIE_HTTPONLY = True` y `SESSION_COOKIE_SAMESITE = "Lax"`.

| Clave en `session` | Uso y Justificación |
| :--- | :--- |
| `trainer` | Identifica al entrenador activo y habilita el acceso mediante `@login_required`. |
| `pokemon_batalla` | Mantiene el Pokémon seleccionado entre vistas y nuevas partidas. |
| `battle` | Serializa el estado del combate; junto al patrón **Post/Redirect/Get (PRG)** en `/battle`, evita repetir ataques al recargar (`F5`). |

**Protección CSRF (Flask-WTF):** Todos los formularios (`EntrenadorForm`, `PrepararBatallaForm` y `AtacarForm`) incluyen token CSRF (`{{ form.hidden_tag() }}`) y validación `validate_on_submit()`.