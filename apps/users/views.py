import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from apps.users.models import Users, GENDER_CHOICES
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required



logger = logging.getLogger(__name__)



class UsersView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        
    def get(self, request, *args, **kwargs):
        return render(request, 'users/users.html', context=self.context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')
    
    
    
    
    
    
class LoadUsersDatatable(BaseDatatableView):
    model = Users
    
    order_columns = ['id','email','username','image','first_name','last_name','is_active']
    
    def get_initial_queryset(self):

        filter_value = self.request.POST.get('columns[3][search][value]', None)
        
        if filter_value == '1':
            return self.model.objects.filter(is_active__contains=1)
        elif filter_value == '2':
            return self.model.objects.filter(is_active__contains=0)
        else:
            return self.model.objects.all()


    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)

        if search:
            qs = qs.filter(email__istartswith=search)

        # more advanced example using extra parameters
        filter_email = self.request.GET.get('email', None)

        if filter_email is not None:
            users_datas = filter_email.split(' ')
            qs_params = None
            for part in users_datas:
                q = Q(email__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs
    

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append({
                'id' : escape(item.id), 
                'email' : escape(item.email),
                'username' : escape(item.username),
                'image' : escape(item.image.url),
                'first_name' : escape(item.first_name),
                'last_name' : escape(item.last_name),
                'is_active' : escape(item.is_active),
                'created_date' : item.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
            })
        return json_data
    
    
    
    
    
@method_decorator(login_required, name='dispatch')
class DestroyUsersRecordsView(View):
    def __init__(self, **kwargs):
        self.response_format = {"status_code": 101, "message": "", "error": ""}

    def post(self, request, *args, **kwargs):
        try:
            users_ids = request.POST.getlist('ids[]')
            if users_ids:
                Users.objects.filter(id__in=users_ids).delete()
                self.response_format['status_code'] = 200
                self.response_format['message'] = 'Success'
        except Exception as e:
            self.response_format['message'] = 'error'
            self.response_format['error'] = str(e)
            
        return JsonResponse(self.response_format, status=200)
    
    
    
    
    
class UserCreateOrUpdateView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.action = "Create"
        self.context['gender'] = GENDER_CHOICES
        self.template = 'users/create-or-update.html'

        
    def get(self, request, *args, **kwargs):
        id = kwargs.pop('id', None)
        if id:
            self.context['users'] = get_object_or_404(Users, id=id)
        return render(request, self.template , context=self.context)

    def post(self, request, *args, **kwargs):
        
        user_id = request.POST.get('user_id', None)
        
        try:
            if user_id:
                self.action = 'Updated'
                user = get_object_or_404(Users, id=user_id)
            else:
                user = Users()
                user.is_verified = 1
                user.is_staff    = 1
                
            user.email         = request.POST.get('email').strip()
            user.username     = request.POST.get('username').strip()
            user.first_name     = request.POST.get('first_name').strip()
            user.last_name     = request.POST.get('last_name').strip()
            user.phone     = request.POST.get('phone').strip()
            user.gender     = request.POST.get('gender').strip()
            user.is_active        = 1
            user.save()
            
            messages.success(request, f"Data Successfully "+ self.action)

        except Exception as e:
            messages.error(request, f"Something went wrong."+str(e))
            if user_id is not None:
                return redirect('users:users.update', id = user_id )   
            return redirect('users:users.create')

        return redirect('users:users.index')
