# from django.http import response
# from django.urls import reverse
# from django.shortcuts import get_object_or_404, redirect
# from account.models import Profile
from django.utils import translation
import requests
import datetime
from django.conf import settings


def language_change_middleware(get_response):
    # Cookei set
    def set_cookie(response, key, value, days_expire=1):
        if days_expire is None:
            max_age = 365 * 24 * 60 * 60    # one year
        else:
            max_age = days_expire * 60
        expires = datetime.datetime.strftime(
            datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
            "%a, %d-%b-%Y %H:%M:%S GMT",
        )
        response.set_cookie(
            key,
            value,
            max_age=max_age,
            expires=expires,
            secure=settings.SESSION_COOKIE_SECURE or None,
        )
    
    
    def active_translate(value):
        if value in {'IN', 'NP'}:
            translation.activate('hi')
        elif value in {'US', 'UK', 'AG', 'AU',
                        'BS', 'BB', 'BZ', 'BW',
                        'CA', 'DM', 'FJ', 'GM',
                        'GH', 'GD', 'GY', 'IE',
                        'JM', 'KE', 'KI', 'LS',
                        'LR', 'MW', 'MT', 'MH',
                        'MU', 'FM', 'NA', 'NR',
                        'NZ', 'NG', 'PW', 'PG',
                        'RW', 'KN', 'LC', 'VC',
                        'WS', 'SL', 'SG', 'SB',
                        'ZA', 'SS', 'SD', 'SZ',
                        'TZ', 'TO', 'TT', 'TV',
                        'UG', 'VU', 'ZM', 'ZW'}:
            translation.activate('en')
        elif value in {'FR', 'BE', 'BJ', 'BF',
                        'BI', 'CF', 'TD', 'KM', 
                        'CD', 'CG', 'CI', 'DJ',
                        'GA', 'GN', 'LU', 'MG',
                        'ML', 'MC', 'NE', 'SN',
                        'SC', 'TG'}:
            translation.activate('fr')
        elif value in {'DZ', 'EG', 'IQ', 'IL',
                        'JO', 'KW', 'LB', 'LY',
                        'MR', 'MA', 'OM', 'QA',
                        'SA', 'SO', 'SY', 'TN',
                        'AE', 'YE'}:
            translation.activate('ar')
        elif value in {'AO', 'BR', 'CV', 'TL', 
                        'GW', 'MZ', 'PT', 'ST'}:
            translation.activate('pt')
        elif value in {'BY', 'RU', 'KZ', 'KG'}:
            translation.activate('ru')
        elif value in {'PH'}:
            translation.activate('ta')
        elif value in {'DE', 'AT', 'LI', 'CH'}:
            translation.activate('de')
        elif value in {'ID'}:
            translation.activate('id')
        elif value in {'IT', 'SM', 'VA'}:
            translation.activate('it')
        elif value in {'JP'}:
            translation.activate('ja')
        elif value in {'VN'}:
            translation.activate('vi')
        elif value in {'AD', 'AR', 'BO', 'CL',
                        'CO', 'CR', 'CU', 'DO',
                        'EC', 'SV', 'GQ', 'GT',
                        'HN', 'MX', 'NI', 'PA',
                        'PY', 'PE', 'ES', 'UY',
                        'VE'}:
            translation.activate('es')
        elif value in {'CN', 'HK'}:
            translation.activate('zh-hans')
        elif value in {'KR', 'KP'}:
            translation.activate('ko')
        elif value in {'NO'}:
            translation.activate('nn')
        else:
            translation.activate('en')

    # Language Change
    def middleware(request):
        response = get_response(request)
        if request.user.is_authenticated:
            translation.activate(request.user.profiles.lang)
        else:
            value = request.COOKIES.get('cookie_name_user')
            if value is None:
                # Cookie is not set
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                curl = requests.get(f'http://ip-api.com/csv/{ip}?fields=countryCode')
                text = curl.text
                country_code = text.split('\n')[0]

                # response.set_cookie('cookie_name', country_code)
                # this function will be used to make cookie
                set_cookie(response, 'cookie_name_user', country_code, 1)
                value = country_code

            # activate language is user is not authenticated
            active_translate(value)
        return response
    return middleware

