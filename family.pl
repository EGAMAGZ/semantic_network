padre(aldaberto, eduardo).
padre(eduardo, gamaliel).
padre(eduardo, emmanuel).
padre(juan, maribel).
padre(juan, esmeralda).
padre(juan, ricardo).

madre(sara, eduardo).
madre(agustina, maribel).
madre(agustina, esmeralda).
madre(agustina, ricardo).
madre(maribel, gamaliel).
madre(maribel, emmanuel).

mujer(maribel).
mujer(agustina).
mujer(sara).
mujer(esmeralda).

hombre(eduardo).
hombre(gamaliel).
hombre(emmanuel).
hombre(aldaberto).
hombre(juan).

sibling(X, Y) :-
    padre(Z, X),
    padre(Z, Y),
    madre(W, X),
    madre(W, Y),
    X \= Y.

hermano(X,Y):-
    sibling(X,Y),
    hombre(X).

hermana(X,Y) :-
    sibling(X,Y),
    mujer(X).

gran(X,Y):-
    madre(X, Z),
    madre(Z, Y);

    madre(X, Z),
    padre(Z, Y);

    padre(X, Z),
    madre(Z, Y);

    padre(X, Z),
    padre(Z, Y).

abuelo(X, Y) :-
    gran(X,Y),
    hombre(X).

abuela(X, Y) :-
    gran(X,Y),
    mujer(X).
