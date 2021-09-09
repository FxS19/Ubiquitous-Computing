{
    "max_speed": 55,
    "speed_table": {
        # LL L C R RR
        # 2  1 0 1 2
        # left and right is swapped automatically

        #   0           1           2
        1: [(0.6,0.6),  (0.2,0.6),    (0,0.7)],    # Bar width: 1
        #   0,1         1,2
        2: [(0.5,0.7),  (-0.6,0.6)],                # Bar width: 2
        #   1,0,1       0,1,2
        3: [(0.6,0.6),  (-0.6,0.5)],                  # Bar width: 3 #corner
        #   1,0,1,2
        4: [(-0.6,0.5)],                              # Bar width: 4 #corner
        #   2,1,0,1,2
        5: [(0,0)]                                  # Bar width: 5 #corner
    }
}