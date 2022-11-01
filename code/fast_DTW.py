#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division
import numbers
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict
from sklearn.metrics import classification_report
import numpy
import time
start = time.time()

# try:
#     range = xrange
# except NameError:
#     pass


def fastdtw(x, y, radius=1, dist=None):
    ''' return the approximate distance between 2 time series with O(N)
        time and memory complexity
        Parameters
        ----------
        x : array_like
            input array 1
        y : array_like
            input array 2
        radius : int
            size of neighborhood when expanding the path. A higher value will
            increase the accuracy of the calculation but also increase time
            and memory consumption. A radius equal to the size of x and y will
            yield an exact dynamic time warping calculation.
        dist : function or int
            The method for calculating the distance between x[i] and y[j]. If
            dist is an int of value p > 0, then the p-norm will be used. If
            dist is a function then dist(x[i], y[j]) will be used. If dist is
            None then abs(x[i] - y[j]) will be used.
        Returns
        -------
        distance : float
            the approximate distance between the 2 time series
        path : list
            list of indexes for the inputs x and y
        Examples
        --------

        import numpy as np
        import fastdtw
       x = np.array([1, 2, 3, 4, 5], dtype='float')
        y = np.array([2, 3, 4], dtype='float')
        fastdtw.fastdtw(x, y)
        (2.0, [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)])
    '''
    x, y, dist = __prep_inputs(x, y, dist)
    return __fastdtw(x, y, radius, dist)


def __difference(a, b):
    return abs(a - b)


def __norm(p):
    return lambda a, b: np.linalg.norm(a - b, p)


def __fastdtw(x, y, radius, dist):
    min_time_size = radius + 2

    if len(x) < min_time_size or len(y) < min_time_size:
        return dtw(x, y, dist=dist)

    x_shrinked = __reduce_by_half(x)
    y_shrinked = __reduce_by_half(y)
    distance, path = \
        __fastdtw(x_shrinked, y_shrinked, radius=radius, dist=dist)
    window = __expand_window(path, len(x), len(y), radius)
    return __dtw(x, y, window, dist=dist)


def __prep_inputs(x, y, dist):
    x = np.asanyarray(x, dtype='float')
    y = np.asanyarray(y, dtype='float')

    if x.ndim == y.ndim > 1 and x.shape[1] != y.shape[1]:
        raise ValueError('second dimension of x and y must be the same')
    if isinstance(dist, numbers.Number) and dist <= 0:
        raise ValueError('dist cannot be a negative integer')

    if dist is None:
        if x.ndim == 1:
            dist = __difference
        else:
            dist = __norm(p=1)
    elif isinstance(dist, numbers.Number):
        dist = __norm(p=dist)

    return x, y, dist


def dtw(x, y, dist=None):
    ''' return the distance between 2 time series without approximation
        Parameters
        ----------
        x : array_like
            input array 1
        y : array_like
            input array 2
        dist : function or int
            The method for calculating the distance between x[i] and y[j]. If
            dist is an int of value p > 0, then the p-norm will be used. If
            dist is a function then dist(x[i], y[j]) will be used. If dist is
            None then abs(x[i] - y[j]) will be used.
        Returns
        -------
        distance : float
            the approximate distance between the 2 time series
        path : list
            list of indexes for the inputs x and y
        Examples
        --------
        import numpy as np
        import fastdtw
        x = np.array([1, 2, 3, 4, 5], dtype='float')
        y = np.array([2, 3, 4], dtype='float')
        fastdtw.dtw(x, y)
        (2.0, [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)])
    '''
    x, y, dist = __prep_inputs(x, y, dist)
    return __dtw(x, y, None, dist)


def __dtw(x, y, window, dist):
    len_x, len_y = len(x), len(y)
    if window is None:
        window = [(i, j) for i in range(len_x) for j in range(len_y)]
    window = ((i + 1, j + 1) for i, j in window)
    D = defaultdict(lambda: (float('inf'),))
    D[0, 0] = (0, 0, 0)
    for i, j in window:
        dt = dist(x[i - 1], y[j - 1])
        D[i, j] = min((D[i - 1, j][0] + dt, i - 1, j), (D[i, j - 1][0] + dt, i, j - 1),
                      (D[i - 1, j - 1][0] + dt, i - 1, j - 1), key=lambda a: a[0])
    path = []
    i, j = len_x, len_y
    while not (i == j == 0):
        path.append((i - 1, j - 1))
        i, j = D[i, j][1], D[i, j][2]
    path.reverse()
    return (D[len_x, len_y][0], path)


