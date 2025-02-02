from flask import Blueprint, jsonify, redirect, render_template, request, abort, url_for, flash
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required, current_user
from App.controllers import Review, Staff, get_latest_karma_score, get_karma_by_id
from App.controllers.user import get_staff
from App.controllers.student import search_student
from App.controllers.voteRecords import get_vote_record_by_staff_and_review


from App.controllers.review import (
    get_reviews_by_staff,
    edit_review,
    delete_review,
    get_reviews,
    get_reviews_for_student, 
    get_review,
    addVote,
)

# Create a Blueprint for Review views
review_views = Blueprint("review_views", __name__, template_folder='../templates')

# Route to list all reviews (you can customize this route as needed)
@review_views.route('/review_details/<int:review_id>', methods=['GET', 'POST'])
@login_required
def view_review(review_id):
    if not isinstance(current_user, Staff):
        return "Unauthorized", 401
    
    if request.method == "POST":
        vote_type = request.json.get('action')
        # print(vote_type)
        addVote(review_id, current_user, vote_type)
        updated_review = get_review(review_id)
        return jsonify({'upvotes': updated_review.upvotes, 'downvotes': updated_review.downvotes})

    review = get_review(review_id)
    if review:
        return render_template('reviewdetails.html', review_id=review_id, review = review) 

# Route to get reviews by student ID
@review_views.route("/student/<string:student_id>/reviews", methods=["GET"])
@login_required
def get_reviews_of_student(student_id):
    if not isinstance(current_user, Staff):
      return "Unauthorized", 401
    
    student = search_student(student_id)
    if student:
        reviews = get_reviews_for_student(student_id)
        karma = get_karma_by_id(student.karmaID)
        return render_template('studentReviews.html', reviews = reviews, student = student, karma = karma)
    
    flash(f"{student_id} does not exist! Please enter a valid student ID")
    return redirect('/home')

# Route to get reviews by staff ID
@review_views.route("/staff/YourReviews", methods=["GET"])
@login_required
def get_reviews_from_staff():
    if not isinstance(current_user, Staff):
      return "Unauthorized", 401
    
    if get_staff(current_user.ID):
        reviews = get_reviews_by_staff(current_user.ID)
        return render_template('profile.html', reviews = reviews, staff = get_staff(current_user.ID), numReviews = len(reviews))

# # Route to edit a review
# @review_views.route("/reviews/edit/<int:review_id>", methods=["PUT"])
# @jwt_required()
# def review_edit(review_id):
#     review = get_review(review_id)
#     if not review:
#       return "Review not found", 404
      
    # if not jwt_current_user or not isinstance(jwt_current_user, Staff) or review.reviewerID != jwt_current_user.ID :
    #   return "You are not authorized to edit this review", 401

    # staff = get_staff(jwt_current_user.ID)

    # data = request.json

    # if not data['comment']:
    #     return "Invalid request data", 400
    
    # if data['isPositive'] not in (True, False):
    #     return jsonify({"message": f"invalid Positivity value  ({data['isPositive']}). Positive: true or false"}), 400

    # updated= edit_review(review, staff, data['isPositive'], data['comment'])
    # if updated: 
    #   return jsonify(review.to_json(), 'Review Edited'), 200
    # else:
    #   return "Error updating review", 400



# # Route to delete a review
# @review_views.route("/reviews/delete/<int:review_id>", methods=["DELETE"])
# @jwt_required()
# def review_delete(review_id):
#     review = get_review(review_id)
#     if not review:
#       return "Review not found", 404

    # if not jwt_current_user or not isinstance(jwt_current_user, Staff) or review.reviewerID != jwt_current_user.ID :
    #   return "You are not authorized to delete this review", 401

    # staff = get_staff(jwt_current_user.ID)
   
    # if delete_review(review, staff):
    #     return "Review deleted successfully", 200
    # else:
    #     return "Issue deleting review", 400

