# Spider Game
## Rules
- One player plays as spider, another one as flies.
- Spider wants to eat flies. Spider wins if it eats most of the flies.
- Flies want to reach final place where they can be safe. Spider cannot enter final place. Flies win if most of them reach final place.
- Number of places figure can move is randomly generated from range 1..6 (like a standard throw a dice).
- During game follow instructions in the top right corner.
## Installation
Clone the repo
```
git clone https://github.com/Wojciech34/Spider-game.git
```
Install dependencies
```
pip install -r requirements.txt
```
Run game
```
py main.py
```
## Random map generation
There is an availability to generate random map. Inside source file `map_generator2.py` there are 2 important options to set before generation. 
Minimum distance beetwen 2 places and maximum distance between 2 neighbour places. Another importang thing to set is random seed. 
Next you can manually add/remove places (`positionsx` file) or connections (`connectionsx` file) and set starting figures positions (`figuresx` file).

