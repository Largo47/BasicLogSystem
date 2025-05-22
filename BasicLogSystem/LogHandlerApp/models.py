from django.db import models
import os


class IssueBin(models.Model):
    project_name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.project_name)

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
    status = models.CharField(choices=STATUS_OPTIONS, max_length=20, default="Open")   # We'll see if that works
    log_raw = models.TextField()

    def __str__(self):
        return str(self.project) + " #" + str(self.id)

    @staticmethod
    def retRelatedIssue(log):
        allIssues = Issue.objects.all()
        for record in allIssues:
            if record.log_raw == log:
                return record.id
        return -1

    def addOccurrence(self):
        time = Occurrence(Issue=self)
        time.save()


class Log(models.Model):
    Issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    line_number = models.IntegerField()
    line_raw = models.TextField()

    def __str__(self):
        return str(self.line_number) + ": " + str(self.line_raw)


class Occurrence(models.Model):
    Issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True, editable=False)

#EOF
