set VERTICES;
set COLORS;

param adj{VERTICES, VERTICES}, binary;

var x{v in VERTICES, c in COLORS}, binary;  # x[v,c] = 1 se v recebe cor c
var y{c in COLORS}, binary;                 # y[c] = 1 se cor c é usada

minimize NumColors: sum{c in COLORS} y[c];

s.t. OneColorPerVertex{v in VERTICES}:
    sum{c in COLORS} x[v,c] = 1;

s.t. AdjacentDifferent{v in VERTICES, u in VERTICES, c in COLORS: v < u && adj[v,u] = 1}:
    x[v,c] + x[u,c] <= 1;

s.t. ColorUsed{v in VERTICES, c in COLORS}:
    x[v,c] <= y[c];