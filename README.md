# pygame_multiplayer
Testing multiplayer functionality using pygame
How to run:
1- Check if you can run mspaint
2- Check if you have pygame installed pip install pygame 
3- just run lol nothing else required.

How to add your own shashke/stuff
1-Everything is organised into classes
2- you want to add a bullet?
  2.1 - create a class bullet1 inherit the bullet. Give your bullet movement override the move function and you are good to go.
3- You want to add a gun?
  3.1 - Create a class (e.g DoubleBarrel). Inherit the gunclass. Define your shooting by overriding the gun.shoot() method as you wish.
4- I believe 99% of the stuff here can be done if you follow english.
e.g. a person ( Class) has a doubleBarrel(gun) which shoots(doubleBarrel.shoot()) 2 9mmBullets(bullet())
