# springs-of-mud-server

This project is a Python-based Multi-User Dungeon (MUD) server. It aims to be a modernized simplification of the Rivers of MUD codebase.
The architecture shifts most of the C struct definitions to Python dataclasses and MongoDB NoSQL. A Java Spring Boot modulith backend is responsible
for providing the RESTful API access. A Java Spring Boot microservice backed by Keycloak provides authentication and authorization.
By shifting the majority of the game data to the modulith, the game logic can be easily extended and modified. Our motto is to let the players
take on the role of the game master and game designer.


