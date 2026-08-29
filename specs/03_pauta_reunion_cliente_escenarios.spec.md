# 📋 Pauta de Entrevista con el Cliente y Simulador de Escenarios
## Sexta Compañía de Bomberos de Chillán Viejo

> **Propósito para Engram:** Registrar los requerimientos elicitados, las preguntas preparadas para el Directorio y los escenarios de respuesta para el levantamiento de información.

---

## 🚒 Bloque A: Inspección Post-Emergencia y Roles en Terreno

### 1. Responsable del Conteo al Retorno de la Emergencia
* **Pregunta:** "Al finalizar una emergencia y revisar el carro, ¿cada carro tiene un encargado que hace el conteo, o cualquier bombero voluntario puede hacerlo?"
* **Escenario A (Cualquier bombero):**
  * *Repregunta Deep Dive:* "¿El sistema debe exigir que el voluntario inicie sesión para registrar su responsabilidad, o el Maquinista/Teniente a cargo del carro debe visar el reporte?"
* **Escenario B (Solo el maquinista / oficial):**
  * *Repregunta Deep Dive:* "¿Y si el oficial está ocupado en el parte de comandancia? ¿Puede delegar en un voluntario y él solo aprobar después desde su celular?"

### 2. Alcance del Recuento (Total vs Parcial)
* **Pregunta:** "¿Se revisa el 100% de las herramientas del carro o solo las cortinas/gavetas utilizadas?"
* **Escenario A (Solo lo usado):**
  * *Repregunta Deep Dive:* "¿Prefieren que la app muestre el carro desglosado por cortinas (ej. Cortina Izquierda 1) para marcar solo esa sección, o un buscador general?"
* **Escenario B (Todo el carro):**
  * *Repregunta Deep Dive:* "¿Les sirve un botón rápido de 'Todo conforme según stock esperado' para que solo editen manualmente si hubo faltantes o herramientas dañadas?"

---

## ⚠️ Bloque B: Alertas de Discrepancias y Bajas Definitivas

### 3. Plazo de Búsqueda y Reaparición de Material
* **Pregunta:** "¿Qué plazo prudente se maneja antes de dar por perdida definitivamente una herramienta?"
* **Escenario:** Esperar 3 a 5 días por si otra compañía la devuelve al cuartel general.
* *Acción en BD:* La alerta queda en estado `PENDIENTE`. Si reaparece, se crea un `MOVIMIENTO` de tipo `RECUPERACION_POST_SINIESTRO` y se cierra la alerta como `RESUELTA_HALLAZGO`.

### 4. Aprobación y Respaldo Documental de Bajas
* **Pregunta:** "Para dar de baja un ítem dañado definitivamente, ¿quién autoriza y qué respaldo se exige?"
* **Escenario:** El Capitán decide lo operativo (material de carros) y el Director lo de cuartel/mobiliario.
* *Acción en BD:* Se exige campo `observaciones` y registro del `id_usuario` resolutor que aprueba la baja.
