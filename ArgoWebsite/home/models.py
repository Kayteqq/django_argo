from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import redirect
from wagtail.admin.panels import PageChooserPanel, FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.images.models import Image
from wagtail.fields import StreamField

from .blocks import NavbarBlockContainer, FooterBlockContainer

from wagtail.models import Page

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
    content_panels = Page.content_panels + [
        FieldPanel('first_column'),
        FieldPanel('second_column'),
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


@register_setting
class SocialMediaSettings(BaseSiteSetting):
    url_x           = models.URLField("URL X",          blank=True, null=True)
    url_facebook    = models.URLField("URL Facebook",   blank=True, null=True)
    url_linkedin    = models.URLField("URL LinkedIn",   blank=True, null=True)
    url_instagram   = models.URLField("URL Instagram",  blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('url_x'),
        FieldPanel('url_facebook'),
        FieldPanel('url_linkedin'),
        FieldPanel('url_instagram'),
    ]

    class Meta:
        verbose_name = 'Social Media - Linki'
        verbose_name_plural = 'Social Media - Linki'




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


class MainPage(Page):
    max_count = 1
    template = 'home/main_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class AboutPage(Page):
    max_count = 1
    template = 'home/about_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class CarpentrySteelPage(Page):
    max_count = 1
    template = 'home/carpentry_steel_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class CarpentryAluminiumPage(Page):
    max_count = 1
    template = 'home/carpentry_aluminium_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


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
    image_display_2 = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    motto_details = models.CharField("Details Summary - Lead", max_length=255, blank=True)
    title_details = models.CharField("Details Summary - Title", max_length=255, blank=True)
    image_details = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    title_1_details = models.CharField("Details Summary - Point 1 - Title", max_length=255, blank=True)
    desc_1_details = models.TextField("Details Summary - Point 1 - Description", blank=True)
    title_2_details = models.CharField("Details Summary - Point 1 - Title", max_length=255, blank=True)
    desc_2_details = models.TextField("Details Summary - Point 1 - Description", blank=True)
    title_3_details = models.CharField("Details Summary - Point 1 - Title", max_length=255, blank=True)
    desc_3_details = models.TextField("Details Summary - Point 1 - Description", blank=True)
    title_4_details = models.CharField("Details Summary - Point 1 - Title", max_length=255, blank=True)
    desc_4_details = models.TextField("Details Summary - Point 1 - Description", blank=True)
    title_5_details = models.CharField("Details Summary - Point 1 - Title", max_length=255, blank=True)
    desc_5_details = models.TextField("Details Summary - Point 1 - Description", blank=True)

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
                FieldPanel('image_display_2'),
            ],
            heading='Section Description - Second Half',
        ),
        MultiFieldPanel(
            [
                FieldPanel('motto_details'),
                FieldPanel('title_details'),
                FieldPanel('image_details'),
                MultiFieldPanel(
                    [
                        FieldPanel('title_1_details'),
                        FieldPanel('desc_1_details'),
                        FieldPanel('title_2_details'),
                        FieldPanel('desc_2_details'),
                        FieldPanel('title_3_details'),
                        FieldPanel('desc_3_details'),
                        FieldPanel('title_4_details'),
                        FieldPanel('desc_4_details'),
                        FieldPanel('title_5_details'),
                        FieldPanel('desc_5_details'),
                    ],
                    heading='Section Details - List',
                )
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


class ConfiguratorPage(Page):
    max_count = 1
    template = 'home/configurator_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class ServicesPage(Page):
    max_count = 1
    template = 'home/services_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class GalleryPage(Page):
    max_count = 1
    template = 'home/gallery_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class ContactPage(Page):
    max_count = 1
    template = 'home/contact_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


class PrivacyPoliticsPage(Page):
    max_count = 1
    template = 'home/privacy_politics_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []


