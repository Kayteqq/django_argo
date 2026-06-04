import json
from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.db import models
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail, EmailMessage
from django import forms
from wagtail.admin.panels import PageChooserPanel, FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.blocks import CharBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page, Orderable, Locale
from wagtail.fields import StreamField, RichTextField
from modelcluster.fields import ParentalKey

from .blocks import NavbarBlockContainer, FooterBlockContainer
from .forms import ContactForm, ConfigForm
from .reports import generate_pdf

@register_setting
class SocialMediaSettings(BaseSiteSetting):
    url_x           = models.URLField("URL X",          blank=True, null=True)
    url_youtube     = models.URLField("URL Facebook",   blank=True, null=True)
    url_instagram   = models.URLField("URL Instagram",  blank=True, null=True)
    url_linkedin    = models.URLField("URL Linkedin",   blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('url_x'),
        FieldPanel('url_youtube'),
        FieldPanel('url_instagram'),
        FieldPanel('url_linkedin'),
    ]

    class Meta:
        verbose_name = 'Social Media - Linki'
        verbose_name_plural = 'Social Media - Linki'

@register_setting
class CompanyParametersSetting(BaseSiteSetting):
    company_name = models.CharField("company name", max_length=255, blank=True)
    address_line_1 = models.CharField("address line 1", max_length=255, blank=True)
    address_line_2 = models.CharField("address line 2", max_length=255, blank=True)
    country = models.CharField("country", max_length=255, blank=True)
    nip = models.CharField('nip', max_length=255, blank=True)
    regon = models.CharField("regon", max_length=255, blank=True)
    stamp = models.CharField("stamp", max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('company_name'),
        FieldPanel('address_line_1'),
        FieldPanel('address_line_2'),
        FieldPanel('nip'),
        FieldPanel('regon'),
        FieldPanel('country'),
        FieldPanel('stamp'),
    ]

    class Meta:
        verbose_name = "Company Parameters"
        verbose_name_plural = "Company Parameters"

class NavbarLinksPage(Page):
    parent_page_types = ['RootRedirectPage']
    subpage_types = []
    max_count = 1
    template = 'home/navbar_preview_page.html'

    navbar_links = StreamField(
        NavbarBlockContainer,
        blank=True,
        null=True,
        verbose_name='Navbar Links',
    )

    content_panels = Page.content_panels + [
        FieldPanel('navbar_links'),
    ]

    show_in_menus = False
    search_fields = []

    def get_url_parts(self, request=None):
        return None

    def get_url(self, request=None, current_site=None):
        return None

    def serve(self, request, *args, **kwargs):
        raise PermissionDenied("This page cannot be accessed directly.")

    class Meta:
        verbose_name = 'Navbar Links'
        verbose_name_plural = 'Navbar Links'

class FooterLinksPage(Page):
    parent_page_types = ['RootRedirectPage']
    subpage_types = []
    max_count = 1
    template = 'home/navbar_preview_page.html'


    first_column = StreamField(
        FooterBlockContainer,
        blank=True,
        null=True,
        verbose_name='Links in First Column',
    )
    second_column = StreamField(
        FooterBlockContainer,
        blank=True,
        null=True,
        verbose_name='Links in Second Column',
    )

    eu_title = models.CharField("ZUS Title", max_length=255, blank=True)
    eu_text = models.TextField("ZUS Text", blank=True)

    eu_certificate = models.ForeignKey(
        Image,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Zus Certificate Image',
    )
    eu_footer = models.ForeignKey(
        Image,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='EU Footer Image',
    )

    content_panels = Page.content_panels + [
        FieldPanel('first_column'),
        FieldPanel('second_column'),
        FieldPanel('eu_certificate'),
        FieldPanel('eu_title'),
        FieldPanel('eu_text'),
        FieldPanel('eu_footer'),
    ]

    show_in_menus = False
    search_fields = []

    def get_url_parts(self, request=None):
        return None

    def get_url(self, request=None, current_site=None):
        return None

    def serve(self, request, *args, **kwargs):
        raise PermissionDenied("This page cannot be accessed directly.")

    class Meta:
        verbose_name = 'Footer Links'
        verbose_name_plural = 'Footer Links'

class RootRedirectPage(Page):
    parent_page_types = ['wagtailcore.Page']
    max_count = 1
    redirect_to = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        PageChooserPanel('redirect_to'),
    ]

    def serve(self, request, *args, **kwargs):
        if self.redirect_to:
            return redirect(self.redirect_to.url)
        else:
            # Jeśli nie wybrano strony, możesz przekierować np. na stronę główną
            return redirect('/')

