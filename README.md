# Fall Guys Anti Sniper
![AitorekBobo](https://raw.githubusercontent.com/4l3j0Ok/fall-guys-anti-sniper/main/src/static/icon.png)
### NOTA: Parece que a Mediatonic le dio por ocultar los nombres de los jugadores de los logs del juego (que es de donde la aplicación obtenía los nombres de los jugadores), por lo tanto, al menos hasta que los vuelvan a poner, la aplicación no podrá mostrar los nombres de los jugadores, y, por lo tanto, la lógica que detecta posibles snipers, queda totalmente obsoleta. La lógica de detectar snipers, sigue funcionando, pero puede fallar si hay nombres parecidos. Denle las gracias a MT.
## [Video explicativo](https://www.youtube.com/watch?v=QgWsRF-0FxI)

## Introducción 🌈

Fall Guys Anti Sniper es un proyecto que nace a partir de la problemática del stream sniping, más concretamente, en el juego Fall Guys.

El objetivo de la aplicación es informar al usuario de los snipers (y posibles snipers) que se encuentren la partida actual, basándose en los logs del juego y en la **"blacklist" personal** que el usuario podrá armar a su gusto y objeto.

El usuario podrá agregar a la blacklist los snipers que él desee, **tanto manualmente como los sugeridos por la propia aplicación**.

Nota 1: *La aplicación nunca agregará jugadores a la blacklist personal del usuario salvo que éste indique lo contrario.*

En el caso de que el usuario y un jugador que forme parte de la blacklist coincidan en la partida en curso, se le advertirá al usuario con una notificación de que posiblemente esté siendo snipeado. A su vez el sniper aparecerá en la **"lista de snipers"**.

Así mismo, el jugador podrá ver la **lista completa de jugadores** en la partida en curso, en el caso de que éste quiera agregar uno de los jugadores y no aparezca en la lista de **"posibles snipers"**.

La lista de "Posibles Snipers" se basa en las últimas 5 partidas del juego, si algún jugador en la partida actual coincide con alguna de las últimas 5 partidas jugadas, éste aparecerá en la lista a modo de sugerencia para agregarlo a la blacklist.

Nota 2: *La blacklist y otros datos utiles para la aplicación se guardan en data.json, son utiles para el funcionamiento de la aplicación. Recomiendo no eliminarlo, aunque, si lo hace, se volverá a crear cuando vuelva a abrir la aplicación. De todas formas este archivo, ni siquiera la aplicación entera maneja datos sensibles. Si tiene dudas, puede chequear el código, no es muy dificil de leer.*

Nota 3: *Se creará también un archivo llamado "application.log", la cual contiene los logs de la aplicación. Si surge un error durante la ejecución, pongase en [contacto](mailto:alejofsarmiento@gmail.com) y/o abra un [issue](https://github.com/4l3j0Ok/fall-guys-anti-sniper/issues) adjuntando este archivo.*

Se acepta toda crítica constructiva y sugerencias, ¡los pull requests están abiertos!

## Opiniones 📈
Aquí les dejo con un par de opiniones de los mas grandes streamers de Fall Guys!
### [Keroro](https://clips.twitch.tv/DreamyOptimisticCormorantYouWHY-6Ni_uHpYBUTYBtzm)
### [Aitorek](https://clips.twitch.tv/UnusualPlayfulOysterVoteNay-Qti2v5hSAqPcJ2wn)
### [Aitorek otra vez](https://clips.twitch.tv/AgileOutstandingAyeayeShazBotstix-JQ0H_uTQAdiVLWJb)

## Pre-requisitos 📋

- Fall Guys

## Descargas 🗃️

Para descargar la aplicación ejecute los siguientes pasos:
- Ve al apartado de "Releases", aquí a la derecha, o presiona [AQUÍ](https://github.com/4l3j0Ok/fall-guys-anti-sniper/releases).
- Descargue y descomprima el archivo .zip en donde usted desee.
- En la carpeta Fall Guys Anti Sniper encontrará el ejecutable "FGAntiSniper.exe", abralo y disfrute la app!
- Nota: *Se recomienda crear un acceso directo de FGAntiSniper.exe en donde sea cómodo y accesible para evitar modificar archivos de la carpeta que son necesarios para el funcionamiento de la aplicación.*
## Desarrollado con 🛠️

- Python 🐍
- Qt 🎨
- Redragon Aryaman ⌨️

## Licencia 📄

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE.md](LICENSE.md) para más detalles.

## Menciones especiales 🎁

La inspiración para desarrollar este proyecto nació desde el stream del bobo de [Aitorek](https://twitch.tv/aitorek), así que gracias a él y a todo su chat 💞.

## Donaciones 💞
Acepto donaciones por paypal! presiona [AQUÍ](https://paypal.me/4l3j0Ok?country.x=AR&locale.x=es_XC) para donarme!

---
⌨️ con ❤️ [Alejoide](https://github.com/4l3j0Ok/) 😎👌

