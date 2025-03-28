# Bare Ball Buster - Progressive Web App

A fast-paced arcade shooter game that can be installed as a Progressive Web App on your device.

## Features

- **Offline Play**: Once installed, play the game without an internet connection
- **Mobile Support**: Touch controls for smooth gameplay on mobile devices
- **Installable**: Add to your home screen for quick access
- **Responsive Design**: Adapts to different screen sizes and orientations

## How to Install

### On Mobile (Android/iOS)

1. Open the game in your mobile browser (Chrome, Safari, etc.)
2. For Chrome/Android:
   - Tap the menu button (three dots)
   - Select "Add to Home Screen"
3. For Safari/iOS:
   - Tap the share button (square with arrow)
   - Select "Add to Home Screen"
4. Give the app a name or keep the default, then tap "Add"
5. The game is now installed on your home screen

### On Desktop

1. Open the game in Chrome
2. Look for the install icon in the address bar (a small "+" icon)
3. Click on it and follow the prompts
4. Alternatively, click the menu (three dots) and select "Install Bare Ball Buster"

## How to Play

### Desktop Controls

- **WASD or Arrow Keys**: Move your character
- **Mouse**: Aim
- **Left Mouse Button**: Shoot
- **Space**: Dash
- **Alt+D**: Toggle debug mode
- **L**: Pause game

### Mobile Controls

- **Left Joystick**: Move your character
- **Right Joystick**: Aim and shoot
- **Dash Button**: Perform a dash move
- **Pause Button**: Pause the game

## Development Setup

To work on this game, you'll need:

1. A modern web browser (Chrome, Firefox, etc.)
2. A local server to test the game and service worker

To run a simple local server, you can use:

```bash
# If you have Python installed
python -m http.server 8000

# If you have Node.js installed
npx serve
```

Then open your browser and navigate to `http://localhost:8000`.

## PWA Components

This game has been converted to a PWA with the following features:

1. **Web App Manifest**: Found in `manifest.json`
2. **Service Worker**: Provides offline functionality via `service-worker.js`
3. **Touch Controls**: Implemented in `touch-controls.js`
4. **Responsive Design**: CSS media queries for different screen sizes

## Future Enhancements

- High score leaderboard with cloud sync
- More power-ups and enemy types
- Multiplayer capabilities
- Advanced touch control options

## License

This project is open source and available under the MIT License.

---

Created with 💖 by JL Studios