class MainPageCarouselItem(Orderable):
    page = ParentalKey('MainPage', related_name='hero_images')
    image = models.ForeignKey(
        Image,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    panels = [FieldPanel('image')]

class MainPage(Page):
    max_count = 1
    template = 'home/main_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    motto_lead = models.CharField("Lead - Lead", max_length=255, blank=True)
    title_lead = models.CharField("Lead - Title", max_length=255, blank=True)
    text_lead = models.TextField("Lead - Text", blank=True)
    button_lead = models.CharField("Lead - Button Text ", max_length=255, blank=True)
    redirect_lead = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    title_steel_carpentry = models.CharField("Carpentry - Steel Title", max_length=255, blank=True)
    text_steel_carpentry = models.TextField("Carpentry - Steel Text", blank=True)
    button_steel_carpentry = models.CharField("Carpentry - Steel Button Text ", max_length=255, blank=True)
    redirect_steel_carpentry = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_steel_carpentry = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    title_aluminium_carpentry = models.CharField("Carpentry - Aluminium Title", max_length=255, blank=True)
    text_aluminium_carpentry = models.TextField("Carpentry - Aluminium Text", blank=True)
    button_aluminium_carpentry = models.CharField("Carpentry - Aluminium Button Text ", max_length=255, blank=True)
    redirect_aluminium_carpentry = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_aluminium_carpentry = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    motto_steel = models.CharField("Steel - Lead", max_length=255, blank=True)
    title_steel = models.CharField("Steel - Title", max_length=255, blank=True)
    text_steel = models.TextField("Steel - Text", blank=True)
    button_steel = models.CharField("Steel - Button Text ", max_length=255, blank=True)
    redirect_steel = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_steel = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    motto_aluminium = models.CharField("Aluminium - Lead", max_length=255, blank=True)
    title_aluminium = models.CharField("Aluminium - Title", max_length=255, blank=True)
    text_aluminium = models.TextField("Aluminium - Text", blank=True)
    button_aluminium = models.CharField("Aluminium - Button Text ", max_length=255, blank=True)
    redirect_aluminium = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_aluminium = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    motto_configurator = models.CharField("Configurator - Lead", max_length=255, blank=True)
    title_configurator = models.CharField("Configurator - Title", max_length=255, blank=True)
    button_configurator = models.CharField("Configurator - Button Text ", max_length=255, blank=True)
    redirect_configurator = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    video_poster = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    video = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('hero_images'),
            ],
            heading="Section Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_lead'),
                FieldPanel('title_lead'),
                FieldPanel('text_lead'),
                FieldPanel('button_lead'),
                FieldPanel('redirect_lead'),
            ],
            heading="Section Lead",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_steel_carpentry'),
                FieldPanel('title_steel_carpentry'),
                FieldPanel('text_steel_carpentry'),
                FieldPanel('button_steel_carpentry'),
                FieldPanel('redirect_steel_carpentry'),
                FieldPanel('image_aluminium_carpentry'),
                FieldPanel('title_aluminium_carpentry'),
                FieldPanel('text_aluminium_carpentry'),
                FieldPanel('button_aluminium_carpentry'),
                FieldPanel('redirect_aluminium_carpentry'),
            ],
            heading="Section Carpentry",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_steel'),
                FieldPanel('motto_steel'),
                FieldPanel('title_steel'),
                FieldPanel('text_steel'),
                FieldPanel('button_steel'),
                FieldPanel('redirect_steel'),
            ],
            heading="Section Steel",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_aluminium'),
                FieldPanel('motto_aluminium'),
                FieldPanel('title_aluminium'),
                FieldPanel('text_aluminium'),
                FieldPanel('button_aluminium'),
                FieldPanel('redirect_aluminium'),
            ],
            heading="Section Aluminium",
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_configurator'),
                FieldPanel('title_configurator'),
                FieldPanel('button_configurator'),
                FieldPanel('redirect_configurator'),
            ],
            heading="Section Text",
        ),
        MultiFieldPanel(
            [
                FieldPanel('video_poster'),
                FieldPanel('video'),
            ],
            heading="Section Video",
        )
    ]

class AboutPageCarouselItem(Orderable):
    page = ParentalKey('AboutPage', related_name='certificates')

    title = models.CharField("Cartificate Title", max_length=255, blank=True)
    text = models.TextField("Certificate Text", blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    panels = [
        FieldPanel('image'),
        FieldPanel('title'),
        FieldPanel('text'),
    ]

class AboutPageReferencesItem(Orderable):
    page = ParentalKey('AboutPage', related_name='references')

    title = models.CharField("Reference Title", max_length=255, blank=True)
    text = models.TextField("Reference Text", blank=True)
    sign = models.TextField("Reference Sign", blank=True)
    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
        FieldPanel('sign'),
    ]

class AboutPage(Page):
    max_count = 1
    template = 'home/about_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    motto_hero = models.CharField("Lead - Hero", max_length=255, blank=True)
    title_hero = models.CharField("Title - Hero", max_length=255, blank=True)
    text_hero = models.TextField("Text - Hero", blank=True)
    image_hero = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    motto_quality = models.CharField("Lead - Quality", max_length=255, blank=True)
    title_quality = models.CharField("Title - Quality", max_length=255, blank=True)
    text_quality = models.TextField("Text - Quality", blank=True)
    image_quality = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    motto_project = models.CharField("Lead - Partners", max_length=255, blank=True)
    title_project = models.CharField("Title - Partners", max_length=255, blank=True)
    text_project = models.TextField("Text - Partners", blank=True)
    image_project = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    button_project = models.CharField("Button Text - Partners", max_length=255, blank=True)
    redirect_project = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    provider_profiles_project  = models.CharField("Profiles Provider Desc - Partners", max_length=255, blank=True)
    logos_profiles_project = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    provider_glass_project  = models.CharField("Glass Provider Desc - Partners", max_length=255, blank=True)
    logos_glass_project = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    provider_software_project  = models.CharField("Software Provider Desc - Partners", max_length=255, blank=True)
    logos_software_project = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    image_team = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_team = models.CharField("Title - Team", max_length=255, blank=True)
    text_team = models.TextField("Text - Team", blank=True)


    title_references = models.CharField("Title - References", max_length=255, blank=True)
    image_references = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')


    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('image_hero'),
                FieldPanel('motto_hero'),
                FieldPanel('title_hero'),
                FieldPanel('text_hero')
            ],
            heading="Section Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_quality'),
                FieldPanel('motto_quality'),
                FieldPanel('title_quality'),
                FieldPanel('text_quality'),
            ],
            heading="Section Quality",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_project'),
                FieldPanel('motto_project'),
                FieldPanel('title_project'),
                FieldPanel('text_project'),
                FieldPanel('button_project'),
                FieldPanel('redirect_project'),
                FieldPanel('provider_profiles_project'),
                FieldPanel('logos_profiles_project'),
                FieldPanel('provider_glass_project'),
                FieldPanel('logos_glass_project'),
                FieldPanel('provider_software_project'),
                FieldPanel('logos_software_project'),
            ],
            heading="Section Partners",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_team'),
                FieldPanel('title_team'),
                FieldPanel('text_team'),
            ],
            heading='Section Team',
        ),
        MultiFieldPanel(
            [
                InlinePanel('certificates'),
            ],
            heading="Section Certificates",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_references'),
                FieldPanel('title_references'),
                InlinePanel('references')
            ],
            heading="Section References",
        )
    ]

