from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import permissions, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics

from authentication.jwt_authentication import JSONWebTokenAuthenticationCookie

from tasks.serializers import TaskSerializer
from tasks.permissions import IsAuthorOfTask, IsCourier
from tasks.models import Task

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by('-pub_date').filter(is_canceled=False)
    serializer_class = TaskSerializer

    def get_authenticators(self):
        return (JSONWebTokenAuthenticationCookie(),)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (permissions.IsAuthenticated(), IsAuthorOfTask(),)
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        if self.request.method == 'DELETE':
            return (permissions.IsAuthenticated(),)
        return (permissions.IsAuthenticated(), IsAuthorOfTask(),)

    def list(self, request):
        if self.request.user and self.request.user.email:
            queryset = self.queryset.exclude(
                author__email=request.user.email).filter(
                    courier=None)
            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data)

        return Response({
            'status': 'Unauthorized',
            'message': 'User must be a courier to accept tasks'
        }, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        task = self.queryset.get(id=pk)
        task.is_canceled = True
        task.save()

        serializer = self.serializer_class(task)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)

        return super(TaskViewSet, self).perform_create(serializer)

class AccountTasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('author').all().filter(is_canceled=False)
    serializer_class = TaskSerializer

    authentication_classes = [JSONWebTokenAuthenticationCookie]

    def get_permissions(self):
        return(permissions.IsAuthenticated(), IsAuthorOfTask(),)

    def list(self, request):
        if self.request.user and self.request.user.email:
            queryset = self.queryset.filter(author__email=request.user.email)
            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data)

        return Response({
            'status': 'Unauthorized',
            'message': 'User must be a courier to accept tasks'
        }, status=status.HTTP_401_UNAUTHORIZED)

class CourierTaskList(generics.ListAPIView):
    queryset = Task.objects.select_related('author').all()

    def list(self, request):
        queryset = self.queryset.filter(author__email=request.user.email)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

class CourierTaskDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    '''
    get - Lists all of courier's tasks
    patch - sets or unsets the current user as the courier
          - set_courier: True
            - sets the courier of the task to the current user
          - remove_courier: True
            - removes the courier of the task
          - complete_task: True
            - sets the task to completed
    '''
    authentication_classes = [JSONWebTokenAuthenticationCookie]
    serializer_class = TaskSerializer
    queryset = Task.objects.order_by('id').filter(is_canceled=False)

    def get(self, request, *args, **kwargs):
        if self.request.user and self.request.user.is_authenticated():
            acceptedTasks = request.user.acceptedTasks
            serializer = self.serializer_class(acceptedTasks, many=True)
            return Response(serializer.data)

        return Response({
            'status': 'Unauthorized',
            'message': 'User must be a courier to accept tasks'
        }, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, *args, **kwargs):
        data = request.data
        task_id = data.get('id', None)
        set_courier = data.get('set_courier', False)
        remove_courier = data.get('remove_courier', False)
        complete_task = data.get('complete_task', False)
        task = Task.objects.get(id=task_id)

        if set_courier:
            # sets tasks' courier to current user if courier isn't set already
            if task.courier:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'Task has already been claimed'
                }, status=status.HTTP_401_UNAUTHORIZED)
            if request.user.is_courier:
                task.courier = request.user
                task.save()
                serializer = self.serializer_class(task)

                return Response(serializer.data)
            return Response({
                'status': 'Unauthorized',
                'message': 'User must be a courier to accept tasks'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif remove_courier:
            # remove tasks' courier if the current courier is the current user
            if request.user == task.courier:
                task.courier = None
                task.save()
                serializer = self.serializer_class(task)

                return Response(serializer.data)
            return Response({
                'status': 'Unauthorized',
                'message': 'User is not current courier of task'
            }, status=status.HTTP_401_UNAUTHORIZED)
        elif complete_task:
            # sets task to completed if the current courier is the current user
            if request.user == task.courier:
                # task.completed = True
                task.is_completed = True
                task.save()
                serializer = self.serializer_class(task)

                return Response(serializer.data)
            return Response({
                'status': 'Unauthorized',
                'message': 'User is not current courier of task'
            }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # return error
            return Response({
                'status': 'Bad Request',
                'message': 'Invalid Courier Patch request'
            }, status=status.HTTP_400_BAD_REQUEST)
