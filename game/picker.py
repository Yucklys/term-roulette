"""A widget to display the character picker."""

from textual.app import ComposeResult, RenderResult
from textual.widgets import Static, Label, ListView, ListItem
from textual.widget import Widget
from textual.reactive import reactive
from textual import on


class Description(Widget):
    """A widget to display the character description."""

    desc = reactive("")

    def __init__(self, desc: str, **kwargs):
        """Initialize the character description."""
        super().__init__(**kwargs)
        self.desc = desc

    def render(self) -> RenderResult:
        """Create the character description."""
        return f"{self.desc}"


class CharacterPicker(Static):
    """A widget to display the character picker."""

    # Redefine the ListItem class to expose the label text
    class LabelItem(ListItem):
        """A label item for the character picker."""

        def __init__(self, label: str, **kwargs) -> None:
            """Initialize the label item."""
            super().__init__(**kwargs)
            self.label = label

        def compose(self) -> ComposeResult:
            """Create the label item."""
            yield Label(self.label)

    descriptions = [
        "Mimic has no brain. He will only do whatever you do.",
        "Berserker is aggressive. He will use all his effort to shoot you.",
    ]
    selected = reactive("")

    def compose(self) -> ComposeResult:
        """Create the character picker."""
        picker = ListView(
            self.LabelItem("Mimic"),
            self.LabelItem("Berserker"),
        )
        yield picker
        yield Description(self.descriptions[picker.index], id="description")

    @on(ListView.Highlighted)
    def handle_picker_switch(self, picker: ListView.Highlighted) -> None:
        """Update the character description."""
        print(f"Label {picker.item}")
        description = self.query_one(Description)
        description.desc = self.descriptions[picker.list_view.index]

    @on(ListView.Selected)
    def handle_picker_select(self, picker: ListView.Selected) -> None:
        """Select the opponent."""
        self.selected = picker.item.label
        print(f"Select {self.selected} as opponent.")
        # Change the class of the picker to hide the picker UI
        self.add_class("hidden")
