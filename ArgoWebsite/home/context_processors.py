from django.utils.translation import get_language
from .models import NavbarLinksPage, FooterLinksPage
from wagtail.models import Locale


def navbar_links_processor(request):
    lang_code = get_language()
    locale = Locale.objects.filter(language_code=lang_code).first()

    if locale:
        translated_navbar_page = NavbarLinksPage.objects.filter(locale=locale).first()
        if not translated_navbar_page or not translated_navbar_page.navbar_links:
            navbar_page = NavbarLinksPage.objects.first()
        else:
            navbar_page = translated_navbar_page
    else:
        navbar_page = NavbarLinksPage.objects.first()

    return {
        'navbar_links': navbar_page.navbar_links if navbar_page else [],
    }

def footer_links_processor(request):
    lang_code = get_language()
    locale = Locale.objects.filter(language_code=lang_code).first()

    if locale:
        translated_footer_page = FooterLinksPage.objects.filter(locale=locale).first()
        if not translated_footer_page or not translated_footer_page.first_column:
            first_column = FooterLinksPage.objects.first()
        else:
            first_column = translated_footer_page
        if not translated_footer_page or not translated_footer_page.second_column:
            second_column = FooterLinksPage.objects.first()
        else:
            second_column = translated_footer_page
    else:
        first_column = FooterLinksPage.objects.first()
        second_column = FooterLinksPage.objects.first()

    return {
        'footer_first_column_links': first_column.first_column if first_column else [],
        'footer_second_column_links': second_column.second_column if second_column else [],

    }
