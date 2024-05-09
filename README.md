# Term Roulette

A simple game simulator of the Russian Roulette game, with more strategy and much safer to play.

## Rules

### Guns
There are three types of guns available: revolver, handgun or shotgun. Each of them have different number of bullets and powerups loaded. You can view more details in the game. The following rules take revolver as an example.

Each round the revolver is loaded with 3 bullets in 6 chambers. The player and the opponent then take action in turns. The player have two choices in their turn: **shoot the opponent** or **shoot himself**.

- If the player choose to shoot.
  - If the chamber is **loaded**, the guy who gets shot loss one HP and the player turn ends.
  - If the chamber is **not loaded** and the player **shoots himself**, the player gets a second turn.
  - If the chamber is **not loaded** and the player **shoots the opponent**, the player turn ends.

### Powerups
The powerups are special bullet in the chambers. The number of powerups are predefined for each gun type, but their locations in the chamber are random. They have special abilities compare with regular bullets, and player needs to use it wisely.

### Game over
Each player have 5 HP. When a player has 0 HP, the game end and that player losses.

## Usage
Just run the `main.py` file to start the game. Press `D` to toggle between dark & light theme, and press `Ctrl-c` to exit the game.
```{bash}
python main.py
```

You can also play the game on browser if your terminal has some limitation. First install `textual-web` by `pip install textual-web` and then run the command to serve the web app.
```{bash}
textual-web --config ganglion.toml
```

Then you shall see a URL printed after a while. Click the link or copy and open it in your browser will open the game.

## Controls
The game support both mouse and keyboard input. For mouse, just click on the buttons to interact.

For keyboard, use **arrow keys** to move the focus between list, and use **TAB** to switch focus between buttons and list. Press **Enter** to confirm selection.

## Test
You can run the test to see the performance of the agent by the winning rate in simulated AI v.s. AI games. The default agent used is Berserker, and tested to run on 10000 times. You can change the parameters in the `test.py` file to see the verbose of each game and add more runs. To see the result with default setting, run `python test.py`.