class CarpentrySteelPageCarouselItem(Orderable):
    page = ParentalKey('CarpentrySteelPage', related_name='realizations_images')
    image = models.ForeignKey(
        Image,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    panels = [FieldPanel('image')]

class CarpentrySteelPage(Page):
    max_count = 1
    template = 'home/carpentry_steel_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    image_hero = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_hero = models.CharField("Title - Hero", max_length=255, blank=True)
    text_hero = models.TextField("Text - Hero", blank=True)


    title_collections = models.CharField("Title - Collections", max_length=255, blank=True)
    text_collections = models.TextField("Text - Collections", blank=True)

    image_1_collections = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    subtitle_1_collections = models.CharField("Subtitle Industrial - Collections", max_length=255, blank=True)
    text_1_collections = models.TextField("Text Industrial - Collections", blank=True)
    button_1_collections = models.CharField("Button Industrial - Collections", max_length=255, blank=True)
    redirect_1_collections = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    image_2_collections = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    subtitle_2_collections = models.CharField("Subtitle Vintage - Collections", max_length=255, blank=True)
    text_2_collections = models.TextField("Text Vintage - Collections", blank=True)
    button_2_collections = models.CharField("Button Vintage - Collections", max_length=255, blank=True)
    redirect_2_collections = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    image_3_collections = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    subtitle_3_collections = models.CharField("Subtitle Glamour - Collections", max_length=255, blank=True)
    text_3_collections = models.TextField("Text Glamour - Collections", blank=True)
    button_3_collections = models.CharField("Button Glamour - Collections", max_length=255, blank=True)
    redirect_3_collections = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    title_realizations = models.CharField("Title - Realization", max_length=255, blank=True)

    image_projects = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_projects = models.CharField("Title - Projects", max_length=255, blank=True)
    text_projects = models.TextField("Text - Projects", blank=True)
    button_projects = models.CharField("Button Text - Projects", max_length=255, blank=True)
    redirect_projects = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    image_divider = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')



    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('image_hero'),
                FieldPanel('title_hero'),
                FieldPanel('text_hero'),
            ],
            heading="Section Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel('title_collections'),
                FieldPanel('text_collections'),

                FieldPanel('image_1_collections'),
                FieldPanel('subtitle_1_collections'),
                FieldPanel('text_1_collections'),
                FieldPanel('button_1_collections'),
                FieldPanel('redirect_1_collections'),

                FieldPanel('image_2_collections'),
                FieldPanel('subtitle_2_collections'),
                FieldPanel('text_2_collections'),
                FieldPanel('button_2_collections'),
                FieldPanel('redirect_2_collections'),

                FieldPanel('image_3_collections'),
                FieldPanel('subtitle_3_collections'),
                FieldPanel('text_3_collections'),
                FieldPanel('button_3_collections'),
                FieldPanel('redirect_3_collections'),
            ],
            heading="Section Collections",
        ),
        MultiFieldPanel(
            [
                FieldPanel('title_realizations'),
                InlinePanel('realizations_images'),
            ],
            heading="Section Realizations",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_projects'),
                FieldPanel('title_projects'),
                FieldPanel('text_projects'),
                FieldPanel('button_projects'),
                FieldPanel('redirect_projects'),
            ],
            heading="Section Projects",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_divider'),
            ],
            heading="Section Image Divider",
        )
    ]

class CarpentryAluminiumPageCarouselItem(Orderable):
    page = ParentalKey('CarpentryAluminiumPage', related_name='realizations_images')
    image = models.ForeignKey(
        Image,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    panels = [FieldPanel('image')]

class CarpentryAluminiumPage(Page):
    max_count = 1
    template = 'home/carpentry_aluminium_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    image_hero = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_hero = models.CharField("Title - Hero", max_length=255, blank=True)
    text_hero = models.TextField("Text - Hero", blank=True)

    title_realizations = models.CharField("Title - Realization", max_length=255, blank=True)

    image_projects = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_projects = models.CharField("Title - Projects", max_length=255, blank=True)
    text_projects = models.TextField("Text - Projects", blank=True)
    button_projects = models.CharField("Button Text - Projects", max_length=255, blank=True)
    redirect_projects = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    image_divider = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('image_hero'),
                FieldPanel('title_hero'),
                FieldPanel('text_hero'),
            ],
            heading="Section Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel('title_realizations'),
                InlinePanel('realizations_images'),
            ],
            heading="Section Realizations",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_projects'),
                FieldPanel('title_projects'),
                FieldPanel('text_projects'),
                FieldPanel('button_projects'),
                FieldPanel('redirect_projects'),
            ],
            heading="Section Projects",
        ),
        MultiFieldPanel(
            [
                FieldPanel('image_divider'),
            ],
            heading="Section Image Divider",
        )
    ]

