import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_is_active_user_is_staff_alter_comment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='p_image_vector',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 39, 17, 653651, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='groupcomment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 39, 17, 655946, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='groupreply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 39, 17, 656586, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_date',
            field=models.DateField(default=datetime.datetime(2026, 6, 26, 18, 39, 17, 654305, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 39, 17, 654330, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 26, 18, 39, 17, 654021, tzinfo=datetime.timezone.utc)),
        ),
    ]
