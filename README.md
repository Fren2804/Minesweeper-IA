# 🧨 Buscaminas en Python

## 📌 Descripción

Este proyecto consiste en un bot para jugar automáticamente al clásico juego del **Buscaminas**. Existen **dos versiones del programa**:

- Una versión **completa y funcional**, ubicada en el directorio principal, que utiliza la biblioteca **PyAutoGUI**.
- Una versión **incompleta**, ubicada en un subdirectorio, que fue desarrollada inicialmente con **Selenium**.

## 🚀 Motivación y evolución

Comencé desarrollando el bot con Selenium. Conseguí que identificara las minas e hiciera clic en las casillas seguras. Sin embargo, el rendimiento era muy lento, así que busqué alternativas más rápidas. Fue entonces cuando descubrí **PyAutoGUI**, que resultó mucho más eficiente para este caso.

---

## 🧪 Versión con Selenium

Esta versión necesita un **driver de Chrome**. Al ejecutar el programa, se abre una ventana del navegador con un mensaje que indica que está siendo automatizado. Esto puede ser un inconveniente en páginas que bloquean la automatización y es algo para tener en cuenta en proyectos futuros.

### ❌ Limitaciones

- Selenium carga todos los elementos de la página (HTML, CSS...), lo cual lo hace **muy lento**.
- Cada vez que se hace clic en una casilla segura, la página se **recarga parcialmente**, haciendo el proceso más pesado.
- En mis pruebas:
  - El nivel **principiante** se resolvía en unos **7 segundos**.
  - El nivel **intermedio** en aproximadamente **18 segundos**.
  - Esto es **demasiado lento** para un bot eficiente.

### ✅ Ventajas

- Al trabajar directamente con los elementos del **DOM**, Selenium permite una mayor **flexibilidad** en cuanto a resolución de pantalla, posición de los elementos y precisión en la interacción.
- Los elementos del juego son **fáciles de identificar** gracias a sus clases e identificadores bien estructurados.

---

### 🧾 Datos del DOM del Buscaminas

Al inspeccionar el HTML del juego, es posible identificar con facilidad la información relevante de cada casilla. Por ejemplo:

- La **clase (`class`)** indica el **estado de la casilla** (en blanco, descubierta, número de minas cercanas, etc.).
- El **identificador (`id`)** proporciona la **posición** de la casilla en formato `fila_columna`.

#### Ejemplos de casillas:

- **Casilla en blanco**, sin descubrir. Podría contener una mina.  
  (x = 20, y = 8)  
  ```html
  <div class="square blank" id="8_20"></div>
  ```

- **Casilla descubierta con el número 2**, lo que indica que hay dos minas alrededor.  
  (x = 16, y = 7)  
  ```html
  <div class="square open2" id="7_16"></div>
  ```

---

### 🎮 Estado de la partida

También es posible detectar el **estado del juego** (en curso, ganado o perdido) a través de un elemento del DOM con identificador `"face"` y una clase que cambia dinámicamente:

- Si la clase es `"facesmile"`, significa que la partida **sigue activa**.  
  ```<div class="facesmile" style="margin-left:182px; margin-right: 182px;" id="face"></div>```

---

### 📋 Resumen de clases útiles

| Clase              | Significado                             |
|-------------------|------------------------------------------|
| `square blank`       | Casilla no descubierta (posible mina)    |
| `square open0`       | Casilla descubierta, 0 minas alrededor   |
| `square open1`       | Casilla descubierta, 1 mina alrededor    |
| `square open2`       | Casilla descubierta, 2 minas alrededor   |
| `square open3`       | Casilla descubierta, 3 minas alrededor   |
| `square open4`       | Casilla descubierta, 4 minas alrededor   |
| `square open5`       | Casilla descubierta, 5 minas alrededor   |
| `square open6`       | Casilla descubierta, 6 minas alrededor   |
| `square open7`       | Casilla descubierta, 7 minas alrededor   |
| `square open8`       | Casilla descubierta, 8 minas alrededor   |
| `square bombflagged` | Casilla marcada con posible bomba           |
| `facesmile`          | Partida en curso                         |
| `facewin`            | Has ganado                               |
| `facedead`           | Has perdido                              |



