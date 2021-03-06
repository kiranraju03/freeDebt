import pickle
import numpy as np
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import UserPersonalDetails
from . import db

# from flask_login import login_required, current_user

survey = Blueprint('survey', __name__)


@survey.route('/survey')
def career():
    return render_template('surveypages/survey.html')


@survey.route('/survey', methods=['POST'])
def careerPost():
    occupation = request.form['occupation']
    print(occupation)

    if occupation == "Student":
        occupation = 1
    else:
        occupation = 0

    print(occupation)

    martial_status = request.form['marital']
    print(martial_status)

    # Not Captured
    education = request.form.get('education')
    print(education)

    # ENSW
    regionStates = {
        'North': [0, 1, 0],
        'South': [0, 0, 1],
        'East': [1, 0, 0],
        'West': [0, 0, 0]
    }

    region = request.form['region']
    print(region)
    regionEncoded = regionStates[region]
    print(regionEncoded)

    salary = request.form.get('salary', type=int)
    print(type(salary))
    print(salary)

    expense = request.form.get('expenses', type=int)
    print(type(expense))
    print(expense)

    savings = request.form.get('savings', type=int)
    print(type(savings))
    print(savings)

    goalType = request.form['goalname']
    print(goalType)


    # Student Loan form
    loan_amt = request.form.get('loan_amt', type=int)
    int_rate = request.form.get('int_rate', type=int)
    loan_span = request.form.get('loan_span', type=int)
    print(type(loan_amt))
    print(loan_amt)

    goal_name = request.form.get('goal_name')
    goal_amt = request.form.get('goal_amt', type=int)
    goal_span = request.form.get('goal_span', type=int)
    print(type(goal_amt))
    print(goal_amt)

    if goalType == "Student Loan":
        save_per_day = loan_amt / (loan_span * 30.417)
    else:
        save_per_day = goal_amt / (goal_span * 30.417)

    print("Saved per day : " + str(save_per_day))

    collective_values = [occupation, savings, expense] + regionEncoded

    with open(r"C:\Users\ravi\Documents\flaskFrontEnd\freedebtWeb\resources\B_Clust_PIK_0.p", "rb") as f:
        n_km = pickle.load(f)

    cluster = int(n_km.predict(np.array(collective_values).reshape(1, -1))[0])
    print("New cluster value : ")
    print(type(cluster))
    print(cluster)

    userpersonaldetails = UserPersonalDetails(occupation=occupation,
                                              martial_status=martial_status,
                                              education=education,
                                              region=region,
                                              salary=salary,
                                              monthly_exp=expense,
                                              savings=savings,
                                              goal_type=goalType,
                                              loan_amt=loan_amt,
                                              interest_value=int_rate,
                                              loan_span=loan_span,
                                              goal_name=goal_name,
                                              amt_value=goal_amt,
                                              goal_span=goal_span,
                                              save_per_day=save_per_day,
                                              cluster=cluster)

    db.session.add(userpersonaldetails)
    db.session.commit()

    return redirect(url_for('authorize.login'))

# invest = {
#     'high': {
#         ['axis', 5, 12.5, 5]
#         ['hdfc', 7, 8, 12]
#     },
#     'medium': {
#         ['axis', 5, 12.5, 5]
#         ['hdfc', 7, 8, 12]
#     }
# }
#
# invest = {
#     1:{
#         'name': 'axis',
#         'risk': 'high',
#     }
# }
