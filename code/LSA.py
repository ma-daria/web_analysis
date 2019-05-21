import Include
import Сlustering

def lsa(measurement):
    col = measurement.columns
    measurement = measurement.T
    measurement = Include.preprocessing.normalize(measurement)
    U, S, Vt = Include.np.linalg.svd(measurement)
    k = int((col.size * 10)/100)
    U = U[:,0:k]
    S = S[0:k]
    Vt = Vt[0:k, :]
    U_S = Include.np.multiply(S, U)
    A_ = Include.np.dot(U_S, Vt)
    #это  мб вообще не нужно
    Сlustering.СlusteringMetod(A_, 0.2, col)
    Include.plt.savefig("Result/LSA.png")