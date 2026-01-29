from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import redirect
from wagtail.admin.panels import PageChooserPanel, FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page, Orderable
from wagtail.fields import StreamField
from modelcluster.fields import ParentalKey

from .blocks import NavbarBlockContainer, FooterBlockContainer



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

    image_divider = models.ForeignKey(
        Image,
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
                FieldPanel('image_divider'),
            ],
            heading="Section Image Divider",
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




    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('realizations_images'),
            ],
            heading="Realizations Hero",
        ),
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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('realizations_images'),
            ],
            heading="Realizations Hero",
        ),
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

class GalleryPageItem(Orderable):
    page = ParentalKey('GalleryPage', related_name='gallery_items', on_delete=models.CASCADE)
    images = StreamField(
        [
            ('image', ImageChooserBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel('images'),
    ]

class GalleryPage(Page):
    max_count = 1
    template = 'home/gallery_page.html'
    parent_page_types = ['RootRedirectPage']
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('gallery_items'),
            ],
            heading="Galleries",
        ),
    ]

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


