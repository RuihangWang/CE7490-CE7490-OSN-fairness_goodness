'''
Code for the paper:
Edge Weight Prediction in Weighted Signed Networks.
Conference: ICDM 2016
Authors: Srijan Kumar, Francesca Spezzano, VS Subrahmanian and Christos Faloutsos

Author of code: Srijan Kumar
Email of code author: srijan@cs.stanford.edu
'''
import networkx as nx
import matplotlib.pyplot as plt
from utils import leave_out_n
from page_rank import pagerank_predict_weight, pagerank_PR_graph
import fairness_goodness_computation as FG
from signed_hits import signed_hits, signed_G_hits
from triadic_status import triadic_status
from Multiple_Regression_Model import Multiple_Regression
import time

G = nx.DiGraph()

filenames = ['OTCNet', 'RFAnet', 'BTCAlphaNet', 'EpinionNetSignedNet', 'WikiSignedNet']
filename = filenames[3]

f = open('./CSV/' + filename +'.csv', "r")
for l in f:
    ls = l.strip().split(",")
    if float(ls[2]) >= 0:
        w = 1
        p = float(ls[2])
        n = 0
    else:
        p = 0
        n = float(ls[2])
        w = 0
    G.add_edge(ls[0], ls[1], weight=float(ls[2]), signed_weight=w, positive=p, negative=n)

f.close()

percentage = list(range(10, 100, 10))

error_FG = []
error_PR = []
error_signed_hits = []
error_triadic_status = []
error_LR = []

pcc_FG = []
pcc_PR = []
pcc_signed_hits = []
pcc_triadic_status = []
pcc_LR = []
start_time = time.time()
for step,n in enumerate(percentage):
    G_n = leave_out_n(G, n)
    print(time.time() - start_time)
    """
        PageRank
    """
    PR = nx.pagerank(G_n, weight='signed_weight')
    G_PR = pagerank_PR_graph(G_n, PR)
    error, pcc = pagerank_predict_weight(G, G_PR)
    error_PR.append(error)
    pcc_PR.append(pcc)
    print(time.time() - start_time)
    """
        Fairness and Goodness
    """
    fairness, goodness = FG.compute_fairness_goodness(G_n)
    error, pcc = FG.FG_predict_weight(G, G_n, fairness, goodness)
    error_FG.append(error)
    pcc_FG.append(pcc)
    print(time.time() - start_time)
    """
        Signed hits
    """
    h, a = nx.hits(G)
    G_hits = signed_G_hits(G_n, h, a)
    error, pcc = signed_hits(G, G_hits)
    error_signed_hits.append(error)
    pcc_signed_hits.append(pcc)
    print(time.time() - start_time)
    """
        Triadic Status
    """
    error, pcc = triadic_status(G, G_n)
    error_triadic_status.append(error)
    pcc_triadic_status.append(pcc)
    print(time.time() - start_time)
    """
        Multiple_Regression
    """
    error, pcc = Multiple_Regression(G, G_n, fairness, goodness, G_PR, G_hits)
    error_LR.append(error)
    pcc_LR.append(pcc)
    print(time.time() - start_time)
    print('G_len:{}, G_{}%:{}, RMSE_FG:{:.3f}, RMSE_PR:{:.3f}, RMSE_SH:{:.3f}, RMSE_TS:{:.3f}, RMSE_LR:{:.3f}'.format(
        len(G.edges()), n, len(G_n.edges()), error_FG[step], error_PR[step], error_signed_hits[step], error_triadic_status[step], error_LR[step]))

    print('G_len:{}, G_{}%:{}, PCC_FG:{:.3f}, PCC_PR:{:.3f}, PCC_SH:{:.3f}, PCC_TS:{:.3f}, PCC_LR:{:.3f}'.format(
        len(G.edges()), n, len(G_n.edges()), pcc_FG[step], pcc_PR[step], pcc_signed_hits[step], pcc_triadic_status[step], pcc_LR[step]))

plt.figure(dpi=500)
plt.xlim(xmax=100, xmin=0)
plt.plot(percentage, error_FG, label='F&G')
plt.plot(percentage, error_PR, label='PageRank')
plt.plot(percentage, error_signed_hits, label='Signed Hits')
plt.plot(percentage, error_triadic_status, label='Triadic Status')
plt.plot(percentage, error_LR, label='LR')
plt.legend()
plt.xlabel('Percentage of edges removed')
plt.ylabel('RMSE Error')
plt.savefig('./img/RMSE_' + filename +'.png')

plt.figure(dpi=500)
plt.xlim(xmax=100, xmin=0)
plt.plot(percentage, pcc_FG, label='F&G')
plt.plot(percentage, pcc_PR, label='PageRank')
plt.plot(percentage, pcc_signed_hits, label='Signed Hits')
plt.plot(percentage, pcc_triadic_status, label='Triadic Status')
plt.plot(percentage, pcc_LR, label='LR')
plt.legend()
plt.xlabel('Percentage of edges removed')
plt.ylabel('PCC')
plt.savefig('./img/PCC_' + filename +'.png')



