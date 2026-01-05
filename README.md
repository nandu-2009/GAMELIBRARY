# 🎮 GameLibrary

A comprehensive collection of competitive multiplayer games built with Python, featuring a modern Tkinter-based launcher and SQLite database for score tracking.

## 📋 Table of Contents

- [Features](#features)
- [Games Included](#games-included)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🎯 Competitive Gaming**: Head-to-head multiplayer games with score tracking
- **📊 Score Persistence**: SQLite database stores player wins across sessions
- **🎨 Modern UI**: Clean, intuitive Tkinter interface with consistent theming
- **🔧 Modular Design**: Well-organized codebase with separate database and configuration modules
- **🎮 Diverse Games**: Variety of game genres including puzzles, action, and strategy
- **👥 Player Management**: User authentication and personalized gaming experience

## 🎲 Games Included

| Game | Genre | Description |
|------|-------|-------------|
| **Guess the Number** | Puzzle | Competitive number guessing with attempt tracking |
| **Connect 4** | Strategy | Classic 4-in-a-row board game |
| **Ping Pong** | Action | Fast-paced paddle ball game |
| **Tic Tac Toe** | Puzzle | Classic 3x3 grid game |
| **Snake** | Action | Competitive snake eating with score comparison |
| **Asteroids** | Action | Space shooter with score-based competition |
| **Flappy Bird** | Action | Competitive bird flying with obstacle avoidance |
| **Dots and Boxes** | Strategy | Territory capture board game |
| **Wordle** | Puzzle | Competitive word guessing game |
| **Maze Game** | Action | Time-based maze navigation |
| **Smash Keys** | Action | Fast keyboard smashing competition |
| **Memory Game** | Puzzle | Sequence memory challenge |

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nandu-2009/GAMELIBRARY.git
   cd gamelibrary
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python gamelibrary.py
   ```

## 🎮 Usage

### First Time Setup

1. **Create Account**: Launch the app and create a user account
2. **Login**: Use your credentials to access the game library
3. **Enter Player Names**: Input names for Player 1 and Player 2
4. **Select Game**: Choose from the available games in the library
5. **Play**: Enjoy competitive gaming with score tracking!

### Game Controls

Each game has its own controls, displayed within the game window. Common controls include:
- Mouse clicks for selection
- Keyboard input for actions
- WASD/Arrow keys for movement

### Score Tracking

- Wins are automatically recorded in the database
- View current scores in the main game library
- Scores persist across sessions

## 📋 Requirements

### Core Dependencies
- `tkinter` (built-in with Python)
- `sqlite3` (built-in with Python)
- `pygame` (for graphical games)
- `turtle` (built-in, for some games)
- `random` (built-in)
- `time` (built-in)
- `os` (built-in)
- `sys` (built-in)

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 512MB minimum
- **Storage**: 50MB free space
- **Display**: 1024x768 resolution minimum

## 🏗️ Project Structure

```
gamelibrary/
├── gamelibrary.py          # Main application launcher
├── database.py             # Database operations module
├── config.py               # Configuration and constants
├── README.md               # This file
├── .gitignore             # Git ignore rules
├── users.db               # SQLite database (auto-generated)
├── games/                 # Individual game modules
│   ├── game_db.py         # Shared database utilities for games
│   ├── tictactoe.py       # Tic Tac Toe game
│   ├── connect4.py        # Connect 4 game
│   ├── pingpong.py        # Ping Pong game
│   ├── snake.py           # Snake game
│   ├── asteroids.py       # Asteroids game
│   ├── flappybird.py      # Flappy Bird game
│   ├── dotsandboxes.py    # Dots and Boxes game
│   ├── wordle.py          # Wordle game
│   ├── mazegame.py        # Maze navigation game
│   ├── smashkeys.py       # Keyboard smashing game
│   ├── memorygame.py      # Memory sequence game
│   ├── guessthenumber.py  # Number guessing game
│   ├── answers.txt        # Wordle answer list
│   ├── words.txt          # Wordle word list
│   └── __pycache__/       # Python cache files
└── icons/                 # Game icons (PNG files)
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a Pull Request

### Adding New Games

1. Create a new Python file in the `games/` directory
2. Follow the existing pattern:
   - Import `record_win` and `get_players` from `game_db`
   - Accept player names as command-line arguments
   - Call `record_win(player)` when a player wins
   - Handle game over gracefully
3. Add the game to `config.py` GAMES list
4. Add an icon PNG to the `icons/` directory
5. Update this README

### Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable names
- Add comments for complex logic
- Test games thoroughly before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's standard library and Pygame
- Inspired by classic arcade games
- Thanks to the open-source community for game development resources

## 🐛 Issues & Support

If you encounter any issues:
1. Check the [Issues](https://github.com/nandu-2009/GAMELIBRARY/issues) page
2. Create a new issue with detailed description
3. Include your Python version and OS

## 🎯 Future Plans

- [ ] Add more games (Chess, Checkers, etc.)
- [ ] Implement online multiplayer
- [ ] Add achievements system
- [ ] Create mobile version
- [ ] Add sound effects and music
- [ ] Implement game statistics and leaderboards

---

**Enjoy gaming! 🎮**