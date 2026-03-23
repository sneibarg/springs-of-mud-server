# Springs of MUD

This project is a Python-based Multi-User Dungeon (MUD) server. It aims to be a modernized simplification of the Rivers of MUD codebase.
The architecture shifts most of the C struct definitions to Python dataclasses and MongoDB NoSQL. A Java Spring Boot modulith backend is responsible
for handling the RESTful API access. By shifting the majority of the game logic to the modulith, the game can be easily extended and modified.

