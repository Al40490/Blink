# Blink v1.0

**Words in a blink of an eye.**

Blink lets people who are unable to speak, and who have a disability from the neck down, express their thoughts in Morse code using only their eyes. It requires no expensive equipment and no heavy software.

## Requirements

- [TouchDesigner](https://derivative.ca/download)
- `MediaPipe.tox` (too large for this repo): download it from the [MediaPipe TouchDesigner releases](https://github.com/torinmb/mediapipe-touchdesigner/releases) and place it in the `toxes` folder

## Credits

Built on top of [MediaPipe TouchDesigner](https://github.com/torinmb/mediapipe-touchdesigner) by torinmb, which we modified for this project.

## How to use

Open `Blink_v1.toe` to launch the project in TouchDesigner.

| Action | Gesture |
|---|---|
| `.` (dot) | Close your eyelid for 0.25 to 0.75 s |
| `_` (dash) | Close your eyelid for 0.75 to 2 s |
| Confirm a letter | Look to the left |
| Delete the last symbol | Close your eyelid for more than 2 s |
| Space | Look to the left twice in a row |

## Tools used for this project

TouchDesigner, MediaPipe, Python, Claude (Opus 5.5) for code debugging and ChatGPT (Free version) for TouchDesigner debugging

## Authors

Daniel Chan, Kevin Tan, Mouhamadou Aliou Diallo and Philippe Pou


This project is made during the hackathon HackConcordia 2026
