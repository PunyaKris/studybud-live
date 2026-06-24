from datetime import timedelta
from random import choice, randint, sample
from django.utils import timezone
from base.models import User, Topic, Room, Message

PASSWORD = "StudyBuddy123"

# WIPE DATABASE
Message.objects.all().delete()
Room.objects.all().delete()
Topic.objects.all().delete()
User.objects.all().delete()

# LOGIN ACCOUNTS
# admin@studybuddy.com -
# rahul.sharma@studybuddy.com -
# priya.verma@studybuddy.com
# aman.preet@studybuddy.com
# neha.singh@studybuddy.com
# aditya.mehta@studybuddy.com
# riya.kapoor@studybuddy.com -
# arjun.nair@studybuddy.com -
# kavya.iyer@studybuddy.com
# rohit.yadav@studybuddy.com -
# sneha.joshi@studybuddy.com -
# vivek.patel@studybuddy.com
# ananya.rao@studybuddy.com
# karan.malhotra@studybuddy.com -
# meera.kulkarni@studybuddy.com -
# siddharth.jain@studybuddy.com
# Password for all users: StudyBuddy123

admin = User.objects.create_superuser(
    username="admin",
    email="admin@studybuddy.com",
    password=PASSWORD,
)
admin.name = "Punya Mohan"
admin.bio = "Creator of StudyBuddy. Interested in software engineering, physics and building communities around learning."
admin.save()
admin.avatar = 'admin dp.jpeg'
admin.save()

users_data = [
    ("Rahul Sharma", "rahul.sharma@studybuddy.com", "Full-stack web developer exploring Django and React."),
    ("Priya Verma", "priya.verma@studybuddy.com", "Machine learning enthusiast who enjoys building small AI projects."),
    ("Aman Gupta", "aman.gupta@studybuddy.com", "Backend developer interested in APIs and databases."),
    ("Neha Singh", "neha.singh@studybuddy.com", "Physics lover fascinated by cosmology and quantum mechanics."),
    ("Aditya Mehta", "aditya.mehta@studybuddy.com", "Engineering student balancing coding and research."),
    ("Riya Kapoor", "riya.kapoor@studybuddy.com", "Interested in astrophysics and scientific communication."),
    ("Arjun Nair", "arjun.nair@studybuddy.com", "Problem solver who enjoys mathematics and programming."),
    ("Kavya Iyer", "kavya.iyer@studybuddy.com", "Passionate about optics and modern physics."),
    ("Rohit Yadav", "rohit.yadav@studybuddy.com", "Mechanical engineering student exploring fluid mechanics."),
    ("Sneha Joshi", "sneha.joshi@studybuddy.com", "Organic chemistry enthusiast and tutor."),
    ("Vivek Patel", "vivek.patel@studybuddy.com", "Interested in thermodynamics and energy systems."),
    ("Ananya Rao", "ananya.rao@studybuddy.com", "Loves calculus, modelling and data science."),
    ("Karan Malhotra", "karan.malhotra@studybuddy.com", "Exploring AI research and deep learning."),
    ("Meera Kulkarni", "meera.kulkarni@studybuddy.com", "Enjoys discussing physics concepts and experiments."),
    ("Siddharth Jain", "siddharth.jain@studybuddy.com", "Curious learner interested in both CS and science."),
]

users = []
for name, email, bio in users_data:
    username = email.split("@")[0]

    u = User.objects.create_user(
        username=username,
        email=email,
        password=PASSWORD,
    )
    u.name = name
    u.bio = bio
    u.save()
    users.append(u)

# Set avatars for specific users
user_map = {u.email: u for u in users}

user_map['sneha.joshi@studybuddy.com'].avatar = 'images (1).jpeg'
user_map['sneha.joshi@studybuddy.com'].save()

user_map['rahul.sharma@studybuddy.com'].avatar = 'Max.jpeg'
user_map['rahul.sharma@studybuddy.com'].save()

user_map['meera.kulkarni@studybuddy.com'].avatar = 'images (3).jpeg'
user_map['meera.kulkarni@studybuddy.com'].save()

user_map['rohit.yadav@studybuddy.com'].avatar = 'images (5).jpeg'
user_map['rohit.yadav@studybuddy.com'].save()

user_map['priya.verma@studybuddy.com'].avatar = 'name.webp'
user_map['priya.verma@studybuddy.com'].save()

