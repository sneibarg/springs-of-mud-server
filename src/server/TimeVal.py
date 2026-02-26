from __future__ import annotations
from dataclasses import dataclass

import time


@dataclass(frozen=True)
class TimeVal:
    """C-compatible timeval: seconds + microseconds since the Unix epoch (UTC)."""
    tv_sec: int  # time_t
    tv_usec: int  # suseconds_t (0..999_999)


def gettimeofday() -> TimeVal:
    """
    Python equivalent of C gettimeofday(&tv, NULL).

    Returns:
        TimeVal(tv_sec, tv_usec) where:
          - tv_sec  = whole seconds since Unix epoch (1970-01-01T00:00:00Z)
          - tv_usec = remaining microseconds (0..999_999)

    Notes:
        - Uses a wall-clock time source (not monotonic), like gettimeofday().
        - No timezone conversion; epoch is UTC by definition.
    """
    ns = time.time_ns()
    sec, nsec = divmod(ns, 1_000_000_000)
    usec = nsec // 1_000
    return TimeVal(int(sec), int(usec))


def stall_until_last_time(last_time: TimeVal, pulse_per_second: int) -> None:
    """
    - Computes (last_time - now) + (1/PULSE_PER_SECOND) in microsecond resolution.
    - If the result is positive, sleeps for that duration (like select(..., &stall_time)).
    """
    now_time = gettimeofday()
    usec_delta = (int(last_time.tv_usec) - int(now_time.tv_usec)) + (1_000_000 // int(pulse_per_second))
    sec_delta  = (int(last_time.tv_sec)  - int(now_time.tv_sec))

    while usec_delta < 0:
        usec_delta += 1_000_000
        sec_delta  -= 1

    while usec_delta >= 1_000_000:
        usec_delta -= 1_000_000
        sec_delta  += 1

    if sec_delta > 0 or (sec_delta == 0 and usec_delta > 0):
        sleep_seconds = sec_delta + (usec_delta / 1_000_000.0)
        time.sleep(sleep_seconds)
