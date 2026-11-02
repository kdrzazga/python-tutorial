"""Take desktop screenshots at a fixed frequency.

Examples:
    python auto_screenshots.py                      # 2 shots/s, full primary monitor, until Ctrl+C
    python auto_screenshots.py --fps 10 --duration 30
    python auto_screenshots.py --interval 5 --count 100
    python auto_screenshots.py --region 267 207 1117 765 --fps 25 --delay 3

Requires: pip install mss
"""
import argparse
import os
import time
from datetime import datetime

import mss
import mss.tools


def parse_args():
    parser = argparse.ArgumentParser(description="Take screenshots with a given frequency.")
    timing = parser.add_mutually_exclusive_group()
    timing.add_argument("--fps", type=float, help="screenshots per second (default 2)")
    timing.add_argument("--interval", type=float, help="seconds between screenshots")
    parser.add_argument("--count", type=int, help="stop after this many screenshots")
    parser.add_argument("--duration", type=float, help="stop after this many seconds")
    parser.add_argument("--delay", type=float, default=0, help="seconds to wait before the first shot")
    parser.add_argument("--monitor", type=int, default=1, help="1 = primary, 2.. = others, 0 = all monitors combined")
    parser.add_argument("--region", type=int, nargs=4, metavar=("X1", "Y1", "X2", "Y2"),
                        help="capture only this rectangle (screen coordinates)")
    parser.add_argument("--out", default="screenshots", help="output directory (default: screenshots)")
    return parser.parse_args()


def capture_area(screen_grabber, args):
    if args.region:
        x1, y1, x2, y2 = args.region
        return {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
    return screen_grabber.monitors[args.monitor]


def main():
    args = parse_args()
    seconds_between_shots = args.interval if args.interval else 1.0 / (args.fps or 2)

    session_dir = os.path.join(args.out, datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(session_dir, exist_ok=True)

    if args.delay:
        print(f"Starting in {args.delay} s...")
        time.sleep(args.delay)

    print(f"Saving to {session_dir} every {seconds_between_shots:.3f} s. Ctrl+C to stop.")
    shot_number = 0
    start_time = time.perf_counter()
    try:
        with mss.mss() as screen_grabber:
            area = capture_area(screen_grabber, args)
            while True:
                if args.count is not None and shot_number >= args.count:
                    break
                if args.duration is not None and time.perf_counter() - start_time >= args.duration:
                    break

                shot = screen_grabber.grab(area)
                shot_number += 1
                file_path = os.path.join(session_dir, f"{shot_number:05d}.png")
                mss.tools.to_png(shot.rgb, shot.size, output=file_path)

                # schedule against the start time so saving time doesn't accumulate drift
                next_shot_time = start_time + shot_number * seconds_between_shots
                wait_time = next_shot_time - time.perf_counter()
                if wait_time > 0:
                    time.sleep(wait_time)
                elif wait_time < -seconds_between_shots:
                    print(f"Falling behind by {-wait_time:.2f} s (frequency too high?)")
    except KeyboardInterrupt:
        pass

    print(f"Done: {shot_number} screenshots in {session_dir}")


if __name__ == "__main__":
    main()
