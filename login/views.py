from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.decorators import action
import jwt
import random
import string
from datetime import datetime, timedelta, date, time
# from django.urls import get_resolver
# import requests


# from rest_framework_api_key.models import APIKey
secret = 'SECRET_KEY'

# Create your views here.
class CreateUserView(GenericAPIView):
    serializer_class = UserRegistrationSerializer


    def get(self, request):
        return render(request, "create_user.html")

    def post(self, request):
        try:
            data=request.data
            username = data.get("username", "")
            email = data.get("email", "")
            password = data.get("password", "")
            if CustomUser.objects.filter(username=username).exists():
                return render(request, "create_user.html", {"message":"username already exists"})
            if CustomUser.objects.filter(email=email).exists():
                return render(request, "create_user.html", {"message": "email already exists"})
            serializer =UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_status="0", password=password)
                return render(request, "create_user.html", {"message":"user registered successfully"})
                # return Response({"success":"user registered"}, status=status.HTTP_201_CREATED)
            return render(request, "create_user.html", {"message":"something went wrong!" })
        except Exception:
            return render(request, "create_user.html", {"message": "something went wrong!"})



class HomeView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password','')
        if CustomUser.objects.filter(email=email).exists():
            object=CustomUser.objects.get(email=email)
            if object.user_status != "1":
                return render(request, 'login.html', {"message": "only an admin is authorized to use this service"})
            if object.check_password(password):
                # now = datetime.now()
                # now_30 = str(now + timedelta(minutes=30))
                # payload = {
                #     "username": object.username,
                #     "valid_time": now_30
                # }
                user_object = CustomUser.objects.get(email=email)
                if APIKeyModel.objects.filter(user = user_object).exists():
                    api_object = APIKeyModel.objects.get(user = user_object)
                    api_key = api_object.api_key
                else:
                    api_key = ''.join(random.choice(user_object.username + string.ascii_lowercase) for x in range(20))
                    api = {'api_key': api_key}

                    serializer = APIKeySerializer(data=api)

                    if serializer.is_valid():
                        serializer.save(user = user_object)
                # api_key = ''.join(
                #     random.choice(object.username + string.ascii_lowercase + string.digits) for x in range(25))
                # serializer = APIKeySerializer(data=request.data)
                # if serializer.is_valid():
                #     serializer.save(api_key=api_key, user=object)

                # encoded_token = jwt.encode(payload, secret, algorithm="HS256")




                # response = render(request, "home.html", context)
                # response['Authoriztion'] = api_key
                # return response
                # return Response({"success":"logged in successfully","api_key":api_key}, status = status.HTTP_201_CREATED)
            else:
                return render(request, 'login.html', {"message": "invalid email/password"})
                # return Response({"failure":"please check your password and try again"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return render(request, 'login.html', {"message": "invalid email/password"})
            # return Response({"failure": "invalid email"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        return render(request, 'login22.html')

    def post(self, request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password', '')
        user = CustomUser.objects.filter(email=email)
        task_serializer = TaskSerializer
        user_serializer = UserRegistrationSerializer
        user = user_serializer(user, many=True)
        tasks = TaskModel.objects.filter(user=user.data[0]["id"])
        tasks = task_serializer(tasks, many=True)
        if CustomUser.objects.filter(email=email).exists():
            object = CustomUser.objects.get(email=email)
            if object.user_status != "0":
                return render(request, 'login22.html', {"message": "only an user is authorized to use this service"})
            if object.password == password or object.check_password(password):
                # return Response(tasks.data, status=status.HTTP_200_OK)
                # return render(request, 'user_task.html', {"tasks": tasks.data, "user_object": user.data})
                return render(request, 'user_task2.html',{"tasks": tasks.data, "user_object": user.data})
            else:
                return render(request, 'login22.html', {"message": "invalid username/password"})
        return render(request, 'login22.html', {"message": "something went wrong"})




class Dashboard(GenericAPIView):
    def get(self, request):
        return render(request, 'home.html')



class LoginView(GenericAPIView):

    serializer_class = CustomUser
    def get(self,request):
        return render(request,'login.html')




    def post(self,request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password','')
        if CustomUser.objects.filter(username=username).exists():
            object = CustomUser.objects.get(username=username)
            if object.check_password(password):
                # now = datetime.now()
                # now_30 = str(now + timedelta(minutes=30))
                # payload = {
                #     "username": username,
                #     "valid_time": now_30
                # }
                encoded_token =''.join(random.choice(object.username + string.ascii_lowercase + string.digits) for x in range(25))
                # encoded_jwt = jwt.encode(payload, secret, algorithm="HS256")
                return render(request, 'login.html',{"message":"login successful", "token":encoded_token})
            else:
                return render(request, 'login.html', {"message": "please enter the correct password"})
        else:
            return render(request, 'login.html', {"message": "username not found"})

class EmailLoginView(GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self,request):
        data = request.data
        email = data.get('email', '')
        password = data.get('password','')
        if CustomUser.objects.filter(email=email).exists():
            object=CustomUser.objects.get(email=email)
            if object.check_password(password):
                # now = datetime.now()
                # now_30 = str(now + timedelta(minutes=30))
                # payload = {
                #     "username": object.username,
                #     "valid_time": now_30
                # }
                user_object = CustomUser.objects.get(email=email)
                if APIKeyModel.objects.filter(user = user_object).exists():
                    api_object = APIKeyModel.objects.get(user = user_object)
                    api_key = api_object.api_key
                else:
                    api_key = ''.join(random.choice(user_object.username + string.ascii_lowercase) for x in range(20))
                    api = {'api_key': api_key}

                    serializer = APIKeySerializer(data=api)

                    if serializer.is_valid():
                        serializer.save(user = user_object)
                # api_key = ''.join(
                #     random.choice(object.username + string.ascii_lowercase + string.digits) for x in range(25))
                # serializer = APIKeySerializer(data=request.data)
                # if serializer.is_valid():
                #     serializer.save(api_key=api_key, user=object)

                # encoded_token = jwt.encode(payload, secret, algorithm="HS256")
                return Response({"success":"logged in successfully","api_key":api_key}, status = status.HTTP_201_CREATED)
            else:
                return Response({"failure":"please check your password and try again"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"failure": "invalid email"}, status=status.HTTP_400_BAD_REQUEST)


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()

    # @action(detail=True, methods=['GET'], url_path="create_task", url_name="createtask")
    # def get_create_task(self, request):
    #     return render(request, 'create_task.html')


    # @action(detail=True, methods=['POST'], url_path="create_task", url_name="createtask")
    # def create_task(self, request):
    #     data = request.data
    #     title = request.data.get('title','')
    #     username = request.data.get('username', '')
    #     for user in username:
    #         if CustomUser.objects.filter(username=user).exists():
    #             pass
    #         else:
    #             return Response({"failure": "username does not exists; task not saved"},status=status.HTTP_400_BAD_REQUEST)
    #     task = TaskModel.objects.filter(title=title)
    #     if task.exists():
    #         return Response({"sorry": "Task already exists"}, status=status.HTTP_201_CREATED)
    #     else:
    #         new_task = TaskModel.objects.create(title=data['title'], time=datetime.now().time(), date=datetime.now().date(),
    #                                             amount=data['amount'], location=data['location'], task_status=data['status'])
    #         for user in username:
    #             user_object = CustomUser.objects.get(username=user)
    #             new_task.user.add(user_object)
    #
    #         return Response({"success": "Task saved successfully"}, status=status.HTTP_201_CREATED)
    #     return Response({"failure": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['GET', 'POST'], url_path="change_status")
    # def change_status(self, request):
    #     data=request.data
    #     task_id = data.get('task_id', '')
    #     new_status = data.get('status','')
    #     if TaskModel.objects.filter(id=task_id).exists():
    #         task_object = TaskModel.objects.get(id=task_id)
    #         if new_status == 'complete':
    #             new_amount = data.get('amount', '')
    #             if len(new_amount)!=0:
    #                 task_object.amount = new_amount
    #                 task_object.save(update_fields=['amount'])
    #             else:
    #                 return Response({"failure": "please provide amount also"}, status=status.HTTP_404_NOT_FOUND)
    #         elif new_status == 'hold' or new_status == 'reject':
    #             reason = data.get('reason', '')
    #             if len(reason) != 0:
    #                 reason_object = ReasonModel.objects.create(reason=reason)
    #                 reason_object.task.add(task_object)
    #             else:
    #                 return Response({"failure": "please provide a reason also"}, status=status.HTTP_404_NOT_FOUND)
    #         task_object.task_status = new_status
    #         task_object.save(update_fields=['task_status'])
    #         return Response({"success":"task updated successfully"}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"failure": "task does not exist"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'], url_path="employees")
    def employee_list(self, request):
        # api_key = request.headers['Authorization']
        # if APIKeyModel.objects.filter(api_key=api_key).exists():
        #     api_object = APIKeyModel.objects.get(api_key=api_key)
        #     user_object = api_object.user
        #     if user_object.user_status == "1":
        queryset = CustomUser.objects.filter(user_status="0")
        serializer = UserRegistrationSerializer
        employee_list = []
        for query in queryset:
            employee_dict = {}
            employee_dict['user_status'] = query.get_user_status_display()
            query = serializer(query)
            employee_dict['user_info'] = query.data
            employee_list.append(employee_dict)
                # queryset = serializer(queryset, many=True)
                # for q in queryset:
                #     print(q.get_user_status_display())
            # print(employee_list)
        return render(request, 'users.html', {"users":employee_list})
            # return Response({"success": employee_list}, status=status.HTTP_200_OK)
        # else:
        #     return Response({"failure": "Invalid API KEY"}, status=status.HTTP_404_NOT_FOUND)


class MyTaskView(GenericAPIView):
    def get(self,request, task_status):
        api_key = request.headers['Authorization']
        if APIKeyModel.objects.filter(api_key=api_key).exists():
            api_object = APIKeyModel.objects.get(api_key=api_key)
            user_object = api_object.user
            if task_status == 'all':
                tasks = TaskModel.objects.filter(user=user_object)
                task_list = []
                for task in tasks:
                    task_dict = {}
                    remarks = RemarkModel.objects.filter(task=task)
                    remark_serializer = RemarkSerializer
                    task_remarks = remark_serializer(remarks, many=True)
                    serializer = TaskSerializer
                    your_tasks = serializer(task)
                    reason_object = ReasonModel.objects.filter(task=task)
                    reason_serializer = ReasonSerializer
                    reasons = reason_serializer(reason_object, many=True)
                    task_dict['Your tasks'] = your_tasks.data
                    task_dict['remarks'] = task_remarks.data
                    task_dict['reasons'] = reasons.data
                    task_list.append(task_dict)
            else:
                tasks = TaskModel.objects.filter(user=user_object, task_status=task_status)
                task_list=[]
                for task in tasks:
                    task_dict = {}
                    remarks = RemarkModel.objects.filter(task=task)
                    remark_serializer = RemarkSerializer
                    task_remarks = remark_serializer(remarks, many=True)
                    serializer = TaskSerializer
                    your_tasks = serializer(task)
                    task_dict['Your tasks'] = your_tasks.data
                    task_dict['remarks'] = task_remarks.data
                    if task_status == 'hold' or task_status == 'reject':
                        reason_object = ReasonModel.objects.filter(task=task)
                        reason_serializer = ReasonSerializer
                        reasons = reason_serializer(reason_object, many=True)
                        task_dict['reasons'] = reasons.data
                    task_list.append(task_dict)
            return Response(task_list, status=status.HTTP_200_OK)
        else:
            return Response({"failure":"Invalid API Key"},status=status.HTTP_400_BAD_REQUEST)



class RemarkView(GenericAPIView):
    serializer_class = RemarkSerializer

    def get(self, request):
        return render(request, 'add_remark.html')

    def post(self, request):
        try:
            data=request.data
            task_id = request.data.get('task_id', '')
            remark_object = RemarkModel.objects.create(remark=data['remark'])
            task_object = TaskModel.objects.get(id=task_id)
            remark_object.task.add(task_object)
            # return render(request, 'login.html', {"message": "please enter the correct password"})
            return render(request, 'add_remark.html', {"message": "remark registered successfully"})
        except Exception:
            return render(request, 'add_remark.html',{"message": "something went wrong"})


class GetRemarkView(GenericAPIView):
    def get(self,request, task_id):
        if TaskModel.objects.filter(id=task_id).exists():
            task_object = TaskModel.objects.get(id=task_id)
            if RemarkModel.objects.filter(task=task_object).exists():
                remarks = RemarkModel.objects.filter(task=task_object)
                serializer = RemarkSerializer(remarks, many=True)
                return Response({"Task ID":task_id,"Remarks": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"Task ID":task_id,"Remarks": "no remarks for now"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"failure":"task does not exist"}, status=status.HTTP_404_NOT_FOUND)



class CreateTaskView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request):
        return render(request, 'create_task.html')

    def post(self, request):
        try:
            data = request.data
            title = request.data.get('title', '')
            username = request.data.get('username', '')
            username = username.split(", ")
            print(username)
            # if not username:
            #     return render(request, 'create_task.html', {"message": "username does not exists; task not saved"})
            for user in username:
                if CustomUser.objects.filter(username=user).exists():
                    pass
                else:
                    return render(request, 'create_task.html', {"message": "username does not exists; task not saved"})
                    # return Response({"failure": "username does not exists; task not saved"},
                    #                 status=status.HTTP_400_BAD_REQUEST)
            task = TaskModel.objects.filter(title=title)
            if task.exists():
                return render(request, 'create_task.html', {"message": "Sorry! Task already exists"})
                # return Response({"sorry": "Task already exists"}, status=status.HTTP_201_CREATED)
            else:
                new_task = TaskModel.objects.create(title=data['title'], time=datetime.now().time(),
                                                    date=datetime.now().date(),
                                                    amount=data['amount'], location=data['location'],
                                                    task_status=data['status'])
                for user in username:
                    user_object = CustomUser.objects.get(username=user)
                    new_task.user.add(user_object)

                return render(request, 'create_task.html', {"message":"task saved successfully"})
                # return Response({"success": "Task saved successfully"}, status=status.HTTP_201_CREATED)
        except Exception:
            return render(request, 'create_task.html', {"message": "something went wrong"})
        # return Response({"failure": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class AllTaskView(GenericAPIView):

    def get(self, request, task_status):
        if task_status != "all":
            tasks = TaskModel.objects.filter(task_status=task_status)
        else:
            tasks = TaskModel.objects.all()
        if len(tasks) == 0 :
            return render(request, 'tasks_list.html', {"message":"Sorry, no tasks of the specified status exist for now!"})
        users = CustomUser.objects.all()
        task_serializer = TaskSerializer
        user_serializer = UserRegistrationSerializer
        tasks = task_serializer(tasks, many=True)
        users = user_serializer(users, many=True)
        return render(request, 'tasks_list.html', {"tasks":tasks.data,"users":users.data})


class ChangeStatusView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request):
        tasks = TaskModel.objects.all()
        return render(request, 'change_status.html', {"tasks":tasks})

    def post(self, request):
        tasks = TaskModel.objects.all()
        try:
            data=request.data
            task_name= data.get('task_name', '')
            new_status = data.get('status', '')

            if TaskModel.objects.filter(title=task_name).exists():
                task_object = TaskModel.objects.get(title=task_name)
                if new_status == 'complete':
                    new_amount = data.get('amount', '')
                    if len(new_amount)!=0:
                        task_object.amount = new_amount
                        task_object.save(update_fields=['amount'])
                    else:
                        return render(request, 'change_status.html', {"message":"please provide amount also","tasks":tasks})
                        # return Response({"failure": "please provide amount also"}, status=status.HTTP_404_NOT_FOUND)
                elif new_status == 'hold':
                    reason_hold = data.get('reason_hold', '')
                    if len(reason_hold) != 0:
                        reason_object = ReasonModel.objects.create(reason_hold=reason_hold)
                        reason_object.task.add(task_object)
                    else:
                        return render(request, 'change_status.html', {"message": "please provide a reason also","tasks":tasks})
                elif new_status == 'reject':
                    reason_reject = data.get('reason_reject', '')
                    if len(reason_reject) != 0:
                        reason_object = ReasonModel.objects.create(reason_reject=reason_reject)
                        reason_object.task.add(task_object)
                    else:
                        return render(request, 'change_status.html',
                                      {"message": "please provide a reason also", "tasks": tasks})
                # return Response({"failure": "please provide a reason also"}, status=status.HTTP_404_NOT_FOUND)
                task_object.task_status = new_status
                task_object.save(update_fields=['task_status'])
                return render(request, 'change_status.html', {"message": "task updated successfully","tasks":tasks})
                # return Response({"success":"task updated successfully"}, status=status.HTTP_200_OK)
            else:
                return render(request, 'change_status.html', {"message": "task does not exist","tasks":tasks})
                # return Response({"failure": "task does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return render(request, 'change_status.html', {"message": "something went wrong", "tasks": tasks})


class UserTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    def get(self, request, user_id):
        user_object = CustomUser.objects.filter(id=user_id)
        # print(user_object.username)
        tasks = TaskModel.objects.filter(user=user_id)
        task_serializer = TaskSerializer
        tasks = task_serializer(tasks, many=True)
        user_serializer = UserRegistrationSerializer
        user = user_serializer(user_object, many=True)
        # return Response(tasks.data, status=status.HTTP_200_OK)
        return render(request, 'user_task.html', {"tasks":tasks.data, "user_object":user.data})