from django.db import models
import uuid
from users.models import Profile


class Project(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    owner = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField(max_length=200)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=200, null=True, blank=True)
    source_link = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.title)

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def getVoteCount(self):
        reviews = self.reviews_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()
        ration = int((upVotes/totalVotes) * 100) if totalVotes > 0 else 0

        if self.vote_ratio != totalVotes or ration != totalVotes:
            self.vote_ratio = ration
            self.vote_total = totalVotes
            self.save()

        return {
            'vote_total': totalVotes,
            'vote_ratio': ration
        }


class Reviews(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.value


class Tag(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