class CollectionPageColdSystems(Orderable):
    page = ParentalKey('CollectionPage', related_name='cold_systems')
    METAL_TYPES = [
        ('b', 'Bronze'),
        ('s', 'Steel'),
    ]

    logo = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    name = models.CharField("Name", max_length=255, blank=True)
    metal = models.CharField("Metal", max_length=1, choices=METAL_TYPES, default='s')
    url = models.URLField(max_length=500, blank=True)

    content_panels = [
        FieldPanel('logo'),
        FieldPanel('name'),
        FieldPanel('metal', widget=forms.RadioSelect),
	FieldPanel('url')
    ]

class CollectionPageHotSystems(Orderable):
    page = ParentalKey('CollectionPage', related_name='hot_systems')
    METAL_TYPES = [
        ('b', 'Bronze'),
        ('s', 'Steel'),
    ]

    logo = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    name = models.CharField("Name", max_length=255, blank=True)
    metal = models.CharField("Metal", max_length=1, choices=METAL_TYPES, default='s')
    url = models.URLField(max_length=500, blank=True)

    content_panels = [
        FieldPanel('logo'),
        FieldPanel('name'),
        FieldPanel('metal', widget=forms.RadioSelect),
	FieldPanel('url')
    ]

class CollectionPage(Page):
    template = 'home/collection_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    motto_hero = models.CharField("Hero - Lead", max_length=255, blank=True)
    title_hero = models.CharField("Hero - Title", max_length=255, blank=True)
    text_hero = models.TextField("Hero - Text", blank=True)
    button_hero = models.CharField("Hero - Button Text ", max_length=255, blank=True)
    redirect_hero = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    image_hero = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


    motto_display_1 = models.CharField("Description 1/2 - Lead", max_length=255, blank=True)
    title_display_1 = models.CharField("Description 1/2 - Title", max_length=255, blank=True)
    text_display_1 = models.TextField("Description 1/2 - Text", blank=True)
    image_display_1 = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    motto_display_2 = models.CharField("Description 2/2 - Lead", max_length=255, blank=True)
    title_display_2 = models.CharField("Description 2/2 - Title", max_length=255, blank=True)
    text_display_2 = models.TextField("Description 2/2 - Text", blank=True)
    video_display_2 = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    motto_details = models.CharField("Details Summary - Lead", max_length=255, blank=True)
    title_details = models.CharField("Details Summary - Title", max_length=255, blank=True)
    text_details = models.TextField("Details Summary - Text", blank=True)

    hot_details = models.CharField("Details Summary - Hot Profile Subtitle", max_length=255, blank=True)
    cold_details = models.CharField("Details Summary - Cold Profile Subtitle", max_length=255, blank=True)

    bronze_details = models.CharField("Details Summary - Bronze Name", max_length=255, blank=True)
    steel_details = models.CharField("Details Summary - Steel Name", max_length=255, blank=True)

    motto_configurator = models.CharField("Configurator - Lead", max_length=255, blank=True)
    title_configurator = models.CharField("Configurator - Title", max_length=255, blank=True)
    button_configurator = models.CharField("Configurator - Button Text ", max_length=255, blank=True)
    redirect_configurator = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('motto_hero'),
                FieldPanel('title_hero'),
                FieldPanel('text_hero'),
                FieldPanel('button_hero'),
                FieldPanel('redirect_hero'),
                FieldPanel('image_hero'),
            ],
            heading='Section Hero',
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_display_1'),
                FieldPanel('title_display_1'),
                FieldPanel('text_display_1'),
                FieldPanel('image_display_1'),
            ],
            heading='Section Description - First Half',
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_display_2'),
                FieldPanel('title_display_2'),
                FieldPanel('text_display_2'),
                FieldPanel('video_display_2'),
            ],
            heading='Section Description - Second Half',
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_details'),
                FieldPanel('title_details'),
                FieldPanel('text_details'),
                FieldPanel('steel_details'),
                FieldPanel('bronze_details'),
                FieldPanel('cold_details'),
                InlinePanel('cold_systems'),
                FieldPanel('hot_details'),
                InlinePanel('hot_systems'),

            ],
            heading='Section Details',
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_configurator'),
                FieldPanel('title_configurator'),
                FieldPanel('button_configurator'),
                FieldPanel('redirect_configurator'),
            ],
            heading='Section Configurator',
        )
    ]

