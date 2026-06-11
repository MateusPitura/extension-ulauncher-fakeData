import os
import subprocess
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.event import ItemEnterEvent
from src.generators.generate_address import generate_address
from src.generators.generate_birth_date import generate_birth_date
from src.generators.generate_cnpj import generate_cnpj
from src.generators.generate_cpf import generate_cpf
from src.generators.generate_email import generate_email
from src.generators.generate_name import generate_name
from src.generators.generate_phone import generate_phone
from src.generators.generate_rg import generate_rg
from src.utils.generate_random_number import generate_random_number
from src.repository.GeneratorRepository import GeneratorRepository


class FakaDataExtension(Extension):
    def __init__(self):
        super(FakaDataExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, CustomActionListener())

        self.repository = GeneratorRepository(
            dirname=os.path.dirname(__file__))
        self.address = None

ADDRESS_KEY = 'Address'

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower().strip()

        if query == "":
            aux_items = []

            fake_data = {
                "BirthDate": generate_birth_date(),
                "CNPJ": generate_cnpj(),
                "CPF": generate_cpf(),
                "Email": generate_email(),
                "Name": generate_name(),
                "Phone": generate_phone(),
                "RG": generate_rg()
            }

            custom_emails_raw = extension.preferences.get('custom_emails', '')
            custom_emails = custom_emails_raw.split(';')

            for custom_email in custom_emails:
                if '=' not in custom_email:
                    continue
                name, email = map(str.strip, custom_email.split('=', 1))

                fake_data[f'Email {name}'] = email.replace(
                    '{random}', generate_random_number(5))

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

                aux_items.append((key, item))

            if extension.address is None:
                extension.address = generate_address()

            aux_items.append((ADDRESS_KEY, ExtensionSmallResultItem(
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
            )))

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
            items = [item for _, item in aux_items]

            return RenderResultListAction(items)

        filtered_items = [
            item
            for key, item in extension.fake_items
            if query in key.lower()
        ]
        return RenderResultListAction(filtered_items)


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
            generate_new_addres = data["generate_new_address"]

            if generate_new_addres:
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


if __name__ == '__main__':
    FakaDataExtension().run()
