import uuid
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    # TODO research Django "taggit" before moving to production
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True) # good for URLs like ?tag=shakespeare

    def __str__(self):
        return self.name

class Work(models.Model):
    WORK_TYPES = [
        ('poem', 'Poem'), # Flexibility to extend this to speech, duologue, etc
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=50, choices=WORK_TYPES)
    metadata = models.JSONField(default=dict, blank=True)
    chunking_strategy = models.CharField(
        max_length=50,
        choices = [('line', 'Line'), ('sentence', 'Sentence'), ('speaker_turn', 'Speaker turn'), ('custom', 'Custom')],
        default = 'line'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    raw_text = models.TextField(blank=True, help_text="Paste full poem text here")

    tags = models.ManyToManyField(Tag, related_name="works", blank=True)

    def __str__(self):
        return f"{self.title} by {self.author if self.author else 'unknown'}"
    
    def split_into_sections_and_units(self):
        # Normalize all line endings to \n
        normalized_text = self.raw_text.replace("\r\n", "\n").replace("\r", "\n").strip()

        sections_text = [s.strip() for s in normalized_text.strip().split("\n\n") if s.strip()]
        structured_sections = []

        for section_index, section in enumerate(sections_text):
            lines = [line.strip() for line in section.split("\n") if line.strip()]
            structured_sections.append({
                "order": section_index, 
                "lines": [{"order": i, "text": line} for i, line in enumerate(lines)]
            })

        return structured_sections
    

class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, blank=True)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order_index"]

    def __str__(self):
        return f"{self.work.title} - {self.title or 'Untitled Section'}"
    

class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='units')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='units')
    order_index = models.PositiveIntegerField()
    text = models.TextField()
    speaker = models.CharField(max_length=255, blank=True, null=True)  # For duologues
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["section__order_index", "order_index"]

    def __str__(self):
        return f"{self.order_index}: {self.text[:30]}..."
    

class UserUnitProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unit_progress')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='progress')
    mastery_score = models.FloatField(default=0.0)  # 0.0 to 1.0
    last_practiced_at = models.DateTimeField(auto_now=True)
    times_practiced = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'unit')


class UserWorkProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_progress')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='progress')
    mastery_score = models.FloatField(default=0.0)
    last_practiced_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'work')


class UserHistory(models.Model):
    PRACTICE_MODES = [
        ('repetition', 'Repetition'),
        ('practice', 'Practice'),
        ('test', 'Test'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='history')
    unit_ids = models.JSONField(default=list)  # store a list of UUIDs
    mode = models.CharField(max_length=50, choices=PRACTICE_MODES)
    score = models.FloatField(default=0.0)
    cap = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)