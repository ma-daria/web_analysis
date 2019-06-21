import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.spatial import distance
from sklearn import preprocessing
from scipy.cluster import hierarchy
import os
import io
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import LatentDirichletAllocation

CO_CHEMISTRY = 0
CO_ZOOPLANKTON = 1
CO_MIX = 2
CO_LSA = 3

CL_ZOOPLANKTON  = 0
CL_LSA = 1
CL_CHEMISTRY = 2

PA_DESCRIPTION = 0
PA_PLACE = 1