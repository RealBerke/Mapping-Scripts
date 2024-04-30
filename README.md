# Compile Pal Plugins
**Note:** These require **Python** to be installed along with **bsp_tool** and **valvevmf** modules.
## Classname Override
Adds a second classname to the entity after compiling, mostly intended to make **point_template** a preserved entity to allow it to spawn other preserved entities in **Counter-Strike: Source**.

FGD keyvalue:

```classnameoverride(string) : "Override Classname" : : "The classname that will override when this entity spawns."```
## Order Entities
Sorts entities in the **VMF** file, useful for making sure **info_observer_point**s and **info_player_teamspawn**s are ordered correctly in **Team Fortress 2**.

FGD keyvalue:

```entityorder(string) : "Entity Order" :  : "Value that will be used to sort the entity."```
## Strip Lights
Removes the **light** entities from the map's entity list with no name and singles them out if they have the same name.
