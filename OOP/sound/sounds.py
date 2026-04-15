"""
Project: Simple sound system using pygame.

This class loads multiple sounds and provides a simple interface
to play them. All pygame details are hidden inside the class.

https://www.pygame.org/docs/ref/mixer.html
https://www.pygame.org/docs/ref/music.html
"""

import pygame

class SoundPlayer:

    def __init__(self, sound_files):
        pygame.mixer.init()

        self.sounds = [pygame.mixer.Sound(f) for f in sound_files]
        self.volume = 0.5

        for sound in self.sounds:
            sound.set_volume(self.volume)

    def play(self, index, loop=False):
        loops = -1 if loop else 0
        self.sounds[index].play(loops=loops)

    def stop(self, index):
        self.sounds[index].stop()

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds:
            sound.set_volume(self.volume)

    def volume_up(self):
        self.set_volume(self.volume + 0.1)

    def volume_down(self):
        self.set_volume(self.volume - 0.1)


if __name__ == "__main__":

    player = SoundPlayer(["sound1.wav", "sound2.wav", "sound3.wav"])

    print("Controls:")
    print("1,2,3 -> play")
    print("q,w,e -> play loop")
    print("a,s,d -> stop")
    print("+ -> volume up")
    print("- -> volume down")
    print("x -> exit")

    # ACTION MAPPING
	# We use lambda to store actions that will be executed later.
	# If we remove lambda, the function is executed immediately instead of being stored.
    actions = {
        "1": lambda: player.play(0),
        "2": lambda: player.play(1),
        "3": lambda: player.play(2),

        "q": lambda: player.play(0, loop=True),
        "w": lambda: player.play(1, loop=True),
        "e": lambda: player.play(2, loop=True),

        "a": lambda: player.stop(0),
        "s": lambda: player.stop(1),
        "d": lambda: player.stop(2),

        # We use a tuple to execute multiple actions in a single lambda.
        "+": lambda: (player.volume_up(), print(f"Volume: {player.volume:.1f}")),
        "-": lambda: (player.volume_down(), print(f"Volume: {player.volume:.1f}")),
    }

    # MAIN LOOP
    while True:
        key = input(">> ")
        if key == "x":
            break
        elif key in actions:
            # The dictionary stores functions, not results.
            # To execute the function, we must call it with parentheses.
            actions[key]()
        else:
            print("Invalid key")