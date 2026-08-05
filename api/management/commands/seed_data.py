"""
seed_data.py — Nostalgia Project Full Mock Data Seeder
======================================================
Run with:  python manage.py seed_data
Re-run safely: uses get_or_create everywhere so it won't duplicate.

LOGIN CREDENTIALS
─────────────────────────────────────────────
Admin (Django panel):
  username: abdur_admin        password: admin1234

Regular users (all password: Pass@1234):
  rahim_sir        fatema_begum     salma_khan
  motin_bhai       nuha_akter       kamal_hossain
  roksana_begum    jahangir_alam    maya_devi
  shiraj_uddin     bilkis_khanam    anwar_hossain
─────────────────────────────────────────────
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from api.models import (
    Division, District, Thana,
    Owner, Hospital, CareType, Caregiver,
    Walk, WalkMember,
    Blog, Comment, Reply, Upvote,
    Trip, TripMember,
    Event, JoinEvent,
    CommunityGroup, GroupMember, GroupPost, GroupComment, GroupReply, GroupUpvote,
    Friend, Chat, Notification,
    Medication, MedAlert, DoneMed, Medicine,
    Additional, Verified,
    Agency, Guide, GhureAshi,
)
from datetime import date, time, timedelta
import random


                                                                  
                                     
                                                                  
def make_owner(username, email, first_name, last_name, gender, phone,
               dob, address, nid, thana, walk_type,
               password='Pass@1234', is_staff=False, is_superuser=False):
    if Owner.objects.filter(username=username).exists():
        return Owner.objects.get(username=username)
    owner = Owner(
        username=username, email=email,
        first_name=first_name, last_name=last_name,
        gender=gender, phone=phone, dob=dob,
        address=address, nid=nid, thana=thana,
        walk_type=walk_type, is_staff=is_staff,
        is_superuser=is_superuser, is_active=True,
    )
    owner.password = password                                                
    owner.save()
    return owner


class Command(BaseCommand):
    help = 'Loads MASSIVE sample data into the database for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO('\n══════════════════════════════════════'))
        self.stdout.write(self.style.HTTP_INFO('  Nostalgia — Full Mock Data Seeder'))
        self.stdout.write(self.style.HTTP_INFO('══════════════════════════════════════\n'))

                                                                            
                      
                                                                            
        self.stdout.write('📍 Creating geographic data...')

        dhaka_div,     _ = Division.objects.get_or_create(division='Dhaka')
        ctg_div,       _ = Division.objects.get_or_create(division='Chittagong')
        rajshahi_div,  _ = Division.objects.get_or_create(division='Rajshahi')
        sylhet_div,    _ = Division.objects.get_or_create(division='Sylhet')
        khulna_div,    _ = Division.objects.get_or_create(division='Khulna')
        barisal_div,   _ = Division.objects.get_or_create(division='Barisal')
        mymensingh_div,_ = Division.objects.get_or_create(division='Mymensingh')

        dhaka_dist,      _ = District.objects.get_or_create(district='Dhaka',        defaults={'division': dhaka_div})
        ctg_dist,        _ = District.objects.get_or_create(district='Chattogram',   defaults={'division': ctg_div})
        rajshahi_dist,   _ = District.objects.get_or_create(district='Rajshahi',     defaults={'division': rajshahi_div})
        sylhet_dist,     _ = District.objects.get_or_create(district='Sylhet',       defaults={'division': sylhet_div})
        khulna_dist,     _ = District.objects.get_or_create(district='Khulna',       defaults={'division': khulna_div})
        gazipur_dist,    _ = District.objects.get_or_create(district='Gazipur',      defaults={'division': dhaka_div})
        narayanganj_dist,_ = District.objects.get_or_create(district='Narayanganj',  defaults={'division': dhaka_div})
        comilla_dist,    _ = District.objects.get_or_create(district='Comilla',      defaults={'division': ctg_div})
        barisal_dist,    _ = District.objects.get_or_create(district='Barisal',      defaults={'division': barisal_div})

        dhanmondi,     _ = Thana.objects.get_or_create(thana='Dhanmondi',      defaults={'district': dhaka_dist})
        mirpur,        _ = Thana.objects.get_or_create(thana='Mirpur',         defaults={'district': dhaka_dist})
        gulshan,       _ = Thana.objects.get_or_create(thana='Gulshan',        defaults={'district': dhaka_dist})
        uttara,        _ = Thana.objects.get_or_create(thana='Uttara',         defaults={'district': dhaka_dist})
        rampura,       _ = Thana.objects.get_or_create(thana='Rampura',        defaults={'district': dhaka_dist})
        motijheel,     _ = Thana.objects.get_or_create(thana='Motijheel',      defaults={'district': dhaka_dist})
        mohammadpur,   _ = Thana.objects.get_or_create(thana='Mohammadpur',    defaults={'district': dhaka_dist})
        badda,         _ = Thana.objects.get_or_create(thana='Badda',          defaults={'district': dhaka_dist})
        double_mooring,_ = Thana.objects.get_or_create(thana='Double Mooring', defaults={'district': ctg_dist})
        kotwali_ctg,   _ = Thana.objects.get_or_create(thana='Kotwali Ctg',   defaults={'district': ctg_dist})
        boalia,        _ = Thana.objects.get_or_create(thana='Boalia',         defaults={'district': rajshahi_dist})
        sylhet_sadar,  _ = Thana.objects.get_or_create(thana='Sylhet Sadar',  defaults={'district': sylhet_dist})
        khulna_sadar,  _ = Thana.objects.get_or_create(thana='Khulna Sadar',  defaults={'district': khulna_dist})
        gazipur_sadar, _ = Thana.objects.get_or_create(thana='Gazipur Sadar', defaults={'district': gazipur_dist})
        narayanganj_sd,_ = Thana.objects.get_or_create(thana='Narayanganj Sadar', defaults={'district': narayanganj_dist})
        comilla_sadar, _ = Thana.objects.get_or_create(thana='Comilla Sadar', defaults={'district': comilla_dist})
        barisal_sadar, _ = Thana.objects.get_or_create(thana='Barisal Sadar', defaults={'district': barisal_dist})

        self.stdout.write(self.style.SUCCESS('  ✓ Geography done'))

                                                                            
                      
                                                                            
        self.stdout.write('🏥 Creating hospitals...')

        dhmc, _         = Hospital.objects.get_or_create(h_name='Dhaka Medical College Hospital', defaults={'h_location': 'Bakshibazar Rd, Dhaka', 'branch': 'Main', 'thana': motijheel})
        square_h, _     = Hospital.objects.get_or_create(h_name='Square Hospital', defaults={'h_location': 'West Panthapath, Dhaka', 'branch': 'Main', 'thana': dhanmondi})
        ctg_medical, _  = Hospital.objects.get_or_create(h_name='Chattogram Medical College Hospital', defaults={'h_location': 'K B Fazlul Kader Rd', 'branch': 'Main', 'thana': double_mooring})
        ibn_sina, _     = Hospital.objects.get_or_create(h_name='Ibn Sina Hospital', defaults={'h_location': 'House 48, Road 9/A, Dhanmondi', 'branch': 'Dhanmondi', 'thana': dhanmondi})
        labaid, _       = Hospital.objects.get_or_create(h_name='LabAid Hospital', defaults={'h_location': 'House 1, Road 4, Dhanmondi', 'branch': 'Main', 'thana': dhanmondi})
        united_h, _     = Hospital.objects.get_or_create(h_name='United Hospital', defaults={'h_location': 'Plot 15, Road 71, Gulshan', 'branch': 'Main', 'thana': gulshan})

        self.stdout.write(self.style.SUCCESS('  ✓ Hospitals done'))

                                                                            
                                    
                                                                            
        self.stdout.write('👨‍⚕️ Creating care types & caregivers...')

        nurse_t, _      = CareType.objects.get_or_create(type='Nurse')
        physio_t, _     = CareType.objects.get_or_create(type='Physiotherapist')
        companion_t, _  = CareType.objects.get_or_create(type='Companion')
        doctor_t, _     = CareType.objects.get_or_create(type='Doctor')
        attendant_t, _  = CareType.objects.get_or_create(type='Attendant')

        caregivers_data = [
            ('Nasrin Akter',    'Female', 1711123456, 5,  nurse_t,     dhmc,      'nasrin.akter@dhmc.bd',        date(1990, 3, 15)),
            ('Karim Uddin',     'Male',   1819234567, 8,  physio_t,    square_h,  'karim.uddin@square.bd',       date(1985, 7, 22)),
            ('Ruhul Amin',      'Male',   1912345678, 12, doctor_t,    ibn_sina,  'ruhul.amin@ibnsina.bd',       date(1978, 1, 5)),
            ('Sonia Parvin',    'Female', 1723456789, 3,  companion_t, labaid,    'sonia.parvin@labaid.bd',      date(1995, 9, 28)),
            ('Mizanur Rahman',  'Male',   1834567890, 6,  attendant_t, united_h,  'mizan.rahman@united.bd',      date(1988, 6, 14)),
            ('Dilruba Khanam',  'Female', 1745678901, 9,  nurse_t,     ctg_medical,'dilruba@ctgmedical.bd',      date(1983, 11, 3)),
            ('Ariful Islam',    'Male',   1956789012, 4,  physio_t,    square_h,  'ariful@square.bd',            date(1992, 4, 17)),
            ('Shamima Begum',   'Female', 1767890123, 7,  companion_t, dhmc,      'shamima@dhmc.bd',             date(1987, 8, 25)),
        ]
        for name, gender, phone, exp, care_type, hosp, email, dob_c in caregivers_data:
            Caregiver.objects.get_or_create(name=name, defaults={
                'gender': gender, 'phone': phone, 'experience': exp,
                'type': care_type, 'h_id': hosp, 'email': email, 'dob': dob_c
            })

        self.stdout.write(self.style.SUCCESS('  ✓ Caregivers done'))

                                                                            
                      
                                                                            
        self.stdout.write('💊 Creating medicines...')

        medicines = [
            ('Hypertension', 'Amlodipine 5mg - Calcium channel blocker for blood pressure', 'Amlodipine'),
            ('Diabetes', 'Metformin 500mg - First-line medication for type 2 diabetes', 'Metformin'),
            ('Arthritis', 'Diclofenac 50mg - Anti-inflammatory pain reliever', 'Diclofenac'),
            ('Gastric', 'Omeprazole 20mg - Proton pump inhibitor for acid reflux', 'Omeprazole'),
            ('Cholesterol', 'Atorvastatin 10mg - Statin for high cholesterol', 'Atorvastatin'),
            ('Asthma', 'Salbutamol 100mcg - Bronchodilator inhaler', 'Salbutamol'),
            ('Insomnia', 'Nitrazepam 5mg - Benzodiazepine for sleep disorders', 'Nitrazepam'),
            ('Vitamin D', 'Vitamin D3 1000IU - Bone health supplement', 'Cholecalciferol'),
            ('Anxiety', 'Clonazepam 0.5mg - For anxiety disorders', 'Clonazepam'),
            ('Gout', 'Allopurinol 100mg - For hyperuricemia and gout', 'Allopurinol'),
        ]
        for disease, content, med_name in medicines:
            Medicine.objects.get_or_create(disease=disease, defaults={'content': content, 'med_name': med_name})

        self.stdout.write(self.style.SUCCESS('  ✓ Medicines done'))

                                                                            
                            
                                                                            
        self.stdout.write('🏢 Creating agencies & guides...')

        agency1, _ = Agency.objects.get_or_create(name='Bangladesh Senior Tours', defaults={'phone': '01711900001', 'email': 'info@bstours.bd', 'address': 'Dhanmondi 15, Dhaka', 'thana': dhanmondi, 'rating': 4.7})
        agency2, _ = Agency.objects.get_or_create(name='GoldenAge Travel', defaults={'phone': '01811900002', 'email': 'info@goldenage.bd', 'address': 'Gulshan 2, Dhaka', 'thana': gulshan, 'rating': 4.5})
        agency3, _ = Agency.objects.get_or_create(name='Probin Paryatan', defaults={'phone': '01911900003', 'email': 'info@probinparyatan.bd', 'address': 'CDA Avenue, Chattogram', 'thana': double_mooring, 'rating': 4.3})

        guides_data = [
            ('Alamin Hossain', '01711800001', 'alamin@bstours.bd', 'Mirpur 12, Dhaka', dhanmondi, 4.8, 10, date(1982, 5, 12), agency1),
            ('Sumaiya Islam',  '01811800002', 'sumaiya@goldenage.bd', 'Gulshan 1, Dhaka', gulshan, 4.6, 7, date(1988, 9, 3), agency2),
            ('Forhad Hossain', '01711800003', 'forhad@probinparyatan.bd', 'Kotwali, Ctg', double_mooring, 4.4, 12, date(1978, 3, 20), agency3),
            ('Mou Akter',      '01611800004', 'mou@bstours.bd', 'Uttara 6, Dhaka', uttara, 4.9, 5, date(1993, 7, 18), agency1),
        ]
        for name, phone, email, addr, thana_g, rating, exp, dob_g, agcy in guides_data:
            Guide.objects.get_or_create(name=name, defaults={'phone': phone, 'email': email, 'address': addr, 'thana': thana_g, 'rating': rating, 'experience': exp, 'dob': dob_g, 'agency': agcy})

        GhureAshi.objects.get_or_create(name='Ghure Ashi Cox Bazar', defaults={'phone': '01711700001', 'email': 'info@ghureashi.bd', 'address': "Cox's Bazar Sea Beach", 'thana': kotwali_ctg, 'rating': 4.8})
        GhureAshi.objects.get_or_create(name='Sundarban Explorer', defaults={'phone': '01811700002', 'email': 'sundarban@ghureashi.bd', 'address': 'Khulna Ghat', 'thana': khulna_sadar, 'rating': 4.6})

        self.stdout.write(self.style.SUCCESS('  ✓ Agencies & guides done'))

                                                                            
                                                   
                                                                            
        self.stdout.write('👤 Creating users...')

               
        admin = make_owner(
            'abdur_admin',   'abdur.rahman.admin@nostalgia.bd',
            'Abdur',         'Rahman',     'Male',   '01933333333',
            date(1948, 2, 28), '50 Agrabad C/A, Chattogram',
            '1122334455', double_mooring, 'General',
            password='admin1234', is_staff=True, is_superuser=True,
        )

                       
        u1 = make_owner('rahim_sir',      'rahim.uddin1950@gmail.com',       'Rahim',    'Uddin',    'Male',   '01711111111', date(1950, 6, 12),  'House 5, Road 8, Dhanmondi',      '1234567890', dhanmondi, 'Evening Walk')
        u2 = make_owner('fatema_begum',   'fatema.begum1955@gmail.com',      'Fatema',   'Begum',    'Female', '01822222222', date(1955, 11, 3),  'Flat 3B, Block A, Mirpur-10',     '9876543210', mirpur,    'Morning Walk')
        u3 = make_owner('salma_khan',     'salma.khan1953@gmail.com',        'Salma',    'Khan',     'Female', '01744444444', date(1953, 4, 15),  'House 12, Road 4, Gulshan',       '5566778899', gulshan,   'Morning Walk')
        u4 = make_owner('motin_bhai',     'motin.rahman1951@gmail.com',      'Abdul',    'Motin',    'Male',   '01855555555', date(1951, 9, 20),  'Sector 4, Road 2, Uttara',        '6677889900', uttara,    'Evening Walk')
        u5 = make_owner('nuha_akter',     'nuha.akter1958@gmail.com',        'Nuha',     'Akter',    'Female', '01766666666', date(1958, 3, 7),   'House 3, Road 12, Rampura',       '7788990011', rampura,   'Morning Walk')
        u6 = make_owner('kamal_hossain',  'kamal.hossain1947@gmail.com',     'Kamal',    'Hossain',  'Male',   '01977777777', date(1947, 12, 1),  'Flat 7A, Mohammadpur Housing',    '8899001122', mohammadpur, 'Evening Walk')
        u7 = make_owner('roksana_begum',  'roksana.begum1960@gmail.com',     'Roksana',  'Begum',    'Female', '01688888888', date(1960, 7, 25),  'House 9, Road 3, Badda, Dhaka',   '9900112233', badda,     'Morning Walk')
        u8 = make_owner('jahangir_alam',  'jahangir.alam1949@gmail.com',     'Jahangir', 'Alam',     'Male',   '01799999999', date(1949, 5, 14),  '45 Boalia, Rajshahi',             '0011223344', boalia,    'Evening Walk')
        u9 = make_owner('maya_devi',      'maya.devi1956@gmail.com',         'Maya',     'Devi',     'Female', '01600000001', date(1956, 8, 30),  '12 Narayanganj Sadar',            '1122334466', narayanganj_sd, 'Morning Walk')
        u10= make_owner('shiraj_uddin',   'shiraj.uddin1952@gmail.com',      'Shiraj',   'Uddin',    'Male',   '01511000001', date(1952, 2, 19),  'House 22, Sylhet Sadar',          '2233445577', sylhet_sadar, 'Evening Walk')
        u11= make_owner('bilkis_khanam',  'bilkis.khanam1957@gmail.com',     'Bilkis',   'Khanam',   'Female', '01411000002', date(1957, 10, 8),  '88 Khulna Sadar Road',           '3344556688', khulna_sadar, 'Morning Walk')
        u12= make_owner('anwar_hossain',  'anwar.hossain1945@gmail.com',     'Anwar',    'Hossain',  'Male',   '01911000003', date(1945, 4, 3),   '5 Comilla Sadar Main Road',       '4455667799', comilla_sadar, 'Evening Walk')

        all_users = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12]
        self.stdout.write(self.style.SUCCESS('  ✓ Users done'))

                                                                            
                            
                                                                            
        for u in [u1, u2, u3, admin]:
            Verified.objects.get_or_create(user=u, defaults={'verified': True})
        for u in [u4, u5, u6]:
            Verified.objects.get_or_create(user=u, defaults={'verified': False})

                                                                            
                            
                                                                            
        additional_data = [
            (u1, 'hobby',      'Morning walk, Reading Quran, Chess'),
            (u1, 'past_job',   'Civil Engineer, LGED, Retired 2005'),
            (u2, 'hobby',      'Gardening, Cooking, Listening to Nazrul Sangeet'),
            (u2, 'past_job',   'School Teacher, Viqarunnisa Noon School'),
            (u3, 'hobby',      'Painting, Knitting, Watching Classic Bangla Movies'),
            (u4, 'hobby',      'Cricket commentary, Carrom board, Tea circle'),
            (u5, 'past_job',   'Bank Officer, Sonali Bank, Retired 2018'),
            (u6, 'hobby',      'Fishing, Reading Newspapers, Bird watching'),
            (u7, 'hobby',      'Singing Rabindra Sangeet, Embroidery, Cooking'),
            (u8, 'past_job',   'Police Officer, Retired Inspector, 2010'),
        ]
        for user, atype, content in additional_data:
            Additional.objects.get_or_create(user=user, type=atype, defaults={'content': content})

                                                                            
                                                               
                                                                            
        self.stdout.write('🤝 Creating friendships...')

                                      
        confirmed_pairs = [
            (u1, u2), (u1, u3), (u1, u4), (u1, u5),
            (u2, u3), (u2, u5), (u2, u6),
            (u3, u4), (u3, u7),
            (u4, u5), (u4, u8),
            (u5, u6), (u5, u9),
            (u6, u7), (u6, u10),
            (u7, u8), (u7, u11),
            (u8, u9), (u8, u12),
            (u9, u10),
            (u10, u11),
            (u11, u12),
            (u1, admin), (u2, admin),
        ]
        for a, b in confirmed_pairs:
            Friend.objects.get_or_create(user1=a, user2=b, defaults={
                'f_created_date': date(2025, random.randint(1, 6), random.randint(1, 28)),
                'is_fnf': 1, 'type': 'friend'
            })

                                                                          
        pending_pairs = [
            (u3, u8), (u6, u12), (u9, u11), (u10, u12), (u4, u7), (u2, u10),
            (u5, u11), (u1, u9),
        ]
        for a, b in pending_pairs:
            if not Friend.objects.filter(user1=a, user2=b).exists() and \
               not Friend.objects.filter(user1=b, user2=a).exists():
                Friend.objects.get_or_create(user1=a, user2=b, defaults={
                    'f_created_date': date(2026, random.randint(1, 7), random.randint(1, 28)),
                    'is_fnf': 0, 'type': 'friend'
                })

        self.stdout.write(self.style.SUCCESS('  ✓ Friendships done'))

                                                                            
                        
                                                                            
        self.stdout.write('📝 Creating blog posts...')

        blogs_data = [
            (u1, date(2025, 1, 16), time(8, 30),
             'আজ রমনা পার্কে পুরনো বন্ধুদের সাথে হাঁটলাম। ১৯৭০ এর দশকে প্রতি শুক্রবার এখানে দেখা হতো। সেই পুরনো স্মৃতিগুলো আবার মনে পড়ে গেল। আল্লাহ যেন সেই সুন্দর দিনগুলো আবার ফিরিয়ে দেন।'),
            (u2, date(2025, 2, 5), time(9, 15),
             'আজ সকালে আমার caregiver Nasrin আমাকে নতুন breathing exercise শিখিয়েছে। সকালের কড়াকড়িতে অনেক উপকার হচ্ছে। সবাইকে recommend করি।'),
            (u3, date(2025, 2, 20), time(10, 0),
             'আমার বারান্দার বাগানে আজ গোলাপ ফুটেছে! গাছ পালন করাই আমার সেরা therapy। সিনিয়র সিটিজেনদের সবাইকে gardening এর কথা বলতে চাই।'),
            (u4, date(2025, 3, 2), time(11, 45),
             'উত্তরার প্রতিবেশীদের সাথে চায়ের আড্ডায় পুরনো স্কুলের দিনের কথা মনে পড়ল। সেই ক্রিকেট খেলা, সেই পাড়ার দোকানের সিঙ্গারা... অসাধারণ লাগছে।'),
            (u5, date(2025, 3, 5), time(9, 0),
             'Nostalgia-তে সবাইকে স্বাগতম! এই platform টি পুরনো বন্ধুদের reconnect করতে এবং walking group তৈরি করতে designed। সবাই post করুন আর trip plan করুন।'),
            (u1, date(2025, 3, 12), time(14, 20),
             "কেউ কি মনে করেন ঢাকার পুরনো সিনেমা হলগুলো, যেমন বলাকা বা মধুমিতা, '৭০ দশকে? সেই পরিবেশ ছিল অসাধারণ।"),
            (u6, date(2025, 4, 1), time(16, 0),
             'মোহাম্মদপুরের লেকের পাশে বসে আজ অনেকক্ষণ পাখি দেখলাম। এই বয়সে এই শান্তিই আমার সবচেয়ে বড় আনন্দ।'),
            (u7, date(2025, 4, 5), time(8, 45),
             'আজ রবীন্দ্র সংগীত শুনতে শুনতে কাজ করলাম। গানের সুর মনকে শান্ত রাখে। "আমার সোনার বাংলা" শুনলে এখনো চোখে জল আসে।'),
            (u8, date(2025, 4, 10), time(17, 30),
             'রাজশাহীর পদ্মার তীরে সূর্যাস্ত দেখলাম। ৪০ বছরের চাকরি শেষে এই অবসর জীবনটাই এখন সবচেয়ে সুন্দর।'),
            (u2, date(2025, 4, 15), time(10, 30),
             'আজ বাড়িতে বিরিয়ানি রান্না করলাম পুরনো রেসিপি দিয়ে। মেয়েরা বলছে ঠিক নানীর হাতের স্বাদ। রান্না করাটাই আমার ধ্যান।'),
            (u3, date(2025, 5, 1), time(9, 0),
             'আজ একটা ছবি আঁকলাম ঢাকার পুরনো রিকশা নিয়ে। যারা সেই রিকশার যুগ মনে রাখেন, তাদের জন্যই এই ছবি।'),
            (u9, date(2025, 5, 10), time(11, 0),
             'নারায়ণগঞ্জের পুরনো পাট কারখানার গল্প মনে পড়ে। আমার বাবা সেখানে কাজ করতেন। সেই ধুলার স্মৃতি, সেই পরিবার।'),
            (u10, date(2025, 5, 20), time(15, 0),
             'সিলেটের চা বাগানে গিয়েছিলাম শেষবার ১৯৮৫ সালে। এবার আবার যাওয়ার পরিকল্পনা করছি। কেউ যেতে চান?'),
            (u4, date(2025, 6, 1), time(7, 0),
             'Morning walk এ আজ ৫ জন নতুন বন্ধু পেলাম। তাদের সাথে কথা বলে মনে হলো বয়স কমে গেছে। হাঁটাহাঁটির কোনো বিকল্প নেই।'),
            (u5, date(2025, 6, 15), time(12, 0),
             'সোনালী ব্যাংকে ৩৫ বছর চাকরি করেছি। Retirement এর পর মনে হচ্ছে এখন সত্যিকারের জীবন শুরু হয়েছে। Nostalgia-র মতো platform-ই এখন সাথী।'),
            (u11, date(2025, 6, 20), time(14, 0),
             'খুলনার ভাইরব নদীতে নৌকায় ভেসে যাওয়ার স্মৃতি অনেক পুরনো। সেই নদী কি আর আগের মতো আছে?'),
            (u12, date(2025, 7, 1), time(8, 0),
             'কুমিল্লার রসমালাই খাওয়ার অনেক দিন হয়েছে। কেউ কি আছেন যিনি সঠিক দোকানের নাম জানেন?'),
            (u6, date(2025, 7, 5), time(16, 30),
             'আজ মাছ ধরতে গেলাম। ৩ ঘণ্টায় মাত্র ছোট একটা মাছ ধরলাম কিন্তু সময়টা অসাধারণ কাটল।'),
        ]

        blog_objs = []
        for author, post_date, post_time_val, content in blogs_data:
            b, _ = Blog.objects.get_or_create(
                author=author, post_date=post_date, content=content,
                defaults={'post_time': post_time_val}
            )
            blog_objs.append(b)

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(blog_objs)} blog posts done'))

                                                                            
                                          
                                                                            
        self.stdout.write('💬 Creating comments, replies & upvotes...')

        comments_data = [
            (blog_objs[0], u2,  'খুব সুন্দর স্মৃতি ভাই! আমিও রমনা পার্কে যেতাম।'),
            (blog_objs[0], u3,  'অসাধারণ! সেই পুরনো দিনগুলো সত্যিই মিস করি।'),
            (blog_objs[0], u4,  'একমত! ৭০ দশকের ঢাকার কথা মনে পড়লে মনটা ভালো হয়ে যায়।'),
            (blog_objs[1], u1,  'Breathing exercise সম্পর্কে আরও জানতে চাই!'),
            (blog_objs[1], u3,  'আমিও এই ব্যায়াম শুরু করব। ধন্যবাদ শেয়ার করার জন্য।'),
            (blog_objs[2], u1,  'গোলাপ ফুলের ছবি দিন না আপু!'),
            (blog_objs[2], u5,  'গাছ পালন সত্যিই অনেক মনকে শান্ত রাখে।'),
            (blog_objs[3], u2,  'হা হা ভাই! সিঙ্গারার কথা মনে করিয়ে দিলেন। অনেক মিস করি।'),
            (blog_objs[3], u6,  'উত্তরার আড্ডা মানেই আলাদা মজা!'),
            (blog_objs[4], u1,  'অনেক ধন্যবাদ! এই platform এ এসে অনেক ভালো লাগছে।'),
            (blog_objs[5], u2,  'হ্যাঁ মনে আছে! বলাকায় হিন্দি সিনেমা দেখতাম।'),
            (blog_objs[5], u4,  'মধুমিতায় অনেক বাংলা ছবি দেখেছি! সেই সব অনেক কিছু মনে পড়ে।'),
            (blog_objs[6], u7,  'পাখি দেখা সত্যিই অনেক relaxing। কোন পার্কে গিয়েছিলেন?'),
            (blog_objs[7], u2,  '"একলা চলো রে" এখন এই বয়সে নতুন মানে পায়।'),
            (blog_objs[8], u9,  'পদ্মার তীর সত্যিই অসাধারণ। আমিও যেতে চাই।'),
            (blog_objs[9], u1,  'রেসিপিটা কি share করবেন? আমিও try করতে চাই!'),
            (blog_objs[10], u5, 'ছবিটা দেখতে চাই!'),
            (blog_objs[12], u11,'সিলেটের tea garden অনেক সুন্দর, আমিও যেতে চাই!'),
        ]

        comment_objs = []
        for blog, user, text in comments_data:
            c, _ = Comment.objects.get_or_create(blogid=blog, username=user, comment=text[:490])
            comment_objs.append(c)

                 
        replies_data = [
            (comment_objs[0], u1, 'হ্যাঁ আপু! এখনও মাঝে মাঝে যাই। কবে একসাথে যাব?'),
            (comment_objs[0], u3, 'আমাকেও নিয়ে যাবেন কিন্তু!'),
            (comment_objs[1], u2, 'অবশ্যই! একদিন একসাথে যাব।'),
            (comment_objs[4], u1, 'রেসিপিটা পরে দেব ইনশাআল্লাহ!'),
            (comment_objs[6], u3, 'আমি Hatirjheel park-এ যাই সকালে।'),
            (comment_objs[9], u5, 'আপনার জন্য অনেক কৃতজ্ঞ ভাই!'),
        ]
        for comment, user, msg in replies_data:
            Reply.objects.get_or_create(cmnt_id=comment, user=user, defaults={'Reply_msg': msg})

                 
        upvote_pairs = [
            (blog_objs[0], u2), (blog_objs[0], u3), (blog_objs[0], u4), (blog_objs[0], u5),
            (blog_objs[1], u1), (blog_objs[1], u3), (blog_objs[1], u6),
            (blog_objs[2], u1), (blog_objs[2], u2), (blog_objs[2], u4), (blog_objs[2], u7),
            (blog_objs[3], u2), (blog_objs[3], u5),
            (blog_objs[4], u1), (blog_objs[4], u2), (blog_objs[4], u3),
            (blog_objs[5], u2), (blog_objs[5], u4), (blog_objs[5], u6),
            (blog_objs[6], u7), (blog_objs[7], u2), (blog_objs[8], u9),
            (blog_objs[9], u1), (blog_objs[10], u5), (blog_objs[11], u8),
        ]
        for blog, user in upvote_pairs:
            Upvote.objects.get_or_create(blogid=blog, Username=user)

        self.stdout.write(self.style.SUCCESS('  ✓ Comments, replies & upvotes done'))

                                                                            
                                                           
                                                                            
        self.stdout.write('👥 Creating community groups...')

        grp1, _ = CommunityGroup.objects.get_or_create(G_username='dhanmondi_elders', defaults={'G_name': 'Dhanmondi Elders Circle', 'Topic': 'Health, Walking, Social Meetups', 'Privacy': 'public', 'time': time(10, 0), 'Creator': u1})
        grp2, _ = CommunityGroup.objects.get_or_create(G_username='gulshan_seniors',  defaults={'G_name': 'Gulshan Seniors Club',      'Topic': 'Literature, Gardening, Art',         'Privacy': 'public', 'time': time(11, 0), 'Creator': u3})
        grp3, _ = CommunityGroup.objects.get_or_create(G_username='uttara_friends',   defaults={'G_name': 'Uttara Retired Friends',    'Topic': 'Politics, Sports, Walking',          'Privacy': 'public', 'time': time(16, 0), 'Creator': u4})
        grp4, _ = CommunityGroup.objects.get_or_create(G_username='nostalgia_music',  defaults={'G_name': 'Nostalgia Music Lovers',    'Topic': 'Bangla Classic Music & Songs',       'Privacy': 'public', 'time': time(18, 0), 'Creator': u7})
        grp5, _ = CommunityGroup.objects.get_or_create(G_username='probin_readers',   defaults={'G_name': 'Probin Readers Club',       'Topic': 'Book reading & Discussion',          'Privacy': 'private','time': time(15, 0), 'Creator': u6})

                       
        group_membership = {
            grp1: [u1, u2, u3, u4, u5, u6],
            grp2: [u3, u1, u2, u7, u8, u9],
            grp3: [u4, u5, u6, u3, u10],
            grp4: [u7, u2, u3, u11, u12, u5],
            grp5: [u6, u1, u8, u9, u10, u11],
        }
        for group, members in group_membership.items():
            for member in members:
                GroupMember.objects.get_or_create(G_username=group, member=member, defaults={
                    'isAdmin': 'yes' if group.Creator == member else 'no',
                    'Block': 0, 'accept': 1,
                })

                     
        gposts_data = [
            (grp1, u1, date(2025, 2, 10), time(10, 15), 'আমাদের Dhanmondi Elders Circle-এর সবাইকে জানাই, আগামী শুক্রবার সকাল ৭টায় রমনা পার্কে আমাদের monthly walk। আসবেন কিন্তু!'),
            (grp1, u2, date(2025, 3, 1),  time(9, 0),   'গতকালের walking session-এ অনেক মজা হয়েছে। পরের বার সবাই আসবেন। সঙ্গে নাশতা আনবেন।'),
            (grp2, u3, date(2025, 2, 25), time(11, 30), 'Gulshan Seniors Club এর জন্য একটা painting workshop আয়োজন করা হচ্ছে। ইচ্ছুকরা নাম দিন।'),
            (grp2, u7, date(2025, 3, 15), time(14, 0),  'গতকালের book discussion সত্যিই অসাধারণ ছিল। হুমায়ূন আহমেদের "মিসির আলি" নিয়ে কথা বলতে পারলাম।'),
            (grp3, u4, date(2025, 3, 5),  time(16, 45), 'Uttara Retired Friends এর পক্ষ থেকে সবাইকে জানাই, এই মাসের get-together হবে ১৫ই মার্চ।'),
            (grp4, u7, date(2025, 4, 1),  time(18, 30), 'Nostalgia Music Lovers এর সবাইকে জানাই, আমরা এবার রবীন্দ্র জন্মবার্ষিকীতে একটা ছোট অনুষ্ঠান করব।'),
            (grp4, u2, date(2025, 4, 10), time(19, 0),  '"আমার সোনার বাংলা" এবং "একুশের গান" - এই দুটো গানের সাথে আমার জীবনের অনেক স্মৃতি জড়িয়ে আছে।'),
            (grp5, u6, date(2025, 5, 1),  time(15, 30), 'Probin Readers Club এই মাসে পড়ব রবীন্দ্রনাথের "গোরা"। সবাই প্রস্তুত থাকুন।'),
        ]

        gpost_objs = []
        for grp, user, gdate, gtime, content in gposts_data:
            gp, _ = GroupPost.objects.get_or_create(G_username=grp, p_username=user, GPost_date=gdate, defaults={'GPost_contents': content, 'GPost_Time': gtime})
            gpost_objs.append(gp)

                        
        gcmts = [
            (gpost_objs[0], u2, 'অবশ্যই আসব! সময়মতো থাকব।'),
            (gpost_objs[0], u3, 'চমৎকার পরিকল্পনা! আমি আসব।'),
            (gpost_objs[1], u1, 'সত্যিই অনেক মজা হয়েছিল!'),
            (gpost_objs[2], u1, 'Painting workshop এ আমি আগ্রহী!'),
            (gpost_objs[3], u3, 'মিসির আলি আমার সবচেয়ে প্রিয় চরিত্র!'),
            (gpost_objs[5], u2, 'অনুষ্ঠানে অংশ নিতে চাই!'),
            (gpost_objs[6], u11, 'একুশের গান শুনলে চোখে পানি আসে।'),
        ]
        gcmt_objs = []
        for gpost, user, text in gcmts:
            gc, _ = GroupComment.objects.get_or_create(blogid=gpost, username=user, defaults={'comment': text})
            gcmt_objs.append(gc)

                       
        for gpost in gpost_objs[:4]:
            for user in [u1, u2, u3, u4]:
                GroupUpvote.objects.get_or_create(blogid=gpost, Username=user)

                       
        GroupReply.objects.get_or_create(cmnt_id=gcmt_objs[0], user=u1, defaults={'Reply_msg': 'দারুণ! আমরা সবাই একসাথে যাব।'})
        GroupReply.objects.get_or_create(cmnt_id=gcmt_objs[2], user=u2, defaults={'Reply_msg': 'পরের বারও এভাবে হোক।'})

        self.stdout.write(self.style.SUCCESS('  ✓ Groups done'))

                                                                            
                                  
                                                                            
        self.stdout.write('🚶 Creating walks...')

        walks_data = [
            ('Ramna Park Morning Walk',     'Ramna Park, Dhaka',               date(2025, 1, 10), date(2025, 1, 15), date(2025, 3, 31),  'public',  time(6, 0),  u1),
            ('Hatirjheel Evening Stroll',   'Hatirjheel, Rampura, Dhaka',      date(2025, 2, 1),  date(2025, 2, 10), date(2025, 4, 30),  'private', time(17, 30),u2),
            ('Gulshan Lake Walk',           'Gulshan Lake Park, Dhaka',        date(2025, 2, 15), date(2025, 2, 22), date(2025, 5, 15),  'public',  time(7, 0),  u3),
            ('Dhanmondi Lake Walking',      'Dhanmondi Lake, Dhaka',           date(2025, 3, 1),  date(2025, 3, 8),  date(2025, 6, 1),   'public',  time(16, 30),u4),
            ('Uttara Sector Park Walk',     'Sector 3 Park, Uttara, Dhaka',    date(2025, 3, 10), date(2025, 3, 15), date(2025, 6, 15),  'private', time(6, 30), u5),
            ('Mohammadpur Morning Walk',    'Mohammadpur Housing, Dhaka',      date(2025, 4, 5),  date(2025, 4, 12), date(2025, 7, 12),  'public',  time(6, 0),  u6),
            ('Badda Park Evening Walk',     'Badda Park, Badda, Dhaka',        date(2025, 5, 1),  date(2025, 5, 8),  date(2025, 8, 8),   'public',  time(17, 0), u7),
            ('Mirpur Botanical Walk',       'National Botanical Garden, Mirpur',date(2025, 5, 20), date(2025, 5, 27), date(2025, 8, 30),  'public',  time(7, 30), u2),
        ]

        walk_objs = []
        for name, addr, pdate, wdate, edate, priv, wtime, creator in walks_data:
            w, _ = Walk.objects.get_or_create(walk_name=name, defaults={
                'address': addr, 'propose_date': pdate, 'walk_date': wdate,
                'end_date': edate, 'privacy': priv, 'time': wtime, 'w_creator': creator
            })
            walk_objs.append(w)

                      
        walk_member_data = [
            (walk_objs[0], [u2, u3, u4, u5]),
            (walk_objs[1], [u1, u3, u5]),
            (walk_objs[2], [u1, u2, u7, u8]),
            (walk_objs[3], [u1, u5, u6]),
            (walk_objs[4], [u2, u4, u6]),
            (walk_objs[6], [u6, u2, u3]),
        ]
        for walk, members in walk_member_data:
            for mem in members:
                WalkMember.objects.get_or_create(walk_id=walk, username=mem, defaults={'cancel': 0, 'accept': 1})

        self.stdout.write(self.style.SUCCESS('  ✓ Walks done'))

                                                                            
                                  
                                                                            
        self.stdout.write("✈️  Creating trips...")

        trips_data = [
            ("Cox's Bazar Senior Tour",  "Cox's Bazar, Bangladesh", date(2025, 5, 10), date(2025, 5, 14), date(2025, 4, 15), 'public',  u1,  double_mooring, 'Local Guide Service'),
            ('Sylhet Tea Garden Visit',  'Sreemangal, Sylhet',       date(2025, 6, 5),  date(2025, 6, 8),  date(2025, 5, 1),  'public',  u3,  sylhet_sadar,   'Sylhet Tourism Guide'),
            ('Sundarbans Cruise',        'Sundarbans, Khulna',       date(2025, 7, 12), date(2025, 7, 16), date(2025, 5, 20), 'public',  u2,  khulna_sadar,   'EcoTour Guides'),
            ('Lalbagh Fort Day Out',     'Lalbagh, Dhaka',           date(2025, 8, 1),  date(2025, 8, 1),  date(2025, 6, 10), 'public',  u5,  dhanmondi,      'Dhaka City Tour Guides'),
            ('Paharpur Heritage Trip',   'Paharpur, Rajshahi',       date(2025, 9, 5),  date(2025, 9, 7),  date(2025, 7, 20), 'public',  u8,  boalia,         'Rajshahi Heritage Guide'),
            ('Kuakata Sunrise Tour',     'Kuakata, Barisal',         date(2025, 10, 10),date(2025, 10, 13),date(2025, 8, 1),  'public',  u11, barisal_sadar,  'Barisal Tour Service'),
            ('Rangamati Hill Track',     'Rangamati, Chittagong',    date(2025, 11, 1), date(2025, 11, 5), date(2025, 9, 1),  'private', u6,  kotwali_ctg,    'CHT Eco Guides'),
        ]

        trip_objs = []
        for name, loc, sdate, edate, pdate, priv, creator, thana_t, guide in trips_data:
            t, _ = Trip.objects.get_or_create(name=name, defaults={
                'Location': loc, 'start_date': sdate, 'end_date': edate,
                'propose_date': pdate, 'Privacy': priv, 'Creator': creator,
                'Thana': thana_t, 'guide': guide
            })
            trip_objs.append(t)

        trip_member_data = [
            (trip_objs[0], [(u2, 1), (u3, 1), (u4, 1), (u5, 0)]),               
            (trip_objs[1], [(u1, 1), (u2, 1), (u7, 1), (u8, 0)]),
            (trip_objs[2], [(u1, 1), (u4, 1), (u9, 1)]),
            (trip_objs[3], [(u1, 1), (u3, 1), (u6, 1), (u10, 0)]),
            (trip_objs[4], [(u9, 1), (u10, 1), (u11, 1)]),
            (trip_objs[5], [(u12, 1), (u10, 1), (u9, 1), (u7, 0)]),
        ]
        for trip, members in trip_member_data:
            for mem, approve in members:
                TripMember.objects.get_or_create(TripID=trip, member=mem, defaults={'cancel': 0, 'Approve': approve})

        self.stdout.write(self.style.SUCCESS('  ✓ Trips done'))

                                                                            
                                  
                                                                            
        self.stdout.write('🎉 Creating events...')

        events_data = [
            ('Senior Health Fair 2025',    'Free health check-up fair: BP, diabetes, eye — all free.', time(9, 0), time(17, 0), date(2025, 10, 10), date(2025, 10, 10), 'Suhrawardy Udyan, Dhaka',       date(2025, 9, 1),  1, 'Health',  'public',  u1, dhanmondi),
            ('Art & Nostalgia Workshop',   'Painting & art exhibition of historic Dhaka.',              time(10, 0),time(15, 0), date(2025, 11, 5),  date(2025, 11, 5),  'Gulshan Youth Club, Dhaka',     date(2025, 10, 1), 1, 'Art',     'public',  u3, gulshan),
            ('Weekly Walking Summit',      'Weekly gathering of all walking buddy groups.',              time(6, 30),time(9, 0),  date(2025, 11, 12), date(2025, 11, 12), 'Ramna Park Lake Side, Dhaka',   date(2025, 10, 10),1, 'Walk',    'public',  u1, motijheel),
            ('Pensioners Get-Together',    'Social event for retired government & private employees.',  time(16, 0),time(19, 0), date(2025, 12, 20), date(2025, 12, 20), 'Uttara Club, Dhaka',            date(2025, 11, 15),1, 'Social',  'public',  u5, uttara),
            ('Rabindra Music Evening',     'Classical Rabindra Sangeet concert for seniors.',           time(17, 0),time(20, 0), date(2025, 11, 25), date(2025, 11, 25), 'Bangladesh Shilpakala Academy', date(2025, 10, 20),1, 'Culture', 'public',  u7, dhanmondi),
            ('Diabetes Awareness Camp',    'Free diabetes screening and counselling for elderly.',      time(9, 0), time(14, 0), date(2025, 12, 5),  date(2025, 12, 5),  'Mirpur DNCC Community Center',  date(2025, 11, 1), 1, 'Health',  'public',  u6, mirpur),
            ('Book Fair for Seniors',      'Curated book fair with discounts for 60+ citizens.',        time(10, 0),time(18, 0), date(2026, 1, 15),  date(2026, 1, 17),  'Bangla Academy, Dhaka',         date(2025, 12, 1), 0, 'Culture', 'public',  u8, motijheel),
            ('Elderly Yoga Workshop',      '3-day yoga workshop designed for senior citizens.',         time(7, 0), time(9, 0),  date(2026, 2, 1),   date(2026, 2, 3),   'Dhanmondi Club, Dhaka',         date(2026, 1, 1),  0, 'Health',  'private', u2, dhanmondi),
        ]

        event_objs = []
        for title, desc, stime, etime, sdate, edate, addr, cdate, approve, etype, priv, creator, thana_e in events_data:
            ev, _ = Event.objects.get_or_create(Event_title=title, defaults={
                'Description': desc, 'start_time': stime, 'end_time': etime,
                'start_date': sdate, 'end_date': edate, 'Address': addr,
                'create_date': cdate, 'Approve': approve, 'E_type': etype,
                'privacy': priv, 'E_creator': creator, 'Thana': thana_e
            })
            event_objs.append(ev)

        join_event_data = [
            (event_objs[0], [(u2, 1, 0), (u3, 1, 0), (u4, 1, 0), (u5, 1, 0), (u6, 0, 0)]),
            (event_objs[1], [(u1, 1, 0), (u2, 1, 0), (u7, 1, 0), (u8, 0, 0)]),
            (event_objs[2], [(u2, 1, 0), (u3, 1, 0), (u4, 1, 0), (u5, 1, 0), (u6, 1, 0), (u7, 1, 0)]),
            (event_objs[3], [(u1, 1, 0), (u3, 1, 0), (u4, 1, 0), (u6, 1, 0)]),
            (event_objs[4], [(u2, 1, 0), (u7, 1, 0), (u11, 1, 0), (u12, 0, 0)]),
        ]
        for event, members in join_event_data:
            for mem, approve, cancel in members:
                JoinEvent.objects.get_or_create(EventID=event, Member=mem, defaults={'Approve': approve, 'cancel': cancel})

        self.stdout.write(self.style.SUCCESS('  ✓ Events done'))

                                                                            
                                                  
                                                                            
        self.stdout.write('💊 Creating medications...')

        meds = [
            (u1, date(2025, 1, 1),  date(2026, 12, 31), 'After meal', 'After', 1, 1, 0, 'Take with water', 'Amlodipine 5mg'),
            (u1, date(2025, 1, 1),  date(2026, 12, 31), 'After meal', 'After', 0, 1, 0, 'Take after breakfast', 'Atorvastatin 10mg'),
            (u2, date(2025, 3, 1),  date(2026, 6, 30),  'After meal', 'After', 1, 1, 1, 'Must take with food', 'Metformin 500mg'),
            (u2, date(2025, 3, 1),  date(2026, 6, 30),  '20mg',       'After', 0, 1, 0, 'For acid reflux', 'Omeprazole 20mg'),
            (u3, date(2025, 2, 1),  date(2026, 5, 31),  '50mg',       'After', 1, 0, 1, 'For arthritis pain', 'Diclofenac 50mg'),
            (u4, date(2025, 4, 1),  date(2025, 12, 31), '100mg',      'After', 0, 1, 0, 'For gout', 'Allopurinol 100mg'),
            (u5, date(2025, 5, 1),  date(2026, 4, 30),  '0.5mg',      'Before','1', 0, 1, 'Take at night', 'Clonazepam 0.5mg'),
            (u6, date(2025, 6, 1),  date(2026, 5, 31),  '1000IU',     'After', 0, 1, 0, 'For bone health', 'Vitamin D3'),
            (u7, date(2025, 1, 15), date(2026, 1, 14),  '100mcg',     'Before','0', 0, 0, 'Inhaler for asthma', 'Salbutamol Inhaler'),
            (u8, date(2025, 2, 1),  date(2026, 2, 28),  '5mg',        'After', 1, 0, 1, 'For blood pressure', 'Amlodipine 5mg'),
        ]
        for user, sdate, edate, dose, after, night, morning, noon, note, med_name in meds:
            Medication.objects.get_or_create(user=user, med_name=med_name, defaults={
                'meds_start_date': sdate, 'meds_end_date': edate, 'dose': dose,
                'after': after, 'night': int(night), 'morning': int(morning),
                'noon': int(noon), 'note': note
            })

                    
        med_alerts = [
            (u1, time(8, 0),  time(13, 0), time(21, 0), 30, 'Time to take your Amlodipine!'),
            (u2, time(7, 30), time(12, 30),time(20, 30), 45, 'Time for your Metformin with food!'),
            (u3, time(9, 0),  time(14, 0), time(22, 0), 60, 'Arthritis medication time!'),
            (u4, time(8, 0),  time(0, 0),  time(21, 0), 30, 'Take your Allopurinol!'),
            (u5, time(0, 0),  time(0, 0),  time(22, 0), 0,  'Night medication reminder!'),
        ]
        for user, morning_t, noon_t, night_t, interval, msg in med_alerts:
            MedAlert.objects.get_or_create(userid=user, defaults={
                'morning': morning_t, 'noon': noon_t, 'night': night_t,
                'interval': interval, 'alert_message': msg
            })

                   
        done_dates = [date(2025, 6, 1), date(2025, 6, 2), date(2025, 6, 3), date(2025, 6, 4), date(2025, 6, 5)]
        for d in done_dates:
            DoneMed.objects.get_or_create(user=u1, done_date=d, defaults={'done_time': '08:00'})
            DoneMed.objects.get_or_create(user=u2, done_date=d, defaults={'done_time': '07:30'})

        self.stdout.write(self.style.SUCCESS('  ✓ Medications done'))

                                                                            
                           
                                                                            
        self.stdout.write('💬 Creating chat messages...')

        now = timezone.now()
        chat_data = [
            (u1, u2, 'আপু কেমন আছেন? অনেক দিন দেখা হয়নি।',                                      now - timedelta(days=5, hours=3)),
            (u2, u1, 'ভালো আছি ভাই। আপনি কেমন আছেন? শরীর ভালো?',                              now - timedelta(days=5, hours=2)),
            (u1, u2, 'আলহামদুলিল্লাহ। পরের শুক্রবার পার্কে যাবেন কি?',                          now - timedelta(days=5, hours=1)),
            (u2, u1, 'অবশ্যই! সকাল ৭টায় রমনা পার্কে।',                                          now - timedelta(days=5)),
            (u1, u3, 'সালমা আপু, আপনার বাগানের গোলাপ দেখতে চাই!',                              now - timedelta(days=3, hours=5)),
            (u3, u1, 'হা হা ভাই, আসুন। চায়ের সাথে বাগান দেখাব।',                               now - timedelta(days=3, hours=4)),
            (u2, u3, 'আপু, painting workshop কবে শুরু হচ্ছে?',                                  now - timedelta(days=2, hours=6)),
            (u3, u2, 'আগামী মাসে। আপনাকে অবশ্যই নিয়ে যাব।',                                    now - timedelta(days=2, hours=5)),
            (u4, u5, 'ভাই, ট্রিপের ব্যাপারে কথা বলা দরকার।',                                    now - timedelta(days=1, hours=8)),
            (u5, u4, 'হ্যাঁ ভাই, Cox\'s Bazar যাওয়ার plan final করা দরকার।',                   now - timedelta(days=1, hours=7)),
            (u1, u4, 'মোতিন ভাই! আজকের walking session কেমন হলো?',                             now - timedelta(hours=10)),
            (u4, u1, 'চমৎকার! ৫ কিলোমিটার হেঁটেছি। শরীর হালকা লাগছে।',                         now - timedelta(hours=9)),
            (u6, u7, 'Roksana আপু, আপনার গান শুনতে মন চাইছে।',                                 now - timedelta(hours=6)),
            (u7, u6, 'হা হা Kamal ভাই! আজ সন্ধ্যায় group-এ একটু গান শেয়ার করব।',             now - timedelta(hours=5)),
            (u3, u7, 'গানের club-এ কবে আসবেন?',                                                  now - timedelta(hours=3)),
            (u7, u3, 'এই সপ্তাহান্তেই যাব ইনশাআল্লাহ।',                                         now - timedelta(hours=2)),
        ]

        for sender, receiver, msg, msg_time in chat_data:
            Chat.objects.get_or_create(Sender=sender, Receiver=receiver, Msg=msg, defaults={'message_time': msg_time})

        self.stdout.write(self.style.SUCCESS('  ✓ Chats done'))

                                                                            
                           
                                                                            
        self.stdout.write('🔔 Creating notifications...')

        notis = [
                                                   
            ('Bondhu', 'sent you a friend request',   u3,  u8,  '0'),
            ('Bondhu', 'accepted your friend request', u2, u1,  '1'),
            ('Bondhu', 'sent you a friend request',   u6,  u12, '0'),
            ('Bondhu', 'sent you a friend request',   u9,  u11, '0'),
            ('Event',  'invited you to Senior Health Fair 2025', u1, u2, '0'),
            ('Event',  'invited you to Rabindra Music Evening',  u7, u2, '0'),
            ('Trip',   'invited you to Cox\'s Bazar Senior Tour', u1, u3, '1'),
            ('Trip',   'invited you to Sylhet Tea Garden Visit',  u3, u2, '0'),
            ('Walk',   'invited you to Ramna Park Morning Walk',  u1, u4, '1'),
            ('Bondhu', 'sent you a friend request',   u4,  u7,  '0'),
            ('Comment','commented on your post',      u2,  u1,  '1'),
            ('Comment','commented on your post',      u3,  u1,  '1'),
            ('Comment','liked your post',             u4,  u2,  '0'),
            ('Bondhu', 'sent you a friend request',   u2, u10,  '0'),
            ('Event',  'invited you to Elderly Yoga Workshop',   u2, u3, '0'),
            ('Trip',   'joined your Sundarbans Cruise trip',     u4,  u2, '1'),
        ]
        for ntype, nmsg, sender, receiver, status in notis:
            Notification.objects.get_or_create(
                noti_type=ntype, noti_sender=sender, noti_receiver=receiver,
                defaults={'noti_msg': nmsg, 'noti_status': status}
            )

        self.stdout.write(self.style.SUCCESS('  ✓ Notifications done'))

                                                                            
                       
                                                                            
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('══════════════════════════════════════════════════'))
        self.stdout.write(self.style.SUCCESS('  ✅  All seed data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('══════════════════════════════════════════════════'))
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('  🔐 LOGIN CREDENTIALS'))
        self.stdout.write(self.style.HTTP_INFO('  ─────────────────────────────────────────────'))
        self.stdout.write(self.style.WARNING(  '  Admin (Django panel + API):'))
        self.stdout.write(self.style.WARNING(  '    username: abdur_admin      password: admin1234'))
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('  Regular users (password: Pass@1234):'))
        users_table = [
            ('rahim_sir',      'Rahim Uddin',     'Male',   'Dhanmondi'),
            ('fatema_begum',   'Fatema Begum',    'Female', 'Mirpur'),
            ('salma_khan',     'Salma Khan',      'Female', 'Gulshan'),
            ('motin_bhai',     'Abdul Motin',     'Male',   'Uttara'),
            ('nuha_akter',     'Nuha Akter',      'Female', 'Rampura'),
            ('kamal_hossain',  'Kamal Hossain',   'Male',   'Mohammadpur'),
            ('roksana_begum',  'Roksana Begum',   'Female', 'Badda'),
            ('jahangir_alam',  'Jahangir Alam',   'Male',   'Rajshahi'),
            ('maya_devi',      'Maya Devi',       'Female', 'Narayanganj'),
            ('shiraj_uddin',   'Shiraj Uddin',    'Male',   'Sylhet'),
            ('bilkis_khanam',  'Bilkis Khanam',   'Female', 'Khulna'),
            ('anwar_hossain',  'Anwar Hossain',   'Male',   'Comilla'),
        ]
        for uname, name, gender, area in users_table:
            self.stdout.write(f'    {uname:<22} {name:<20} {gender:<8} {area}')
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('  📊 DATA SUMMARY'))
        self.stdout.write(self.style.HTTP_INFO('  ─────────────────────────────────────────────'))
        self.stdout.write(f'    Users (Owner):      {Owner.objects.count()}')
        self.stdout.write(f'    Friendships:        {Friend.objects.count()} ({Friend.objects.filter(is_fnf=1).count()} confirmed, {Friend.objects.filter(is_fnf=0).count()} pending)')
        self.stdout.write(f'    Blog Posts:         {Blog.objects.count()}')
        self.stdout.write(f'    Comments:           {Comment.objects.count()}')
        self.stdout.write(f'    Upvotes:            {Upvote.objects.count()}')
        self.stdout.write(f'    Groups:             {CommunityGroup.objects.count()}')
        self.stdout.write(f'    Group Posts:        {GroupPost.objects.count()}')
        self.stdout.write(f'    Trips:              {Trip.objects.count()}')
        self.stdout.write(f'    Events:             {Event.objects.count()}')
        self.stdout.write(f'    Walks:              {Walk.objects.count()}')
        self.stdout.write(f'    Medications:        {Medication.objects.count()}')
        self.stdout.write(f'    Chat Messages:      {Chat.objects.count()}')
        self.stdout.write(f'    Notifications:      {Notification.objects.count()}')
        self.stdout.write(self.style.SUCCESS('══════════════════════════════════════════════════'))
