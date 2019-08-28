import neat
from ai import visualize
import os

# for visualizing output network
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

inputs = [
    [193.074, 185.823, 0.715357, -1.01931, 53.1486, 218.89, 0.24280963, 25, 0, 5, 2, -1, 1, 209, 0, -1, 14, 0,
     0, 4, 2, 0, 0, 5, 25, 0, 0, 0, 0, 1, 0, 0],
    [267.097, 271.73, -0.157986, -2.80704, 108.93, 270.314, 0.402975799, 32, 3, 9, 2, 0, 2, 484, 1, -1, 19, 0,
     8, 2, 6, 0, 0.07344166, 3, 32, 0, 0, 0, 0, 0, 1, 0],
    [525.104, 500.521, -0.201409, -3.42919, 144.433, 502.584, 0.287380816, 57, 2, 14, 4, 0, 4, 848, 1, -1, 34,
     1, 5, 8, 9, 0.006923625, 0.034618127, 11, 57, 0, 0, 0, 1, 1, 0, 0],
    [448.113, 419.279, 1.44648, -3.36321, 86.0421, 454.487, 0.189316966, 54, 3, 10, 3, -2, 3, 614, 0, -2, 30,
     0, 5, 6, 8, 0, 0.058111087, 9, 54, 0, 0, 0, 0, 2, 0, 0],
    [230.094, 224.258, 3.15557, -3.64663, 35.9188, 255.13, 0.140786266, 31, 1, 4, 1, -1, 2, 277, 0, -1, 17, 0,
     0, 4, 3, 0, 0, 3, 31, 0, 0, 0, 0, 1, 0, 0],
    [514.237, 518.092, 7.50594, -8.79024, 50.789, 553.293, 0.09179404, 69, 0, 5, 1, -1, 6, 831, 0, -1, 39, 0,
     0, 7, 6, 0, 0, 7, 69, 0, 0, 0, 0, 1, 0, 0],
    [137.024, 120.519, 1.25618, -1.32798, 45.1946, 141.74, 0.318855651, 15, 0, 5, 1, -1, 1, 133, 0, -1, 10, 0,
     0, 1, 0, 0, 0, 1, 15, 0, 0, 0, 0, 1, 0, 0],
    [349.066, 297.433, -0.269092, -2.05038, 114.459, 294.674, 0.388425854, 36, 0, 13, 4, -1, 3, 578, 0, -1, 25,
     0, 2, 2, 1, 0, 0.017473506, 4, 36, 0, 0, 0, 0, 1, 0, 0],
    [378.902, 252.54, 0.772575, -4.55218, 102.975, 281.059, 0.366382148, 28, 1, 10, 4, 0, 2, 571, 0, 0, 20, 0,
     1, 1, 2, 0, 0.009711095, 2, 28, 0, 0, 0, 1, 0, 0, 0],
    [645.142, 639.673, -0.31936, -6.57789, 182.693, 610.805, 0.299102005, 45, 3, 19, 4, -1, 5, 1250, 0, -1, 44,
     1, 9, 8, 10, 0.005473663, 0.049262971, 12, 45, 0, 0, 0, 0, 1, 0, 0],
    [225.086, 206.629, -1.66662, -1.78613, 93.7013, 226.394, 0.413885969, 16, 0, 6, 4, 1, 2, 308, 1, 0, 16, 0,
     2, 3, 3, 0, 0.021344421, 4, 16, 0, 0, 0, 1, 0, 1, 0],
    [246.126, 254.642, 2.58608, -2.25393, 42.181, 288.138, 0.14639166, 36, 2, 5, 1, -1, 2, 494, 0, -1, 18, 0,
     5, 4, 7, 0, 0.118536782, 4, 36, 0, 0, 0, 0, 1, 0, 0],
    [296.964, 210.356, -0.374064, -3.22592, 104.021, 239.275, 0.434734093, 17, 0, 10, 4, 0, 2, 316, 0, 0, 17,
     0, 1, 0, 1, 0, 0.009613443, 1, 17, 0, 0, 0, 1, 0, 0, 0],
    [229.052, 217.447, -1.04958, -2.00012, 71.7411, 225.845, 0.317656357, 15, 2, 6, 3, 0, 2, 331, 0, 0, 15, 0,
     7, 1, 4, 0, 0.097573079, 2, 15, 0, 0, 0, 1, 0, 1, 0],
    [287.078, 227.531, -2.96911, -1.764, 105.329, 274.392, 0.383863232, 19, 1, 8, 4, -2, 2, 354, 0, -2, 19, 0,
     0, 4, 4, 0, 0, 5, 19, 0, 0, 0, 1, 0, 0, 0],
    [180.042, 168.038, 1.1816, -1.65193, 49.4842, 190.315, 0.260012085, 21, 0, 6, 1, -1, 1, 212, 0, -1, 13, 0,
     0, 3, 1, 0, 0, 3, 21, 0, 0, 0, 0, 1, 0, 1],
    [273.063, 211.508, -3.38471, -1.01282, 106.494, 254.85, 0.417869335, 30, 0, 8, 4, -2, 2, 327, 0, -2, 18, 0,
     0, 3, 3, 0, 0, 5, 30, 0, 0, 0, 1, 0, 0, 0],
    [224.08, 254.25, -0.734363, -1.79637, 65.8791, 239.993, 0.274504256, 28, 2, 6, 2, 0, 2, 388, 0, 0, 16, 0,
     8, 2, 4, 0, 0.121434567, 2, 28, 0, 0, 0, 0, 0, 1, 0],
    [421.038, 317.663, 2.15131, -4.66218, 102.915, 353.567, 0.291076373, 41, 1, 10, 4, 0, 3, 740, 0, 0, 27, 0,
     1, 2, 3, 0, 0.009716757, 4, 41, 0, 0, 0, 1, 0, 0, 0],
    [294.949, 212.025, -0.290636, -2.30232, 103.926, 231.327, 0.449260138, 23, 0, 10, 3, -1, 2, 532, 0, -1, 17,
     0, 1, 0, 0, 0, 0.009622231, 1, 23, 0, 0, 0, 1, 0, 0, 0],
    [241.11, 234.92, 3.59308, -3.91814, 36.1633, 270.794, 0.133545426, 33, 0, 3, 2, -1, 2, 292, 0, -1, 18, 0,
     0, 3, 2, 0, 0, 3, 33, 0, 0, 0, 0, 1, 0, 0],
    [455.057, 439.584, -0.115239, -4.13379, 139.534, 424.644, 0.328590537, 47, 2, 14, 4, -1, 3, 833, 0, -1, 30,
     1, 5, 7, 6, 0.007166712, 0.03583356, 9, 47, 0, 0, 0, 1, 1, 0, 1],
    [389.027, 326.187, 1.35827, -4.99217, 103.549, 334.726, 0.309354517, 40, 4, 10, 4, 0, 4, 758, 0, 0, 24, 3,
     5, 0, 6, 0.028971791, 0.048286319, 2, 40, 0, 0, 0, 1, 0, 0, 0],
    [324.184, 339.594, 2.4134, -3.29994, 35.6466, 364.613, 0.097765576, 48, 4, 4, 1, 1, 4, 457, 1, 0, 24, 3, 4,
     4, 9, 0.084159499, 0.112212665, 4, 48, 0, 0, 0, 0, 0, 1, 0],
    [211.096, 218.652, -1.07108, -1.5625, 70.2669, 225.035, 0.312248761, 28, 2, 5, 3, 0, 2, 327, 0, 0, 15, 0,
     8, 1, 5, 0, 0.113851614, 2, 28, 0, 0, 0, 1, 0, 1, 0],
    [418.272, 490.639, 4.22882, -5.70397, 56.7318, 502.814, 0.112828601, 68, 7, 7, 1, 0, 3, 706, 0, 0, 30, 2,
     13, 10, 19, 0.035253597, 0.229148379, 7, 68, 0, 0, 0, 0, 0, 1, 0],
    [395.036, 389.6, 0.0290967, -4.62301, 129.945, 352.688, 0.368441796, 39, 2, 11, 5, -1, 3, 739, 0, -1, 30,
     2, 13, 10, 19, 0.015391127, 0.100042326, 6, 39, 0, 0, 0, 1, 1, 0, 0],
    [287.152, 309.435, 3.19902, -3.61089, 47.7272, 327.27, 0.145834326, 42, 1, 4, 2, -1, 3, 400, 0, -1, 21, 0,
     3, 6, 8, 0, 0.062857239, 4, 42, 0, 0, 0, 0, 1, 0, 0],
    [330.008, 255.536, 1.56879, -3.58297, 96.5352, 293.636, 0.328758054, 32, 0, 9, 4, -1, 2, 481, 0, -1, 21, 0,
     0, 2, 1, 0, 0, 5, 32, 0, 0, 0, 1, 1, 0, 0],
    [357.077, 340.582, 3.94696, -5.88537, 51.3057, 362.671, 0.141466232, 41, 0, 6, 1, -1, 3, 506, 0, -1, 25, 0,
     0, 5, 3, 0, 0, 5, 41, 0, 0, 0, 0, 1, 0, 0],
    [236.004, 195.12, -0.63179, -1.57015, 88.5676, 215.095, 0.411760385, 22, 0, 10, 2, 0, 1, 419, 0, 0, 14, 0,
     2, 3, 2, 0, 0.022581621, 2, 22, 0, 0, 0, 1, 0, 0, 1],
    [334.099, 339.557, 2.54711, -2.61468, 69.8134, 347.392, 0.200964328, 41, 3, 8, 2, -1, 3, 530, 0, -1, 23, 1,
     4, 5, 7, 0.014323898, 0.057295591, 5, 41, 0, 0, 0, 0, 1, 0, 0],
    [347.094, 360.758, -0.968932, -3.36359, 90.6857, 347.4, 0.261041163, 41, 3, 9, 4, -1, 3, 600, 0, -1, 24, 1,
     5, 4, 5, 0.011027097, 0.055135484, 5, 41, 0, 0, 0, 1, 1, 0, 0],
    [411.185, 408.773, 4.59879, -5.69053, 63.6476, 445.986, 0.142712103, 56, 2, 5, 3, -1, 3, 590, 0, -1, 30, 0,
     0, 10, 7, 0, 0, 8, 56, 0, 0, 0, 0, 1, 2, 0],
    [383.036, 363.064, 0.114936, -3.75558, 117.888, 348.187, 0.338576684, 38, 2, 11, 4, -1, 3, 669, 0, -1, 25,
     1, 5, 4, 4, 0.008482628, 0.042413138, 6, 38, 0, 0, 0, 1, 1, 0, 0],
    [612.232, 635.464, 2.49889, -6.47166, 154.398, 633.095, 0.243878091, 80, 4, 14, 6, -2, 4, 1150, 0, -2, 44,
     0, 8, 11, 12, 0, 0.051814143, 10, 80, 0, 0, 0, 1, 0, 2, 0],
    [364.109, 327.291, 2.93964, -4.18936, 95.8205, 376.291, 0.254644677, 45, 0, 9, 4, -1, 2, 528, 0, -1, 25, 0,
     0, 5, 4, 0, 0, 8, 45, 0, 0, 0, 1, 1, 0, 0],
    [252.116, 250.742, 0.328501, -2.50416, 71.5098, 289.906, 0.246665471, 33, 0, 4, 3, 0, 1, 296, 0, 0, 17, 0,
     0, 7, 5, 0, 0, 8, 33, 0, 0, 0, 0, 0, 0, 0],
    [308.152, 322.967, 3.99071, -3.69545, 34.2353, 344.527, 0.09936899, 43, 0, 4, 0, -1, 3, 389, 0, -1, 23, 0,
     3, 4, 5, 0, 0.087628851, 5, 43, 0, 0, 0, 0, 0, 0, 0],
    [320.126, 343.548, 2.09457, -3.43291, 74.3909, 345.474, 0.215329952, 43, 0, 8, 2, -1, 2, 486, 0, -1, 23, 0,
     2, 9, 7, 0, 0.026885009, 6, 43, 0, 0, 0, 0, 1, 0, 0],
    [358.156, 393.556, 0.184695, -4.53057, 100.563, 398.088, 0.252615, 50, 2, 10, 5, -2, 1, 519, 1, -3, 24, 0,
     3, 13, 11, 0, 0.029832046, 12, 50, 0, 0, 0, 1, 2, 0, 0],
    [422.162, 392.804, 4.8734, -6.44764, 78.7578, 448.687, 0.175529489, 53, 0, 5, 2, -1, 4, 520, 0, -1, 30, 0,
     0, 6, 6, 0, 0, 8, 53, 0, 0, 0, 0, 0, 1, 0],
    [367.039, 354.723, -1.06422, -3.98501, 90.6857, 341.498, 0.265552653, 50, 3, 9, 4, -1, 3, 606, 0, -1,
     24, 1,
     5, 3, 4, 0.011027097, 0.055135484, 5, 38, 0, 0, 0, 1, 1, 0, 0],
    [454.171, 400.745, -0.189174, -4.67831, 164.081, 442.541, 0.370770166, 55, 1, 12, 7, -2, 3, 704, 0, -2, 33, 0,
     0, 8, 5, 0, 0, 10, 55, 0, 0, 0, 2, 2, 0, 0]
    ]

