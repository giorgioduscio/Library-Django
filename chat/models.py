from django.db import models
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField("auth.User", verbose_name=_("Users"))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id}: {self.name}"

class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("auth.User", verbose_name=_("User"), on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey("Room", verbose_name=_("Room"), on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    was_transferred = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.username}: {self.text}"
