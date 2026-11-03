
# BOARD REPRESENTATION
     a  b  c  d  e  f  g  h
0    1  2  3  4  5  6  7  8    9
10   11 12 13 14 15 16 17 18   19
    -------------------------
20 | r  n  b  q  k  b  n  r  | 29   # 8
30 | p  p  p  p  p  p  p  p  | 39   # 7
40 | 41 42 43 44 45 46 47 48 | 49   # 6
50 | 51 52 53 54 55 56 57 58 | 59   # 5
60 | 61 62 63 64 65 66 67 68 | 69   # 4
70 | 71 72 73 74 75 76 77 78 | 79   # 3
80 | P  P  P  P  P  P  P  P  | 89   # 2
90 | r  n  b  q  k  b  n  r  | 99   # 1
    -------------------------
100 101 102 103 104 105 106 107 108 109
110 111 112 113 114 115 116 117 118 119


0: "P",  # white pawn
1: "N",  # white knight
2: "B",  # white bishop
3: "R",  # white rook
4: "Q",  # white Queen
5: "K",  # white King
6: "p",  # black pawn
7: "n",  # black knight
8: "b",  # black bishop
9: "r",  # black rook
10: "q", # black Queen
11: "k", # black King


# KNIGHT MOVES
    -21		-19	
-12				-8
        N		
8				12
    19		21	


### Perf Test 03.11.2026 
Starting Perft Test (Mode: compare, Divide: False)
Board Class: MyBoard
FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
------------------------------------------------------------

--- Depth 1 ---
[Reference] Nodes: 20 | Time: 0.0005s
[MyBoard  ] Nodes: 20 | Time: 0.0044s
Status: ✅ PASS

--- Depth 2 ---
[Reference] Nodes: 400 | Time: 0.0055s
[MyBoard  ] Nodes: 400 | Time: 0.0979s
Status: ✅ PASS

--- Depth 3 ---
[Reference] Nodes: 8,902 | Time: 0.1101s
[MyBoard  ] Nodes: 8,902 | Time: 2.3663s
Status: ✅ PASS

--- Depth 4 ---
[Reference] Nodes: 197,281 | Time: 2.5039s
[MyBoard  ] Nodes: 197,281 | Time: 51.9407s
Status: ✅ PASS