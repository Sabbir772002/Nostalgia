import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 7, 8, 766129, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='groupcomment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 7, 8, 767303, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='groupreply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 7, 8, 767563, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_date',
            field=models.DateField(default=datetime.datetime(2026, 6, 26, 18, 7, 8, 766638, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 7, 8, 766659, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 7, 8, 766414, tzinfo=datetime.timezone.utc)),
        ),
    ]
