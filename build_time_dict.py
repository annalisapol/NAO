def measure_single_move(move_name):
    posture.goToPosture("StandInit", 0.5)
    time.sleep(0.3)

    print("\nMeasuring:", move_name)
    start = time.time()
    moves[move_name](ip, port)
    end = time.time()

    duration = round(end - start, 2)
    print("[RESULT] {} takes {} seconds".format(move_name, duration))
    return duration

def build_move_time_dict():
    move_time = {}

    for move in sorted(moves.keys()):
        t = measure_single_move(move)
        move_time[move] = t

    print("\n\n===== MOVE_TIME DICTIONARY =====")
    for k, v in move_time.items():
        print('"{}": {},'.format(k, v))

    return move_time


build_move_time_dict()


