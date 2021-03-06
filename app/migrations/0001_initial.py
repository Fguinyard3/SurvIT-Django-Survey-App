# Generated by Django 4.0.3 on 2022-03-30 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(max_length=1000)),
                ('display_type', models.IntegerField(choices=[(0, 'One Page'), (1, 'Multiple Pages')], default=0)),
                ('redirect_url', models.URLField(blank=True, verbose_name='Redirect URL')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Surveys',
            },
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('participant_key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answered_on', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.survey')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('text', 'text'), ('select', 'select'), ('select-multiple', 'Select Multiple'), ('integer', 'integer')], default='text', max_length=200)),
                ('question_text', models.CharField(max_length=200)),
                ('required', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.survey')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.survey')),
            ],
        ),
    ]
