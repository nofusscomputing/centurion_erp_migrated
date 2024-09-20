
import re

from django.template.loader import render_to_string
from django.urls import reverse

from markdown_it import MarkdownIt
from markdown_it.rules_core import StateCore
from markdown_it.token import Token

# Regex string to match a whitespace character, as specified in
# https://github.github.com/gfm/#whitespace-character
# (spec version 0.29-gfm (2019-04-06))
_GFM_WHITESPACE_RE = r"[ \t\n\v\f\r]"


def plugin(
    md: MarkdownIt,
    enabled: bool = False,
) -> None:
    """markdown_it plugin to render model references

    Placing `$<type>-<number>` within markdown will be rendered as a pretty link to the model.

    Args:
        md (MarkdownIt): markdown object
        enabled (bool, optional): Enable the parsing of model references. Defaults to False.

    Returns:
        None: nada
    """

    def main(state: StateCore) -> None:
       
        tokens = state.tokens
        for i in range(0, len(tokens) - 1):
            if is_tag_item(tokens, i):
                tag_render(tokens[i])


    def is_inline(token: Token) -> bool:
        return token.type == "inline"


    def is_tag_item(tokens: list[Token], index: int) -> bool:

        return (
            is_inline(tokens[index])
            and contains_tag_item(tokens[index])
        )


    def tag_html(match):

        id = match.group('id')
        item_type = match.group('type')

        try:

            if item_type == 'cluster':

                from itim.models.clusters import Cluster

                model = Cluster

                url = reverse('ITIM:_cluster_view', kwargs={'pk': int(id)})

            elif item_type == 'config_group':

                from config_management.models.groups import ConfigGroups

                model = ConfigGroups

                url = reverse('Config Management:_group_view', kwargs={'pk': int(id)})

            elif item_type == 'device':

                from itam.models.device import Device

                model = Device

                url = reverse('ITAM:_device_view', kwargs={'pk': int(id)})

            elif  item_type == 'operating_system':

                from itam.models.operating_system import OperatingSystem

                model = OperatingSystem

                url = reverse('ITAM:_operating_system_view', kwargs={'pk': int(id)})

            elif item_type == 'service':

                from itim.models.services import Service

                model = Service

                url = reverse('ITIM:_service_view', kwargs={'pk': int(id)})

            elif item_type == 'software':

                from itam.models.software import Software

                model = Software

                url = reverse('ITAM:_software_view', kwargs={'pk': int(id)})


            if url:

                item = model.objects.get(
                    pk = int(id)
                )

                return f'<a href="{ url }">{ item.name }, <span style="color: #777; font-size: smaller;">{ item_type }</span></a>'

        except Exception as e:

            return str(f'${item_type}-{id}')


    def tag_render(token: Token) -> None:
        assert token.children is not None

        checkbox = Token("html_inline", "", 0)

        checkbox.content = tag_replace(token.content)

        token.children[0] = checkbox


    def tag_replace(text):

        return re.sub('\$(?P<type>[a-z_]+)-(?P<id>\d+)', tag_html, text)

    def contains_tag_item(token: Token) -> bool:

        return re.match(rf"(.+)?\$[a-z_]+-\d+{_GFM_WHITESPACE_RE}?(.+)?", token.content) is not None

    if enabled:

        md.core.ruler.after("inline", "links", fn=main)
