from wagtail import blocks
from wagtail.models import Orderable


class InternalLinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(label="Tekst Linku", blank=True, null=True, max_length=255, required=True)
    page = blocks.PageChooserBlock(label="Strona do przekierowania", blank=True, null=True, required=True)

    class Meta:
        icon = 'placeholder'
        label = 'Link - Przekierowanie na Podstronę'

class InternalLinkBlockBolded(blocks.StructBlock):
    text = blocks.CharBlock(label="Tekst Linku", blank=True, null=True, max_length=255, required=True)
    page = blocks.PageChooserBlock(label="Strona do przekierowania", blank=True, null=True, required=True)

    class Meta:
        icon = 'placeholder'
        label = 'Link - Przekierowanie na Podstronę (Pogrubione)'


class MultipleInternalLinksContainer(blocks.StreamBlock):
    page_link = InternalLinkBlock()

    class Meta:
        icon = 'placeholder'
        label = 'Link - Lista Przekierowań na Podstrony'


class NavbarBlockContainer(blocks.StreamBlock):
    page_link = InternalLinkBlock()
    multiple_link = MultipleInternalLinksContainer()

    class Meta:
        label = 'Navbar - Element'
        icon = 'list-ul'


class FooterBlockContainer(blocks.StreamBlock):
    bold_page_link = InternalLinkBlockBolded()
    regular_page_link = InternalLinkBlock()

    class Meta:
        label = 'Footer - Element'
        icon = 'list-ul'
