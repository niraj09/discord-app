from django.db import models
from datetime import datetime


class UserSearchModel(models.Model):
    user = models.CharField(max_length=100, db_index=True, null=False)
    search_term = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True, db_index=True)
