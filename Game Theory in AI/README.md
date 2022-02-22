# Game Theory in AI

It is a graphic simulation of sequential games that uses the Minimax algorithm as well as some of its modifications (Alpha-beta prunning, Expectimax and Minimax for more than two players).

The main application window contains two-dimensional map which consists of different kinds of fields (road and hole) and players (bots/opponents and agents) who is moving through the map using a beforehand defined algorithm. The goal of each agent is to prevent all other agents from moving.

## Bots
**_Aki_** in every move choses an action which brings him closer to agent by Manhattan distance, and in the case of two or more such actions, he choses the field on the certain side of the world (north, northeast, east, southeast, south, southwest, west, northwest).

**_Jocke_** in every move choses an action randomly.

**_Draza_** uses implementation of Minimax algorithm with alpha-beta pruning.

**_Bole_** uses implementation of Minimax algorithm for more than two players

## Agents
**_MinimaxAgent_** uses Minimax algorithm implementation for two rational players.

**_MinimaxABAgent_** uses Minimax algorithm implementation with alpha-beta pruning for two relational players.

**_MaxNAgent_** uses Minimax algorithm generalization for games with more than two rational players where every player plays for his own gain.

**_ExpectAgent_** uses Expectimax algorithm implementation for two players which consists of only Max and Chance nodes. It is considered that every oponent plays randomly.

## Images
**MinimaxAgent vs Jocke:**

![min1](https://user-images.githubusercontent.com/40174491/155135606-4b238d8f-51a7-4734-beee-20d870fbbf65.PNG)

**ExpectAgent vs Jocke:**
![exp](https://user-images.githubusercontent.com/40174491/155135733-51fdff9d-2e31-483d-8375-5a238e2594d8.PNG)


**MaxNAgent vs Bole:**

![minN](https://user-images.githubusercontent.com/40174491/155135793-dec6fbfc-2244-4ad8-a1a9-233ae285361a.PNG)



