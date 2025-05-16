# Log

Time format: dd/mm/yyyy



## 03/05/2025

I started my project, did plants, planting, and basic rendering. The foundation was being laid.



## 04/05/2025

Here I am, coding zombies, shovel, and other shenanigans.

I wonder for how long I'll be able to uphold this project without getting bored.

Hopefully I'll finally make a functioning game... I'll see

PLAN OF ACTION:
* Make ui.py module
* Move shovel to the bottom right like in pvz2
* Turn grid list into a 3D tensor
* Multiple terrain types; for now, just water and land
* Multiple types of plants per tile, e.g. Lily Pad + Pumpkin + Peashooter
* Pausing and speed-up working + ui buttons
* "Ready, Set, Plant!" countdown before level begins
* Flags (major waves)



## 05/05/2025

hi

REVISED PLANT OF ACTION:
- ui.py made, add more button classes so I can add them here - added shovel! - FULLY DONE!
- shovel to be repositioned - DONE!
- grid to be tensor-ified - DONE!
- terrain to be added
- multi-plant to be added - DONE!
- NO MORE SPEEDING UP OR PAUSING UNTIL I CAN FIGURE IT OUT MYSELF
- - I am considering using the 'time' module, but it'll time a significant amount of time (ha!) to restructure my tickers to time-based stuff
- countdown to be implemented - this one will require pausing or some sort of "layered loading" to the level... but that would be less than ideal.
- - I'll probably implement the countdown when I'll have my hands on pausing and speeding up, so that I can pause everything else while the countdown does its thing
- flags to be done - I could do this right after terrain I think



## 08/05/2025

my keyboard's not living the best life right now
I got the perfect damage reduction (DR) case handling for zombies with helmets cuz they resist cherry bombs and me no like dat



## 09/05/2025

replacin' tensors with something more epic, I'll tell ye later what it is ;)

finish the ui.py, it's nearly done



## 10/05/2025

hi I'm back :)
- entities.py could use ECS system (do later, this is a long-term goal rather than immediate emergency)
- finish LawnTile class in ui.py
- do lawn creation system in systems.py
- maybe it's time to `time`? tickers are not very precise (1 tick is 16.67 ms) and very FPS-dependant so uhh yeah

finally, it's about 17:33 and I've finally transitioned from tensors to buttons regarding lawn

and also some other neat features along the way, like MULTIPLE TERRAIN SUPPORT!!!!!111!!!!1111 LETS GO BABYYYYYYYY

z-layers would also be nice, since python uses a very fast Timsort for repetitive or near-completed data, which is basically what I'm going to have for z ordering

asset manager finished: it loads, caches, and forgets

started working on the Terra-Fern

NOT happy with the current plant sprites, will very likely (DEFINITELY, actually) re-do, but later (after I am certain that everything works)

auto-resizer-on-load not done yet

sprites aren't actually loaded or used right now, but the logic is done

tmrw I'll finish the Terra-Fern plant and FINALLY make the game not look like squares and circles

ALSO! I need to make seed_packet_image_generator because:
1) I am too lazy to manually do EVERY image for EVERY seed packet. what if I want to change the background? I'll have to redraw the entire image!
2) I can use custom font that dynamically updates with my shit balancing!
3) come on, automation is super fun... (I am a Factorio, Satisfactory, and Mindustry addict #1; have tried Shapez but never bought, whoopsies!)



## 11/05/2025
doing the Terra-Fern right now

JUST CAME UP WITH AN IDEA:

Rotobaga and Starfruit, instead of using raycasts to check if a zombie threat exists in range

could simply check if a slope between two points is correct for the projectile trajectory

since they fire in straight lines

I could also technically use this for the Peashooter, but a simple x-coord equality check never hurts, right?

also, if (x2 - x1) in m = (y2 - y1) / (x2 - x1) is equal to 0, we're dividing by zero

so use a try/except and return float('inf') instead (ezpz)

HELL YEAH, MATH!!!!

--- updates

Terra-Fern as a Lily Pad is done; in the future, I'll add Flower Pot, Hot Potato, and Grave Buster behavior to it (so you don't carry 1236123 tool plants)

also zlayers will have to wait, the system I'm currently using needs refactoring in best case scenario and complete rewriting in worst

12:43 - did Starfruit, and used angles instead of slopes using atan2. turns out I already had coords between two points to angle converter sooooooo

12:45 - imma start doing sprites and autoscaling



## 12/05/2025

Just ported everything I wanted to GitHub and finished porting logs.

Hopefully someone notices this project... Eventually.

Also I have awards night the day after tmrw (14/05/2025) and apparently I got something. Well sh*t.

Really don't wanna go anywhere tmrw tomorrow or go to grad... :(((



## 16/05/2025

Polished GitHub repo, added all the essentials, and made it look nice n' stuff.

Good news: I just realized that pygame surfaces/displays support additive blending, so I'll look into that when implementing the zlayers

Hopefully I'll refacture it by the end of this day, see you in a bit I guess...
