from tortoise.models import Model
from tortoise import fields

class ProjectIdea(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    description = fields.TextField()
    difficulty_level = fields.CharField(max_length=50)
    category = fields.CharField(max_length=100, null=True)
    technologies = fields.JSONField(null=True)
    estimated_duration = fields.CharField(max_length=100, null=True)
    learning_outcomes = fields.JSONField(null=True)
    prerequisites = fields.JSONField(null=True)
    reference_links = fields.JSONField(null=True)
    submitted_by = fields.ForeignKeyField(
        'models.User', related_name='submitted_project_ideas')
    upvotes = fields.IntField(default=0)
    is_approved = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "project_ideas"

    def __str__(self):
        return self.title