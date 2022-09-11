# Reglas para cercar la liebre:

* A. Tablero de Alquerque
* B. Movimiento en Cercar la liebre
* C. Disposición inicial de las fichas
* E. Estado final

## A. Tablero en Alquerque

Tablero 5x5

|   | 1 | 2 | 3 | 4 | 5 |
| - | - | - | - | - | - |
| 0 |   |   |   |   |   |
| 1 |   |   |   |   |   |
| 2 |   |   |   |   |   |
| 3 |   |   |   |   |   |
| 4 |   |   |   |   |   |


## B. Movimiento en _Cercar la liebre_

De todas los posibles movimientos, solo se pueden utilizar aquellos que no contengan otras fichas o no salgan fuera del tablero

### Movimientos Cazadores

#### Movimiento Pares

(X + Y) // 2 == 0

[-1, -1], [-1, 0], [-1, 1]
[-1, 0], [1, 0]
[-1, 1], [0, 1], [1, -1]

#### Movimiento impares

(X + Y) // 2 == 1

[-1, 0]
[-1, 0], [1, 0]
0, 1]

### Movimientos liebre

movimientos_cazadores + m*2 in movimientos cazadores if m ocupado por cazador

La liebre puede encadenar varios saltos


## C. Disposición inicial de las fichas

### Variante 12


|   | 1 | 2 | 3 | 4 | 5 |
| - | - | - | - | - | - |
| 0 | X | X | X | X | X |
| 1 | X | X | X | X | X |
| 2 | X |   | 0 |   | X |
| 3 |   |   |   |   |   |
| 4 |   |   |   |   |   |

### Variante 11


|   | 1 | 2 | 3 | 4 | 5 |
| - | - | - | - | - | - |
| 0 | X | X | X | X | X |
| 1 | X | X | X | X | X |
| 2 | X |   | 0 |   |   |
| 3 |   |   |   |   |   |
| 4 |   |   |   |   |   |

### Variante 10


|   | 1 | 2 | 3 | 4 | 5 |
| - | - | - | - | - | - |
| 0 | X | X | X | X | X |
| 1 | X | X | X | X | X |
| 2 |   |   | 0 |   |   |
| 3 |   |   |   |   |   |
| 4 |   |   |   |   |   |

### E. Estado final

Si la liebre no tiene movimientos disponibles -> ganan los cazadores

Si quedan <= 9 cazadores -> gana la liebre


