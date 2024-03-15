{{instances}}

% Regla que define la relación de hermano entre dos personas
hermano(X, Y) :-
    padre(Z, X), % X comparte al menos un padre (Z) con Y
    padre(Z, Y), % Y comparte al menos un padre (Z) con X
    madre(W, X), % X comparte al menos una madre (W) con Y
    madre(W, Y), % Y comparte al menos una madre (W) con X
    X \= Y.     % X no es igual a Y, para evitar que alguien sea su propio hermano

% Regla que define la relación de tío entre dos personas
tio(X, Y) :-
    hermano(X, Z),   % X es hermano de Z
    (padre(Z, Y); madre(Z, Y)). % Z es padre o madre de Y, por lo tanto X es tío de Y

% Regla que define la relación de abuelo entre dos personas
abuelo(X,Y):-
    (madre(X, Z), madre(Z, Y)); % X es madre de Z y Z es madre de Y, por lo tanto X es abuelo de Y
    (madre(X, Z), padre(Z, Y)); % X es madre de Z y Z es padre de Y, por lo tanto X es abuelo de Y
    (padre(X, Z), madre(Z, Y)); % X es padre de Z y Z es madre de Y, por lo tanto X es abuelo de Y
    (padre(X, Z), padre(Z, Y)). % X es padre de Z y Z es padre de Y, por lo tanto X es abuelo de Y

% Regla que define la relación de primo entre dos personas
primo(X, Y) :-
    abuelo(Z, X),   % Z es abuelo de X
    abuelo(Z, Y),   % Z es abuelo de Y
    X \= Y,         % X no es igual a Y
    not(hermano(X, Y)). % X y Y no son hermanos, ya que si lo fueran no serían primos sino hermanos
