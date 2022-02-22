# Intelligent-systems
There are three projects about Machine Learning (ML) and Artificial Intelligence (AI) written in Python programming language.

## Search algorithms
It is a graphic simulation of searching algorithms. The main application window contains two-dimensional map which consists of different kinds of fields and an agent who is moving through the map using a beforehand defined searching algorithm. The final cost of the path depends on the cost of different kinds of fields. The goal is to lead the agent from start to finish.

Different agents use different searching algorithms:

1. Aki uses the depth first searching (DFS) strategy and gives the advantage to the fields with lower cost, and in case of two or more fields with the same cost, he chooses the field on the certain side of the world (north, east, south, west).

2. Jocke uses the breadth first searching (BFS) strategy and gives the advantage to the fields with lower cost of his neighbors collectively, and in case of two or more fields with the same collective cost, he chooses the field on the certain side of the world (north, east, south, west).

3. Draza uses branch and bound searching (BBS) strategy, and in case of two paths with the same cost, he chooses the one with less fields in the path, that is any of them in case of two or more paths with same number of fields.

4. Bole uses A* searching strategy, with heuristic which simulates the air distance.
