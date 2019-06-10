import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import seaborn as sns
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from scipy.spatial import distance
from sklearn import preprocessing
from scipy.cluster import hierarchy
import os
import io



CHEMISTRY = 0
ZOOPLANKTON = 1
MIX = 2

CL_ZOOPLANKTON  = 0
CL_CHEMISTRY = 2