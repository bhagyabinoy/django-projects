from django.core.mail import send_mail
from calorie_tracker.celery import app
import pdfkit
from django.template.loader import render_to_string
from .utils import accounts_utils,logs_utils
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import pdfkit
from .models import User
from .models import *
import datetime
from calorie_tracker.celery import app   

@app.task
def send_password_reset_email(user_email, reset_link):
    subject = 'Password Reset'
    message = f'Click the following link to reset your password: {reset_link}'
    from_email = 'useruser8118@gmail.com'
    send_mail(subject, message, from_email, user_email)



@app.task(name='convert_pdf_and_send')
def convert_pdf_and_send():
    print("export to pdf")
    users = User.objects.all()
    date=datetime.date.today()
    for user in users:
        consumed_list = list(accounts_utils.consumedlist_by_date(user,date))   
        food_id_list = [x[0] for x in consumed_list]
        calories_list = [x[2] for x in consumed_list]
        quantity_list = [x[1] for x in consumed_list]
        date_list = [x[3] for x in consumed_list]
        food_name_list=[]
        for i in food_id_list:
            food_name_list.append(list(FoodItem.objects.values_list('name', flat=True).filter(id=i)))
        flat_list = [item for sublist in food_name_list for item in sublist]
        foodlist = list(zip(flat_list, calories_list, quantity_list, date_list))
        net_calories = sum(calories_list)
        table_data={}
        table_data['foodlist'] = foodlist
        table_data['net_calories'] = net_calories
        html_string = render_to_string('pdfsheet.html', table_data)
        result = pdfkit.from_string(html_string, False)
        
        # Send the PDF via email
        subject = 'Food List PDF'
        body = "Please find the attached PDF of your today's calorie log."
        from_email = 'useruser8118@gmail.com'
        to_email = [user.email]
        print(to_email)
        email_message = EmailMessage(subject, body, from_email, to_email)
        email_message.attach(filename='foodlist.pdf', content=result, mimetype='application/pdf')
        email_message.send()
        print("mail sent succesfully")