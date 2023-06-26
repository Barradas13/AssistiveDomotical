import math

def razaoDistOlhos(p2, p6, p3, p5, p1, p4):
    a = p2[0] - p6[0]
    b = p2[1] - p6[1]

    p2p6 = math.sqrt(a * a + b * b)

    a = p3[0] - p5[0]
    b = p3[1] - p5[1]

    p3p5 = math.sqrt(a * a + b * b)

    a = p1[0] - p4[0]
    b = p1[1] - p4[1]

    p1p4 = math.sqrt(a * a + b * b)

    return (p2p6 + p3p5) / (2 * p1p4)