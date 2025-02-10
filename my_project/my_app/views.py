from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile ,Quiz
from .forms import LoginForm
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User , auth
from django.contrib.auth import login
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .models import Category

def welcome(request):
    return render(request, 'welcome.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "User Already Exist")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Used. Try to Login. ")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username , email=email, password= password)
                user.save()

                # login the user to login page 
                user_login = auth.authenticate(username=username, password=password )
                auth.login(request , user_login)

                #create profile for new user
                user_model =User.objects.get(username=username)
                new_profile = Profile.objects.create( user=user_model, email_address=email)
                new_profile.save()
                return redirect('profile', username)



        else:
            messages.info(request, "Password Not Matching")
            return redirect('register')

    context = {}
    return render(request, 'register.html')


@login_required(login_url='login')
def profile(request, username):

    user_object= User.objects.get(username=username)
    user_profile= Profile.objects.get(user=user_object)

    context = {"user_profile":user_profile}
    return render(request , 'profile.html', context )


def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate( username=username, password=password )
        if user is not None:
            auth.login(request , user)
            return redirect('profile', username)
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html' )
    

@login_required(login_url='login')
def logout(request):
    auth.logout(request)    
    return redirect('login')



@login_required(login_url='login')
def all_quiz_view(request):
    user_object = User.objects.get(username=request.user)
    user_profile  = Profile.objects.get(user=user_object)
      # Fixed the typo here
    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()

    context = {"user_profile": user_profile, "quizzes": quizzes, "categories": categories}
    return render(request, 'all_quiz.html', context)

@login_required(login_url='login')
def quiz_view(request, quiz_id): 
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quiz = Quiz.objects.filter(id=quiz_id).first()

    if quiz is not None:
        # Debugging
        print(f"Quiz: {quiz.title}")
        print(f"Questions: {quiz.question_set.all()}")

        context = {"user_profile": user_profile, "quiz": quiz}
    else:
        return redirect('all_quiz')

    return render(request, 'quiz.html', context)


# def submit_quiz(request, quiz_id):
#     quiz = get_object_or_404(Quiz, id=quiz_id)
    
#     if request.method == 'POST':
#         # Process answers here
#         # For example, you can access answers with request.POST.get('q1') to get the selected option for question 1
#         # Logic to save or process answers here
        
#         return redirect('quiz:thank_you')  # Redirect to a thank-you page or a results page

#     return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})

# from .models import Question

# from .serializers import StudentSerializer

# from templates import index.html

# class StudentApi(APIView):
#     def get(self, request):
#         queryset = Student.objects.all()  
#         serializer = StudentSerializer(queryset, many=True)
#         return Response({
#             "status" :True,
#             "data": serializer.data
#         })


# # def home(request):
#     context = {}
#     qs = Question.objects.all()


#     if 'qnumber' not in request.session:
#         request.session['qnumber'] = 0
#         request.session['score'] = 0

#     if request.session['qnumber'] >= len(qs):
#         return redirect('leaderboard')

#     current_question = qs[request.session['qnumber']]
#     print("Options for the current question:", current_question.op1, current_question.op2, current_question.op3, current_question.op4)

#     context['question'] = current_question.text
#     context['op1'] = current_question.op1
#     context['op2'] = current_question.op2
#     context['op3'] = current_question.op3
#     context['op4'] = current_question.op4

#     if request.method == "POST":
#         target = request.POST.get('target')

#         if target == 'optionclick':
#             answervalue = request.POST.get('answervalue')

#              # If the selected answer is correct, increment the score
#             if current_question.answer == answervalue:
#                 request.session['score'] += 1

#             # Move to the next question                
#             request.session['qnumber'] += 1

#             # If there are more questions, fetch the next question
#             if request.session['qnumber'] < len(qs):

#                 current_question = qs[request.session['qnumber']]
#                 context['question'] = current_question.text
#                 context['op1'] = current_question.op1
#                 context['op2'] = current_question.op2
#                 context['op3'] = current_question.op3
#                 context['op4'] = current_question.op4
#             else:
#                 # If no more questions, redirect to the leaderboard
#                 request.session['final_score'] = request.session['score']
#                 request.session['testcomplete']= "True"
#                 return redirect('result')

#     context['score'] = request.session['score']
#     return render(request, 'index.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')

def leaderboard(request):
    # Get the score from session
    final_score = request.session.get('final_score', 0)

    # Clear session values to reset the quiz for next time
    if 'qnumber' in request.session:
        del request.session['qnumber']
    if 'score' in request.session:
        del request.session['score']
    if 'final_score' in request.session:
        del request.session['final_score']

    # Pass the final score to the leaderboard context
    context = {
        'final_score': final_score,
        # Add any other leaderboard data if necessary
    }

    return render(request, 'leaderboard.html', context)

def adminpanel(request):
    if request.method == "POST":
        target = request.POST.get('target')
        if target == "add_question":
            question_text = request.POST.get('question')
            op1 = request.POST.get('op1')
            op2 = request.POST.get('op2')
            op3 = request.POST.get('op3')
            op4 = request.POST.get('op4')
            answer  = request.POST.get('answer')

            a = Question(text=question_text, op1=op1, op2=op2, op3=op3, answer=answer)   
            a.save()
        # if target == "optionclick":
        #     answervalue = request.POST.get('answervalue')
    return render(request, 'admin.html')
 
def result(request):
    if not 'testcomplete' in request.session.keys() or request.session['testcomplete'] != "True":
        return redirect('home')
    # Get the score from session
    final_score = request.session.get('final_score', 0)

    # Clear session values to reset the quiz for next time
    # if 'qnumber' in request.session:
    #     del request.session['qnumber']
    # if 'score' in request.session:
    #     del request.session['score']
    # if 'final_score' in request.session:
    #     del request.session['final_score']

    # Reset session data properly
    for key in ['qnumber', 'score', 'final_score', 'testcomplete']:
        request.session.pop(key, None)  # Safe removal

    context = {'final_score': final_score}
    return render(request, 'result.html', context)
    # # Pass the final score to the leaderboard context
    # context = {
    #     'final_score': final_score,
    #     # Add any other leaderboard data if necessary
    # }

    # return render(request, 'result.html', context)
