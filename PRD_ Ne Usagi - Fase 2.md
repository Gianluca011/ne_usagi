> **PRD:** **Ne** **Usagi** **-** **Fase** **2**
>
> **1.** **Visión** **del** **Producto**

Evolucionar el prototipo actual del Tamagotchi "Ne Usagi" hacia una
experiencia virtual más inmersiva, aplicando buenas prácticas de
programación en Python y preparando el terreno para una futura
escalabilidad a otras plataformas. El objetivo es aumentar la retención
del jugador mediante sistemas de progresión, personalización y una base
de código modular.

> **2.** **Estado** **Actual** **del** **Sistema**
>
> ● **Mecánicas** **Base**: El juego gestiona tres estadísticas (hambre,
> energía y felicidad) que decaen con el paso del tiempo.
>
> ● **Persistencia**: El estado de la mascota se guarda localmente
> mediante la lectura y escritura de un archivo JSON.
>
> ● **Entorno**: El ciclo visual de día y noche cambia de forma dinámica
> evaluando la hora del sistema operativo.
>
> ● **Interactividad**: Existe un minijuego de atrapar zanahorias
> integrado para aumentar la felicidad del conejo.
>
> ● **Configuración**: Las dimensiones de pantalla, rutas de archivos y
> atajos de teclado están centralizados.
>
> **3.** **Requisitos** **Funcionales** **(Nuevas** **Características)**
>
> **3.1.** **Sistema** **de** **Economía** **y** **Tienda**
>
> ● **Moneda** **Virtual**: El minijuego de atrapar zanahorias
> actualmente solo suma puntos de felicidad. Se implementará una moneda
> ("Zanahorias Doradas") que se obtenga al jugar.
>
> ● **Cosméticos** **y** **Temáticas**: Crear una tienda donde se puedan
> comprar accesorios para el conejo. Se pueden incluir cosméticos
> inspirados en la estética *yankii* japonesa o elementos históricos
> asiáticos para darle una identidad visual única al juego.
>
> **3.2.** **Mejoras** **de** **UI/UX** **y** **Feedback**
>
> ● **Efectos** **de** **Sonido** **(SFX)** **y** **Música**: Incorporar
> una pista lo-fi de fondo y efectos sonoros al presionar la barra
> espaciadora para alimentar (KEY_FEED) o al atrapar una zanahoria en el
> minijuego.
>
> ● **Notificaciones** **de** **Estado**: Añadir pequeños globos de
> diálogo o iconos flotantes (además de las barras de progreso) cuando
> una estadística esté en nivel crítico (rojo).
>
> **4.** **Requisitos** **Técnicos** **y** **Refactorización**
> **(Deuda** **Técnica)**
>
> **4.1.** **Programación** **Orientada** **a** **Objetos** **(POO)**
>
> ● **Clase** **Pet**: Actualmente, el estado del conejo se maneja en un
> diccionario pet = load_data(). Se debe crear una clase Tamagotchi que
> encapsule sus métodos (ej. alimentar(), dormir(),
> actualizar_estado()).
>
> ● **Separación** **de** **Responsabilidades** **(MVC)**:
>
> ○ Mover la lógica del minijuego, que actualmente reside dentro de
> pet.py, a un archivo dedicado minigames.py.
>
> ○ Extraer las funciones de dibujado de interfaz (como draw_bar) de
> pet.py hacia un módulo ui.py.
>
> **4.2.** **Optimización** **del** **Bucle** **Principal**
>
> ● En game.py, la evaluación del fondo (día/noche) se realiza en cada
> fotograma (hour = time.localtime().tm_hour). Esto puede optimizarse
> evaluando la hora solo una vez por minuto o cuando haya un cambio de
> estado significativo.
