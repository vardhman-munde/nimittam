import flet as ft
from ollama import Client
import whisper
import os
import tempfile
from PIL import Image

def main(page: ft.Page):
    # --- UI CONFIG ---
    page.title = "Nimittam AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.padding = 20
    
    # Initialize Ollama & Whisper
    client = Client(host='http://127.0.0.1:11434')
    whisper_model = whisper.load_model("base") # Loads locally

    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    model_name = "gemma4:e4b"
    selected_image_path = None

    # --- FUNCTIONS ---
    def on_file_result(e: ft.FilePickerResultEvent):
        nonlocal selected_image_path
        if e.files:
            selected_image_path = e.files[0].path
            page.snack_bar = ft.SnackBar(ft.Text(f"Image selected: {e.files[0].name}"))
            page.snack_bar.open = True
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)

    def send_message(e):
        nonlocal selected_image_path
        user_text = message_input.value
        if not user_text and not selected_image_path:
            return

        # Add User Message to UI
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(user_text, color=ft.Colors.WHITE),
                alignment=ft.alignment.center_right,
                bgcolor=ft.Colors.BLUE_GREY_900,
                padding=10,
                border_radius=10,
            )
        )
        
        message_input.value = ""
        page.update()

        # Call Ollama
        try:
            msg_payload = {"role": "user", "content": user_text}
            if selected_image_path:
                msg_payload["images"] = [selected_image_path]

            response = client.chat(model=model_name, messages=[msg_payload])
            bot_res = response['message']['content']

            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(bot_res, color=ft.Colors.GREEN_200),
                    alignment=ft.alignment.center_left,
                    bgcolor=ft.Colors.BLACK,
                    padding=10,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREEN_900)
                )
            )
            selected_image_path = None # Reset image
        except Exception as ex:
            chat_history.controls.append(ft.Text(f"Error: {ex}", color="red"))
        
        page.update()

    # --- UI LAYOUT ---
    message_input = ft.TextField(
        hint_text="Type your message...",
        expand=True,
        border_color=ft.Colors.GREEN_700,
        on_submit=send_message
    )

    page.add(
        ft.Text("Nimittam Chatbot", size=30, weight="bold", color=ft.Colors.GREEN_accent),
        ft.Divider(),
        chat_history,
        ft.Row(
            [
                ft.IconButton(ft.Icons.IMAGE, on_click=lambda _: file_picker.pick_files()),
                message_input,
                ft.FloatingActionButton(icon=ft.Icons.SEND, on_click=send_message, bgcolor=ft.Colors.GREEN_700),
            ]
        )
    )

ft.app(target=main)
