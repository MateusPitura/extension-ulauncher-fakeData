from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from generators.generate_address import generate_address
from generators.generate_birth_date import generate_birth_date
from generators.generate_cnpj import generate_cnpj
from generators.generate_cpf import generate_cpf
from generators.generate_email import generate_email
from generators.generate_name import generate_name
from generators.generate_phone import generate_phone
from generators.generate_postal_code import generate_postal_code
from generators.generate_rg import generate_rg


class FakaDataExtension(Extension):
    def __init__(self):
        super(FakaDataExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower().strip()
        items = []

        if query == "":
            extension.fakeData = {
                "Address": generate_address(),
                "BirthDate": generate_birth_date(),
                "CNPJ": generate_cnpj(),
                "CPF": generate_cpf(),
                "Email": generate_email(),
                "Name": generate_name(),
                "Phone": generate_phone(),
                "CEP": generate_postal_code(),
                "RG": generate_rg()
            }

            for key, value in extension.fakeData.items():
                items.append(
                    ExtensionSmallResultItem(
                        icon='images/logo.png',
                        name=f"{key}: {value}",
                        on_enter=CopyToClipboardAction(value)
                    )
                )

            return RenderResultListAction(items)

        filtered_items = [
            ExtensionSmallResultItem(
                icon='images/logo.png',
                name=f"{key}: {value}",
                on_enter=CopyToClipboardAction(value)
            )
            for key, value in extension.fakeData.items()
            if query in key.lower()
        ]
        return RenderResultListAction(filtered_items)


if __name__ == '__main__':
    FakaDataExtension().run()
