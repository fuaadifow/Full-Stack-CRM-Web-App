from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('priority', models.CharField(choices=[('high', 'High priority'), ('medium', 'Medium priority'), ('low', 'Low priority')], default='medium', max_length=10)),
                ('assigned_to_name', models.CharField(blank=True, max_length=100, null=True)),
                ('assigned_to_position', models.CharField(blank=True, max_length=100, null=True)),
                ('assigned_to_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('completed', 'Completed')], default='not_started', max_length=20)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
