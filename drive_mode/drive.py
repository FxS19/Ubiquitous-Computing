value = {
    "max_speed": 46,
    "speed_table": {
        # LL L C R RR
        # 2  1 0 1 2
        # left and right is swapped automatically
        # Values for the right half of the sensor

        #   0           1              2
        1: [(0.5,0.5),  (0.6,0.35),    (0.75,0.1)],  #Bar width: 1
        #   0,1         1,2
        2: [(0.5,0.35),  (0.6,-0.15)],                # Bar width: 2
        #   1,0,1       0,1,2
        3: [(0.5,0.5),  (0.7, -0.55)],               # Bar width: 3 #corner
        #   1,0,1,2
        4: [(0.5,-0.5)],                            # Bar width: 4 #corner
        #   2,1,0,1,2
        5: [(0,0)]                                  # Bar width: 5
    },
	"outside_line_speed": (0.7, -0.5)
}
