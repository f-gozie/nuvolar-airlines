import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    public_id = models.UUIDField(
        unique=True, primary_key=False, default=uuid.uuid4, editable=False
    )
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ["-created"]
        get_latest_by = "created"

