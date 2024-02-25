import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC

from company.models import CompanyData, Company
from scrapper.admin import CompanyDataResource
from .utils import list_to_dict

# Create your views here.

def filter_company_data_by_date(company, start_date, end_date):
    company_data = CompanyData.objects.filter(company=company, created_at__date__range=[start_date, end_date])
    return company_data

def company_detail_admin(request, company_id):
    today = timezone.now().date()
    context = {
        'today': today.strftime('%Y-%m-%d'),
    }
    try:
        company = Company.objects.get(id=company_id)
        today_company_data = CompanyData.objects.get(company=company, created_at__date=today)
    except Company.DoesNotExist:
        company = None
        messages.success(request, "Company does not exists")
    except CompanyData.DoesNotExist:
        today_company_data = None
        messages.error(request, "No data found")
    finally:
        context['company'] = company
        context['company_data'] = today_company_data

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        filtered_company_data = filter_company_data_by_date(company, start_date, end_date)
        context['floorsheet'] = filtered_company_data.order_by('-updated_at')
        context['start_date'] = start_date
        context['end_date'] = end_date
    else:
        context['floorsheet'] = company.company_data.all().order_by('-updated_at')

    return render(request, 'scrapper/detail.html', context=context)

def company_detail(request):
    company = request.user.company
    today = timezone.now().date()
    context = {
        'company': company,
    }

    if company is None:
        messages.error(request, "User is not assoiciated with any company")
    else:
        try:
            company_data = CompanyData.objects.get(company=company, created_at__date=today)
        except CompanyData.DoesNotExist:
            company_data = None
            messages.error(request, "No data found")
        finally:
            context['company_data'] = company_data
    
    context['floorsheet'] = company.company_data.all().order_by('-updated_at')
    return render(request, 'scrapper/detail.html', context=context)


def scrap_from_nepse(request, company_id):
    if request.method == 'POST':
        today = timezone.now()
        company = Company.objects.get(id=company_id)

        try:
            company_data = CompanyData.objects.get(company=company, created_at__date=today.date())
        except CompanyData.DoesNotExist:
            company_data = CompanyData(company=company, created_at=today, updated_at=today)

        nepse_url = company.urls.nepse_url     # the urls should be initialized from the company update page

        driver = webdriver.Chrome()
        try:
            driver.get(nepse_url)
        except InvalidArgumentException:
            messages.error("Error: Invalid Nepse url!")
        else:
            table = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'table'))
            )

            table_soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

            data_dict = {}

            tbody = table_soup.find('tbody')
            rows = tbody.find_all('tr')[1:-1]

            for row in rows:
                th_text = row.find('th').get_text(strip=True)
                td_text = row.find('td').get_text(strip=True)
                data_dict[th_text] = td_text

            company_data.last_scrapped_from = 'Nepse'
            company_data.last_traded_price = data_dict['Last Traded Price'][0:6]
            company_data.total_traded_quantity = data_dict['Total Traded Quantity']
            company_data.total_trades = data_dict['Total Trades']
            company_data.previous_day_close_price = data_dict['Previous Day Close Price']
            company_data.high_price_low_price = data_dict['High Price / Low Price']
            company_data.week_high_week_low = data_dict['52 Week High / 52 Week Low']
            company_data.open_price = data_dict['Open Price']
            company_data.close_price = data_dict['Close Price*']
            company_data.total_listed_shares = data_dict['Total Listed Shares']
            company_data.total_paid_up_value = data_dict['Total Paid up Value']
            company_data.market_capitalization = data_dict['Market Capitalization']
            company_data.save()
            messages.success(request, "Success: Data updated")
    redirect_url = request.META.get('HTTP_REFERER')
    return redirect(redirect_url)


def scrap_from_mero_lagani(request, company_id):
    if request.method == 'POST':
        today = timezone.now()
        company = Company.objects.get(id=company_id)

        try:
            company_data = CompanyData.objects.get(company=company, created_at__date=today.date())
        except CompanyData.DoesNotExist:
            print("Company data is not of today")
            company_data = CompanyData(company=company, created_at=today, updated_at=today)
        else:
            print("Company data is of today")
        
        mero_lagani_url = company.urls.mero_lagani_url
        response = requests.get(mero_lagani_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')

        table_data = {}
        for row in rows:
            try:
                th = row.find('th').get_text(strip=True)
                td = row.find('td').get_text(strip=True)
                table_data[th] = td  
            except AttributeError:
                table_data[th] = ""
        
        company_data.last_scrapped_from = 'Mero Lagani'
        company_data.total_listed_shares = table_data['Shares Outstanding']
        company_data.last_traded_price =table_data['Market Price']
        company_data.week_high_week_low = table_data['52 Weeks High - Low']
        company_data.market_capitalization = table_data['Market Capitalization']
        company_data.total_listed_shares = table_data['Listed Shares']
        company_data.total_paid_up_value = table_data['Total Paidup Value']
        company_data.save()
        messages.success(request, "Success: Data updated")
    redirect_url = request.META.get('HTTP_REFERER')
    return redirect(redirect_url)
    
def scrap_from_share_sansar(request, company_id):
    if request.method == 'POST':
        today = timezone.now()
        company = Company.objects.get(id=company_id)

        try:
            company_data = CompanyData.objects.get(company=company, created_at__date=today.date())
        except CompanyData.DoesNotExist:
            print("Company data is not of today")
            company_data = CompanyData(company=company, created_at=today, updated_at=today)
        else:
            print("Company data is of today")

        share_sansar_url = company.urls.share_sansar_url
        response = requests.get(share_sansar_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        last_traded_price = soup.find('span', class_="comp-price").get_text(strip=True)
        second_rows = soup.find_all('div', class_=["second-row margin-bottom-15"])

        scrapped_data = {}
        for row in second_rows:
            arr = row.text.replace(' ', '').split('\n')
            arr_dict = list_to_dict(arr)
            scrapped_data.update(arr_dict)

        table = soup.find('table', id='myTableCInfo')
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            key = cells[0].get_text(strip=True).replace("\n", "")
            value = cells[1].get_text(strip=True).replace("\n", "")
            scrapped_data[key] = value

        company_data.last_scrapped_from = 'Share sansar'
        company_data.high_price_low_price= f"{scrapped_data['High']}/{scrapped_data['Low']}"
        company_data.week_high_week_low = scrapped_data['52WeekHigh-Low']
        company_data.total_listed_shares= scrapped_data['Listed Shares']
        company_data.total_paid_up_value= scrapped_data['Total Paid Up Value']
        company_data.last_traded_price = last_traded_price
        company_data.open_price= scrapped_data['Open']
        company_data.save()
        messages.success(request, "Success: Data updated")
    redirect_url = request.META.get('HTTP_REFERER')
    return redirect(redirect_url)
    
def export_company_data(request, company_data_id):
    if request.method == 'POST':
        qs = CompanyData.objects.get(id=company_data_id)
        dataset = CompanyDataResource().export(qs)
        format = 'xls'
        ds = dataset.xls
        response = HttpResponse(ds, content_type=f'{format}')
        response['Content-Disposition'] = f'attachment; filename={qs.company.name}.{format}'
        return response
    