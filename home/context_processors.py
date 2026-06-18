from django.utils.translation import get_language
from .models import NavbarLinksPage, FooterLinksPage
from wagtail.models import Locale, Site


def navbar_links_processor(request):
    lang_code = get_language()
    locale = Locale.objects.filter(language_code=lang_code).first()

    if locale:
        translated_navbar_page = NavbarLinksPage.objects.filter(locale=locale).first()
        if not translated_navbar_page or not translated_navbar_page.navbar_links:
            navbar_page = NavbarLinksPage.objects.first()
        else:
            navbar_page = translated_navbar_page
        if not translated_navbar_page or not translated_navbar_page.eu_certificate_desktop:
            navbar_page_eu_d = NavbarLinksPage.objects.first()
        else:
            navbar_page_eu_d = translated_navbar_page
        if not translated_navbar_page or not translated_navbar_page.eu_certificate_mobile:
            navbar_page_eu_m = NavbarLinksPage.objects.first()
        else:
            navbar_page_eu_m = translated_navbar_page
        if not translated_navbar_page or not translated_navbar_page.eu_redirect:
            navbar_page_eu_r = NavbarLinksPage.objects.first()
        else:
            navbar_page_eu_r = translated_navbar_page
        if not translated_navbar_page or not translated_navbar_page.zus_certificate_desktop:
            navbar_page_zus_d = NavbarLinksPage.objects.first()
        else:
            navbar_page_zus_d = translated_navbar_page
        if not translated_navbar_page or not translated_navbar_page.zus_certificate_mobile:
            navbar_page_zus_m = NavbarLinksPage.objects.first()
        else:
            navbar_page_zus_m = translated_navbar_page
        if not translated_navbar_page or not translated_navbar_page.zus_redirect:
            navbar_page_zus_r = NavbarLinksPage.objects.first()
        else:
            navbar_page_zus_r = translated_navbar_page
    else:
        navbar_page = NavbarLinksPage.objects.first()
        navbar_page_eu_d = NavbarLinksPage.objects.first()
        navbar_page_eu_m = NavbarLinksPage.objects.first()
        navbar_page_eu_r = NavbarLinksPage.objects.first()
        navbar_page_zus_d = NavbarLinksPage.objects.first()
        navbar_page_zus_m = NavbarLinksPage.objects.first()
        navbar_page_zus_r = NavbarLinksPage.objects.first()

    return {
        'navbar_links': navbar_page.navbar_links if navbar_page else [],
        'eu_certificate_desktop': navbar_page_eu_d.eu_certificate_desktop if navbar_page_eu_d else [],
        'eu_certificate_mobile': navbar_page_eu_m.eu_certificate_mobile if navbar_page_eu_m else [],
        'eu_redirect': navbar_page_eu_r.eu_redirect if navbar_page_eu_r else [],
        'zus_certificate_desktop': navbar_page_zus_d.zus_certificate_desktop if navbar_page_zus_d else [],
        'zus_certificate_mobile': navbar_page_zus_m.zus_certificate_mobile if navbar_page_zus_m else [],
        'zus_redirect': navbar_page_zus_r.zus_redirect if navbar_page_zus_r else [],

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
        if not translated_footer_page or not translated_footer_page.eu_footer:
            eu_footer = FooterLinksPage.objects.first()
        else:
            eu_footer = translated_footer_page

    else:
        first_column = FooterLinksPage.objects.first()
        second_column = FooterLinksPage.objects.first()

        eu_footer = FooterLinksPage.objects.first()


    return {
        'footer_first_column_links': first_column.first_column if first_column else [],
        'footer_second_column_links': second_column.second_column if second_column else [],
        'eu_footer': eu_footer.eu_footer if eu_footer else [],

    }

def home_link_processor(request):

    locale = Locale.get_active()


    site = Site.objects.filter(is_default_site=True).select_related('root_page').first()
    if not site or not site.root_page:
        return {'home_page': None}

    home = site.root_page

    if locale and home.locale_id != locale.id:
        home = home.get_translation_or_none(locale) or home

    return {'home_page': home}