from nicegui import ui
import asyncio
import websockets
import threading

## ¿Qué es un Web Socket?
## ¿Qué es Async y Await?
## async tiene la funcion de ser asincrona y await espera a que se complete una tarea asincrona

data = {'pot_value': '0', 'led_status': 'OFF'} 
esp32_socket = None

async def ws_serve_logic(websocket, path):
    global esp32_socket
    esp32_socket = websocket
    print("ESP32 conectado") 
    try:
        async for message in websocket:
            ##recibir la informacion del potenciometro
            data['pot_value'] = message
            ui_update.refresh()
    except websockets.exceptions.ConnectionClosed:
        print("ESP32 desconectado")
    finally:
        esp32_socket = None

def start_ws_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(ws_serve_logic, "0.0.0.0", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever() 

def toggle_led():
    if esp32_socket:
        new_status = 'ON' if data['led status'] == 'OFF' else 'OFF'
        data['led_status'] = new_status

threading.Thread(target=start_ws_thread, daemon=True).start()
@ui.refreshable
def ui_update():
    with ui.card().classes('items-center q-pa-lg'):
        ui.label(f'Potenciometro: {data["pot_value"]}').classes('text-h3')
        #Representacion visual de mi potenciometro
        val = int(data['pot_value']) if data['pot_value'].isdigit() else 0
        ui.knob(value=val, min=0, max=4095, show_value=True).classes('m-4')
        #led
        ui.label(f'LED: {data["led_status"]}').classes('text-h3')
        ui.button('Cambiar LED', on_click=toggle_led).props('elevated')