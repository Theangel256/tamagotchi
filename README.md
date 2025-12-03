# Tamagotchi GUI Project

## Overview
Este proyecto para la clase de Programación 1, implementa una interfaz gráfica de usuario (GUI) del clásico juego Tamagotchi. Los usuarios pueden interactuar con su mascota virtual alimentándola, dándole agua, jugando y monitoreando su salud y felicidad.

## Project Structure
```
tamagotchi
├── src
│   ├── main.py          # El núcleo de el juego
│   ├── tamagotchi.py    # Contiene la logica atrás de el videojuego Tamagotchi
│   ├── gui
│   │   ├── app.py       # Interfáz Gráfica base para la app
│   │   └── components.py # Componentes de la gui para su propia interacción
├── requirements.txt      # Lista de dependencias
└── README.md             # Documentación de el Proyecto
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd tamagotchi
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application
Para iniciar el juego, ejecuta en tu terminal:
```
python src/main.py
```

## Features
- **GUI Interactiva**: Agregamos la comodidad para la mejor experiencia de usuario al momento de movilizarse y jugar.
- **Manejo Interactivo**: Varias formas de como cuidar a tu mascota y probabilidades diferentes de cada Tamagotchi.
- **Real-time Updates**: La Interfaz de usuario usa estadisticas en tiempo real basado en sus interacciones.