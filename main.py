from mts import MTS

# Driver Method
if __name__ == '__main__':
    txt = str(input("Enter text here: "))
    lang = input("Enter target Language: ", ) or None
    inter_lang = input("Enter intermediate Language (If any): ", ) or None
    _mts = MTS()
    if lang == None and inter_lang == None:
        output_txt = _mts.translate(txt)    
    elif inter_lang == None:
        output_txt = _mts.translate(txt, lang)
    else:
        output_txt = _mts.translate(txt, lang, inter_lang)
    print("Output Result: ", output_txt)