class ConfiguratorPage(RoutablePageMixin, Page):
    max_count = 1
    template = 'home/configurator_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    is_featured = models.BooleanField(default=True, verbose_name="Is page featured?")

    motto_hero = models.CharField("Hero - Lead", max_length=255, blank=True)
    title_hero = models.CharField("Hero - Title", max_length=255, blank=True)
    text_hero = models.TextField("Hero - Text", blank=True)
    button_hero = models.CharField("Hero - Button Text ", max_length=255, blank=True)

    step_word = models.CharField("Step Word", max_length=32, blank=True)
    button_word = models.CharField("Button Word", max_length=32, blank=True)
    confirm_word = models.CharField("Confirm Word", max_length=32, blank=True)


    title_step_1 = models.CharField("Step 1 - Title", max_length=255, blank=True)
    title_step_2 = models.CharField("Step 2 - Title", max_length=255, blank=True)
    title_step_3 = models.CharField("Step 3 - Title", max_length=255, blank=True)
    title_step_4 = models.CharField("Step 4 - Title", max_length=255, blank=True)
    title_step_5 = models.CharField("Step 5 - Title", max_length=255, blank=True)
    title_step_6 = models.CharField("Step 6 - Title", max_length=255, blank=True)

    description_step_1a = models.CharField("Step 1a - Description", max_length=255, blank=True)
    description_step_1b = models.CharField("Step 1b - Description", max_length=255, blank=True)
    subtitle_step_1b = models.CharField("Step 1b - Subtitle", max_length=255, blank=True)
    description_step_2 = models.CharField("Step 2 - Description", max_length=255, blank=True)
    description_step_3 = models.CharField("Step 3 - Description", max_length=255, blank=True)
    description_step_4 = models.CharField("Step 4 - Description", max_length=255, blank=True)
    description_step_5a = models.CharField("Step 5a - Description", max_length=255, blank=True)
    subtitle_step_5a = models.CharField("Step 5a - Subtitle", max_length=255, blank=True)
    description_step_5b = models.CharField("Step 5b - Description", max_length=255, blank=True)
    subtitle_step_5b = models.CharField("Step 5b - Subtitle", max_length=255, blank=True)
    description_step_6 = models.CharField("Step 6 - Description", max_length=255, blank=True)

    # step 1
    step_1_choice_1_subtitle = models.CharField("Step 1 - Choice 1 Subtitle", max_length=255, blank=True)
    step_1_choice_2_subtitle = models.CharField("Step 1 - Choice 2 Subtitle", max_length=255, blank=True)
    step_1_choice_3_subtitle = models.CharField("Step 1 - Choice 3 Subtitle", max_length=255, blank=True)

    step_1_choice_1_text = models.TextField("Step 1 - Choice 1 Text", blank=True)
    step_1_choice_2_text = models.TextField("Step 1 - Choice 2 Text", blank=True)
    step_1_choice_3_text = models.TextField("Step 1 - Choice 3 Text", blank=True)

    step_1_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_1_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_1_choice_3_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # step 2
    step_2_choice_1_subtitle = models.CharField("Step 2 - Choice 1 Subtitle", max_length=255, blank=True)
    step_2_choice_2_subtitle = models.CharField("Step 2 - Choice 2 Subtitle", max_length=255, blank=True)

    step_2_choice_1_text = models.CharField("Step 2 - Choice 2 Text", max_length=255,  blank=True)
    step_2_choice_2_text = models.CharField("Step 2 - Choice 2 Text", max_length=255,  blank=True)

    step_2_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_2_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # step 3
    step_3_choice_1_title = models.CharField("Step 3 - Choice 1 Title", max_length=255, blank=True)
    step_3_choice_2_title = models.CharField("Step 3 - Choice 2 Title", max_length=255, blank=True)
    step_3_choice_3_title = models.CharField("Step 3 - Choice 3 Title", max_length=255, blank=True)
    step_3_choice_4_title = models.CharField("Step 3 - Choice 4 Title", max_length=255, blank=True)
    step_3_choice_5_title = models.CharField("Step 3 - Choice 5 Title", max_length=255, blank=True)

    step_3_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_3_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_3_choice_3_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_3_choice_4_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_3_choice_5_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')


    # step 4
    step_4_input_1_option_1 = models.CharField("Step 4 - Input 1 Option 1", max_length=255, blank=True)
    step_4_input_1_option_2 = models.CharField("Step 4 - Input 1 Option 2", max_length=255, blank=True)
    step_4_input_1_option_3 = models.CharField("Step 4 - Input 1 Option 3", max_length=255, blank=True)
    step_4_input_2 = models.CharField("Step 4 - Input 2", max_length=255, blank=True)
    step_4_input_3 = models.CharField("Step 4 - Input 3", max_length=255, blank=True)
    step_4_input_4 = models.CharField("Step 4 - Input 4", max_length=255, blank=True)
    step_4_input_5 = models.CharField("Step 4 - Input 5", max_length=255, blank=True)
    step_4_input_6 = models.CharField("Step 4 - Input 6", max_length=255, blank=True)
    step_4_input_7 = models.CharField("Step 4 - Input 7", max_length=255, blank=True)
    step_4_input_8 = models.CharField("Step 4 - Input 8", max_length=255, blank=True)
    step_4_input_9 = models.CharField("Step 4 - Input 9", max_length=255, blank=True)

    # step 5 industrial
    step_5_industrial_choice_1_subtitle = models.CharField("Step 5 - Industrial - Choice 1 Subtitle", max_length=255, blank=True)
    step_5_industrial_choice_2_subtitle = models.CharField("Step 5 - Industrial - Choice 2 Subtitle", max_length=255, blank=True)
    step_5_industrial_choice_3_subtitle = models.CharField("Step 5 - Industrial - Choice 3 Subtitle", max_length=255, blank=True)
    step_5_industrial_choice_1_text = models.TextField("Step 5 - Industrial - Choice 1 Text", blank=True)
    step_5_industrial_choice_2_text = models.TextField("Step 5 - Industrial - Choice 2 Text", blank=True)
    step_5_industrial_choice_3_text = models.TextField("Step 5 - Industrial - Choice 3 Text", blank=True)
    step_5_industrial_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_5_industrial_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_5_industrial_choice_3_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # step 5 vintage
    step_5_vintage_choice_1_subtitle = models.CharField("Step 5 - Vintage - Choice 1 Subtitle", max_length=255, blank=True)
    step_5_vintage_choice_2_subtitle = models.CharField("Step 5 - Vintage - Choice 2 Subtitle", max_length=255, blank=True)
    step_5_vintage_choice_3_subtitle = models.CharField("Step 5 - Vintage - Choice 3 Subtitle", max_length=255, blank=True)
    step_5_vintage_choice_1_text = models.TextField("Step 5 - Vintage - Choice 1 Text", blank=True)
    step_5_vintage_choice_2_text = models.TextField("Step 5 - Vintage - Choice 2 Text", blank=True)
    step_5_vintage_choice_3_text = models.TextField("Step 5 - Vintage - Choice 3 Text", blank=True)
    step_5_vintage_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_5_vintage_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_5_vintage_choice_3_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # step 5 glamour
    step_5_glamour_choice_1_subtitle = models.CharField("Step 5 - Glamour - Choice 1 Subtitle", max_length=255, blank=True)
    step_5_glamour_choice_2_subtitle = models.CharField("Step 5 - Glamour - Choice 2 Subtitle", max_length=255, blank=True)
    step_5_glamour_choice_3_subtitle = models.CharField("Step 5 - Glamour - Choice 3 Subtitle", max_length=255, blank=True)
    step_5_glamour_choice_1_text = models.TextField("Step 5 - Glamour - Choice 1 Text", blank=True)
    step_5_glamour_choice_2_text = models.TextField("Step 5 - Glamour - Choice 2 Text", blank=True)
    step_5_glamour_choice_3_text = models.TextField("Step 5 - Glamour - Choice 3 Text", blank=True)
    step_5_glamour_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_5_glamour_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_5_glamour_choice_3_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # step 5 color
    step_5_color_placeholder = models.CharField("Step 5 - Color - Placeholder", max_length=255, blank=True)

    # step 6
    step_6_choice_1_subtitle = models.CharField("Step 6 - Contactron Subtitle", max_length=255, blank=True)
    step_6_choice_2_subtitle = models.CharField("Step 6 - Multi Point Lock Subtitle", max_length=255, blank=True)
    step_6_choice_3_subtitle = models.CharField("Step 6 - Actuator Subtitle", max_length=255, blank=True)
    step_6_choice_1_text = models.TextField("Step 6 - Contactron Text", blank=True)
    step_6_choice_2_text = models.TextField("Step 6 - Multi Point Lock Text", blank=True)
    step_6_choice_3_text = models.TextField("Step 6 - Actuator Text", blank=True)
    step_6_choice_1_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_6_choice_2_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    step_6_choice_3_img = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    title_summary = models.CharField("Summary - Title", max_length=255, blank=True)
    text_summary = models.CharField("Summary - Text", max_length=255, blank=True)
    styleline_summary = models.CharField("Summary - Style Line", max_length=255, blank=True)
    usecase_summary = models.CharField("Summary - Use Case", max_length=255, blank=True)
    type_summary = models.CharField("Summary - Type", max_length=255, blank=True)
    additions_summary = models.CharField("Summary - Additions", max_length=255, blank=True)
    color_summary = models.CharField("Summary - Color Base", max_length=255, blank=True)
    color_second_summary = models.CharField("Summary - Color Second", max_length=255, blank=True)
    smarthome_summary = models.CharField("Summary - Smart Home", max_length=255, blank=True)

    button_download_summary = models.CharField("Summary - Button Download", max_length=255, blank=True)
    button_mail_summary = models.CharField("Summary - Button Mail", max_length=255, blank=True)
    button_back_summary = models.CharField("Summary - Back", max_length=255, blank=True)
    button_redirection_summary = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )




    content_panels = Page.content_panels + [
        FieldPanel("is_featured"),
	MultiFieldPanel(
            [
                FieldPanel("motto_hero"),
                FieldPanel("title_hero"),
                FieldPanel("text_hero"),
                FieldPanel("button_hero"),
            ],
            heading='Section Hero',
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_word"),
                FieldPanel("button_word"),
                FieldPanel("confirm_word"),
            ],
            heading='Base Configurator Parameters'
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_step_1"),
                FieldPanel("description_step_1a"),
                FieldPanel("description_step_1b"),
                FieldPanel("subtitle_step_1b"),
                FieldPanel("title_step_2"),
                FieldPanel("description_step_2"),
                FieldPanel("title_step_3"),
                FieldPanel("description_step_3"),
                FieldPanel("title_step_4"),
                FieldPanel("description_step_4"),
                FieldPanel("title_step_5"),
                FieldPanel("description_step_5a"),
                FieldPanel("subtitle_step_5a"),
                FieldPanel("description_step_5b"),
                FieldPanel("subtitle_step_5b"),
                FieldPanel("title_step_6"),
                FieldPanel("description_step_6"),
            ],
            heading='Configurator Step Titles'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_1_choice_1_subtitle"),
                FieldPanel("step_1_choice_1_text"),
                FieldPanel("step_1_choice_1_img"),
                FieldPanel("step_1_choice_2_subtitle"),
                FieldPanel("step_1_choice_2_text"),
                FieldPanel("step_1_choice_2_img"),
                FieldPanel("step_1_choice_3_subtitle"),
                FieldPanel("step_1_choice_3_text"),
                FieldPanel("step_1_choice_3_img"),
            ],
            heading='Configurator Step 1'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_2_choice_1_subtitle"),
                FieldPanel("step_2_choice_1_text"),
                FieldPanel("step_2_choice_1_img"),
                FieldPanel("step_2_choice_2_subtitle"),
                FieldPanel("step_2_choice_2_text"),
                FieldPanel("step_2_choice_2_img"),
            ],
            heading='Configurator Step 2'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_3_choice_1_title"),
                FieldPanel("step_3_choice_1_img"),
                FieldPanel("step_3_choice_2_title"),
                FieldPanel("step_3_choice_2_img"),
                FieldPanel("step_3_choice_3_title"),
                FieldPanel("step_3_choice_3_img"),
                FieldPanel("step_3_choice_4_title"),
                FieldPanel("step_3_choice_4_img"),
                FieldPanel("step_3_choice_5_title"),
                FieldPanel("step_3_choice_5_img"),
            ],
            heading='Configurator Step 3'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_4_input_1_option_1"),
                FieldPanel("step_4_input_1_option_2"),
                FieldPanel("step_4_input_1_option_3"),
                FieldPanel("step_4_input_2"),
                FieldPanel("step_4_input_3"),
                FieldPanel("step_4_input_4"),
                FieldPanel("step_4_input_5"),
                FieldPanel("step_4_input_6"),
                FieldPanel("step_4_input_7"),
                FieldPanel("step_4_input_8"),
                FieldPanel("step_4_input_9"),
            ],
            heading='Configurator Step 4'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_5_industrial_choice_1_subtitle"),
                FieldPanel("step_5_industrial_choice_1_text"),
                FieldPanel("step_5_industrial_choice_1_img"),
                FieldPanel("step_5_industrial_choice_2_subtitle"),
                FieldPanel("step_5_industrial_choice_2_text"),
                FieldPanel("step_5_industrial_choice_2_img"),
                FieldPanel("step_5_industrial_choice_3_subtitle"),
                FieldPanel("step_5_industrial_choice_3_text"),
                FieldPanel("step_5_industrial_choice_3_img"),
            ],
            heading='Configurator Step 5 Industrial'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_5_glamour_choice_1_subtitle"),
                FieldPanel("step_5_glamour_choice_1_text"),
                FieldPanel("step_5_glamour_choice_1_img"),
                FieldPanel("step_5_glamour_choice_2_subtitle"),
                FieldPanel("step_5_glamour_choice_2_text"),
                FieldPanel("step_5_glamour_choice_2_img"),
                FieldPanel("step_5_glamour_choice_3_subtitle"),
                FieldPanel("step_5_glamour_choice_3_text"),
                FieldPanel("step_5_glamour_choice_3_img"),
            ],
            heading='Configurator Step 5 Glamour'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_5_vintage_choice_1_subtitle"),
                FieldPanel("step_5_vintage_choice_1_text"),
                FieldPanel("step_5_vintage_choice_1_img"),
                FieldPanel("step_5_vintage_choice_2_subtitle"),
                FieldPanel("step_5_vintage_choice_2_text"),
                FieldPanel("step_5_vintage_choice_2_img"),
                FieldPanel("step_5_vintage_choice_3_subtitle"),
                FieldPanel("step_5_vintage_choice_3_text"),
                FieldPanel("step_5_vintage_choice_3_img"),
            ],
            heading='Configurator Step 5 Vintage'
        ),
        MultiFieldPanel(
            [
                FieldPanel("step_6_choice_1_subtitle"),
                FieldPanel("step_6_choice_1_text"),
                FieldPanel("step_6_choice_1_img"),
                FieldPanel("step_6_choice_2_subtitle"),
                FieldPanel("step_6_choice_2_text"),
                FieldPanel("step_6_choice_2_img"),
                FieldPanel("step_6_choice_3_subtitle"),
                FieldPanel("step_6_choice_3_text"),
                FieldPanel("step_6_choice_3_img"),
            ],
            heading='Configurator Step 6'
        ),
        MultiFieldPanel(
            [
                FieldPanel("title_summary"),
                FieldPanel("text_summary"),
                FieldPanel("styleline_summary"),
                FieldPanel("color_summary"),
                FieldPanel("usecase_summary"),
                FieldPanel("type_summary"),
                FieldPanel("additions_summary"),
                FieldPanel("color_second_summary"),
                FieldPanel("smarthome_summary"),
                FieldPanel("button_download_summary"),
                FieldPanel("button_mail_summary"),
                FieldPanel("button_back_summary"),
                FieldPanel("button_redirection_summary"),
            ],
            heading='Configurator Summary',
        )
    ]

    @route(r'download-pdf/$')
    def serve_pdf(self, request, *args, **kwargs):
        pdf_file = generate_pdf(request.session.get('config_data'), '', request.LANGUAGE_CODE)
        return HttpResponse(pdf_file, content_type='application/pdf')

    def serve(self, request, *args, **kwargs):
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"errors": "Invalid JSON"}, status=400)

            form = ConfigForm(data)
            if not form.is_valid():
                return JsonResponse({"errors": form.errors}, status=400)
            request.session['config_data'] = form.cleaned_data

            return JsonResponse(
                {
                    "status": "success",
                },
                status=200,
            )
        if not self.is_featured:
            locale = Locale.objects.get(language_code=request.LANGUAGE_CODE)
            root = Page.objects.filter(
                locale=locale,
                depth=2
            ).first()
            if root:
                return redirect(root.url)

        return super().serve(request, *args, **kwargs)

