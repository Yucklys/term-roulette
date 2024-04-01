# Term Roulette

A simple game simulator of the Russian Roulette game, with more strategy and much safer to play.

## Rules

### Revolver
Each round the revolver is loaded with 3 bullets in 6 chambers. The player and the opponent then take action in turns. The player have three choices in their turn: **shoot the opponent**, **shoot himself**, or **use an item**.

- If the player choose to shoot.
  - If the chamber is **loaded**, the guy who gets shot loss one Armor and the player turn ends.
  - If the chamber is **not loaded** and the player **shoots himself**, the player gets a second turn.
  - If the chamber is **not loaded** and the player **shoots the opponent**, the player turn ends.

### Items
Items are distributed randomly at the start of each round. Each player receive 3 items, and they can use as many as they like in their turn. Items have different effects, like **increase the player Armor**, **double the next damage**, **skip the next chamber**, etc.

### Game over
Each player have 5 Armor. Each will block one shoot for you. When a player have 0 Armor, he can no longer regain Armor, and he will loss if he gets one more shoot. The last player standing wins the game.

## Usage
Just run the `main.py` file to start the game. Press `D` to toggle between dark & light theme, and press `Ctrl-c` to exit the game.
```{python}
python main.py
```

## TODO
- [ ] Add items.
- [ ] Add UI for Armors.
- [ ] Add checks for game ends.
- [ ] Add selector for AI or human opponent.
- [ ] Implement AI for the opponent.
- [ ] Add more game modes with different number of bullets, players, or items for each turn.
