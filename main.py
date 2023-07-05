import openai
from os import name, system
from art import tprint
from winreg import SetValueEx, CloseKey, CreateKey, HKEY_CURRENT_USER, REG_SZ, OpenKey, KEY_READ, QueryValueEx

def add_reg_apikey(key):
    try:
        # Abrir la clave del registro (o crearla si no existe)
        hkey = CreateKey(HKEY_CURRENT_USER, "Software\\fast_chatgpt")

        # Guardar la clave en el registro
        SetValueEx(hkey, "Key", 0, REG_SZ, key)

        # Cerrar la clave del registro
        CloseKey(hkey)

    except Exception:
        input('ERROR - The key could not be saved to the registry.')

def add_reg_line_breaks(line_breaks):
    try:
        # Abrir la clave del registro (o crearla si no existe)
        hkey = CreateKey(HKEY_CURRENT_USER, "Software\\fast_chatgpt")

        # Guardar la clave en el registro
        SetValueEx(hkey, "LineBreaks", 0, REG_SZ, str(line_breaks))

        # Cerrar la clave del registro
        CloseKey(hkey)
    except Exception:
        input('ERROR - The LineBreaks could not be saved to the registry.')

def check_reg_apikey():
    try:
        # Abrir la clave del registro
        hkey = OpenKey(HKEY_CURRENT_USER, "Software\\fast_chatgpt", 0, KEY_READ)

        # Leer el valor de la clave del registro
        clave, _ = QueryValueEx(hkey, "Key")

        # Cerrar la clave del registro
        CloseKey(hkey)

        return clave
    except Exception:
        return None

def check_reg_line_breaks():
    try:
        # Abrir la clave del registro
        hkey = OpenKey(HKEY_CURRENT_USER, "Software\\fast_chatgpt", 0, KEY_READ)

        # Leer el valor de la clave del registro
        clave, _ = QueryValueEx(hkey, "LineBreaks")

        # Cerrar la clave del registro
        CloseKey(hkey)

        # Un poco chapucero
        if clave == 'True':
            return True
        else:
            return False
    except Exception:
        return False

class Settings():
    line_breaks = check_reg_line_breaks()
    key_openai = check_reg_apikey()

def clear():
    linux = 'clear'
    windows = 'cls'

    system ([linux, windows][name == 'nt'])

def welcome():
    tprint('FAST-ChatGPT')
    if Settings.line_breaks:
        print('Send a message...\nType ":end" at the end to send, otherwise it will continue on the next line\n')
    else:
        print('Send a message...\n')
    print('[TYPE] CLEAR')
    print('[TYPE] EXIT')
    print('\n[S] SETTINGS')
    print('[I] INFO')
    print('[X] EXIT')

def return_text_quest():
    texto_entrada = ''
    if Settings.line_breaks:
        texto_entrada_final = ''
        while True:
            texto_entrada = input('[>] ')
            if texto_entrada != '':
                if texto_entrada_final != ':end\n':
                    texto_entrada_final += texto_entrada + '\n'

                    if ':end' in texto_entrada and texto_entrada != '' or texto_entrada_final.rstrip() == 'clear' or texto_entrada_final.rstrip() == 'exit' or texto_entrada_final.rstrip() == 's' or texto_entrada_final.rstrip() == 'i' or texto_entrada_final.rstrip() == 'x':
                        break
        
        return str(texto_entrada_final.replace(':end', '').rstrip())
    else:
        while texto_entrada.rstrip() == '':
            texto_entrada = input('[>] ')
        
        return str(texto_entrada)

def settings_menu():
    while True:
        clear()
        tprint('FAST-ChatGPT')
        print('Line Breaks -> Allows writing on multiple lines. TYPE ":end" TO END AND SEND MESSAGE\nSETTINGS\n')
        print(f'[1] API KEY: {Settings.key_openai}')
        print(f'[2] LINE BREAKS: {str(Settings.line_breaks)}')
        print('[X] BACK')

        settings_entrada = input('[>] ')
        if settings_entrada == '1':
            clear()
            print(openai.api_key)
            Settings.key_openai = input('You can obtain an API key from https://platform.openai.com/account/api-keys.\nEnter the API Key of:\n[>] ')
            openai.api_key = Settings.key_openai
            add_reg_apikey(Settings.key_openai)
        elif settings_entrada == '2':
            if Settings.line_breaks:
                Settings.line_breaks = False
            else:
                Settings.line_breaks = True

            add_reg_line_breaks(Settings.line_breaks)
        elif settings_entrada.lower() == 'x':
            clear()
            welcome()
            break
        else:
            clear()

def info():
    clear()
    input('[TOOL OWNER] https://github.com/sonklol\n[API] https://openai.com\n[VERSION] 1.0\n\nPress ENTER to continue...')

openai.api_key = Settings.key_openai

if Settings.key_openai == None:
    input('[WARNING] In order to use ChatGPT, you must set an API KEY in [S] SETTINGS.\n\nPress ENTER to continue...')

clear()
welcome()

while True:
    texto_entrada = return_text_quest()

    if texto_entrada.lower() == 'exit' or texto_entrada.lower() == 'quit' or texto_entrada.lower() == 'x':
        break
    elif texto_entrada.lower() == 'cls' or texto_entrada.lower() == 'clear':
        clear()
        welcome()
    elif texto_entrada.lower() == 's':
        settings_menu()
    elif texto_entrada.lower() == 'i':
        info()
        clear()
        welcome()
    else:
        # Generar una respuesta del modelo usando el método completions de la API
        try:
            completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=texto_entrada,
                max_tokens=4000,
                n=1,
                stop=None,
                temperature=0.5,
            )

            # Obtener la respuesta del modelo del objeto completions
            respuesta = completions.choices[0].text.strip()

            # Imprimir la respuesta del modelo
            print(respuesta)
        except Exception as e:
            #clear()
            print('ERROR - Failed to connect to the OPENAI API.')
            if str(e).rstrip() == '<empty message>':
                print('Possibly the API KEY is wrong.')
                print('You can obtain an API key from https://platform.openai.com/account/api-keys.')
            else:
                print(str(e).rstrip())
            input('\nPress ENTER to continue...')
            #clear()
            welcome()