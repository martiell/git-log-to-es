from datetime import tzinfo, timedelta, datetime

class LogParser:

    def __init__(self, log):
        self.log = log
        self.lookahead = None

    def readline(self):
        tmp = self.log.readline()
        if tmp and not self.lookahead:
            self.lookahead = self.log.readline()
        line = self.lookahead
        self.lookahead = tmp
        if line and line[-1] == '\n':
            return line[:-1]
        return line

    def parseSHA(self, line):
        return line.split(' ')[1]

    def readSHA(self):
        return self.parseSHA(self.readline())

    def readAction(self, line):
        name_start = line.find(' ')
        mail_start = line.find('<')
        mail_end = line.find('>')
        name = line[name_start + 1:mail_start - 1]
        mail = line[mail_start + 1:mail_end]
        time = line[mail_end + 2:]
        splits = time.split(' ')
        seconds = long(splits[0])
        timezone = splits[1]
        tz = GitOffset(timezone)
        timestamp = datetime.fromtimestamp(seconds, tz)
        return {
            "name": name,
            "mail": mail,
            "time": timestamp.isoformat()
        }

    def readDelta(self):
        line = self.readline()
        adds = 0
        dels = 0
        while line:
            splits = line.split('\t')
            if splits[0] != '-':
                adds += int(splits[0])
            if splits[1] != '-':
                dels += int(splits[1])
            line = self.readline()
        return adds - dels

    def readCommit(self):
        hash = self.readSHA()
        tree = self.readSHA()
        parents = []
        line = self.readline()
        while line.startswith("parent"):
            parents.append(self.parseSHA(line))
            line = self.readline()
        author = self.readAction(line)
        line = self.readline()
        committer = self.readAction(line)
        message = ''
        self.readline()
        line = self.readline()
        while line:
            message += line[4:] + '\n'
            line = self.readline()
        commit = {
            'hash': hash,
            'parents': parents,
            'author': author,
            'committer': committer,
            'message': message
        }
        if self.lookahead.find('\t') >= 0:
            commit['delta'] = self.readDelta()
        return commit

    def readCommits(self, importer):
        commit = self.readCommit()
        importer.commit(commit)
        while self.lookahead:
            commit = self.readCommit()
            importer.commit(commit)


class GitOffset(tzinfo):

    def __init__(self, offset):
        minutes = int(offset[:-2]) * 60 + int(offset[-2:])
        self.minutes = minutes
        self.__offset = timedelta(minutes = minutes)

    def __repr__(self):
        return ('{:+03d}'.format(self.minutes / 60) +
            '{:02d}'.format(self.minutes % 60))

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        raise NotImplementedError

    def dst(self, dt):
        return timedelta(0)
