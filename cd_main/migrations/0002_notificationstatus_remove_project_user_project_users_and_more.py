# Generated by Django 4.1.7 on 2023-04-26 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cd_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('code', models.CharField(max_length=127)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(through='cd_main.UserProjectRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprojectrelation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relations', to='cd_main.project'),
        ),
        migrations.AlterField(
            model_name='userprojectrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_relations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(blank=True, max_length=8192)),
                ('notification_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cd_main.notificationstatus')),
                ('request_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request', to=settings.AUTH_USER_MODEL)),
                ('response_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]