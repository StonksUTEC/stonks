#para ejecutar correr lo siguiente en python manage.py shell:
#exec(open('<direccion>/generate_data.py').read())
from accounts.models import Client
from stocks.models import Portfolio, Company, Order
from knox.models import AuthToken as KnoxAuthToken
from django.utils import timezone


user1_data = {
    'dni': '12345678',
    'names': 'TestName',
    'lastname': 'TestLastName',
    'password': 'TestPassword',
    'email': 'test@te st.com'
}

user2_data = {
    'dni': '87654321',
    'names': 'ExtraName',
    'lastname': 'ExtraLastName',
    'password': 'ExtraPassword',
    'email': 'extra@test.com'
}

companies_data = [
    {
        'ruc': '12345678901',
        'acronym': 'TST',
        'company_name': 'TestCompany',
        'lastest_price': 52.50,
    },
    {
        'ruc': '12345678902',
        'acronym': 'MOV',
        'company_name': 'MovementCompany',
        'lastest_price': 28.30,
    },
]

portafolio1_data = [
    {
        'client_dni': user1_data['dni'],
        'company_ruc': companies_data[0]['ruc'],
      	'avg_price': 64.90,
        'quantity': 5,
    },
    {
        'client_dni': user1_data['dni'],
        'company_ruc': companies_data[1]['ruc'],
      	'avg_price': 53.10,
        'quantity': 10,
    },
]

portafolio2_data = [
    {
        'client_dni': user2_data['dni'],
        'company_ruc': companies_data[0]['ruc'],
      	'avg_price': 49.10,
        'quantity': 15,
    },
    {
        'client_dni': user2_data['dni'],
        'company_ruc': companies_data[1]['ruc'],
      	'avg_price': 52.10,
        'quantity': 20,
    },
]

orders1_data = [
    {
        'client_dni': user1_data['dni'],
        'company_ruc': companies_data[0]['ruc'],
        'quantity': 15,
      	'quantity_left': 15,
        'price': 25.62,
        'transaction_type': Order.TransactionType.BUY_LIMIT,
      	'avg_price': 25.70,
      	'date' : timezone.now()
    },
    {
        'client_dni': user1_data['dni'],
        'company_ruc': companies_data[1]['ruc'],
        'quantity': 20,
      	'quantity_left': 20,
        'price': 23.41,
      	'avg_price': 23.60,
        'transaction_type': Order.TransactionType.SELL_STOP,
      	'date' : timezone.now()
    },
]

orders2_data = [
    {
        'client_dni': user2_data['dni'],
        'company_ruc': companies_data[0]['ruc'],
      	'date' : timezone.now(),
        'quantity': 11,
      	'quantity_left': 11,
        'price': 78.94,
      	'avg_price': 0,
        'transaction_type': Order.TransactionType.BUY_MARKET,
    },
    {
        'client_dni': user2_data['dni'],
        'company_ruc': companies_data[1]['ruc'],
      	'date' : timezone.now(),
        'quantity': 19,
      	'quantity_left': 19,
        'price': 65.21,
      	'avg_price': 0,
        'transaction_type': Order.TransactionType.SELL_LIMIT,
    },
]

def utility_generate_user_data_and_token(user_data):
        """
        Create user and get auth token.
        """
        client = Client.objects.create_user(**user_data)
        token = KnoxAuthToken.objects.create(client)
        return token[1]

def utility_generate_companies(companies_list):
    """
    Create companies.
    """
    for c in companies_list:
        Company.objects.create(**c)

def utility_generate_portafolio(portafolio_list):
    """
    Create portafolio data.
    """
    for p in portafolio_list:
        tmp = p.copy()
        tmp['client_dni'] = Client.objects.get(dni=p['client_dni'])
        tmp['company_ruc'] = Company.objects.get(ruc=p['company_ruc'])
        Portfolio.objects.create(**tmp)

def utility_generate_orders(orders_list):
    """
    Create order data.
    """
    for o in orders_list:
        tmp = o.copy()
        tmp['client_dni'] = Client.objects.get(dni=o['client_dni'])
        tmp['company_ruc'] = Company.objects.get(ruc=o['company_ruc'])
        Order.objects.create(**tmp)

utility_generate_user_data_and_token(user1_data)
utility_generate_user_data_and_token(user2_data)
utility_generate_companies(companies_data)
utility_generate_portafolio(portafolio1_data)
utility_generate_portafolio(portafolio2_data)
utility_generate_orders(orders1_data)
utility_generate_orders(orders2_data)