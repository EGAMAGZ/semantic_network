padre(aldaberto, eduardo).
padre(eduardo, gamaliel).
padre(eduardo, emmanuel).
padre(juan, maribel).
padre(juan, esmeralda).
padre(juan, ricardo).
padre(fernando, rosalba).
padre(fernando, jesenia).
padre(fernando, picos).

madre(sara, eduardo).
madre(agustina, maribel).
madre(agustina, esmeralda).
madre(agustina, ricardo).
madre(maribel, gamaliel).
madre(maribel, emmanuel).
madre(esmeralda, rosalba).
madre(esmeralda, jesenia).
madre(esmeralda, picos).

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
