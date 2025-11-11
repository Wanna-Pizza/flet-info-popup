# Introduction

FletInfoPopup for Flet.

## Examples

```
import flet as ft

from flet_info_popup import FletInfoPopup


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletInfoPopup(
                    tooltip="My new FletInfoPopup Control tooltip",
                    value = "My new FletInfoPopup Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletInfoPopup](FletInfoPopup.md)