user_map['arjun.nair@studybuddy.com'].avatar = 'images (4).jpeg'
user_map['arjun.nair@studybuddy.com'].save()

user_map['vivek.patel@studybuddy.com'].avatar = 'VHW1965_2007417871_m.jpg'
user_map['vivek.patel@studybuddy.com'].save()

user_map['aditya.mehta@studybuddy.com'].avatar = 'images.jpeg'
user_map['aditya.mehta@studybuddy.com'].save()

TOPICS = {
    "Web Development": ["Django Beginners Hub", "React Frontend Discussions", "Building Full-Stack Projects", "API Design & Backend Development"],
    "Machine Learning": ["First ML Project", "Neural Networks & Deep Learning", "Kaggle Competitions", "AI Research Papers Club"],
    "Astrophysics": ["Black Holes & Event Horizons", "James Webb Space Telescope Discoveries", "Exoplanets and Life Beyond Earth"],
    "Multivariable Calculus": ["Partial Derivatives Help Desk", "Vector Calculus Discussions"],
    "Electromagnetism": ["Maxwell's Equations Simplified", "Electric Fields & Potentials", "Electromagnetism Problem Solving"],
    "Thermodynamics": ["Entropy and the Second Law", "Heat Engines & Refrigeration"],
    "Quantum Physics": ["Quantum Mechanics for Beginners", "Double Slit Experiment Discussion", "Schrodinger Equation Study Group", "Quantum Computing Concepts"],
    "Organic Chemistry": ["Reaction Mechanisms Made Easy", "Organic Chemistry Problem Solving"],
    "Fluid Mechanics": ["Bernoulli Equation Applications", "Fluid Flow and Pipe Systems"],
    "Optics": ["Mirrors and Lens Problems", "Human Eye and Vision", "Optical Instruments Discussion"],
}

message_bank = [
    "Can someone explain the intuition behind this concept?",
    "I found a great resource on this topic yesterday.",
    "That explanation makes much more sense now.",
    "Has anyone solved a similar problem before?",
    "I think the key assumption is often overlooked.",
    "Thanks, that cleared up my confusion.",
    "Interesting point. I had not considered that perspective.",
    "Can you share the derivation or reasoning?",
    "I tried implementing this and got different results.",
    "This topic is much easier once you visualize it.",
]

# Featured hosts for special rooms
featured_hosts = [
    user_map['sneha.joshi@studybuddy.com'],
    user_map['rahul.sharma@studybuddy.com'],
    user_map['meera.kulkarni@studybuddy.com'],
    user_map['aman.gupta@studybuddy.com'],
    user_map['rohit.yadav@studybuddy.com'],
    user_map['siddharth.jain@studybuddy.com'],
    user_map['priya.verma@studybuddy.com'],
]

featured_room_counter = 0

for topic_name, room_names in TOPICS.items():
    topic = Topic.objects.create(name=topic_name)

    for room_name in room_names:
        if featured_room_counter < len(featured_hosts):
            host = featured_hosts[featured_room_counter]
        else:
            host = choice(users)

        room = Room.objects.create(
            host=host,
            topic=topic,
            name=room_name,
            description=f"Discussion room for {room_name}. Students collaborate, ask questions and share resources.",
        )

        room_created = timezone.now() - timedelta(days=randint(1, 30), hours=randint(0, 23))
        Room.objects.filter(id=room.id).update(
            create=room_created,
            update=room_created,
        )

        if featured_room_counter < len(featured_hosts):
            featured_time = timezone.now() - timedelta(minutes=featured_room_counter)
            Room.objects.filter(id=room.id).update(update=featured_time)
            featured_room_counter += 1

        participants = sample(users, randint(5, min(10, len(users))))
        for p in participants:
            room.participants.add(p)

        count = randint(8, 16)
        for _ in range(count):
            author = choice(participants)
            msg = Message.objects.create(
                user=author,
                room=room,
                body=choice(message_bank),
            )

            max_age_seconds = max(1, int((timezone.now() - room_created).total_seconds()))
            random_offset = randint(0, max_age_seconds)
            message_time = room_created + timedelta(seconds=random_offset)

            Message.objects.filter(id=msg.id).update(
                create=message_time,
                update=message_time,
            )

print("Demo dataset created successfully.")

