**#### This is the Final Project of Introduction to Visual Media Programming(MAS2011-01). ####**
- Written by 20191104 Juhee Seong 
- On 12.12, 2023

**Link of the recorded demo video:** https://www.youtube.com/watch?v=l1yPjGhFIUA

**How to Play**
1. Click the falling rings to get score.
2. Click the coin to get gold. You can spend gold to upgrade your stats.
   You can check the upgrading buttons on the bottom panel of the screen.
3. Click the heal orb to heal HP. 
   When HP reaches 0, it is game over, so keep check on your HP.
4. Do NOT click trap. It decreases your HP.
5. Click Freezer orb to slow down all fallings for several seconds.
   Duration time depends on your upgrade level.
6. Click Flame orb to activate flame for several seconds.
   Flame can auto click rings. (Notice it does not auto click orbs or traps.)
   Duration time depends on your upgrade level.
7. Click Lightning orb to activate lightning for very short seconds.
   Lightning clicks several rings at once, even when you click empty space.
   Number of clicked rings depends on your upgrade level.


**Description of the Content**
1. /resources: All image, sound file.
2. main.py: main() function
3. UserStat.py: Contains all classes and functions related to user states and upgradeable stat.
4. FallingObjects.py: Contains all classes and functions to manage falling objects.
5. GameState.py: Logics for game play.
6. Drawing.py: Used for drawing.
7. USerInput.py: Used for processing user inputs.


**Below are links where i got the assets for this project.**
1. background image: https://opengameart.org/content/ruined-city-background
2. All other files in /resources are made by myself, so please don't copy. 
   Instead, ask me when you want to use them.