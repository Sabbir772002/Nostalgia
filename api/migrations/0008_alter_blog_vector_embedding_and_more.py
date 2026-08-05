import pgvector.django.indexes
import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_blog_vector_embedding_and_more'),
    ]

    operations = [
        pgvector.django.VectorExtension(),
        migrations.AlterField(
            model_name='blog',
            name='vector_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=384, null=True),
        ),
        migrations.AlterField(
            model_name='communitygroup',
            name='vector_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=384, null=True),
        ),
        migrations.AlterField(
            model_name='owner',
            name='vector_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=384, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='vector_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=384, null=True),
        ),
        migrations.AlterField(
            model_name='walk',
            name='vector_embedding',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=384, null=True),
        ),
        migrations.AddIndex(
            model_name='blog',
            index=pgvector.django.indexes.HnswIndex(fields=['vector_embedding'], name='blog_vector_hnsw_idx', opclasses=['vector_cosine_ops']),
        ),
    ]
