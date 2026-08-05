import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_comment_time_alter_groupcomment_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medalert',
            name='userid',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to='api.owner',
            ),
        ),
        migrations.AlterField(
            model_name='verified',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                serialize=False,
                to='api.owner',
            ),
        ),
    ]
