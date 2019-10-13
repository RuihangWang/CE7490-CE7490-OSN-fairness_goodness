"""
    experiment for
    Leave one out
"""
import sys
sys.path.append('../src')
from utils import *
from page_rank import Page_Rank
from bias_deserve import Bias_Deserve
from fairness_goodness import Fairness_Goodness
from reciprocal import Reciprocal
from signed_hits import Sighed_Hits
from status_theory import Status_Theory
from triadic_balance import Triadic_Balance
from triadic_status import Triadic_Status
from multiple_regression import Linear_Regression

G = init_Graph(filename='OTCNet.csv', path='../dataset/')

### remove edges
remove_edges = leave_out_edges(G, 1000)
### G_1
G_1 = G.copy()
total_w_ = {'FG':[], 'PR':[], 'SH':[], 'TS':[], 'LR':[], 'BD':[], 'RP':[], 'ST':[], 'TB':[]}
total_w = []

PR = Page_Rank(G_1)
BD = Bias_Deserve(G_1)
FG = Fairness_Goodness(G_1)
RP = Reciprocal(G_1)
SH = Sighed_Hits(G_1)
ST = Status_Theory(G_1)
TB = Triadic_Balance(G_1)
TS = Triadic_Status(G_1)
LR = Linear_Regression(G,G_1,PR,FG,SH)

for step, (u, v) in enumerate(remove_edges):
    G_1.remove_edge(u, v)
    print(predict_weight(PR, G, G_1, (u, v)))
    print(predict_weight(BD, G, G_1, (u, v)))
    print(predict_weight(FG, G, G_1, (u, v)))
    print(predict_weight(RP, G, G_1, (u, v)))
    print(predict_weight(SH, G, G_1, (u, v)))
    print(predict_weight(ST, G, G_1, (u, v)))
    print(predict_weight(TB, G, G_1, (u, v)))
    print(predict_weight(TS, G, G_1, (u, v)))
    print(predict_weight(LR, G, G_1, (u, v)))
    G_1.add_edge(u, v, weight=G[u][v]['weight'],
                 signed_weight=G[u][v]['signed_weight'],
                 positive=G[u][v]['positive'],
                 negative=G[u][v]['negative'])














