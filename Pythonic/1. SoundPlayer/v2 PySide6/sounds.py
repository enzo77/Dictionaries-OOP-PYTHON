"""
Simple sound system with a PySide6 GUI.
pip install pyside6 pygame
"""

import sys
import pygame

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)


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


class SoundPlayerWindow(QWidget):
    """
    Main application window.

    This class provides a graphical interface to control a SoundPlayer object.

    The window contains:
        - Three rows of buttons, one row for each sound.
        - A volume control section.
        - A label showing the current volume.

    Each row has three buttons:
        - Play: play the sound once.
        - Loop: play the sound continuously.
        - Stop: stop the sound.

    The class inherits from QWidget, which is the basic building block for
    windows and controls in Qt.
    """

    def __init__(self):
        # Always call the constructor of the base class first.
        super().__init__()

        # Create the object that contains all sound-related functionality.
        # The GUI does not know anything about pygame; it only calls methods
        # of SoundPlayer.
        self.player = SoundPlayer([
            "sound1.wav",
            "sound2.wav",
            "sound3.wav",
        ])

        # Set the text displayed in the title bar of the window.
        self.setWindowTitle("Sound Player")

        # QLabel is a widget used to display text.
        # It will show the current volume.
        self.volume_label = QLabel(
            f"Volume: {self.player.volume:.1f}"
        )

        # QVBoxLayout arranges widgets vertically from top to bottom.
        # This will be the main layout of the window.
        layout = QVBoxLayout()

        # Create one row of controls for each sound.
        for index in range(3):

            # QHBoxLayout arranges widgets horizontally from left to right.
            # Each row will contain three buttons.
            row = QHBoxLayout()

            # Create the buttons for this sound.
            play_button = QPushButton(f"Play {index + 1}")
            loop_button = QPushButton(f"Loop {index + 1}")
            stop_button = QPushButton(f"Stop {index + 1}")

            # clicked is a Qt signal emitted when the button is pressed.
            # connect() associates the signal with a function to execute.
            #
            # We use lambda to delay execution until the user clicks.
            #
            # "i=index" is essential. Without it, all lambdas would capture
            # the same final value of index (2), and all buttons would
            # control the third sound.

            # We use a lambda because self.player.play() requires the index argument.
            # The lambda creates a new parameterless function that remembers the current
            # value of index.
            #
            # Equivalent code:
            #
            #     def play_sound():
            #         self.player.play(index)
            #
            #     play_button.clicked.connect(play_sound)
            #
            # Without the lambda, writing self.player.play(index) would execute the
            # function immediately instead of passing it to connect()
            play_button.clicked.connect(
                lambda checked=False, i=index: self.player.play(i)
            )
            

            # Play the selected sound in an infinite loop.
            loop_button.clicked.connect(
                lambda checked=False, i=index:
                self.player.play(i, loop=True)
            )

            # Stop the selected sound.
            stop_button.clicked.connect(
                lambda checked=False, i=index: self.player.stop(i)
            )

            # Add the buttons to the horizontal row.
            row.addWidget(play_button)
            row.addWidget(loop_button)
            row.addWidget(stop_button)

            # Add the completed row to the main vertical layout.
            layout.addLayout(row)

        # Create the volume control section.
        volume_row = QHBoxLayout()

        # Buttons to decrease and increase the volume.
        volume_down_button = QPushButton("Volume -")
        volume_up_button = QPushButton("Volume +")

        # Connect the buttons to methods of this class.
        volume_down_button.clicked.connect(self.decrease_volume)
        volume_up_button.clicked.connect(self.increase_volume)

        # Add widgets to the horizontal volume layout.
        volume_row.addWidget(volume_down_button)
        volume_row.addWidget(self.volume_label)
        volume_row.addWidget(volume_up_button)

        # Add the volume section to the main layout.
        layout.addLayout(volume_row)

        # Set the main layout of the window.
        # Once assigned, Qt automatically positions all widgets.
        self.setLayout(layout)

    def increase_volume(self):
        """
        Increase the volume and refresh the label.
        """
        self.player.volume_up()
        self.update_volume_label()

    def decrease_volume(self):
        """
        Decrease the volume and refresh the label.
        """
        self.player.volume_down()
        self.update_volume_label()

    def update_volume_label(self):
        """
        Update the label that displays the current volume.
        """
        self.volume_label.setText(
            f"Volume: {self.player.volume:.1f}"
        )


if __name__ == "__main__":
    # Create the QApplication object.
    #
    # Every Qt program must create exactly one QApplication instance.
    # This object initializes the GUI framework and manages the main
    # event loop of the application.
    #
    # sys.argv contains the command-line arguments passed to the program.
    # Qt can use them to process optional configuration parameters.
    app = QApplication(sys.argv)

    # Create the main window of the application.
    #
    # This instantiates our SoundPlayerWindow class, which builds all
    # widgets (buttons, labels, layouts) and connects their signals
    # to the corresponding methods.
    window = SoundPlayerWindow()

    # Make the window visible on the screen.
    #
    # Creating a widget does not automatically display it.
    # The show() method tells Qt to display the window.
    window.show()

    # Start the Qt event loop.
    #
    # app.exec() enters an infinite loop managed by Qt.
    # Inside this loop, Qt waits for events such as:
    #   - button clicks
    #   - key presses
    #   - mouse movements
    #   - window resize events
    #   - repaint requests
    #
    # The event loop continues running until the user closes the window.
    #
    # app.exec() returns an integer exit code, usually:
    #   0 -> normal termination
    #   non-zero -> abnormal termination or error
    #
    # sys.exit(...) terminates the Python program and returns the same
    # exit code to the operating system.
    sys.exit(app.exec())