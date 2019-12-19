# Generated by Django 3.0 on 2019-12-18 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shoutouts', '0003_auto_20191213_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='PinnedShoutout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoutout', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='shoutouts.Shoutout')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
