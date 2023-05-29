# Romance of the Three Kingdoms XI Scenario Editor

WIP scenario editor for the strategy game 'Romance of the Three Kingdoms XI' Released by Koei.

Currently only supports the English PC release of the game.

This is made purely by reverse-engineering the binary layout of the scenario files, with the help and documented knowledge of the fine folks at [The Scholars of Shen Zhou](https://the-scholars.com/)

## Usage
To install the necessary requirements:

`python3 -m pip install -r requirements.txt`

Make sure to have imported the submodules as well:

`git submodule update --init --recursive`

To run the application:

`python3 rtk11.py`

## Disclaimer

As it's WIP, expect plenty of bugs and missing features.

This project does not, and will never contain any copyrighted material from Koei. You will need a copy of the game and its scenario files in order to use this tool.

## Roadmap

- Support for the [PUK version available on Steam](https://store.steampowered.com/app/628070)
- Support for the PS2 version of the game (Possibly also PUK)
- Support for in-game events