for e in inputs:
    assert len(e) == 32, e

outputs = [1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           1,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0,
           0

           ]

test_inputs = [
    [446.207, 432.381, 4.31897, -5.17769, 105.423, 474.81, 0.222031971, 59, 0, 8, 3, -2, 4, 656, 0, -2, 33, 0, 0, 8, 7,
     0, 0, 8, 59, 0, 0, 0, 0, 1, 1, 0],
    [424.246, 457.587, 2.50836, -2.44788, 97.8024, 485.291, 0.201533513, 66, 8, 9, 4, -1, 2, 656, 0, -1, 30, 2, 8, 13,
     17, 0.020449396, 0.081797584, 11, 66, 0, 0, 0, 0, 1, 3, 0],
    [435.227, 427.718, 5.02817, -5.79391, 93.4272, 490.087, 0.190633908, 61, 1, 8, 2, -2, 3, 608, 0, -2, 32, 0, 0, 11,
     9, 0, 0, 11, 61, 0, 0, 0, 0, 1, 0, 0],
    [440.16, 404.725, 5.2218, -6.63067, 95.6163, 441.5, 0.216571461, 53, 0, 8, 2, -2, 5, 660, 0, -2, 33, 0, 0, 4, 3, 0,
     0, 7, 53, 0, 0, 0, 0, 1, 0, 0],
    [302.011, 280.171, 3.22154, -3.71515, 49.9466, 299.874, 0.166558621, 31, 0, 6, 1, -1, 1, 370, 0, -1, 19, 0, 0, 7, 3,
     0, 0, 6, 31, 0, 0, 0, 0, 1, 0, 0],
    [179.095, 187.264, 1.96378, -2.31502, 30.6239, 218.055, 0.140441173, 26, 0, 3, 1, 0, 1, 162, 0, 0, 13, 0, 0, 4, 3,
     0, 0, 4, 26, 0, 0, 0, 0, 0, 0, 1],
    [152.016, 138.206, -0.235168, -2.60213, 45.1179, 141.892, 0.317973529, 14, 0, 4, 2, 1, 2, 190, 1, 0, 10, 0, 2, 0, 0,
     0, 0.044328304, 0, 14, 0, 0, 0, 0, 0, 0, 0],
    [385.248, 421.067, 1.52703, -1.91196, 55.8225, 441.722, 0.126374733, 59, 0, 7, 0, 1, 4, 529, 1, 0, 28, 1, 12, 4, 15,
     0.017913924, 0.214967083, 6, 59, 0, 0, 0, 0, 0, 0, 0],
    [454.283, 514.207, 5.27969, -4.98191, 51.6173, 549.866, 0.093872507, 71, 1, 6, 0, 1, 2, 606, 1, 0, 33, 0, 0, 15, 14,
     0, 0, 14, 71, 0, 0, 0, 0, 0, 0, 0],
    [426.217, 434.885, 4.94765, -6.71307, 76.1362, 470.385, 0.161859328, 58, 0, 6, 1, -1, 5, 624, 0, -1, 32, 0, 5, 4, 8,
     0, 0.065671783, 6, 58, 0, 0, 0, 0, 0, 0, 0],
    [356.088, 353.613, 4.01376, -5.27717, 44.4057, 363.416, 0.122189722, 42, 0, 6, 1, -2, 3, 616, 0, -2, 25, 0, 3, 5, 3,
     0, 0.067558894, 4, 42, 0, 0, 0, 0, 1, 0, 0],
    [331.063, 305.577, 1.38647, -3.6079, 80.726, 313.125, 0.257807585, 36, 0, 8, 2, 0, 3, 611, 0, 0, 23, 0, 2, 2, 1, 0,
     0.024775165, 3, 36, 0, 0, 0, 0, 0, 1, 0],
    [396.045, 396.192, 0.461149, -3.3527, 91.7535, 379.303, 0.241900275, 42, 2, 11, 2, -1, 3, 680, 0, -1, 26, 1, 5, 6,
     6, 0.010898767, 0.054493834, 8, 42, 0, 0, 0, 0, 1, 0, 1],
    [378.902, 252.54, 0.772575, -4.55218, 102.975, 281.059, 0.366382148, 28, 1, 10, 4, 0, 2, 571, 0, 0, 20, 0, 1, 1, 2,
     0, 0.009711095, 2, 28, 0, 0, 0, 1, 0, 0, 0],
    [645.142, 639.673, -0.31936, -6.57789, 182.693, 610.805, 0.299102005, 45, 3, 19, 4, -1, 5, 1250, 0, -1, 44, 1, 9, 8,
     10, 0.005473663, 0.049262971, 12, 45, 0, 0, 0, 0, 1, 0, 0],
    [225.086, 206.629, -1.66662, -1.78613, 93.7013, 226.394, 0.413885969, 16, 0, 6, 4, 1, 2, 308, 1, 0, 16, 0, 2, 3, 3,
     0, 0.021344421, 4, 16, 0, 0, 0, 1, 0, 1, 0],
    [246.126, 254.642, 2.58608, -2.25393, 42.181, 288.138, 0.14639166, 36, 2, 5, 1, -1, 2, 494, 0, -1, 18, 0, 5, 4, 7,
     0, 0.118536782, 4, 36, 0, 0, 0, 0, 1, 0, 0],
    [296.964, 210.356, -0.374064, -3.22592, 104.021, 239.275, 0.434734093, 17, 0, 10, 4, 0, 2, 316, 0, 0, 17, 0, 1, 0,
     1, 0, 0.009613443, 1, 17, 0, 0, 0, 1, 0, 0, 0],
    [229.052, 217.447, -1.04958, -2.00012, 71.7411, 225.845, 0.317656357, 15, 2, 6, 3, 0, 2, 331, 0, 0, 15, 0, 7, 1, 4,
     0, 0.097573079, 2, 15, 0, 0, 0, 1, 0, 1, 0],
    [287.078, 227.531, -2.96911, -1.764, 105.329, 274.392, 0.383863232, 19, 1, 8, 4, -2, 2, 354, 0, -2, 19, 0, 0, 4, 4,
     0, 0, 5, 19, 0, 0, 0, 1, 0, 0, 0],
    [180.042, 168.038, 1.1816, -1.65193, 49.4842, 190.315, 0.260012085, 21, 0, 6, 1, -1, 1, 212, 0, -1, 13, 0, 0, 3, 1,
     0, 0, 3, 21, 0, 0, 0, 0, 1, 0, 1],
    [273.063, 211.508, -3.38471, -1.01282, 106.494, 254.85, 0.417869335, 30, 0, 8, 4, -2, 2, 327, 0, -2, 18, 0, 0, 3, 3,
     0, 0, 5, 30, 0, 0, 0, 1, 0, 0, 0],
    [224.08, 254.25, -0.734363, -1.79637, 65.8791, 239.993, 0.274504256, 28, 2, 6, 2, 0, 2, 388, 0, 0, 16, 0, 8, 2, 4,
     0, 0.121434567, 2, 28, 0, 0, 0, 0, 0, 1, 0],
    [421.038, 317.663, 2.15131, -4.66218, 102.915, 353.567, 0.291076373, 41, 1, 10, 4, 0, 3, 740, 0, 0, 27, 0, 1, 2, 3,
     0, 0.009716757, 4, 41, 0, 0, 0, 1, 0, 0, 0],
    [294.949, 212.025, -0.290636, -2.30232, 103.926, 231.327, 0.449260138, 23, 0, 10, 3, -1, 2, 532, 0, -1, 17, 0, 1, 0,
     0, 0, 0.009622231, 1, 23, 0, 0, 0, 1, 0, 0, 0],
    [241.11, 234.92, 3.59308, -3.91814, 36.1633, 270.794, 0.133545426, 33, 0, 3, 2, -1, 2, 292, 0, -1, 18, 0, 0, 3, 2,
     0, 0, 3, 33, 0, 0, 0, 0, 1, 0, 0]
    ]
