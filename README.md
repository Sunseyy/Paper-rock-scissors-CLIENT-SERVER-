# Game Server Project

## Overview

This project is a Python-based server for managing a multiplayer game where players can challenge each other to random matches or participate in a tournament. It uses socket programming to facilitate communication between the server and clients. The game is based on the classic "Rock, Paper, Scissors" game, and includes features such as user login, game invitations, and ranking displays.

## Features

- **User Authentication**: Allows users to sign up and log in.
- **Random Matchmaking**: Pairs up players randomly for a match.
- **Game Invitations**: Players can send and accept invitations to challenge others.
- **Tournament Mode**: Players can join a tournament and compete in rounds.
- **Ranking System**: Displays the rankings based on player scores.
- **Game Logic**: Implements "Rock, Paper, Scissors" game rules with win/loss/tie outcomes.

## Installation

To run this project, make sure you have Python installed on your system. Then, clone the repository and install the necessary dependencies.

1. Clone the repository:

2. Run the server:
   '''python server.py'''


## Game Commands

Once connected, the client can interact with the server through the following options:

### `menu`
Displays the main menu with options like starting a random match, sending an invite, accepting an invite, viewing rankings, or quitting.

### `random_match`
Start a random match with another player.

### `send_invite`
Send a game invitation to another user.

### `accept_invite`
Accept an incoming game invitation.

### `view_rankings`
Display the leaderboard with player rankings.

### `Tournoi`
Join a tournament.

## Example Usage:

1. **Start a random match**: 
   - Send the `random_match` command to the server to get matched with a random player.

2. **Send an invite**: 
   - Use the `send_invite` command to invite a specific player to play against you.

3. **Join a tournament**: 
   - Use the `Tournoi` command to join an ongoing tournament and compete against other players.