## 🧪 Versión con PyAutoGUI (versión final)

Esta versión no necesita interactuar con el navegador ni analizar el DOM. En su lugar, **actúa directamente sobre capturas de pantalla**, analizando los **píxeles** de la imagen y comparándolos con los píxeles de tu pantalla. El bot actúa como si fueras tú utilizando el ratón.

---

### ❌ Limitaciones

- Aunque PyAutoGUI permite buscar **patrones visuales** o imágenes dentro de la pantalla, cuanto **más amplia** es la zona que analizas, **más lento** será el proceso.
- Si usas **valores de píxeles exactos**, el sistema es muy rápido, pero pierde flexibilidad. Si la página se desplaza incluso **un solo píxel**, el bot puede dejar de funcionar.
- Cuanta más **precisión** exijas, menor será el **margen de error** permitido.
- Es necesario hacer una especie de **"data mining" manual** para identificar qué píxeles o colores te interesa capturar y qué significan. Es decir, tú defines tus propios datos a partir de la imagen.

---

### ✅ Ventajas

- Usando coordenadas y colores de **píxeles exactos**, el bot es **extremadamente rápido**.
- Permite un mayor **margen de optimización** que Selenium.
- Al hacer clic, **no es necesario recargar la página** ni esperar ninguna transición.
- En mis pruebas:
  - El nivel **principiante** se resolvía en aproximadamente **1 segundo**.
  - El nivel **intermedio** en unos **3 segundos**.
  - El nivel **experto** en unos **10 segundos**.
  - Estos tiempos son **muy superiores** a los que obtuve usando Selenium.

---

### 📊 Datos de ejemplo

A diferencia de Selenium, aquí los datos **los defines tú** a partir de lo que ves en pantalla. Por ejemplo:
```python
config.x_victory = 446 - config.screenshot_left
```  

Este valor (`x_victory`) representa la posición horizontal (coordenada X) del píxel donde se muestra la **cara de victoria**. Se calcula en base al desplazamiento del área capturada.

Otro ejemplo:
```python
(255, 0, 0): 3
``` 

Esto indica que el color **rojo puro** `(255, 0, 0)` representa el número **3** en el tablero. Es una forma directa de identificar qué número aparece en una casilla.

Como se puede ver, esta técnica requiere definir manualmente los valores relevantes, pero te da un **control total** sobre cómo interpretar la imagen.

### 🧾 Conclusión

Aunque **PyAutoGUI** no tolera errores y requiere realizar **pruebas manuales** para identificar los píxeles y extraer los datos útiles, ofrece un rendimiento **mucho más rápido** que otras soluciones como Selenium.

Es una herramienta muy eficaz cuando se prioriza la **velocidad de ejecución** y el **control total** sobre el entorno, a cambio de una menor tolerancia a cambios visuales y más trabajo inicial de configuración.

---

## 🧪 Detección de píxeles y extracción de datos

En el apartado `sources` se encuentran los distintos iconos que la página usa para representar cada elemento del tablero. Esto es muy útil para analizar los píxeles y decidir qué información buscar.

![Iconos](Minesweeper/Icons.png)

Una vez recopilados, el siguiente paso es **analizar los elementos y dividirlos al máximo**, con el objetivo de reducir comprobaciones y generalizar el proceso lo más posible.

---

### ✂️ Mi división

#### 🟨 Al principio

Al principio recortaba cada imagen directamente desde la página para comparar los patrones completos. Funcionaba, pero resultaba lento y poco eficiente.
Investigando, descubrí que podía optimizar la búsqueda analizando solo píxeles clave y no imagenes, porque al final una imagen 24x24 son 576 pixeles cada vez.

La primera separación que hice fue distinguir entre:

- El tablero de minas
- El cuadro del smile

### 🔲 Casillas

Con el zoom al **150%**, cada casilla ocupa **24×24 píxeles**.
Uso un píxel de la esquina superior izquierda para saber si la casilla está pulsada o no. Para diferenciarlas me baso en el color blanco y el gris `(192, 192, 192)`.

![Squares](Minesweeper/Squares.png)

