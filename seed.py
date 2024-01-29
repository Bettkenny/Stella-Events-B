from app import app, db, bcrypt
from models import User, Event, Ticket, Review
from datetime import datetime


def seed_data():
    with app.app_context():
        db.create_all()

        print('Creating Users')
        # Create users
        hashed_password1 = bcrypt.generate_password_hash('Evans123').decode('utf-8')
        user1 = User(username='Evans', role='user', password=hashed_password1)

        hashed_password2 = bcrypt.generate_password_hash('Evanny254').decode('utf-8')
        user2 = User(username='Evanny', role='admin', password=hashed_password2)

        hashed_password3 = bcrypt.generate_password_hash('Event123').decode('utf-8')
        user1 = User(username='Event', role='admin', password=hashed_password1)

        hashed_password2 = bcrypt.generate_password_hash('Bett123').decode('utf-8')
        user2 = User(username='Bett', role='admin', password=hashed_password2)
        print('Creating Events')
        
        # Create events
        event1 = Event(
            title='PIKIKA BRUNCH FEST - 2024 KATAMBE EDITION',
            description='Tantalizing food delights and amazing dishes from top chefs...',
            date=datetime(2024, 2, 3, 12, 0, 0),
            location='TBA',
            organizer=user1,
            image_url='https://www.ticketsasa.com/components/com_enmasse/upload/WhatsApp_Image_2024-01-15_at_17.11.54.jpeg1705329054.jpg'
        )

        event2 = Event(
            title='Tribal Chic 2024',
            description='Tribe Hotel is once again ready to host Nairobis most glamorous annual fashion event...',
            date=datetime(2024, 2, 3, 18, 0, 0),
            location='Tribe Hotel Limited',
            organizer=user2,
            image_url='https://www.ticketsasa.com/components/com_enmasse/upload/Tribal_Chic_2024_post-_Ticketing_WITHOUT_QR_code-01.jpg1702996894.jpg'
        )
        # Create tickets
        print('Creating tickets')
        ticket1 = Ticket(
            event=event1,
            user=user1,
            quantity=5,
            ticket_price=2000.0,
            image_url='https://www.ticketsasa.com/components/com_enmasse/upload/WhatsApp_Image_2024-01-15_at_17.11.54.jpeg1705329054.jpg',
            tickets_available=100,
            tickets_purchased=0
        )

        ticket2 = Ticket(
            event=event2,
            user=user2,
            quantity=3,
            ticket_price=10000.0,
            image_url='https://www.ticketsasa.com/components/com_enmasse/upload/Tribal_Chic_2024_post-_Ticketing_WITHOUT_QR_code-01.jpg1702996894.jpg',
            tickets_available=50,
            tickets_purchased=0
        )
        print('Creating Reviews')
        # Create reviews
        review1 = Review(text='Great event!')
        review2 = Review(text='Awesome experience!')
        db.session.add_all([user1, user2, event1, event2, ticket1, ticket2, review1, review2])

        db.session.commit()

if __name__ == "__main__":
    seed_data()