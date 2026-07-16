'''Weekly deployment window problem.

We deploy services throughout the week, but deployments are only allowed during scheduled deployment windows and must be 
blocked during freeze windows. Time is represented as minute_of_week from 0 to 10079, where 0 is Monday 00:00 and 10079 is 
Sunday 23:59. Each window is half-open, meaning [start, end) includes start but excludes end.
For Part 1, each CSV row is start,end,type, where type is either allowed or freeze. A minute is deployable only if it falls 
inside at least one allowed window and inside no freeze windows. Return the sorted list of continuous deployable intervals 
as a 2D integer array.
In Part 2, deployment windows may come from teams in different time zones, so each CSV row becomes start, end, type, 
timezone_offset_minutes, where start and end are local minute_of_week values. Convert each row to UTC using 
utc = local - timezone_offset_minutes, then compute deployable windows using the same rule: inside at least one allowed window 
and zero freeze windows. The first input row gives utc_now,lead_time_minutes,min_continuous_minutes,k. A valid deployment start 
must be at or after utc_now + lead_time_minutes, must remain continuously deployable for at least min_continuous_minutes, and 
must not go beyond the end of the week. Return the next k valid deployable UTC intervals, or fewer if not enough exist.
'''

import os

WEEK = 10080


def parse(row):
    return [x.strip() for x in row.split(",")]


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def split_week_window(start, end):
    """Split a weekly half-open interval into non-wrapping intervals."""
    if start == end:
        return []

    if start < end:
        return [[start, end]]

    return [[start, WEEK], [0, end]]


def local_to_utc_windows(local_start, local_end, offset):
    """Convert a local weekly interval to UTC and split if it wraps."""
    # local = utc + offset
    # utc = local - offset

    if local_start == local_end:
        return []

    if local_start < local_end:
        duration = local_end - local_start
    else:
        duration = WEEK - local_start + local_end

    if duration >= WEEK:
        return [[0, WEEK]]

    utc_start = (local_start - offset) % WEEK
    utc_end = utc_start + duration

    if utc_end <= WEEK:
        return [[utc_start, utc_end]]

    return [[utc_start, WEEK], [0, utc_end - WEEK]]


def add_interval(diff, start, end):
    """Apply one interval to a difference array."""
    start = max(0, min(WEEK, start))
    end = max(0, min(WEEK, end))

    if start >= end:
        return

    diff[start] += 1
    diff[end] -= 1


def compute_deployable(allowed, frozen):
    """Return sorted deployable intervals after subtracting frozen windows."""
    allowed_diff = [0] * (WEEK + 1)
    frozen_diff = [0] * (WEEK + 1)

    for start, end in allowed:
        add_interval(allowed_diff, start, end)

    for start, end in frozen:
        add_interval(frozen_diff, start, end)

    result = []
    allowed_count = 0
    frozen_count = 0
    open_start = None

    for minute in range(WEEK):
        allowed_count += allowed_diff[minute]
        frozen_count += frozen_diff[minute]

        deployable = allowed_count > 0 and frozen_count == 0

        if deployable and open_start is None:
            open_start = minute

        if not deployable and open_start is not None:
            result.append([open_start, minute])
            open_start = None

    if open_start is not None:
        result.append([open_start, WEEK])

    return result


def solve_part1(inputCsv):
    allowed = []
    frozen = []

    for row in inputCsv:
        cols = parse(row)

        if len(cols) < 3:
            continue

        if not is_int(cols[0]) or not is_int(cols[1]):
            continue

        start = int(cols[0])
        end = int(cols[1])
        window_type = cols[2].lower()

        windows = split_week_window(start, end)

        if window_type == "allowed":
            allowed.extend(windows)
        elif window_type == "freeze":
            frozen.extend(windows)

    return compute_deployable(allowed, frozen)


def solve_part2(inputCsv):
    config_index = 0

    while config_index < len(inputCsv):
        cols = parse(inputCsv[config_index])

        if len(cols) >= 4 and all(is_int(cols[i]) for i in range(4)):
            break

        config_index += 1

    if config_index == len(inputCsv):
        return []

    utc_now, lead_time, min_duration, k = map(int, parse(inputCsv[config_index]))

    if k <= 0:
        return []

    allowed = []
    frozen = []

    for row in inputCsv[config_index + 1:]:
        cols = parse(row)

        if len(cols) < 4:
            continue

        if not is_int(cols[0]) or not is_int(cols[1]) or not is_int(cols[3]):
            continue

        local_start = int(cols[0])
        local_end = int(cols[1])
        window_type = cols[2].lower()
        offset = int(cols[3])

        utc_windows = local_to_utc_windows(local_start, local_end, offset)

        if window_type == "allowed":
            allowed.extend(utc_windows)
        elif window_type == "freeze":
            frozen.extend(utc_windows)

    deployable = compute_deployable(allowed, frozen)

    earliest_start = utc_now + lead_time

    if earliest_start >= WEEK:
        return []

    answer = []

    for start, end in deployable:
        valid_start = max(start, earliest_start)

        if valid_start + min_duration <= end:
            answer.append([valid_start, end])

            if len(answer) == k:
                break

    return answer


def findDeployableWindows(part, inputCsv):
    part = part.strip().lower()

    if part == "part1":
        return solve_part1(inputCsv)

    if part == "part2":
        return solve_part2(inputCsv)

    return []


if __name__ == "__main__":
    fptr = open(os.environ["OUTPUT_PATH"], "w")

    part = input()

    inputCsv_count = int(input().strip())

    inputCsv = []

    for _ in range(inputCsv_count):
        inputCsv_item = input()
        inputCsv.append(inputCsv_item)

    result = findDeployableWindows(part, inputCsv)

    fptr.write("\n".join([" ".join(map(str, x)) for x in result]))
    fptr.write("\n")

    fptr.close()
