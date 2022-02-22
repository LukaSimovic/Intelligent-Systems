# Search algorithms
It is a graphic simulation of searching algorithms. The main application window contains two-dimensional map which consists of different kinds of fields and an agent who is moving through the map using a beforehand defined searching algorithm. The final cost of the path depends on the cost of different kinds of fields. The goal is to lead the agent from start to finish.

Different agents use different searching algorithms:

1. **_Aki_** uses the **depth first searching (DFS)** strategy and gives the advantage to the fields with lower cost, and in case of two or more fields with the same cost, he chooses the field on the certain side of the world (north, east, south, west). ![aki](https://user-images.githubusercontent.com/40174491/155127938-b8113465-34aa-4954-9a93-8f95da66575a.PNG)


2. **_Jocke_** uses the **breadth first searching (BFS)** strategy and gives the advantage to the fields with lower cost of his neighbors collectively, and in case of two or more fields with the same collective cost, he chooses the field on the certain side of the world (north, east, south, west). ![jocke](https://user-images.githubusercontent.com/40174491/155128068-d2d27c7b-97c1-4da7-a128-30105f63be92.PNG)


3. **_Draza_** uses **branch and bound searching (BBS)** strategy, and in case of two paths with the same cost, he chooses the one with less fields in the path, that is any of them in case of two or more paths with same number of fields. ![draza](https://user-images.githubusercontent.com/40174491/155128319-2a18aef0-672c-4b83-ad1e-75f55da32eb9.PNG)


4. **_Bole_** uses **A* searching** strategy, with heuristic which simulates the air distance. ![bole](https://user-images.githubusercontent.com/40174491/155128358-aebbdd00-202e-4289-a079-e03af1cf24a5.PNG)
