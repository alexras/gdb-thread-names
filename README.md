# About This Script

This script can be used within GDB to set thread names by extracting them from
`/proc` in situations where `prctl(PR_SET_NAME, ...)` and similar methods are
not being read properly by GDB.

# Requirements

A (recent) version of GDB that was compiled with `--with-python`.

# Installation

To install this script, add the following to `~/.gdbinit`:

```
python
import sys
sys.path.insert(0, '/path/to/gdb-thread-names')
from gdb_thread_names import get_thread_names
end
```

# Usage

While in GDB, just type

`python get_thread_names()`

It will print the threads for which it was able to successfully find names.

Subsequent calls to `info threads` and similar commands will show correct
thread names.
