class Positions:
    # A1 B C D E F G H1
    # A2 x x x x x x H2
    # A3 x x x x x x H3
    # A4 x x x x x x H4
    # A5 x x x x x x H5
    # A6 x x x x x x H6
    # A7 x x x x x x H7
    # A8 B C D E F G H8
    
    joint1_table = [[310, 340, 0, 0, 370, 363, 345, 338],
                    [410, 425, 0, 0, 452, 450, 432, 410],
                    [490, 510, 0, 0, 535, 536, 515, 498],
                    [570, 585, 0, 0, 615, 611, 600, 587],
                    [650, 665, 0, 0, 696, 705, 688, 668],
                    [715, 735, 0, 0, 790, 790, 782, 765],
                    [790, 810, 0, 0, 880, 889, 893, 880],
                    [860, 890, 0, 0, 974, 990, 998, 1004]]

    joint2_table = [[987, 890, 0, 0, 662, 647, 597, 517],
                    [880, 795, 0, 0, 620, 562, 513, 475],
                    [805, 720, 0, 0, 540, 478, 435, 388],
                    [730, 655, 0, 0, 465, 404, 355, 303],
                    [665, 585, 0, 0, 397, 334, 278, 236],
                    [615, 530, 0, 0, 335, 269, 214, 160],
                    [570, 490, 0, 0, 278, 210, 145, 90],
                    [530, 445, 0, 0, 194, 160, 95, 1]]


    joint1_table_p = [[310, 0, 0, 0, 0, 0, 0, 338],
                     [410, 0, 0, 0, 0, 0, 0, 0],
                     [490, 0, 0, 0, 0, 0, 0, 0],
                     [560, 0, 0, 0, 0, 0, 0, 0],
                     [620, 0, 0, 0, 0, 0, 0, 0],
                     [700, 0, 0, 0, 0, 0, 0, 0],
                     [770, 0, 0, 0, 0, 0, 0, 0],
                     [860, 0, 0, 0, 0, 0, 0, 1004]]

    joint2_table_p = [[987, 0, 0, 0, 0, 0, 0, 528],
                     [880, 0, 0, 0, 0, 0, 0, 0],
                     [805, 0, 0, 0, 0, 0, 0, 0],
                     [740, 0, 0, 0, 0, 0, 0, 0],
                     [702, 0, 0, 0, 0, 0, 0, 0],
                     [642, 0, 0, 0, 0, 0, 0, 0],
                     [607, 0, 0, 0, 0, 0, 0, 0],
                     [567, 0, 0, 0, 0, 0, 0, 1]]

    # Higher offset is for when magnet is too close to ground
    height_offset = [[0, 0, 0, 0, 0, 0, 0, -2],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, -6]]



    kill_b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    kill_w = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    kill_b_joint_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    kill_b_joint_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    kill_w_joint_1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    kill_w_joint_2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
