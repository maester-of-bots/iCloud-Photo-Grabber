import asyncio

import PySimpleGUI as sg
from pyicloud import PyiCloudService

from modules.photos import *
from modules.timestuff import *

apple_login = None
photos = None


async def event_loop():

    # Layout
    layout = [
        [sg.Frame('', [
            [sg.Input(key='-INCAL1-', enable_events=True, visible=False), sg.CalendarButton('Select date', target='-INCAL1-', key='-CAL1-', format='%Y-%m-%d'), sg.Text('', key='-CALSTATUS-', size=(15,1))],
    ], relief=sg.RELIEF_GROOVE, tooltip='Use the calendar to pick a date')],
    [sg.HorizontalSeparator()],

        [sg.Frame('iCloud Login', [
            [sg.Column([
                [sg.Text('Username:', size=(10, 1)), sg.InputText(key='-USERNAME-', size=(20,1))],
            [sg.Text('Password:', size=(10, 1)), sg.InputText(key='-PASSWORD-', password_char='*', size=(20,1))],
            [sg.Button('Login', key='-LOGIN-', bind_return_key=True, button_color=('white', 'teal')), sg.Text('', key='-LOGIN-STATUS-', size=(15,1))]
            ], element_justification='right')]
        ], relief=sg.RELIEF_GROOVE)],

    [sg.HorizontalSeparator()],
    [sg.Frame('', [
        [sg.Button('Download Photos', key='-DOWNLOAD-', size=(20,1), pad=((5,5),(10,10)), button_color=('white', 'gray'))],
    ], relief=sg.RELIEF_GROOVE, tooltip='Download photos for the selected date')]
    ]
    window = sg.Window('iCloud Photo Grabber', size=(400, 400), resizable=True, finalize=True).Layout(layout).finalize()

    while True:
        global apple_login

        event, value = window.Read()
        if event in (sg.WIN_CLOSED, 'EXIT'):
            window.close()
            break
        elif event == '-INCAL1-':
            cal_set = True  # Placeholder for actual login status
            window['-CALSTATUS-'].update('Date selected' if cal_set else 'Date missing',text_color=('white' if cal_set else 'red'))
            window['-DOWNLOAD-'].update(button_color=('white', 'green'))


        elif event == '-LOGIN-':
            logged_in = True  # Placeholder for actual login status
            window['-LOGIN-STATUS-'].update('Logged In' if logged_in else 'Not Logged In',text_color=('white' if logged_in else 'red'))
            username = value['-USERNAME-']
            password = value['-PASSWORD-']

            try:
                apple_login = PyiCloudService(username, password)
            except Exception as e:
                print(e)
                break

            if apple_login.requires_2fa:
                security_code = sg.popup_get_text('Enter Security Code', 'iCloud Security Code')
                result = apple_login.validate_2fa_code(security_code)
                print("Code validation result: %s" % result)
                if not result:
                    print("Failed to verify security code")
                    break
                if not apple_login.is_trusted_session:
                    print("Session is not trusted. Requesting trust...")
                    result = apple_login.trust_session()
                    print("Session trust result %s" % result)
                    if not result:
                        print(
                            "Failed to request trust. You will likely be prompted for the code again in the coming weeks")
            else:
                print("Logged into iCloud.")
                window['-DOWNLOAD-'].update(button_color=('white', 'green'))

        elif event == '-DOWNLOAD-':
            try:
                choice = value['-INCAL1-']

                timestamp = convert_to_datetime(choice)

                photos = apple_login.photos.albums['All Photos']

                for photo in photos:

                    newDate = adjust_apple_time(photo.created)
                    if newDate > timestamp:
                        await process_photo(photo, newDate)
                    else:
                        break

                print("All done!")

            except Exception as e:
                print(e)


async def main():

    await asyncio.gather(event_loop())


if __name__ == "__main__":

    asyncio.run(main())
