# Developer Notes


## Manual Test Programs

I developed the following test programs in order to be able to manually run UI subcomponents outside the game itself.

If you run these inside of PyCharm run them as modules and set the current directory to the project base.

* **AppTestEventScheduler** - Allows you to run the event scheduler.  Manually increment the time 1-9 star dates and 
  observe game events happen
  * Keys
    * Q -Quit
    * A -reset up the test program
    * U - Update the game clock by one unit
    * 1-9 update the game clock by the pressed number
* **AppTestHelpView** - Run the help view to verify correctness and the help text
* **AppTestShooting** - Test the sprites associated with shooting;  There is a pallet of enemies to choose from.  Choose one by clicking on it.  Then click on the quadrant.  A test Enterprise is conveniently situated in the test quadrant.  After testing shooting for a specific enemy reset up by pressing A
  * Keys
    * A - Reset up the test program
    * K - Fire Klingon Torpedo
    * C - Fire Commander Torpedo
    * S - Fire Super Commander Torpedo
    * P - Fire Phasers
    * Q - Quit 
* **AppTestExplosions** - Displays all the animations associated with the game explosions
  * Keys
    * A - Re-run the animations
    * Q - Quit
* **AppTestWarpEffect** - I bet you can guess what this does
* **AppTestWarpDialog** - Ensures that the quadrant and warp speed validations work;  Prints good results to the debug console