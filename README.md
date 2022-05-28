# Fall Guys Anti Sniper
![AitorekBobo](https://raw.githubusercontent.com/4l3j0Ok/fall-guys-anti-sniper/main/src/static/icon.png)
## Introducción 🌈

Fall Guys Anti Sniper es un proyecto que nace a partir de la problemática del stream sniping, más concretamente, en el juego Fall Guys.

El objetivo de la aplicación es informar al usuario de los snipers (y posibles snipers) que se encuentren la partida actual, basándose en los logs del juego y en la **"blacklist" personal** que el usuario podrá armar a su gusto y objeto.

El usuario podrá agregar a la blacklist los snipers que él desee, **tanto manualmente como los sugeridos por la propia aplicación**.

Nota 1: *La aplicación nunca agregará jugadores a la blacklist personal del usuario salvo que éste indique lo contrario.*

En el caso de que el usuario y un jugador que forme parte de la blacklist coincidan en la partida en curso, se le advertirá al usuario con una notificación de Windows de que posiblemente esté siendo snipeado. A su vez el sniper aparecerá en la **"lista de snipers"**.

Así mismo, el jugador podrá ver la **lista completa de jugadores** en la partida en curso, en el caso de que éste quiera agregar uno de los jugadores y no aparezca en la lista de **"posibles snipers"**.

La lista de "Posibles Snipers" se basa en las últimas 5 partidas del juego, si algún jugador en la partida actual coincide con alguna de las últimas 5 partidas jugadas, éste aparecerá en la lista a modo de sugerencia para agregarlo a la blacklist.

Nota 2: *La blacklist y otros datos utiles para la aplicación se guardan en data.json, son utiles para el funcionamiento de la aplicación. Recomiendo no eliminarlo, aunque, si lo hace, se volverá a crear cuando vuelva a abrir la aplicación. De todas formas este archivo, ni siquiera la aplicación entera maneja datos sensibles. Si tiene dudas, puede chequear el código, no es muy dificil de leer.*

Nota 3: *Se creará también un archivo llamado "application.log", la cual contiene los logs de la aplicación. Si surge un error durante la ejecución, pongase en [contacto](mailto:afsarmiento@gmail.com) y/o abra un [issue](https://github.com/4l3j0Ok/fall-guys-anti-sniper/issues) adjuntando este archivo.*

Se acepta toda crítica constructiva y sugerencias, ¡los pull requests están abiertos!

## Pre-requisitos 📋

- Fall Guys

## Descargas 🗃️

Para descargar la aplicación simplemente ve al apartado de "Releases", aquí a la derecha, o presiona [AQUÍ](https://github.com/4l3j0Ok/fall-guys-anti-sniper/releases).
Ejecute el instalador, y siga los pasos y abra la aplicación. Igual que cualquier otro instalador!

## Desarrollado con 🛠️

- Python 🐍
- Qt 🎨
- Redragon Aryaman ⌨️

## Licencia 📄

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE.md](LICENSE.md) para más detalles.

## Menciones especiales 🎁

La inspiración para desarrollar este proyecto nació desde el stream del bobo de [Aitorek](https://twitch.tv/aitorek), así que gracias a él y a todo su chat 💞.

---
⌨️ con ❤️ [Alejoide](https://github.com/4l3j0Ok/) 😎👌

