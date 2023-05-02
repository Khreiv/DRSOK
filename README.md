# DRSOK

Digital Radio Station Player

[![Python](https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)

![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)

![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)


### Do you want to download a compiled version (exe)?

[![HERE](https://img.shields.io/badge/HERE-00AFAA.svg?style=for-the-badge&logo=HERE&logoColor=white)](https://github.com/Khreiv/DRSOK/releases/tag/EXE)
_______________________________________________________________________________________________________________________________________________________________________


# <img src="https://hatscripts.github.io/circle-flags/flags/es.svg" width="25"> ¡IMPORTANTE! 

Este software ha sido construido usando Python 3.10. La razón es que la librería principal es Pygame, la cual no esta aún actualizada a la última versión de python.

Además, el motor de audio que usa es VLC, una potente librería de código abierto. ES IMPORTANTE TENER INSTALADO EL REPRODUCTOR VLC para que el programa funcione correctamente ya que depende de sus librerías.

Si aún no lo tienes descargado puedes obtenerlo en el diguiente enlace::

[![VLC](https://img.shields.io/badge/VLC%20media%20player-FF8800.svg?style=for-the-badge&logo=VLC-media-player&logoColor=white)](https://www.videolan.org/vlc/index.es.html)


## ¿CÓMO FUNCIONA?

Una interfaz simple e intuitiva hace que sea facil de usar, separando el programa en tres áreas. El programa ofrece acceso a mas de 37000 estaciones de radio de todo el mundo vía internet.


### REPRODUCTOR

Prev / Play / Stop / Next -> Controles con los que estamos familiarizados, aunque con una variante. Los botones de siguiente y anterior solo iteran sobre la lista de favoritos cuando se está reproduciendo uno de sus elementos, de esta forma no es necesario volver a la pestaña de favoritos para seleccionar uno.

Fav / Buscar / Guardar Fav -> Controles simples, con los dos primeros alternaremos la vista del reproductor, pasando al modo busqueda o a los favoritos guardados. El ercer boton almacena la emisora que esta sonando actualmente en un archivo .json para ser cargado en favoritos.


### FAVORITOS

No hay mucho que contar aquí, se pueden almacenar infinitas emisoras a razón de 9 por página. Cada una de ellas aparecerá con su nomnbre y simplemente clickando en este se reproduciran. Junto con el nombre aparece un icono que se encargará de borrar esta emisora de los favoritos si así lo queremos.


### BÚSQUEDA

Este es el apartado más amplio ya que prácticamente es el encanto de este reproductor. Nada más entrar se pueden observar tres botones principales: BY_NAME, BY_TAG, BY_COUNTRY

Los dos primeros son muy parecidos, salvo que uno buscara en base a los nombres de las emisoras y otro buscara en base a las etiquetas de las emisoras, pero el funcionameinto será practicamente igual.

El tercer campo no requiere de ningun termino de búsqueda ya que al pulsarse nos ofrecera una lista completa de todos los países, una vez encontramos el país que queremos solo tenemos que clicar en el para que aparezcan por orden alfabético todas las emisoras disponibles en ese país. Una vez mas solo hay que clicar en una de ellas y se reproducira automáticamente.


## CÓDIGO

El código está dividido en 5 módulos. 

El primero, CONFIG.py almacena las variables comunes que serán usadas el todos los módulos. Es una práctica que me gusta ya que a la hora de hacer pruebas es bastante efectiva para retocar campos concretos en lugar de tener que buscar a lo largo de cientos de lineas de código. En este módulo hay una variable llamada DEBUG (un valor booleano) que se encarga de hacer que el programa dibuje los rects (cuadros de colisión) de los botones. Muy util para manejar si hay interferencias entre unas partes del reproductor y otras.

El segundo, api.py contiene funciones de llamada a la API cuyo enlace dejaré abajo. La API original provee sus propias funciones, pero para hacerlo mas personalizado y simple construí las mías propias, así consigo que tanto los argumentos como las funciones en sí queden lo más compactos posibles, además, resulta mas facil de entender.

El tercero, interface.py se encarga de la construcción de la interfaz. Carga imagenes en tres clases que manejaran el dibujado de los tres apartados del programa y los encapsula en diccionarios que posteriormente seran faciles de iterar para tratarlos como botones.

El cuarto, backend.py es el módulo más extenso, se encarga de implementar las clases del modulo interface, de capturar los eventos de teclado y mouse y los flujos de procesos. Múltiples variables de control alojadas en CONFIG.py facilitan el trabajo y a travez de listas, los eventos se capturan bastante bien, auqnue creoq ue podría mejorarla con el tiempo.

Y el quinto, main.py. Es simple, se llama al backend, que se dibuja y actualiza y se añade un retardo mínimo que hace que el programa ralentice sus ciclos, haciendolo más eficiente.



## Este proyecto esta apoyado en una API de un tercero contruida para un sitio web

Aquí tienes el link del sito web el proyecto https://gitlab.com/radiobrowser/radiobrowser-web-angular

Aquí puedes acceder a la API con implementación en multiples lenguages de programación https://api.radio-browser.info


_______________________________________________________________________________________________________________________________________________________________________



# <img src="https://hatscripts.github.io/circle-flags/flags/gb.svg" width="25"> IMPORTANT! 

This software was built using python 3.10. The reason is that the main library is PYGAME, which is not yet updated to the latest version of python.

Also, the audio engine it uses is VLC, a powerful open source library. IT IS IMPORTANT TO HAVE VLC PLAYER INSTALLED for the player to work correctly, since it depends on those libraries.

Here you can download the VLC media player if you don't have it yet:

[![VLC](https://img.shields.io/badge/VLC%20media%20player-FF8800.svg?style=for-the-badge&logo=VLC-media-player&logoColor=white)](https://www.videolan.org/vlc/index.es.html)


## HOW DOES IT WORK?

A simple and intuitive interface makes it easy to use, splitting the program into three areas. The program provides acces to more than 37000 radio stations from around the world


### PLAYER

Prev / Play / Stop / Next -> Controls we are familiar with. The next and previous buttons only iterate over the favorites list when one of its items is playing, so there's no need to go back to the favorites tab to select one.

Fav / Search / Save Fav -> Simple controls, with the first two we will alternate the view of the player, going to search mode or saved favorites. The third button stores the currently playing station in a .json file to be loaded into favorites.


### FAVOURITES

There is not much to tell here, infinite stations can be stored at a rate of 9 per page. Each one of them will appear with its name and simply by clicking on it they will be reproduced. Along with the name there is an icon that will take care of deleting this station from the favorites if we want it.


### SEARCH

This is the broadest section since it is practically the charm of this player. As soon as you enter you can see three main buttons: BY_NAME, BY_TAG, BY_COUNTRY

The first two are very similar, except that one will search based on the names of the stations and the other will search based on the labels of the stations, but the operation will be practically the same.

The third field does not require any search term since when pressed it will offer us a complete list of all the countries, once we find the country we want, we only have to click on it so that all the stations available in that country appear in alphabetical order . Once again you just have to click on one of them and it will play automatically.


## CODE

The code is divided into 5 modules.

The first, CONFIG.py stores common variables that will be used by all modules. It is a practice that I like since when testing it is quite effective to tweak specific fields instead of having to search through hundreds of lines of code. In this module there is a variable called DEBUG (a boolean value) that is responsible for making the program draw the rects (collision boxes) of the buttons. Very useful to manage if there is interference between some parts of the player and others.

The second one, api.py contains API call functions which I will link below. The original API provides its own functions, but to make it more custom and simple I built my own, so I keep both the arguments and the functions themselves as compact as possible, plus it's easier to understand.

The third, interface.py is responsible for building the interface. It loads images into three classes that will handle the drawing of the three sections of the program and encapsulates them in dictionaries that will later be easy to iterate over to treat them as buttons.

The fourth, backend.py is the most extensive module, it is responsible for implementing the interface module classes, for capturing keyboard and mouse events and process flows. Multiple control variables housed in CONFIG.py make it easy to work and through lists, events are captured quite well, although I think it could be improved over time.

And the fifth, main.py. It's simple, the backend is called, which is drawn and updated, and a minimal delay is added that makes the program slow down its cycles, making it more efficient.



## This project is supported by an third-party service API built for a wesite

Here you can check the link of the website project https://gitlab.com/radiobrowser/radiobrowser-web-angular

Here you can acces the API in multiple programing languages https://api.radio-browser.info


_______________________________________________________________________________________________________________________________________________________________________


## UNDER MIT LICENSE

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