test_outputs = [0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                ]


def get_data():
    return inputs, outputs


def sd(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return msd_list(a, b)

    return (a - b) ** 2


def msd_list(a, b):
    assert len(a) == len(b), 'Target output length doesnt match predictions'
    return len(a) / sum([sd(*x) for x in zip(a, b)])


def create_config(conf_file):
    # have everything set to default settings for now, can technically change the config file.
    return neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        conf_file
        )


def fitness(genomes, conf):
    train_input, train_output = get_data()

    for gid, genome in genomes:
        genome.fitness = len(train_input)
        net = neat.nn.FeedForwardNetwork.create(genome, conf)

        for xi, xo in zip(train_input, train_output):
            pred = net.activate(xi)
            genome.fitness -= sd(pred[0], xo)
            # print('fitness of', gid, 'is', sd(pred[0], xo))


def run(epochs):
    conf_filepath = './configs/flappy_ai.config'

    # make a config file
    conf = create_config(conf_filepath)

    # make a new population
    pop = neat.Population(conf)

    # make statistical reporters
    stats = neat.StatisticsReporter()
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(stats)

    # make a checkpointer to save progress every 10 epochs
    pop.add_reporter(neat.Checkpointer(10))

    # find the winner
    winner = pop.run(fitness, epochs)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, conf)

    node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    visualize.draw_net(conf, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


run(3000)

# p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
# p.run(fitness, 10)
