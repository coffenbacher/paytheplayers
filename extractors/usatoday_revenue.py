import requests
import csv
from bs4 import BeautifulSoup

def d2f(b):
    return int(b.text.replace('$', '').replace(',',''))
def main():
    l = BeautifulSoup(requests.get('http://sports.usatoday.com/ncaa/finances/').content, "lxml")
    revenue_rows = []
    expense_rows = []
    for school in l("a", {'class':'show-popup'}):
        id = school.attrs['data-passid']
        r = requests.get('http://sports.usatoday.com/ajaxservice/ncaa/finances__school__%s__' % id).content
        data = BeautifulSoup(r, 'lxml')
        school_name = data('p', {'class': 'sp-subhead-profile-schoolname'})[0].text.strip()
        print 'Extracting school: %s' % school_name
        
        # Revenue
        revenue_table = data('table', {'class': 'Revenues'})[0]
        revenue_data = revenue_table('td')
        revenue_years = []
        for i in range(len(revenue_data)/8):
            revenue_rows.append({
                'school': school_name,
                'year': d2f(revenue_data[8*i + 0]),
                'ticket_sales': d2f(revenue_data[8*i + 1]),
                'contributions': d2f(revenue_data[8*i + 2]),
                'rights_and_licensing': d2f(revenue_data[8*i + 3]),
                'student_fees': d2f(revenue_data[8*i + 4]),
                'school_funds': d2f(revenue_data[8*i + 5]),
                'other': d2f(revenue_data[8*i + 6]),
                'total_revenues': d2f(revenue_data[8*i + 7])
            })
            
        # Expenses
        expense_table = data('table', {'class': 'Expenses'})[0]
        expense_data = expense_table('td')
        for i in range(len(expense_data)/6):
            expense_rows.append({
                'school': school_name,
                'year': d2f(expense_data[6*i + 0]),
                'coaching_staff':d2f(expense_data[6*i + 1]),
                'scholarships':d2f(expense_data[6*i + 2]),
                'building_and_grounds':d2f(expense_data[6*i + 3]),
                'other':d2f(expense_data[6*i + 4]),
                'total_expenses':d2f(expense_data[6*i + 5]),
            })
    
    with open('data/usatoday_revenue.csv', 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=revenue_rows[0].keys())
        writer.writeheader()
        for row in revenue_rows:
            writer.writerow(row)
            
    with open('data/usatoday_expense.csv', 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=expense_rows[0].keys())
        writer.writeheader()
        for row in expense_rows:
            writer.writerow(row)
        
if __name__ == "__main__":
    main()