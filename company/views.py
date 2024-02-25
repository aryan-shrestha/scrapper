from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import FloatField, ExpressionWrapper, Func
from django.db.models.functions import Substr
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from account.decorators import user_in_groups
from scrapper.admin import CompanyDataResource, CompanyResource

from .forms import AGMForm, BoardOfDirectorForm, CompanyCategoryForm, CompanyDataForm, CompanyForm, CompanyUrlsForm, FloorsheetForm
from .models import AGM, BoardOfDirector, Category, Company, CompanyData, CompanyUrls, Floorsheet

# Create your views here.
@user_in_groups(['super admin', 'super editor'])
def company_list(request):
    company_list = Company.objects.all()
    context = {
        'company_list' : company_list
    }
    if request.method == 'POST':
        if 'xls' in request.POST:
            dataset = CompanyResource().export(company_list)
            ds = dataset.xls
            response = HttpResponse(ds, content_type='xls')
            response['Content-Disposition'] = f'attachment; filename=company_list.xls'
        elif 'pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="company_list.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []
            table_data = [['Name', 'email', 'phone', 'symbol', 'Category']]

            for item in company_list:
                table_data.append([item.name, item.email, item.phone, item.symbol, item.category.name])
            
            table = Table(table_data)
            elements.append(table)
            doc.build(elements)
        return response

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
    first_company_data = CompanyData.objects.order_by('created_at')[0]
    start_date = first_company_data.created_at.date()

    while today >= start_date:
        today_company_data = CompanyData.objects.filter(created_at__date=today)
        if today_company_data.exists():
            break
        today = today - timedelta(days=1)
    else:
        messages.error(request, "Data does not exists")
  
    today_company_data = today_company_data.annotate(
        first_six_characters=ExpressionWrapper(
            Substr('last_traded_price', 1, 6),
            output_field=FloatField()
        )
    )
    sorted_company_data = today_company_data.order_by('-first_six_characters')

    if request.method == 'POST':
        if 'xls' in request.POST:
            dataset = CompanyDataResource().export(sorted_company_data)
            ds = dataset.xls
            response = HttpResponse(ds, content_type='xls')
            response['Content-Disposition'] = f'attachment; filename={today}.xls'
            
        elif 'pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{today}.pdf"'
            
            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []
            table_data = [['Company', 'Symbol', 'LTP', 'Source']]
            
            for item in sorted_company_data:
                table_data.append([item.company.name, item.company.symbol, item.last_traded_price, item.last_scrapped_from])

            table = Table(table_data)
            table.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
                                    ]))
            elements.append(table)
            doc.build(elements)
        return response

    context = {
        'sorted_company_data' : sorted_company_data,
    }

    return render(request, 'company/today_floorsheet.html', context=context)

@user_in_groups(['super admin', 'super editor', 'company admin'])
def company_data_create(request):
    form = CompanyDataForm()

    if request.method == 'POST':
        form = CompanyDataForm(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, "Company data created")

    context = {
        'form': form
    }

    return render(request, 'company/company_data_create.html', context=context)


def import_company_data(request):
    if request.method == 'POST':
        resource = CompanyDataResource()
        uploaded_file = request.FILES['file']
        # Get the file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        # Check if the file format is supported
        if file_extension in ['xls', 'xlsx']:
            dataset = resource.import_data(uploaded_file.read(), format='xls')  # Use 'xls' for Excel 97-2003 format
        else:
            messages.error(request, 'Unsupported file format. Please upload an Excel file (.xls or .xlsx).')

        if dataset.has_errors():
            messages.error(request, "Error in file")
        else:
            messages.success(request, 'File data has been imported')
        
    return redirect('company:today_market')

@user_in_groups(['super admin', 'super editor'])
def agm_list(request):
    agm_list = AGM.objects.all()
    context = {
        'agm_list': agm_list
    }
    return render(request, 'company/agm_list.html', context=context)

@user_in_groups(['super admin', 'super editor'])
def agm_create(request):
    form = AGMForm()

    if request.method == 'POST':
        form = AGMForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New AGM created")
            return redirect('company:agm_list')

    context = {
        'form': form
    }
    
    return render(request, 'company/agm_create.html', context=context)


@user_in_groups(['super admin', 'super editor'])
def agm_update(request, agm_slug):
    agm = AGM.objects.get(slug=agm_slug)

    form = AGMForm(instance=agm)

    if request.method == 'POST':
        form = AGMForm(request.POST, request.FILES, instance=agm)
        if form.is_valid():
            form.save()
            messages.success(request, "AGM updated")
            return redirect('company:agm_list')

    context = {
        'form': form
    }
    
    return render(request, 'company/agm_create.html', context=context)

@user_in_groups(['super admin'])
def agm_delete(request, agm_slug):
    agm = AGM.objects.get(slug=agm_slug)
    
    if request.method == 'POST':
        agm.delete()
        messages.success(request, "AGM deleted")
        return redirect('company:agm_list')
    return render(request, 'company/agm_delete.html')
