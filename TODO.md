
TODO LIST
=========

- implementare jump point search (neighbor pruning)
- implementare subgoals
- fare refactor con classi, classe node etc
- mettere controlli su dimensione finestra
- mettere controllo su input files
- migliorare sogliatura su parti non testuali
- fare in modo che si possano passare parametri da terminal con flags etc.
- FATTO - fare in modo che da terminale possa passare più di un'immagine e ciò corrisponda ad eseguire un ciclo
- FATTO - implementare text line localization
- provare dilatazione per migliorare la line localization
- FATTO - implementare A* e sue funzioni di costo
- creare groundtruth

Problemi:
- aggiungere controllo di in bounds nella funzione jump
- fare jump iterativo
- creare grid con matlab

FATTO - RICONTROLLARE I SEGNI IN JUMP E IN FIND_NEIGHBORS


main
    - sauvola
    - linelocalization
    - pathfinder
        - astar
        - jps


main chiama pathfinder
pathfinder crea open, close, grid, crea oggetto astar passando gli quei parametri
posso chiamare pathfind di astar per trovare path con astar normale
per jps? in pathfinder creo astar con i soliti parametri, creo jps passandogli l'oggetto astar
posso chiamare pathfind di jps per trovare path con astar + jps
in jps c'è la struttura simile ad astar più identify_successors, jump etc
in astar c'è l'algoritmo di pathfind e le varie funzioni di costo, in più tiene le liste e la mappa
