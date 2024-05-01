class EpgChannel:
    def __init__(self, id: str, display_name: str, icon: str):
        self.id = id
        self.display_name = display_name
        self.icon = icon

    def toRaw(self) -> str:
        result = f'<channel id="{self.id}">\n'
        result += f'\t<display-name lang="ru">{self.display_name}</display-name>\n'
        if self.icon is not None:
            result += f'\t<icon src="{self.icon}" /> \n'
        result += '</channel>'
        return result
    