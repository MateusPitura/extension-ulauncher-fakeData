import os
import subprocess
import re
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.event import ItemEnterEvent
from src.generators.generate_address import generate_address
from src.generators.generate_credit_card import generate_credit_card
from src.generators.generate_cnpj import generate_cnpj
from src.generators.generate_date import generate_date
from src.generators.generate_cpf import generate_cpf
from src.generators.generate_email import generate_email
from src.generators.generate_name import generate_name
from src.generators.generate_rg import generate_rg
from src.generators.generate_lorem import generate_lorem
from src.generators.generate_random_number import generate_random_number
from src.generators.generate_home_phone import generate_home_phone
from src.generators.generate_mobile_phone import generate_mobile_phone
from src.generators.generate_company import generate_company
from src.generators.generate_color import generate_color
from src.utils.get_number_modifiers import parse_number
from src.repository.GeneratorRepository import GeneratorRepository


class FakaDataExtension(Extension):
    def __init__(self):
        super(FakaDataExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, CustomActionListener())

        self.repository = GeneratorRepository(
            dirname=os.path.dirname(__file__))
        self.address = None
        self.credit_card = None


ADDRESS_KEY = 'Address'
CREDIT_CARD_KEY = 'Credit Card'


def handle_keyword_query(event, extension):
    query = (event.get_argument() or "").lower().strip()

    if query == "":
        aux_items = []

        fake_data = {
            "Date": generate_date(),
            "CNPJ": generate_cnpj(),
            "CPF": generate_cpf(),
            "Email": generate_email(),
            "Name": generate_name(),
            "CellPhone": generate_mobile_phone(),
            "Phone": generate_home_phone(),
            "RG": generate_rg(),
            "Lorem": generate_lorem(10),
            "Company": generate_company(),
            "Color": generate_color(),
            "Number": f'{generate_random_number()}'
        }

        custom_emails_raw = extension.preferences.get('custom_emails', '')
        custom_emails = custom_emails_raw.split(';')

        for custom_email in custom_emails:
            if '=' not in custom_email:
                continue
            name, email = map(str.strip, custom_email.split('=', 1))

            fake_data[f'Email {name}'] = email.replace(
                '{random}', generate_random_number(digit_count=5))

        for key, value in fake_data.items():
            item = ExtensionSmallResultItem(
                icon='images/logo.png',
                name=f"{key}: {value}",
                on_enter=ExtensionCustomAction(
                    {
                        "action": "update_last_used",
                        "key": key,
                        "value": value
                    },
                    keep_app_open=False
                ),
            )

            aux_items.append((key, item, value))

        if extension.address is None:
            extension.address = generate_address()

        if extension.credit_card is None:
            extension.credit_card = generate_credit_card()

        aux_items.append((
            ADDRESS_KEY,
            ExtensionSmallResultItem(
                icon='images/logo.png',
                name=f"{ADDRESS_KEY}: {extension.address[0]}",
                on_enter=ExtensionCustomAction(
                    {
                        "action": "display_address_fields",
                        "address_string": extension.address[0],
                        "fields": extension.address[1],
                        "generate_new_address": False
                    },
                    keep_app_open=True
                ),
            ),
            extension.address[0]
        ))

        aux_items.append((
            CREDIT_CARD_KEY,
            ExtensionSmallResultItem(
                icon='images/logo.png',
                name=f"{CREDIT_CARD_KEY}: {extension.credit_card[0]}",
                on_enter=ExtensionCustomAction(
                    {
                        "action": "display_credit_card_fields",
                        "credit_card_string": extension.credit_card[0],
                        "fields": extension.credit_card[1],
                        "generate_new_credit_card": False
                    },
                    keep_app_open=True
                )
            ),
            extension.credit_card[0]
        ))

        # Order by last_used from DB; unknown ones go to the end, then by name
        usage_order = {
            n: idx
            for idx, n in enumerate(extension.repository.get_items())}

        aux_items.sort(
            key=lambda pair: (usage_order.get(
                pair[0], float('inf')), pair[0].lower())
        )

        extension.fake_items = aux_items

        # Drop names, keep only items
        items = [item for _, item, _ in aux_items]

        return RenderResultListAction(items)

    match = re.match(r'lorem\s+(\d+)', query)
    if match:
        number = int(match.group(1))
        if 1 <= number <= 1000:
            new_text = generate_lorem(number)
            new_item = ExtensionSmallResultItem(
                icon='images/logo.png',
                name=f'Lorem: {new_text}',
                on_enter=ExtensionCustomAction(
                    {
                        "action": "update_last_used",
                        "key": 'Lorem',
                        "value": new_text
                    },
                    keep_app_open=False
                ))

            return RenderResultListAction([new_item])

    if query in ("date p", "date f"):
        new_date = generate_date(
            only_past=True) if query == "date p" else generate_date(only_future=True)
        new_item = ExtensionSmallResultItem(
            icon='images/logo.png',
            name=f'Date: {new_date}',
            on_enter=ExtensionCustomAction(
                {
                    "action": "update_last_used",
                    "key": 'Date',
                    "value": new_date
                },
                keep_app_open=False
            ))

        return RenderResultListAction([new_item])

    min_value, max_value, digit_count = parse_number(query)
    if min_value is not None or max_value is not None or digit_count is not None:
        new_number = generate_random_number(
            min_value=min_value, max_value=max_value, digit_count=digit_count)
        new_item = ExtensionSmallResultItem(
            icon='images/logo.png',
            name=f'Number: {new_number}',
            on_enter=ExtensionCustomAction(
                {
                    "action": "update_last_used",
                    "key": 'Number',
                    "value": f'{new_number}'
                },
                keep_app_open=False
            ))

        return RenderResultListAction([new_item])

    filtered_items = [
        item
        for key, item, _ in extension.fake_items
        if query in key.lower()
    ]
    return RenderResultListAction(filtered_items)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        try:
            return handle_keyword_query(
                event, extension
            )

        except Exception as e:
            return RenderResultListAction(
                [
                    ExtensionResultItem(
                        icon="images/logo.png",
                        name="FakeData",
                        description=str(e)
                    )
                ]
            )


class CustomActionListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()

        if data.get("action") == "update_last_used":
            key = data["key"]
            value = data["value"]

            extension.repository.mark_as_used(key)

            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=value.encode(), check=False)

        if data.get("action") == "display_address_fields":
            generate_new = data["generate_new_address"]

            if generate_new:
                extension.address = generate_address()
                address_string = extension.address[0]
                fields = extension.address[1]
            else:
                address_string = data["address_string"]
                fields = data["fields"]

            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=address_string.encode(), check=False)

            extension.repository.mark_as_used(ADDRESS_KEY)

            items = [
                ExtensionSmallResultItem(
                    icon='images/reset.png',
                    name="Generate new address",
                    on_enter=ExtensionCustomAction(
                        {
                            "action": "display_address_fields",
                            "generate_new_address": True
                        },
                        keep_app_open=True
                    ),
                )
            ]

            items += [
                ExtensionSmallResultItem(
                    icon='images/logo.png',
                    name=f"{key}: {value}",
                    on_enter=CopyToClipboardAction(value),
                )
                for key, value in fields.items()
            ]

            return RenderResultListAction(items)

        if data.get("action") == "display_credit_card_fields":
            generate_new = data["generate_new_credit_card"]

            if generate_new:
                extension.credit_card = generate_credit_card()
                credit_card_string = extension.credit_card[0]
                fields = extension.credit_card[1]
            else:
                credit_card_string = data["credit_card_string"]
                fields = data["fields"]

            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=credit_card_string.encode(), check=False)

            extension.repository.mark_as_used(CREDIT_CARD_KEY)

            items = [
                ExtensionSmallResultItem(
                    icon='images/reset.png',
                    name="Generate new credit card",
                    on_enter=ExtensionCustomAction(
                        {
                            "action": "display_credit_card_fields",
                            "generate_new_credit_card": True
                        },
                        keep_app_open=True
                    ),
                )
            ]

            items += [
                ExtensionSmallResultItem(
                    icon='images/logo.png',
                    name=f"{key}: {value}",
                    on_enter=CopyToClipboardAction(value),
                )
                for key, value in fields.items()
            ]

            return RenderResultListAction(items)


if __name__ == '__main__':
    FakaDataExtension().run()
