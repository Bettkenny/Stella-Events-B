from flask import request
from flask_restful import Resource, reqparse
from models import db, User, Event

class EventResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help='Title cannot be blank')
    parser.add_argument('description', type=str, required=True, help='Description cannot be blank')
    parser.add_argument('date', type=str, required=True, help='Date cannot be blank')
    parser.add_argument('location', type=str, required=True, help='Location cannot be blank')
    parser.add_argument('image_url', type=str)
    
    def get(self, event_id=None):
        if event_id is None:
            events = Event.query.all()
            return [{"id": event.id, "title": event.title, "description": event.description,
                     "date": event.date.isoformat(), "location": event.location,
                     "organizer_id": event.organizer_id, "image_url": event.image_url} for event in events]

        event = Event.query.get(event_id)
        if not event:
            return {"message": "Event not found."}, 404

        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date.isoformat(),
            "location": event.location,
            "organizer_id": event.organizer_id,
            "image_url": event.image_url
        }

    def post(self):
        try:
            data = request.get_json()

            new_event = Event(
                title=data['title'],
                description=data['description'],
                date=data['date'],
                location=data['location'],
                organizer_id=current_user.id,
                image_url=data.get('image_url')
            )

            db.session.add(new_event)
            db.session.commit()

            return {
                "message": "Event added successfully.",
                "event": {
                    "id": new_event.id,
                    "title": new_event.title,
                    "description": new_event.description,
                    "date": new_event.date.isoformat(),
                    "location": new_event.location,
                    "organizer_id": new_event.organizer_id,
                    "image_url": new_event.image_url
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

class AdminEventResource(Resource):
    def post(self):
        try:
            current_user = User.query.filter_by(username=get_jwt_identity()).first()

            if current_user.role != 'admin':
                return {"error": "Access denied. Admins only."}, 403

            data = request.get_json()

            new_event = Event(
                title=data['title'],
                description=data['description'],
                date=data['date'],
                location=data['location'],
                organizer_id=data['organizer_id'],
                image_url=data.get('image_url')
            )

            db.session.add(new_event)
            db.session.commit()

            return {
                "message": "Event added successfully.",
                "event": {
                    "id": new_event.id,
                    "title": new_event.title,
                    "description": new_event.description,
                    "date": new_event.date.isoformat(),
                    "location": new_event.location,
                    "organizer_id": new_event.organizer_id,
                    "image_url": new_event.image_url
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, event_id):
        try:
            current_user = User.query.filter_by(username=get_jwt_identity()).first()
            event = Event.query.get(event_id)
            
            if not event:
                return {"message": "Event not found."}, 404
            
            if current_user.role != 'admin':
                return {"message": "Access denied. Admins only."}, 403

            data = request.get_json()
            event.title = data['title']
            event.description = data['description']
            event.date = data['date']
            event.location = data['location']
            event.organizer_id = data['organizer_id']
            event.image_url = data.get('image_url')

            db.session.commit()

            return {
                "message": "Event updated successfully.",
                "event": {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "date": event.date.isoformat(),
                    "location": event.location,
                    "organizer_id": event.organizer_id,
                    "image_url": event.image_url
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, event_id):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        event = Event.query.get(event_id)

        if not event:
            return {"message": "Event not found."}, 404

        if current_user.role != 'admin':
            return {"message": "Access denied. Admins only."}, 403

        db.session.delete(event)
        db.session.commit()
        
        return {"message": "Event deleted successfully."}