from django.db import models

class Event(models.Model):
    HN = models.CharField(max_length=10)
    HnYear = models.CharField(max_length=4)
    Reason = models.CharField(max_length=255, blank=True, null=True)
    MDate = models.DateField(blank=True, null=True)
    MTime = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ScheduleDoctor"
        unique_together = (("HN", "HnYear"),)

    def __str__(self):
        return f"{self.HN} - {self.HnYear} - {self.MDate}"
