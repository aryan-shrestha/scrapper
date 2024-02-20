from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from company.models import Company, CompanyData

from .forms import AccountCreationForm, AccountUpdateForm, GroupForm
from .decorators import user_in_groups

# Create your views here.

def dashboard(request):
   
    return render(request, 'empty.html')
   

@user_in_groups(['super admin'])
def user_create_view(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect('account:user_list')
    else:
        form = AccountCreationForm()

    return render(request, 'account/create.html', {'form': form})

@user_in_groups(['super admin', 'super editor'])
def user_list(request):
    User = get_user_model()
    users = User.objects.all()

    context = {
        'users': users
    }

    return render(request, 'account/list.html', context=context)

@user_in_groups(['super admin', 'super editor'])
def user_update(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        messages.success(request, "User updated")
        return redirect('account:user_list')

    context = {
        'form': AccountUpdateForm(instance=user)
    }
    return render(request, 'account/update.html', context=context)


def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are successfully logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            context = {
                'email': email,
            }
            render(request, 'account/signin.html', context=context)
        
    return render(request, 'account/signin.html')

@user_in_groups(['super admin'])
def user_delete(request, user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.info(request, "User deleted")
        return redirect('account:user_list')
    return render(request, 'account/delete.html', context={'user': user})

def logout_view(request):
    logout(request)
    return redirect('account:login_view')

@user_in_groups(['super admin', 'super editor'])
def group_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        group = Group.objects.create(name=name)
        messages.success(request, "New role created")
        return redirect('account:group_list')
    
    context = {
        'groups': Group.objects.all()
    }

    return render(request, 'account/group_list.html', context=context)

@user_in_groups(['super admin'])
def group_create(request):
    models = [Company, CompanyData ]
    content_types = []
    for model in models:
        content_type = ContentType.objects.get_for_model(model)
        content_types.append(content_type)        
    permissions = Permission.objects.filter(content_type__in=content_types)

    if request.method == 'POST':
        try:
            group = Group.objects.create(
                name = request.POST.get('group_name')
            )
        except Exception as e:
            messages.error(request, f"{e}")
            return redirect('account:group_create')

        permission_ids = request.POST.getlist('permissions')  
        if len(permission_ids) <= 0:
            messages.error(request, "Atleast one permission must be selected")
            return redirect('account:group_create')
        permissions = Permission.objects.filter(id__in=permission_ids)
        group.permissions.clear()
        group.permissions.add(*permissions)
        messages.success(request, "Group Added")
        return redirect('account:group_list')

    context = {
        'form': GroupForm(),
        'permissions': permissions
    }

    return render(request, 'account/group_create.html', context=context)

@user_in_groups(['super admin', 'super editor'])
def group_update(request, group_id):
    group = Group.objects.get(id=group_id)
    models = [Company, CompanyData]
    content_types = []

    for model in models:
        content_type = ContentType.objects.get_for_model(model)
        content_types.append(content_type)        
    permissions = Permission.objects.filter(content_type__in=content_types)

    if request.method == 'POST':
        permission_ids = request.POST.getlist('permissions')  
        if len(permission_ids) <= 0:
            messages.error(request, "Atleast one permission must be selected")
            return redirect('account:group_update')
        permissions = Permission.objects.filter(id__in=permission_ids)
        group.permissions.clear()
        group.permissions.add(*permissions)
        messages.success(request, "Group Updated")
        return redirect('account:group_list')

    context = {
        'group': group,
        'permissions': permissions
    }

    return render(request, 'account/group_update.html', context=context)

@user_in_groups(['super admin'])
def group_delete(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, 'Role deleted')
        return redirect('account:group_list')
    
    context = {
        'group': group
    }
    
    return render(request, 'account/group_delete.html', context=context)

