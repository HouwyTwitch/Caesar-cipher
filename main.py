from re import finditer, MULTILINE
from PySimpleGUI import Text, Multiline, Button, Window, WRITE_ONLY_KEY, WIN_CLOSED, ProgressBar
from tkinter import Tk

tk = Tk()
tk.withdraw()

def get_dictionary():
    dictionary = []
    with open("dictionary.txt", "r", encoding="utf-8", errors="ignore") as f_in:
        for line in f_in:
            dictionary.append(line.replace('\n', ''))
    return dictionary

dictionary = get_dictionary()

def decode_caesar_code(text):
    original_text = text
    text = text.lower()
    results = []
    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
    for i in range(len(alphabet)):
        result = ""
        results.append(text)
        for symbol in text:
            try:
                result = result + alphabet[(alphabet.index(symbol) + 1) % len(alphabet)]
            except ValueError:
                result = result + symbol
        text = result
    results.append(text)
    accuracy = []
    if text.count(' ')<=10:
        for i in range(len(results)):
            window['-BAR-'].update_bar(i)
            _accuracy = 0
            regex = r"([а-я-ё]+\-*[а-я-ё]+)"
            matches = finditer(regex, results[i], MULTILINE)
            for _, match in enumerate(matches, start=1):   
                if match.group(1) in dictionary:
                    _accuracy+=1
            accuracy.append(_accuracy)
    else:
        for i in range(len(results)):
            window['-BAR-'].update_bar(i)
            _accuracy = 0
            for word in dictionary:
                if word in results[i]:
                    _accuracy+=1
            accuracy.append(_accuracy)
    shift = 33 - accuracy.index(max(accuracy))
    if shift == 33:
        shift = 0
    if max(accuracy) == 0:
        shift = 0
        result = "Не удалось расшифровать введённый текст."
    text = results[accuracy.index(max(accuracy))]
    result = ""
    for i in range(len(original_text)):
        if original_text[i].isupper():
            result = result + text[i].upper()
        else:
            result = result + text[i]
    if max(accuracy) == 0:
        shift = 0
        result = "Не удалось расшифровать текст!"
    return result, shift

layout =    [[Text('Расшифровать шифр Цезаря')],
            [Multiline(key='-ML1-', size=(64,16), right_click_menu=['&Edit', ['Заменить на содержимое буфера обмена',]])],
            [Text('Сдвиг с которым был защифрован текст:'), Text(size=(15,1), key='-OUTPUT-')],
            [Multiline(key='-ML2-'+WRITE_ONLY_KEY, size=(64,16))],
            [ProgressBar(33, orientation='h', key="-BAR-", size=(43, 20))],
            [Button('Расшифровать'), Button('Выйти')]]

window = Window('Дешифровщик кода Цезаря', layout, finalize=True)

while True:
    event, values = window.read(timeout=17)
    if event in (WIN_CLOSED, 'Выйти'):
        break
    if event == 'Заменить на содержимое буфера обмена':
        try:
            window['-ML1-'].update(tk.clipboard_get())
        except:
            window['-ML1-'].update("Буфер обмена не содержит текста!")
    if event == 'Расшифровать':
        result, shift = decode_caesar_code(values['-ML1-'])
        window['-ML2-'+WRITE_ONLY_KEY].update(result)
        window['-OUTPUT-'].update(shift)
window.close()
