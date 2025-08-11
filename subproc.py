import subprocess

def run(cmd, max_minutes = 6000):
    import time
    p = subprocess.Popen(cmd ,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         close_fds=True)


    (file_stdin, file_stdout, file_stderr) = (p.stdin, p.stdout, p.stderr)

    t = 0
    r = ''
    e = ''
    while t < 60*max_minutes and p.poll() is None:
        time.sleep(1)  # (comment 1)
        t += 1
        r += file_stdout.read()
        e += file_stderr.read()
    r += file_stdout.read()
    e += file_stderr.read()

    
    file_stdin.close()
    #lines = file_stdout.read()
    lines_stderr = file_stderr.read()
    exit_code = file_stdout.close()
    
    file_stdout.close()
    file_stderr.close()

    return (r, e, exit_code)
