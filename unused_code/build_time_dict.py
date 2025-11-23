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


def compute_transition_matrix(target_moves, ip, port):
    """
    Computes transition times:
        for each X in all moves
        to each Y in target_moves
    """
    matrix = {}
    all_moves = list(moves.keys())

    for x in all_moves:
        matrix[x] = {}
        for y in target_moves:
            matrix[x][y] = measure_transition(x, y, ip, port)
            time.sleep(2)     # allow robot to rest joints

    return matrix


def measure_transition(x, y, ip, port):
    """
    Measures the real time of executing Y *immediately after* X.
    """
    if x not in moves or y not in moves:
        print("[ERROR] Move not found:", x, y)
        return None

    print("\n[TRANSITION] %s -> %s" % (x, y))

    # 1. Move X
    try:
        print("  Executing X:", x)
        moves[x](ip, port)
    except Exception as e:
        print("  ERROR executing X:", e)
        return None

    time.sleep(1.0)   # small stabilization wait

    # 2. Measure Y
    try:
        print("  Measuring Y:", y)
        start = time.time()
        moves[y](ip, port)
        end = time.time()
    except Exception as e:
        print("  ERROR executing Y:", e)
        return None

    duration = end - start
    print("  Result: %.2f seconds" % duration)
    return duration
