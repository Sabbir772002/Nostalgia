from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_comment_time_alter_groupcomment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='vector_embedding',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='communitygroup',
            name='vector_embedding',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='owner',
            name='vector_embedding',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='vector_embedding',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='walk',
            name='vector_embedding',
            field=models.TextField(blank=True, null=True),
        ),
    ]
