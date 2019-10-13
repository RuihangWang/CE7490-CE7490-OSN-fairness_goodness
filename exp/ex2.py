"""
    experiment for
    Leave one out
"""
from src.utils import *
from src.page_rank import Page_Rank
from src.bias_deserve import Bias_Deserve
from src.fairness_goodness import Fairness_Goodness
from src.reciprocal import Reciprocal
from src.signed_hits import Sighed_Hits
from src.status_theory import Status_Theory
from src.triadic_balance import Triadic_Balance
from src.triadic_status import Triadic_Status
from src.multiple_regression import Linear_Regression
G = init_Graph(filename='OTCNet.csv', path='../dataset/')

percentages = list(range(10, 100, 10))

for step, n in enumerate(percentages):
    G_n = leave_out_n(G, n)

    PR = Page_Rank(G_n)
    BG = Bias_Deserve(G_n)
    FG = Fairness_Goodness(G_n)
    RP = Reciprocal(G_n)
    SH = Sighed_Hits(G_n)
    ST = Status_Theory(G_n)
    TB = Triadic_Balance(G_n)
    TS = Triadic_Status(G_n)
    LR = Linear_Regression(G,G_n,PR,FG,SH)

    print(predict_weight(PR, G, G_n))
    print(predict_weight(BG, G, G_n))
    print(predict_weight(FG, G, G_n))
    print(predict_weight(RP, G, G_n))
    print(predict_weight(SH, G, G_n))
    print(predict_weight(ST, G, G_n))
    print(predict_weight(TB, G, G_n))
    print(predict_weight(TS, G, G_n))
    print(predict_weight(LR, G, G_n))













