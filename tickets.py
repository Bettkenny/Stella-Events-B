from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, Ticket, User

class TicketResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')

    def get(self, ticket_id=None):
        if ticket_id is None:
            tickets = Ticket.query.all()
            return [{"id": ticket.id, "event_id": ticket.event_id, "user_id": ticket.user_id,
                     "quantity": ticket.quantity, "ticket_price": ticket.ticket_price,
                     "image_url": ticket.image_url,
                     "tickets_available": ticket.tickets_available,
                     "tickets_purchased": ticket.tickets_purchased} for ticket in tickets]

        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return {"message": "Ticket not found."}, 404

        return {
            "id": ticket.id,
            "event_id": ticket.event_id,
            "user_id": ticket.user_id,
            "quantity": ticket.quantity,
            "ticket_price": ticket.ticket_price,
            "image_url": ticket.image_url,
            "tickets_available": ticket.tickets_available,
            "tickets_purchased": ticket.tickets_purchased
        }


    def patch(self, ticket_id):
        try:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"message": "Ticket not found."}, 404

            data = request.get_json()
            ticket.quantity = data.get('quantity', ticket.quantity)
            ticket.ticket_price = data.get('ticket_price', ticket.ticket_price)
            ticket.image_url = data.get('image_url', ticket.image_url)
            ticket.tickets_available = data.get('tickets_available', ticket.tickets_available)
            ticket.tickets_purchased = data.get('tickets_purchased', ticket.tickets_purchased)
            db.session.commit()

            # Return the details of the updated ticket
            return {
                "message": "Ticket updated successfully.",
                "ticket": {
                    "id": ticket.id,
                    "event_id": ticket.event_id,
                    "user_id": ticket.user_id,
                    "quantity": ticket.quantity,
                    "ticket_price": ticket.ticket_price,
                    "image_url": ticket.image_url,
                    "tickets_available": ticket.tickets_available,
                    "tickets_purchased": ticket.tickets_purchased
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

class AdminTicketResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('event_id', type=int, required=True, help='Event ID cannot be blank.')
    parser.add_argument('quantity', type=int, required=True, help='Quantity cannot be blank')

    @jwt_required()  # Requires admin privileges
    def post(self):
        try:
            data = request.get_json()
            event_id = data.get('event_id')
            quantity = data.get('quantity')

            if not event_id or not quantity:
                return {"error": "Event ID and quantity are required."}, 400

            current_user = User.query.filter_by(username=get_jwt_identity()).first()
            if not current_user or current_user.role != 'admin':
                return {"message": "Access denied. Admins only."}, 403

            new_ticket = Ticket(event_id=event_id, user_id=current_user.id,
                                quantity=quantity, ticket_price=data.get('ticket_price'),
                                image_url=data.get('image_url'),
                                tickets_available=data.get('tickets_available'),
                                tickets_purchased=data.get('tickets_purchased'))

            db.session.add(new_ticket)
            db.session.commit()

            # Return the details of the created ticket
            return {
                "message": "Ticket added successfully.",
                "ticket": {
                    "id": new_ticket.id,
                    "event_id": new_ticket.event_id,
                    "user_id": new_ticket.user_id,
                    "quantity": new_ticket.quantity,
                    "ticket_price": new_ticket.ticket_price,
                    "image_url": new_ticket.image_url,
                    "tickets_available": new_ticket.tickets_available,
                    "tickets_purchased": new_ticket.tickets_purchased
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()  # Requires admin privileges
    def put(self, ticket_id):
        try:
            current_user = User.query.filter_by(username=get_jwt_identity()).first()
            if not current_user or current_user.role != 'admin':
                return {"message": "Access denied. Admins only."}, 403

            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"message": "Ticket not found."}, 404

            data = request.get_json()
            ticket.quantity = data.get('quantity')
            ticket.ticket_price = data.get('ticket_price')
            ticket.image_url = data.get('image_url')
            ticket.tickets_available = data.get('tickets_available')
            ticket.tickets_purchased = data.get('tickets_purchased')
            db.session.commit()

            # Return the details of the updated ticket
            return {
                "message": "Ticket updated successfully.",
                "ticket": {
                    "id": ticket.id,
                    "event_id": ticket.event_id,
                    "user_id": ticket.user_id,
                    "quantity": ticket.quantity,
                    "ticket_price": ticket.ticket_price,
                    "image_url": ticket.image_url,
                    "tickets_available": ticket.tickets_available,
                    "tickets_purchased": ticket.tickets_purchased
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500

    @jwt_required()  # Requires admin privileges
    def delete(self, ticket_id):
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if not current_user or current_user.role != 'admin':
            return {"message": "Access denied. Admins only."}, 403

        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return {"message": "Ticket not found."}, 404

        db.session.delete(ticket)
        db.session.commit()
        return {"message": "Ticket deleted successfully."}