class ServicesPage(Page):
    max_count = 1
    template = 'home/services_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    image_hero = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_hero = models.CharField('Hero - Title', max_length=255, blank=True)
    text_hero = models.TextField('Hero - Text', blank=True)

    image_display = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    title_display = models.CharField('Display - Title', max_length=255, blank=True)
    text_display = models.TextField('Display - Text', blank=True)
    button_display = models.CharField("Display - Button Text", max_length=255, blank=True)
    redirect_display = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    lead_display_2 = models.CharField('Display 2 - Lead', max_length=255, blank=True)
    title_display_2 = models.CharField('Display 2 - Title', max_length=255, blank=True)
    text_display_2 = models.TextField('Display 2 - Text', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image_hero"),
                FieldPanel('title_hero'),
                FieldPanel('text_hero'),
            ],
            heading='Section Hero',
        ),
        MultiFieldPanel(
            [
                FieldPanel("image_display"),
                FieldPanel("title_display"),
                FieldPanel("text_display"),
                FieldPanel("button_display"),
                FieldPanel("redirect_display"),
            ],
            heading='Section Display 1',
        ),
        MultiFieldPanel(
            [
                FieldPanel("lead_display_2"),
                FieldPanel("title_display_2"),
                FieldPanel("text_display_2"),
            ],
            heading='Section Display 2',
        ),
    ]


