"""Run a Python script and record every file it opens or passes to a subprocess.

Usage: python3 code/python/trace_raw_reads.py <log_file> <script.py> [args...]

Appends "<script>\t<path>" lines to <log_file>. Used on 2026-11-09 to find which raw
files the pipeline reads (docs/2026-11-09/data-bundle-unused-raw.md). pyarrow opens
parquet files in C++, so those reads are not seen; check them in the code.
"""
import sys, os, runpy, atexit
log_path, script, *args = sys.argv[1:]
fd = os.open(log_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT)   # opened before the hook is installed
seen = []
def hook(event, a):
    if event == "open" and a and isinstance(a[0], (str, bytes, os.PathLike)):
        seen.append(os.fsdecode(a[0]))
    elif event == "subprocess.Popen":
        seen.append("SUBPROCESS " + " ".join(map(str, a[1] if isinstance(a[1], (list, tuple)) else [a[1]])))
@atexit.register
def dump():
    os.write(fd, ("".join(f"{script}\t{p}\n" for p in dict.fromkeys(seen))).encode())
sys.addaudithook(hook)
sys.argv = [script, *args]
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
runpy.run_path(script, run_name="__main__")
