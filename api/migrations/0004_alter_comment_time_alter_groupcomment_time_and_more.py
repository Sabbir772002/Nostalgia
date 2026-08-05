import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_p_image_vector_alter_comment_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 29, 19, 16, 34, 17215, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='groupcomment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 29, 19, 16, 34, 18755, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='groupreply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 29, 19, 16, 34, 19041, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_date',
            field=models.DateField(default=datetime.datetime(2026, 6, 29, 19, 16, 34, 17776, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='noti_time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 29, 19, 16, 34, 17801, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2026, 6, 29, 19, 16, 34, 17535, tzinfo=datetime.timezone.utc)),
        ),
    ]