class GalleryPageItem(Orderable):
    page = ParentalKey('GalleryPage', related_name='gallery_items', on_delete=models.CASCADE)

    title = models.CharField("Collection Title", max_length=255, blank=True)
    images = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    tags = StreamField(
        [
            ('tag', CharBlock(required=False, max_length=255)),
        ],
        blank=True,
        use_json_field=True,
    )
    external = models.CharField("External Description", max_length=255, blank=True)
    internal = models.CharField("Internal Description", max_length=255, blank=True)
    finishes = models.CharField("Finishes Description", max_length=255, blank=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('images'),
        FieldPanel('tags'),
        FieldPanel('external'),
        FieldPanel('internal'),
        FieldPanel('finishes')
    ]

class GalleryPage(Page):
    max_count = 1
    template = 'home/gallery_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


    top_tags = StreamField(
        [
            ('tag', CharBlock(required=False, max_length=255)),
        ],
        blank=True,
        use_json_field=True,
    )

    external_keyword = models.CharField("External Keyword", max_length=80, blank=True)
    internal_keyword = models.CharField("Internal Keyword", max_length=80, blank=True)
    finishes_keyword = models.CharField("Finishes Keyword", max_length=80, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("top_tags"),
                FieldPanel("internal_keyword"),
                FieldPanel("external_keyword"),
                FieldPanel("finishes_keyword"),
            ],
            heading='General'
        ),
        MultiFieldPanel(
            [
                InlinePanel('gallery_items'),
            ],
            heading="Galleries",
        ),
    ]

