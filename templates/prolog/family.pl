{{instances}}

hermano(X, Y) :-
    padre(Z, X),
    padre(Z, Y),
    madre(W, X),
    madre(W, Y),
    X \= Y.

tio(X, Y) :-
    hermano(X, Z),
    (padre(Z, Y); madre(Z, Y)).

abuelo(X,Y):-
    madre(X, Z),
    madre(Z, Y);
    madre(X, Z),
    padre(Z, Y);
    padre(X, Z),
    madre(Z, Y);
    padre(X, Z),
    padre(Z, Y).

primo(X, Y) :-
    abuelo(Z, X),
    abuelo(Z, Y),
    X \= Y,
    not(hermano(X, Y)).
