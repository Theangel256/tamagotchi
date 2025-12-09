<p align="center">
    <img src="icons/tamagotchi.ico" height="128">
    <h1 align="center">Tamagotchi</h1>
</p>

## Overview
Este proyecto para la clase de Programación 1, implementa una interfaz gráfica de usuario (GUI) del clásico juego Tamagotchi. Los usuarios pueden interactuar con su mascota virtual alimentándola, dándole agua, jugando y monitoreando su salud y felicidad.

## Screenshots
<img width="200" height="370" alt="Screenshot_1" src="https://github.com/user-attachments/assets/19567c88-2f86-4fd6-bf52-5a0e56881036" /> 
<img width="200" height="370" alt="Screenshot_2" src="https://github.com/user-attachments/assets/fbc340fd-c41f-4092-9533-c712b55b9929" /> 
<img width="200" height="370" alt="Screenshot_3" src="https://github.com/user-attachments/assets/8e78d5f7-268b-4276-9bfd-1aa9a1fd3a6f" /> 
<img width="200" height="370" alt="Screenshot_4" src="https://github.com/user-attachments/assets/cb129c60-b0cc-4bdb-a9c2-1501f227dbe6" />
<img width="200" height="370" alt="Screenshot_5" src="https://github.com/user-attachments/assets/0389d08f-4559-4ac0-81b5-c2361f71a84a" /> 

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
python -m src.main
```

## Features
- **GUI Interactiva**: Agregamos la comodidad para la mejor experiencia de usuario al momento de movilizarse y jugar.
- **Manejo Interactivo**: Varias formas de como cuidar a tu mascota y probabilidades diferentes de cada Tamagotchi.
- **Real-time Updates**: La Interfaz de usuario usa estadisticas en tiempo real basado en sus interacciones.