from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    bin = models.CharField(max_length=24, db_index=True, unique=True)
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f"{self.bin} - {self.title}"

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    is_good = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.comment} - {self.is_good}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Contract(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    agent_id = models.ForeignKey(to=Agent, on_delete=models.SET_NULL, null=True)
    comment_id = models.ForeignKey(to=Comment, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    file_path = models.FileField(upload_to="files/")

    def __str__(self):
        return f"{self.author} - {self.agent_id} - {self.total} - {self.date}"

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"


class Log(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, null=True, db_index=True
    )
    ip = models.CharField(max_length=40, db_index=True)
    date = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.ip} - {self.date}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