def __reduce_by_half(x):
    return [(x[i] + x[1 + i]) / 2 for i in range(0, len(x) - len(x) % 2, 2)]


def __expand_window(path, len_x, len_y, radius):
    path_ = set(path)
    for i, j in path:
        for a, b in ((i + a, j + b)
                     for a in range(-radius, radius + 1)
                     for b in range(-radius, radius + 1)):
            path_.add((a, b))

    window_ = set()
    for i, j in path_:
        for a, b in ((i * 2, j * 2), (i * 2, j * 2 + 1),
                     (i * 2 + 1, j * 2), (i * 2 + 1, j * 2 + 1)):
            window_.add((a, b))

    window = []
    start_j = 0
    for i in range(0, len_x):
        new_start_j = None
        for j in range(start_j, len_y):
            if (i, j) in window_:
                window.append((i, j))
                if new_start_j is None:
                    new_start_j = j
            elif new_start_j is not None:
                break
        start_j = new_start_j

    return window


import numpy as np
from scipy.spatial.distance import euclidean

from fastdtw import fastdtw
from dtaidistance import dtw
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from dtaidistance import dtw_visualisation as dtwvis

predict_array = []
test_array = []
def dtw_fuction(df,test,ind):
    win_lenth = [int((len(df) * 2) / 10)]
    mean_y_test = []
    mean_total = []
    print('==================================')
    # sec_test = int((len(test) * 2) / 10)
    win_test = []
    win_per = []  # for period size (20,40,80)
# for test_ind in range(0, len(test), sec_test):
#     win_test.append(test.iloc[test_ind:test_ind + 200])
    for per in range(0, len(win_lenth), 1):
        win_min = 0
        kj = win_lenth[per]
        # print('result in win_length ', win_lenth)
        dis_array = []
        path_array = []
        win = []
        half_len_win = int(win_lenth[per] / 2)
        for i in range(half_len_win, len(df), half_len_win):
            counter = i - half_len_win
            while (counter < kj):
                win.append(df.iloc[counter:kj])
                counter = counter + 1
                kj = kj + 1
                if kj >= len(df):
                    break;
            # print(len(win))
        print('finish win creation...please wait...')
        # print(win[0 : 1])
        print('test file ' + str(ind) + ' compare starting...')

        for ii in range(0, len(win), 1):
            distance, path = fastdtw(win[ii], test, radius=1, dist=None)
            # print('In win size', per, ' distance with win number', ii, 'is', distance)
            dis_array.append([distance])
            path_array.append([path])
            minimum_dist = min(dis_array)
            win_min = win[dis_array.index(minimum_dist)]
        print('minimum window:', win_min)
        print('minimum distance:', minimum_dist)
        print('===================================')
        # print('path:', path_array[dis_array.index(minimum_dist)])

        win_per.append(win_min['grand'].iloc[-1])
        predict_array.append(win_per)
    print('Predicted Label:', win_per)
    mean_y_test.append(test['grand'].iloc[-1])
    # print('True Label', int(mean_y_test[0].iloc[0]))
    # print(mean_y_test)
    print('True Label', int(mean_y_test[0]))
    test_array.append(int(mean_y_test[0]))
    print('finished!')

    # plt.plot(win_min['grand'],test['grand'])
    # plt.show()


df = pd.read_csv('final_DB_as.csv', delimiter=',', header=None, names=['grand', 's1', 's2'], usecols=[0, 1, 2])
print(df)
df.columns = ['grand', 's1', 's2']
for ind in range(1,11,1):
    test = pd.read_csv('FlyerZz2_Dsr_test'+str(ind)+'.csv', delimiter=',', names=['grand', 's1', 's2'], usecols=[0, 1, 2])
    test.columns = ['grand', 's1', 's2']
    dtw_fuction(df,test,ind)

plt.figure()
df.plot(y='grand');
test.plot(y='grand');
plt.legend(loc='best')

print('======== Report Project Result =====================')
report = classification_report(test_array, predict_array)
print(report)
from sklearn.metrics import accuracy_score
accuracy=accuracy_score(test_array,predict_array)
print('ACCURACY is: ',accuracy)

end = time.time()
print(end - start)