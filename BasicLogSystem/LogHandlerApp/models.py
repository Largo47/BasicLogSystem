from django.db import models
import os


class IssueBin(models.Model):
    latest_issue = models.IntegerField(default=0)

    def CreateIssueFromFile(self, path):
        # Take a log from file and either create a new issue for it or add it to existing one
        raw_file = open(path, "r", errors="ignore").readlines()
        # Figured that missing a character here or there is not that big of a deal
        # considering the purpose of this is human analysis anyway
        filtered_log = self.filterLog(raw_file)
        raw_log = '\n'.join(filtered_log)  # tbc
        return 0

    @staticmethod
    def filterLog(log, tags=['rror:', 'arning:'], stack_tags=['failed.', 'allstack']):
        # Take log a list of lines and find the ones with relevant substrings.
        # If specific substring indicating start of a call stack found, put the rest of the file in
        ret = {}
        line_counter = 0
        stack_reached = False
        for line in log:
            line_counter += 1
            if stack_reached is True:
                ret[line_counter] = line
                continue
            for tag in tags:
                if tag in line:
                    ret[line_counter] = line
                    break
            for tag in stack_tags:
                if tag in line:
                    ret[line_counter] = line
                    stack_reached = True
                    break
        return ret


class Issue(models.Model):
    project = models.ForeignKey(IssueBin, on_delete=models.CASCADE)
    STATUS_OPTIONS = {
        "Open": "Open",
        "In progress": "In progress",
        "Resolved": "Resolved",
        "Suspended": "Suspended"
    }
    status = models.CharField(choices=STATUS_OPTIONS, default="Open")   # We'll see if that works

    @staticmethod
    def retRelatedIssue(log, IssueBinId = 1):
        allLogs = Log.objects.all()
        for record in allLogs:
            if record.log_raw == log:
                return record.id
        newIssue = Issue(project=IssueBin.objects.get(id=IssueBinId))
        newIssue.save()
        return newIssue.id

class Log(models.Model):
    Issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    log_time = models.DateTimeField()
    log_raw = models.TextField()

    def __str__(self):
        return str(self.log_raw)


class Line(models.Model):
    Log = models.ForeignKey(Log, on_delete=models.CASCADE)
    line_number = models.IntegerField()
    line_raw = models.TextField()

    def __str__(self):
        return '#'+str(self.line_number)+' '+str(self.line_raw)

#EOF