class ContactPagePhone(Orderable):
    page = ParentalKey('ContactPage', related_name='contact_phones', on_delete=models.CASCADE)
    description = models.CharField("Description", max_length=255, blank=True)
    telephone = models.CharField("Telephone", max_length=100, blank=True)
    mail = models.CharField("Mail", max_length=100, blank=True)

    panels = [
        FieldPanel('description'),
        FieldPanel('telephone'),
        FieldPanel('mail'),
    ]

class ContactPage(Page):
    max_count = 1
    template = 'home/contact_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    motto_contact = models.CharField("Lead", max_length=255, blank=True)
    title_contact = models.CharField("Title", max_length=255, blank=True)
    text_contact = models.TextField("Description", blank=True)

    title_phone = models.CharField("Phones Title", max_length=255, blank=True)

    image_hero = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    recipient_mail = models.EmailField()
    success_message = models.CharField(max_length=255)

    label_name = models.CharField(max_length=100, default="Imie i Nazwisko")
    label_email = models.CharField(max_length=100, default="E-mail")
    label_phone = models.CharField(max_length=100, default="Telefon")
    label_message = models.CharField(max_length=100, default="Twoja wiadomosc")
    label_send = models.CharField(max_length=100, default="Prześlij wiadomość")
    label_sending = models.CharField(max_length=100, default="Wysyłanie...")
    label_attachment = models.CharField(max_length=100, default="Załącznik")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('image_hero'),
            ],
            heading="Section Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_contact'),
                FieldPanel('title_contact'),
                FieldPanel('text_contact'),
            ],
            heading="Section Contact"
        ),
        MultiFieldPanel(
            [
                FieldPanel('title_phone'),
                InlinePanel('contact_phones'),
            ],
            heading="Contact Information",
        ),
        MultiFieldPanel(
            [
                FieldPanel('recipient_mail'),
                FieldPanel('success_message'),
                FieldPanel('label_name'),
                FieldPanel('label_email'),
                FieldPanel('label_phone'),
                FieldPanel('label_message'),
                FieldPanel('label_send'),
                FieldPanel('label_sending'),
            ],
            heading="Form Settings",
        )
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        config_data = request.session.get('config_data')
        context.update({
            'config_data': config_data,
            'date': datetime.now().strftime("%Y-%m-%d"),
        })
        return context

    def serve(self, request, *args, **kwargs):
        custom_labels = {
            'name': self.label_name,
            'email': self.label_email,
            'phone': self.label_phone,
            'message': self.label_message,
        }

        if request.method == 'POST':
            form = ContactForm(request.POST, custom_labels=custom_labels)
            if form.is_valid():
                data = form.cleaned_data
                full_message = f"""
                Nowa wiadomość od: {data['name']}
                Email: {data['email']}
                Tel: {data['phone']}
                
                Treść:
                {data['message']}
                """

                email = EmailMessage(
                    subject=f'Kontakt ze strony: {data["name"]}',
                    body=full_message,
                    from_email=None,
                    to=[self.recipient_mail],
                )

                if request.session.get('config_data'):
                    pdf_buffer = generate_pdf(request.session.get('config_data'), data['email'], request.LANGUAGE_CODE)
                    email.attach(
                        filename='produkt.pdf',
                        content=pdf_buffer.getvalue(),
                        mimetype='application/pdf',
                    )

                email.send(fail_silently=False)

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': self.success_message,
                    })

                return render(request, self.template, {
                    'page': self,
                    'form': ContactForm(custom_labels=custom_labels),
                    'submitted': True,
                })
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'errors': form.errors.get_json_data(),
                    }, status=400)
        else:
            form = ContactForm(custom_labels=custom_labels)

        context = self.get_context(request, *args, **kwargs)
        context.update({
            'form': form,
            'submitted': False,
        })
        return render(request, self.template, context)

class PrivacyPoliticsPage(Page):
    max_count = 1
    template = 'home/privacy_politics_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    policy_title = models.CharField("Title", max_length=255, blank=True)
    policy_body = RichTextField(blank=True, features=['h2'])

    content_panels = Page.content_panels + [
        FieldPanel('policy_title'),
        FieldPanel('policy_body'),
    ]