#### 🔢 Casilla seleccionada (números)

En las casillas seleccionadas necesito obtener el número que aparece.
Analizando los patrones, encontré una fila muy favorable donde casi todos los números presentan píxeles característicos.
De ahí seleccioné los píxeles del 2 o del 7, ya que son los más restrictivos.

![Numbers](Minesweeper/Numbers.png)

A partir de este punto ya puedo mapear los números utilizando una tabla de colores RGB:

```python
colors = {
    (192, 192, 192): 0,
    (0, 0, 255): 1,
    (0, 128, 0): 2,
    (255, 0, 0): 3,
    (0, 0, 128): 4,
    (128, 0, 0): 5,
    (0, 128, 128): 6,
    (0, 0, 0): 7,
    (128, 128, 128): 8,
}
```

#### 🚩 Casilla sin seleccionar

En las casillas sin seleccionar hay dos casos posibles:
- Vacía
- Con bandera

La diferencia se puede detectar fácilmente eligiendo un píxel del centro donde exista diferencia de color.

![BombFlagged](Minesweeper/Flagged.png)


### 🙂 Smile

El smile tiene 3 posibles estados:

- Jugando (cara contenta)
- Derrota (cara muerta)
- Victoria (cara con gafas)

Para diferenciarlos seleccioné píxeles restrictivos.
Primero verifico si se ha ganado la partida: si no, la zona de píxeles correspondiente es idéntica en los otros dos casos.
Y la siguiente diferencia clave está en la boca de la cara muerta.

![Smiles](Minesweeper/Smiles.png)

### 🖼️ Otras imágenes

Existen más iconos y variaciones de caras, pero no son relevantes. Por ejemplo, si aparecen minas, ya sabemos que la partida está perdida (cara muerta). 
Las demás expresiones intermedias no aportan información esencial, ya que lo importante es diferenciar muerte y victoria. Por eso, en este análisis lo fundamental es identificar los píxeles críticos de las caras que permitan distinguir el estado real de la partida.

### ⚙️ Configuración

En la configuración se definen los parámetros necesarios para que el bot pueda funcionar correctamente, entre ellos:
- Steps entre casillas, muy útiles para trabajar con posiciones relativas en lugar de coordenadas absolutas.
- La posición de todos los píxeles críticos, que permiten identificar estados clave del tablero.
- La cantidad de filas y columnas en función de la dificultad seleccionada (principiante, intermedio o experto).
- Los colores de referencia, usados para diferenciar casillas, números y banderas.

### 💾 Guardado de datos

La información del tablero se almacena en una tabla de representación interna, donde cada símbolo indica un estado:

- X → Mina.
- '-' → Casilla en blanco o desconocida.
- Número (0–8) → Cantidad de minas alrededor de la casilla.
- ? → Desconocido, este símbolo se usa de forma interna cuando se hace clic en una casilla y aún no se han cargado los datos.

```
###########
#11001X100#
#X10011100#
#110000000#
#011100000#
#12X101110#
#--2101X10#
#--1001221#
#--11111X2#
#--11X112X#
###########
```

## Lógica

Lo primero que hago es hacer clic en el centro para empezar la partida. Y que se habrán las casillas, a partir de ahí cargo los datos y analizamos.

### Fase 1

Primera fase, la facil. Primero, busqueda de minas claras, por ejemplo si sale 2 y solo hay dos posibles minas pues las dos son minas seguras y pongo la X en ambas. O tengo un 3, 2 minas seguras y una posibilidad pues eso es una mina segura.

####
#11#
#-1#
####
#####
#---#
#-21#
#121#
#01X#
#####

Y segundo, hacemos clic en los lugares seguros, si hay un 2 tres minas marcadas y 2 espacios disponibles pues hacemos clic en los espacios seguros. 
```⚠️❗A partir de aquí creo que se puede hacer mejor, aunque a mi me funcione, creo que no es lo más optimo.```

### Fase 2

Segunda fase, a esta fase solo pasamos si no se realiza ningun cambio en la primera. Esta fase la llamo bloques.


  ![Blocks](Minesweeper/Blocks.png)


### Fase 3 - Muerte aleatoria (Imperfecta)
