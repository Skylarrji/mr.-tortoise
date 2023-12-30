# Purpose
This battlesnake was designed to compete in the autonomous survival game: https://play.battlesnake.com/

# Algorithm
The main algorithm of the battlesnake is implemented in the `move()` function in `main.py`. After eliminating all of the obvious unsafe moves (i.e. moves that will result in collisions to walls, other snakes and itself), it then eliminates secondary unsafe moves (i.e. any moves that could potentially cause the snake to lose in a head-to-head collision with another snake or getting trapped) by looking a few moves in advance. 

Then, out of the possible remaining moves, it pathfinds and returns a move that allows it to either search for food or chase its tail depending on conditions involving the snake's health and length.

# Technologies Used
Python 3 was used in developing this project.

# Link to Design Document Video 🔗
https://www.canva.com/design/DAFG44FR6zs/pBWxtP3eViR93ZUymiTlAw/view?utm_content=DAFG44FR6zs&utm_campaign=share_your_design&utm_medium=link&utm_source=shareyourdesignpanel

# Image of Design Document 🖼️
![image](https://user-images.githubusercontent.com/72311728/209414073-36057f43-117e-4e13-8e02-1638bf6115e0.png)
