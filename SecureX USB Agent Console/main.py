import flet as ft
import userpaths
import os


def main(page: ft.Page):
    page.title = "SecureX USB Agent Config. Console"
    page.window_height = 700
    page.window_width = 700
    page.window_max_height = 700
    page.window_max_width = 700
    page.window_min_height = 600
    page.window_min_width = 500
    page.window_maximizable = False
    page.window_center = True
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.scroll = True

    outputPath = f"{userpaths.get_my_documents()}\SecureX\\USB Agent\\output\\"

    page.add(
        ft.AppBar(
            bgcolor="#FA6900",
            elevation=1,
            title=ft.Text(value="SecureX",color="#FFFFFF"),
            )
        )
    
    def adIntegration(e):
        if(adIntegrationSW.value):
            adCol.disabled = False
        else:
            adCol.disabled = True
        page.update()
    
    
    page.add(ft.Row())

    failsafe1 = ft.Switch(
        label="Enable Failsafe #1",
        value=True,
        active_color="#FA6900",
        thumb_color = "#FA6900",
        on_change=adIntegration,
        )

    failsafe2 = ft.Switch(
        label="Enable Failsafe #2",
        value=True,
        active_color="#FA6900",
        thumb_color = "#FA6900",
        on_change=adIntegration,
        )
    
    page.add(failsafe1,failsafe2)

    adIntegrationSW = ft.Switch(
        label="Enable Active Directory Integration",
        value=False,
        active_color="#FA6900",
        thumb_color = "#FA6900",
        on_change=adIntegration,
        )

    page.add(adIntegrationSW)

    adCol = ft.Column(
        disabled= True,
        width= 600,
        horizontal_alignment="center",
        controls=[
            ft.TextField(
                label="Active Directory IP:PORT",
                border=ft.InputBorder.OUTLINE,
                color="#FA6900",
                border_color="#FA6900",
                focused_color="#FA6900",
                focused_border_color="#FA6900",
                hint_text="192.168.100.100:389",
                ),

            ft.TextField(
                label="Username",
                border=ft.InputBorder.OUTLINE,
                color="#FA6900",
                border_color="#FA6900",
                focused_color="#FA6900",
                focused_border_color="#FA6900",
                ),
            ft.TextField(
                label="Password",
                border=ft.InputBorder.OUTLINE,
                color="#FA6900",
                border_color="#FA6900",
                focused_color="#FA6900",
                focused_border_color="#FA6900",
                password= True,
                can_reveal_password=True
                ),
            ft.TextField(
                label="Base path",
                border=ft.InputBorder.OUTLINE,
                color="#FA6900",
                border_color="#FA6900",
                focused_color="#FA6900",
                focused_border_color="#FA6900",
                
                ),
            ft.TextField(
                label="Group",
                border=ft.InputBorder.OUTLINE,
                color="#FA6900",
                border_color="#FA6900",
                focused_color="#FA6900",
                focused_border_color="#FA6900",
                hint_text= "USB Enabled"
                ),

            ft.Switch(
                label="SSL",
                value=False,
                active_color="#FA6900",
                thumb_color = "#FA6900",
                label_position= "left"
                )
        ]
    )
    page.add(adCol)

    page.add(ft.Divider(height=5, thickness=1),)

    whiteListUSB =  ft.TextField(
            label="Whitelist USB Device(s)",
            multiline=True,
            width= 600,
            border_color="#FA6900",
            color="#727272",
            value="",
            hint_text= "Separate devices by a comma. eg (XXXXXX,XXXXXX,XXXXXX)"
        )
    page.add(whiteListUSB)

    whiteListUser =  ft.TextField(
            label="Whitelist User(s)",
            multiline=True,
            width= 600,
            border_color="#FA6900",
            color="#727272",
            value="",
            hint_text= "Separate devices by a comma. eg (Administrator,Sebastian,Charles,)",
        )
    page.add(whiteListUser)

    page.add(ft.Divider(height=5, thickness=1),)

    

    outputPath =  ft.TextField(
            label="Output Path",
            multiline=True,
            width= 600,
            border_color="#FA6900",
            color="#727272",
            value=outputPath,
            read_only= True
            
        )
    page.add(outputPath)

    page.add(ft.Divider(height=5, thickness=1),)

    exportAgent = ft.ElevatedButton(
            text="Export USB Agent",
            width=600,
            bgcolor="#FA6900",
            color="#FFFFFF"
            )
    page.add(exportAgent)

    page.add(ft.Row())


ft.app(target=main, assets_dir="assets")