# Generated by Django 4.1 on 2022-09-23 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0002_alter_status_name'),
        ('labels', '0001_initial'),
        ('tasks', '0013_alter_tasklabelsrelations_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, through='tasks.TaskLabelsRelations', to='labels.label'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='statuses.status'),
        ),
    ]