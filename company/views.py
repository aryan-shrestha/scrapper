from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import FloatField, ExpressionWrapper, Func
from django.db.models.functions import Substr
from django.utils import timezone

from account.decorators import user_in_groups

from .forms import BoardOfDirectorForm, CompanyCategoryForm, CompanyForm, CompanyUrlsForm, FloorsheetForm
from .models import BoardOfDirector, Category, Company, CompanyData, CompanyUrls, Floorsheet

# Create your views here.
@user_in_groups(['super admin', 'super editor'])
def company_list(request):
    company_list = Company.objects.all()
    context = {
        'company_list' : company_list
    }
    return render(request, 'company/company_list.html', context=context)

@user_in_groups(['super admin'])
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            new_company = form.save()
            CompanyUrls.objects.create(company=new_company)
            return redirect('company:company_list')
    
    context = {
        'form': CompanyForm()
    }
    return render(request, 'company/company_create.html', context=context)

@user_in_groups(['super admin', 'super editor', 'company admin'])
def company_update(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    try:
        company_url = company.urls
    except:
        company_url = None

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company:company_list')
    else:
        form = CompanyForm(instance=company)
        company_url_form = CompanyUrlsForm(instance=company_url)

    context = {
        'form': form, 
        'company_url_form': company_url_form,
        'company_url': company_url,
        'company': company,
        'floorsheet': company.company_data.all().order_by('-updated_at'),
    }
    return render(request, 'company/company_update.html', context=context)

def company_data_chart(request, company_id):
    company = Company.objects.get(id=company_id)
    company_data = CompanyData.objects.filter(company=company).order_by('created_at')

    data = {
        'labels': [str(data.created_at.date()) for data in company_data],
        'last_traded_price': [data.last_traded_price for data in company_data],
    }

    return JsonResponse(data)

@user_in_groups(['super admin'])
def company_delete(request, company_id):
    company = Company.objects.get(id=company_id)
    if request.method == 'POST':
        company.delete()
        messages.success(request, "Company Deleted")
        return redirect('company:company_list')
    
    context = {
        'company': company
    }
    return render(request, 'company/company_delete.html', context=context)

@user_in_groups(['super admin', 'super editor', 'company admin'])
def update_company_url(request, company_url_id):
    if request.method == 'POST':
        company_urls = CompanyUrls.objects.get(id=company_url_id) 
        form = CompanyUrlsForm(request.POST, instance=company_urls)
        if form.is_valid():
            form.save()
            messages.success(request, "URLS updated")
        else:
            messages.error(request, form.errors)
        referring_url = request.META.get('HTTP_REFERER', None)
        return redirect(referring_url)
    
@user_in_groups(['super admin', 'super editor', 'company admin'])
def board_of_director_create(request):
    if request.method == 'POST':
        form = BoardOfDirectorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success! BOD Added")
    context = {
        'form': BoardOfDirectorForm()
    }
    return render(request, 'company/bod_create.html', context=context)


@user_in_groups(['super admin', 'super editor', 'company admin'])
def board_of_director_update(request, bod_id):
    bod = BoardOfDirector.objects.get(id=bod_id)

    if request.method == 'POST':

        form = BoardOfDirectorForm(request.POST, instance=bod)
        if form.is_valid():
            form.save()
            messages.success(request, "Success! BOD Updated")
    context = {
        'form': BoardOfDirectorForm(instance=bod)
    }
    return render(request, 'company/bod_update.html', context=context)


@user_in_groups(['super admin', 'super editor', 'company admin'])
def board_of_director_delete(request, bod_id):
    member = BoardOfDirector.objects.get(id=bod_id)

    if request.method == 'POST':
        member.delete()
        messages.info(request, 'Info: BOD member deleted')
        return redirect('company:company_list')

    context = {
        'member': member
    }
    return render(request, 'company/bod_delete.html', context=context)


@user_in_groups(['super admin', 'super editor'])
def category_list(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'company/category_list.html', context=context)


@user_in_groups(['super admin'])
def category_create(request):
    if request.method == 'POST':
        form = CompanyCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Success: New category created")
            return redirect('company:category_list')

    context = {
        'form': CompanyCategoryForm()
    }
    return render(request, 'company/category_create.html', context=context)

@user_in_groups(['super admin', 'super editor'])
def category_update(request, category_id):
    category = Category.objects.get(id=category_id)
    form = CompanyCategoryForm(instance=category)
    if request.method == 'POST':
        form = CompanyCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Success: New category created")
            return redirect('company:category_list')

    context = {
        'form': CompanyCategoryForm(instance=category)
    }
    return render(request, 'company/category_update.html', context=context)

@user_in_groups(['super admin'])
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Success: Category deleted")
        return redirect('company:category_list')
    return render(request, 'company/category_delete.html')


@user_in_groups(['super admin', 'super editor'])
def floorsheet_list(request):
    floorsheets = Floorsheet.objects.all()
    context = {
        'floorsheets': floorsheets
    }

    return render(request, 'company/floorsheet_list.html', context=context)

@user_in_groups(['super admin',])
def floorsheet_create(request):
    context = {
        'form' : FloorsheetForm()
    }
    if request.method == 'POST':
        form = FloorsheetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Floorsheet created")
            return redirect('company:floorsheet_list')
        
    return render(request, 'company/floorsheet_create.html', context=context)


@user_in_groups(['super admin', 'super editor'])
def floorsheet_update(request, floorsheet_id):
    floorsheet = Floorsheet.objects.get(id=floorsheet_id)
    if request.method == 'POST':
        form = FloorsheetForm(request.POST, instance=floorsheet)
        if form.is_valid():
            form.save()
            messages.success(request, "Floorsheet updated")
            return redirect('company:floorsheet_list')

    context = {
        'form' : FloorsheetForm(instance=floorsheet)
    }
    return render(request, 'company/floorsheet_update.html', context=context)


@user_in_groups(['super admin'])
def floorsheet_delete(request, floorsheet_id):
    floorsheet = Floorsheet.objects.get(id=floorsheet_id)
    if request.method == 'POST':
        floorsheet.delete()
        messages.success(request, "Floorsheet deleted")
        return redirect('company:floorsheet_list')
    context = {
        'floorsheet': floorsheet
    }
    return render(request, 'company/floorsheet_delete.html', context=context)


class Substring(Func):
    function = 'SUBSTRING'

@user_in_groups(['super admin', 'super editor'])
def today_market(request):
    today = timezone.now().date()
    today_company_data = CompanyData.objects.filter(created_at__date=today)

    today_company_data = today_company_data.annotate(
        first_six_characters=ExpressionWrapper(
            Substr('last_traded_price', 1, 6),
            output_field=FloatField()
        )
    )

    sorted_company_data = today_company_data.order_by('-first_six_characters')
    context = {
        'sorted_company_data' : sorted_company_data,
    }

    return render(request, 'company/today_floorsheet.html', context=context)

