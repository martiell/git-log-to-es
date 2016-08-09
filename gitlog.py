from subprocess import Popen, PIPE

class GitLog:

    def log(self):
        args = [
            'git',
            'log',
            '--format=raw',
            '--numstat'
        ]
        proc = Popen(
            args,
            executable='/usr/bin/git',
            stdout=PIPE
        )
        return proc.stdout
