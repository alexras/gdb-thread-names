import re
import gdb
import os

def get_thread_names():
    thread_regex = re.compile("(\d+)\s+Thread\s+0x[0-9a-f]+\s+\(LWP (\d+)\)")
    # Capture the result of 'info threads' to a string
    thread_info = gdb.execute("info threads", False, True)

    # Store the currently-selected thread so that we can go back to it
    original_thread = gdb.selected_thread()

    if original_thread is not None:
        original_thread_num = original_thread.num
    else:
        original_thread_num = None

    for line in thread_info.split('\n'):
        line = line.strip()

        thread_match = thread_regex.search(line)

        if thread_match != None:
            thread_number = int(thread_match.group(1))
            thread_tid = int(thread_match.group(2))

            # Get a pointer to the current thread from GDB
            gdb.execute("thread %d" % (thread_number), False, True)
            current_thread = gdb.selected_thread()

            # Read this thread's stat file in /proc
            thread_stat_file = "/proc/%d/stat" % (thread_tid)

            if os.path.exists(thread_stat_file):
                with open(thread_stat_file, 'r') as fp:
                    stat_file_contents = fp.read()

                # Extract the thread's name from the stat file (it should be in
                # parens, after the thread ID itself)
                stat_file_regex = re.compile("^%d \((.*?)\)" % (thread_tid))

                stat_match = stat_file_regex.search(stat_file_contents)

                if stat_match is not None:
                    # Set the thread's name to the string extracted from stat
                    thread_name = stat_match.group(1)

                    print "Got thread name '%s' for thread %d (%d)" % (
                        thread_name, thread_number, thread_tid)
                    current_thread.name = thread_name

                else:
                    print "No thread name match for thread %d (%d)" % (
                        thread_number, thread_tid)

    # Switch back to original thread (if any)
    if original_thread_num != None:
        gdb.execute("thread %d" % (original_thread_num), False, True)
