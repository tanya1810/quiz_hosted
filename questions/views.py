from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AnswerForm
from .models import Questions, Answer
from home.models import User
import datetime
import xlwt


def question(request):
    if not request.user.is_authenticated:
        return redirect('login')

    ans=Answer.objects.all()
    for a in ans:
        if request.user == a.candidate :

            return render(request, 'home/ThankYou.html')
            break
    if not (request.user.start_time):
        u = request.user
        u.start_time = datetime.datetime.now()
        u.save()
    ques = Questions.objects.filter(slot=2).order_by("ques_no")

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            # f = form.save()
            # f.candidate = request.user
            form.instance.candidate = request.user
            form.save()
            return render(request, 'home/ThankYou.html')

    context = { 
        'form': AnswerForm(),
        'questions': ques,
        'end_time': (request.user.start_time + datetime.timedelta(minutes=15)).strftime("%B %d, %Y %H:%M:%S")
    }
    
    print(request.user.start_time, context['end_time'])
    return render(request, 'questions/index.html', context)


def marks_page(request):
    if request.user.is_superuser:
        return render(request, 'questions/marks.html')
    else:
        return redirect('login')


def calculate_marks(request):
    if request.user.is_superuser:

        answers = Answer.objects.all()
        x = 1
        for x in range(1,4):
            questions = Questions.objects.filter(slot = x, ques_type = 'MCQ')
            for answer in answers:
                if answer.candidate.slot == x:
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print(x)
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    i = 1
                    for i in range(1,13):
                        no = "answer" + str(i)
                        ans = answer.__getattribute__(no)
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        print(ans)
                        print(questions.filter(ques_no = i))
                        print(questions.filter(ques_no = i).first())
                        print(questions.filter(ques_no = i).first().ques_no)
                        print(questions.filter(ques_no = i).first().correct_ans)
                        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                        if ans == questions.filter(ques_no = i).first().correct_ans:
                            answer.candidate.points += 10
                            user_save = answer.candidate
                            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                            print("DONE DANA DONE DONE")
                            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                            user_save.save()
                        i += 1

        return render(request, 'questions/marks.html')
    else:
        return redirect('login')

# def calculate_marks(request):
#     answers = Answer.objects.all()

#     for answer in answers:
#         for slot in range(1, 5):
#             correct_answer = Answer()
#             if answer.candidate.slot == slot:
#                 temp = "Slot" + str(slot)
#                 u = User.objects.get(name=temp)
#                 correct_answer = Answer.objects.get(candidate=u)
#                 break
            
            
#         for i in range(1, 13):
#             ans = "answer" + str(i)
#             if answer.__getattribute__(ans) == correct_answer.__getattribute__(ans):
#                 answer.candidate.points += 10
#                 answer.save()
#         print(answer.candidate, answer.candidate.points)

#     return redirect('thank-you')



def export_answers_xls(request):
    if request.user.is_superuser:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="responses.xls"'
    
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Quiz Responses') # this will make a sheet named Users Data
    
        # Sheet header, first row
        row_num = 0
    
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
    
        columns = ['Email', 'Name', 'Points', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15']
    
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
    
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
    
        rows = Answer.objects.all().values_list('candidate__email', 'candidate__name', 'candidate__points', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9', 'answer10', 'answer11', 'answer12', 'answer13', 'answer14', 'answer15')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
    
        wb.save(response)
    
        return response        
    else:
        return redirect('login')

