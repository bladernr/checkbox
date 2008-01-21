signal_description_table = {
    'SIGHUP':  'Hangup detected on controlling terminal or death of controlling process',
    'SIGINT':  'Interrupt from keyboard',
    'SIGQUIT': 'Quit from keyboard',
    'SIGILL':  'Illegal Instruction',
    'SIGABRT': 'Abort signal from abort(3)',
    'SIGFPE':  'Floating point exception',
    'SIGKILL': 'Kill signal',
    'SIGSEGV': 'Invalid memory reference',
    'SIGPIPE': 'Broken pipe: write to pipe with no readers',
    'SIGALRM': 'Timer signal from alarm(2)',
    'SIGTERM': 'Termination signal',
    'SIGUSR1': 'User-defined signal 1',
    'SIGUSR2': 'User-defined signal 2',
    'SIGCHLD': 'Child stopped or terminated',
    'SIGCONT': 'Continue if stopped',
    'SIGSTOP': 'Stop process',
    'SIGTSTP': 'Stop typed at tty',
    'SIGTTIN': 'tty input for background process',
    'SIGTTOU': 'tty output for background process'}

signal_name_table = {
    1: 'SIGHUP',
    2: 'SIGINT',
    3: 'SIGQUIT',
    4: 'SIGILL',
    6: 'SIGABRT',
    8: 'SIGFPE',
    9: 'SIGKILL',
    10: 'SIGUSR1',
    11: 'SIGSEGV',
    12: 'SIGUSR2',
    13: 'SIGPIPE',
    14: 'SIGALRM',
    15: 'SIGTERM',
    16: 'SIGUSR1',
    21: 'SIGTTIN',
    22: 'SIGTTOU',
    23: 'SIGSTOP',
    24: 'SIGTSTP',
    25: 'SIGCONT',
    26: 'SIGTTIN',
    27: 'SIGTTOU',
    30: 'SIGUSR1',
    31: 'SIGUSR2'}

def signal_to_name(signal):
    """Convert a signal number to its string representation.

    Keyword arguments:
    signal -- number of the signal as returned by wait
    """

    if signal_name_table.has_key(signal):
        return signal_name_table[signal]
    return "UNKNOWN"

def signal_to_description(signal):
    """Convert a signal number to its corresponding description.

    Keyword arguments:
    signal -- number of the signal as returned by wait
    """

    name = convert_to_name(signal)
    if signal_description_table.has_key(name):
        return signal_description_table[name]
    return "Unknown signal"