from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from generators.generate_email import generate_email
from generators.generate_birth_date import generate_birth_date
from generators.generate_cpf import generate_cpf


class FakaDataExtension(Extension):
    def __init__(self):
        super(FakaDataExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = (event.get_argument() or "").lower().strip()

        print(f"🌠 query: {query}")
        if query == "":
            extension.fakeData = {
                "Email": generate_email(),
                "BirthDate": generate_birth_date(),
                "CPF": generate_cpf(),
            }

        items = []

        print(f"🌠 extension.fakeData: {extension.fakeData}")
        for key, value in extension.fakeData.items():
            items.append(
                ExtensionSmallResultItem(
                    icon='images/logo.png',
                    name=f"{key}: {value}",
                    on_enter=CopyToClipboardAction(value)
                )
            )
        print(f"🌠 items: {items}")
        return RenderResultListAction(items)


if __name__ == '__main__':
    FakaDataExtension().run()
