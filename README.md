# Detect-Object

# V3

This version uses [Simplify](https://github.com/EgeEken/Simplify) and then [Fill Object V1](https://github.com/EgeEken/Fill-Object) to fill the resulting sketch, and then keeps the original color pixels on the selected "object" pixels while replacing the rest with an either manually given or automatically selected background color.

The user will be asked to input two parameters for each created image, one for the contrast threshold for the simplifcation process, which will be determining how much detail is picked up, (Too little and the object won't be detected, too much and the background will be detected as well, i find that 100 is a good starting point for most images) and another for the direction count for Fill Object, which will be determining the amount of directions that will be checked from each pixel (further explanation is in the readme document for Fill Object that i linked above, explaining the shortcomings of lower and higher direction counts, i would recommend using 8 on all images unless theres specific areas requiring more)

Warning: The program is relatively slow, expect roughly 5 minutes of computing time for a 1000x1000 image, exponentially more or less depending on the resolution (a 3000x3000 image takes over an hour to compute on my laptop and a 300x300 image takes less than 5 seconds)

# Results:

## Automatically chosen background color:
### Threshold: 100, Direction Count: 8
![Result Automatic Background](https://user-images.githubusercontent.com/96302110/181904088-78246a0f-54ee-4b03-a041-adb8b81c59b8.png)

## Custom background colors:
### Threshold: 30, Direction Count: 8
![Result Chosen Background](https://user-images.githubusercontent.com/96302110/181904100-2972b22c-0df0-43bd-9198-45fb54c79ff2.png)

### Threshold: 200, Direction Count: 8
![Result Chosen Background 2](https://user-images.githubusercontent.com/96302110/181904478-741f9e7c-7e6c-45d0-a372-c955226128cb.png)
