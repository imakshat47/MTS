from mts import MTS

# Driver Method
if __name__ == '__main__':
    txt = str(input("Enter text here: "))
    lang = str(input("Enter target Language: ", ) or 'en')
    inter_lang = str(input("Enter intermediate Language (If any): ", ) or 'hi')
    _mts = MTS()
    output_txt = _mts.translate(txt, lang, inter_lang)
    print("Output Result: ", output_txt)
