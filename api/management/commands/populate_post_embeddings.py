from django.core.management.base import BaseCommand
from api.models import Blog, Owner, CommunityGroup, Trip, Walk


class Command(BaseCommand):
    help = 'Populate missing 384-dimensional vector embeddings for Blog posts, Owners, CommunityGroups, Trips, and Walks.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting vector embedding backfill script..."))

                                
        blogs = Blog.objects.filter(vector_embedding__isnull=True)
        self.stdout.write(f"Found {blogs.count()} Blog posts missing vector embeddings.")
        blog_count = 0
        for blog in blogs:
            vec = blog.generate_vector()
            if vec:
                blog.save(update_fields=['vector_embedding'])
                blog_count += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {blog_count} Blog post embeddings."))

                            
        owners = Owner.objects.filter(vector_embedding__isnull=True)
        self.stdout.write(f"Found {owners.count()} Owners missing vector embeddings.")
        owner_count = 0
        for owner in owners:
            vec = owner.generate_vector()
            if vec:
                owner.save(update_fields=['vector_embedding'])
                owner_count += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {owner_count} Owner embeddings."))

                                     
        groups = CommunityGroup.objects.filter(vector_embedding__isnull=True)
        self.stdout.write(f"Found {groups.count()} CommunityGroups missing vector embeddings.")
        group_count = 0
        for g in groups:
            vec = g.generate_vector()
            if vec:
                g.save(update_fields=['vector_embedding'])
                group_count += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {group_count} CommunityGroup embeddings."))

                           
        trips = Trip.objects.filter(vector_embedding__isnull=True)
        self.stdout.write(f"Found {trips.count()} Trips missing vector embeddings.")
        trip_count = 0
        for t in trips:
            vec = t.generate_vector()
            if vec:
                t.save(update_fields=['vector_embedding'])
                trip_count += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {trip_count} Trip embeddings."))

                           
        walks = Walk.objects.filter(vector_embedding__isnull=True)
        self.stdout.write(f"Found {walks.count()} Walks missing vector embeddings.")
        walk_count = 0
        for w in walks:
            vec = w.generate_vector()
            if vec:
                w.save(update_fields=['vector_embedding'])
                walk_count += 1
        self.stdout.write(self.style.SUCCESS(f"Successfully populated {walk_count} Walk embeddings."))

        self.stdout.write(self.style.SUCCESS("Vector backfill process completed!"))
