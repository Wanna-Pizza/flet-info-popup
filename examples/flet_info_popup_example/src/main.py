import asyncio
import flet as ft

from flet_info_popup import FletInfoPopup, PopupDismissTriggerBehavior, PopupPosition


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    has_started = [False]

    current_popup = [0]

    async def open_next_popup(e):
        if not has_started[0]:
            has_started[0] = True
            controls.controls[current_popup[0]].open()
            return
        controls.controls[current_popup[0]].close()
        
        if current_popup[0] == len(controls.controls) - 1:
            has_started[0] = False
            current_popup[0] = 0
            return
        
        current_popup[0] = (current_popup[0] + 1) % len(controls.controls)
        await asyncio.sleep(0.2)
        controls.controls[current_popup[0]].open()
    
    def custom_body(description="Ok bro, this is blue box, you got this? Bruh."):
        body = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            value=description,
                            color="black", weight=ft.FontWeight.BOLD, size=20),
                        ft.ElevatedButton(
                            "Next",
                            on_click=open_next_popup,
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=10,
                    expand=True,
                ),
                bgcolor='white',
                width=200,
                height=250,
                padding=20,
                border_radius=10,
            )
        return body
    
    def custom_box(color=ft.Colors.BLUE, text="Bruh"):
        content = ft.Container(
                width=200,
                height=200,
                content=ft.Text(text, color="black", weight=ft.FontWeight.BOLD, size=20),
                bgcolor=color,
                alignment=ft.alignment.center,
                border_radius=10,
            )
        return content
    
    texts = {
        "Blue Box": {
            "description": "Ok bro, this is blue box, you got this? Bruh."
        },
        "Green Box": {
            "description": "duh this is green, obviously you got this? Bruh."
        },
        "Red Box": {
            "description": "Really? Are you sure you got this? Bruh."
        },
    }

    controls = ft.Row([], spacing=50)
    for color_name, params in texts.items():
        box = custom_box(
            color={
                "Blue Box": ft.Colors.BLUE,
                "Green Box": ft.Colors.GREEN,
                "Red Box": ft.Colors.RED,
            }[color_name],
            text=color_name
        )
        popup_body = custom_body(description=params["description"])
        pop = FletInfoPopup(
            body=popup_body,
            content=box,
            area_background_color=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
            dismiss_trigger_behavior=PopupDismissTriggerBehavior.MANUAL,
            popup_position=PopupPosition.RIGHT,
            enable_highlight=True,
            highlight_background_color=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
            highlight_border_radius=10,
            highlight_padding=10,
        )
        controls.controls.append(pop)
    

    page.add(
        controls,
        ft.Button("4242", on_click=open_next_popup)
    )


ft.app(main)
