# Compile Pal Plugins
**Note:** These require **Python**.
## Classname Override
Adds a second classname to the entity after compiling,
Useful for making **point_template** a preserved entity to allow it to spawn other preserved entities in **Counter-Strike: Source**.

**Note:**
Requires the **bsp_tool** module.

FGD keyvalue:

```classnameoverride(string) : "Override Classname" : : "The classname that will override when this entity spawns."```
## Order Entities
Sorts entities in the **VMF** file.
Useful for making sure **info_observer_point**s and **info_player_teamspawn**s are ordered correctly in **Team Fortress 2**.

**Note:**
Requires the **valvevmf** module.

FGD keyvalue:

```entityorder(string) : "Entity Order" :  : "Value that will be used to sort the entity."```
## Strip Lights
Removes the **light** entities from the map's entity list with no name and singles them out if they have the same name.
Useful for reducing the edict count at the start of the round.

**Note:**
Requires the **bsp_tool** module.
## Set Model Support
Allows "SetModel" input to function by replacing it via "modelindex" method.
Useful for easily setting the model of players in **Counter-Strike: Source**.

**Note:** 
Requires the **bsp_tool**, **vpk** and **vdf** module.
Specify the location of "propdata.txt" file. Can be a "VPK" file.
While the "propdata.txt" file is created and packed, custom model files are not packed.
