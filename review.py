from flask import request
from flask_restful import Resource, reqparse
from models import db, Event, Review

class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('text', type=str, required=True, help='Text cannot be blank')

    def get(self, review_id=None):
        if review_id is None:
            reviews = Review.query.all()
            return [{"id": review.id, "text": review.text} for review in reviews]

        review = Review.query.get(review_id)
        if not review:
            return {"message": "Review not found."}, 404

        return {"id": review.id, "text": review.text}

    def post(self, event_id):
        try:
            data = request.get_json()
            event = Event.query.get(event_id)

            if not event:
                return {"message": "Event not found."}, 404

            new_review = Review(text=data['text'])
            event.reviews.append(new_review)
            db.session.commit()

            return {
                "message": "Review added successfully.",
                "review": {
                    "id": new_review.id,
                    "text": new_review.text
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500
        
    def put(self, review_id):
        try:
            review = Review.query.get(review_id)
            
            if not review:
                return {"message": "Review not found."}, 404

            data = request.get_json()
            review.text = data['text']
            db.session.commit()

            return {
                "message": "Review updated successfully.",
                "review": {
                    "id": review.id,
                    "text": review.text
                }
            }
        except Exception as e:
            return {"error": str(e)}, 500
        
    def delete(self, review_id):
        review = Review.query.get(review_id)

        if not review:
            return {"message": "Review not found."}, 404

        db.session.delete(review)
        db.session.commit()

        return {"message": "Review deleted successfully."}