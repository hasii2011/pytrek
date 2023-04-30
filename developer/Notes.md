# Developer Notes


## Manual Test Programs

I developed the following test programs in order to be able to run UI sub components manually outside of the game itself.

If your run these inside of PyCharm run them as modules and set the current directory to the project base.

* **TestEventScheduler** - Allows you to run the event scheduler.  Manually increment the time 1-9 star dates and 
observe game events happen
  * Keys
    * Q -Quit
    * A -reset up the test program
    * U - Update the game clock by one unit
    * 1-9 update the game clock by the pressed number
* **TestHelpView** - Run the help view to verify correctness and the help text
* **TestShooting** - Test the sprites associated with shooting;  There is a pallet of enemies to choose from.  Choose one by clicking on 
it.  Then click on quadrant;  A test Enterprise is conveniently situated in the test quadrant.  After testing shooting for a specific
enemy reset up by pressing A
  * Keys
    * A - Reset up the test program
    * K - Fire Klingon Torpedo
    * C - Fire Commander Torpedo
    * S - Fire Super Commander Torpedo
    * P - Fire Phasers
    * Q - Quit 
* **TestExplosions** - Displays all the animations associated with the game explosions
  * Keys
    * A - Re-run the animations
    * Q - Quit
* **TestWarpEffect** - I bet you can guess what this does
* **TestWarpDialog** - Ensures that the quadrant and warp speed validations work;  Prints good results to the debug console
* 