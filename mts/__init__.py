#!/usr/bin/env python3

"""
    Library to preform Machine Translation using Recurrent Neural Networks.
"""

""" Import Libs """
# Details
try:
    import re
    import string
    import demoji
    from googletrans import Translator
    from google_trans_new import google_translator
    from textblob import TextBlob
    from translate import Translator as trans
    import goslate
    import requests
    import json
    from key import _debug
except ModuleNotFoundError as e:
    print("Missing required library:- "+str(e))
translator = Translator(service_urls=[
    'translate.googleapis.com',
    'translate.google.com',
])

# Details
__author__ = "Imakshat47"
__version__ = "1.2.3"
__license__ = "GNU"

# Local Variables
# bool
if(_debug == None):
    _debug = True
# msg
_initiated_cls_msg = " Initaited !!"
_distructed_cls_msg = " Instance Removed !!"

"""
    Cleaner Class
"""


class Cleaner(object):

    def __init__(self):
        _debug and print("Cleaner"+_initiated_cls_msg)

    def __del__(self):
        _debug and print("Cleaner"+_distructed_cls_msg)

    # Cleans text message
    """ clean function removes all extra symbols, unwanted noise, urls and username from input test if present and
        returns a clean text as output.
    """

    def _clean(self, preprocess_text):
        try:
            # Text to lower
            preprocess_text = preprocess_text.lower()
            # Remove punctuation
            exclude = set(string.punctuation)
            preprocess_text = ''.join(
                ch for ch in preprocess_text if ch not in exclude)

            # Convert more than 2 letter repetitions to 2 letter
            # funnnnny --> funny
            preprocess_text = re.sub(r'(.)\1+', r'\1\1', preprocess_text)

            # Remove - & '
            preprocess_text = re.sub(r'(-|\')', ' ', preprocess_text)

            # Replaces #hashtag with hashtag
            preprocess_text = re.sub(r'#(\S+)', r' \1 ', preprocess_text)

            # Replace 1+ dots with space
            preprocess_text = re.sub(r'\.{1,}', ' ', preprocess_text)

            # Strip space, " and ' from text
            preprocess_text = preprocess_text.strip('  "\'')

            # Replace @handle with the word USER_MENTION
            preprocess_text = re.sub(
                "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", preprocess_text)
            preprocess_text = re.sub(
                r'@[\S]+', 'USER_MENTION', preprocess_text)

            # Replaces URLs with the word URL
            preprocess_text = re.sub(
                r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ', preprocess_text)
            preprocess_text = re.sub(r'http\S+', '', preprocess_text)
            preprocess_text = re.sub(
                r'((www\.[\S]+)|(https://[\S]+))', 'url', preprocess_text)

            # Replace multiple spaces with a single space
            preprocess_text = re.sub(r'\s+', ' ', preprocess_text)

            # removing http/url
            preprocess_text = re.sub(r'http', ' ', preprocess_text)
            preprocess_text = re.sub(r'https', ' ', preprocess_text)
            preprocess_text = re.sub(r'url', ' ', preprocess_text)
            preprocess_text = re.sub(r'USER_MENTION', ' ', preprocess_text)

            preprocess_text = preprocess_text.strip('    ')
            _debug and print("Cleaned Text: ", preprocess_text)
        except Exception as e:
            _debug and print('PreProcessor Error => ', e)
        return preprocess_text

    # Handle Emojies
        """ demojis removed the emoticons present in input text and returns a clean text by altering corresponsding emoticons with text
        """

    def _demojis(self, text, _demoji_to_text=True):
        try:
            if _demoji_to_text:
                text = demoji.replace_with_desc(text, "")
            shock_emoji = re.compile(
                "[" u"\ud83d\ude31" "]+", flags=re.UNICODE)
            text = shock_emoji.sub(r'EMONEG', text)
            # Smile -- :), : ), :-), (:, ( :, (-:, :')
            text = re.sub(r'(:\)|:-\)|\(\s:|\(-:|:\'\))', 'EMOPOS', text)
            # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D, :-d, :d
            text = re.sub(r'(:D|:-D|x-D|X-D|:-d|:d)', 'EMOPOS', text)
            # Love -- <3, :*
            text = re.sub(r'(<3|:\*)', 'EMOPOS', text)
            # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
            text = re.sub(r'(;-\)|;-D|\(-;)', 'EMOPOS', text)
            # Sad -- :-(, : (, :(, ):, )-:, -_-
            text = re.sub(r'(:\(|:-\(|\)\s:|\)-:|-_-)', 'EMONEG', text)
            # Cry -- :,(, :'(, :"(
            text = re.sub(r'(:,\(|:\'\(|:"\()', 'EMONEG', text)
            # Shout -- :@
            text = re.sub(r'(:\@)', 'EMONEG', text)
            _debug and print("Demoji Text: ", text)
            text = self.__handle_coded_emojis(text)
            _debug and print(
                "Emoticons removed Text: ", text)
        except Exception as e:
            _debug and print('PreProcessor Error => ', e)
        return text

    # Handle Coded Emojies
        """ Handle Codee Emojis using the unicodes removes the unwanted emoticons.
            prerocessed_text a noise free test with emoticons that neeced to be removed.
            Returns:
             string: preprocessed_text clean text after processing.
        """

    def __handle_coded_emojis(self, processed_text):
        try:
            # ----------------------------------------------------------------------------------------------
            # --------------\ud83d\ude------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------

            happy_emoji = re.compile(
                u"(\ud83d[\ude00-\ude09])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\ude17-\ude19])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\ude42-\ude43])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\ude47-\ude49])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\ude38-\ude39])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude0a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude0b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude0c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude0d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude0e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude1a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude1b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude1c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude1d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude2c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude3a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude3b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude3c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude3d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude4a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude4b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude4c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\ude4e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\ude47\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\ude46\u200d\u2642)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\ude4b\u200d\u2642)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\ude4e\u200d\u2642)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udeb4\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udeb5\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udeb5\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # ----------------
            sad_emoji = re.compile(
                u"(\ud83d[\ude13-\ude16])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83d[\ude10-\ude12])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83d[\ude20-\ude37])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83d[\ude40-\ude41])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83d[\ude44-\ude45])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83d\ude4d\u200d\u2642)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude0f)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude1e)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude1f)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude2b)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude2f)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude2e)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude3f)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude2d)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude2a)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\ude3e)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)
            # --------------------------------------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------------------------------
            # --------------\ud83e\udd----------

            happy_emoji = re.compile(
                u"(\ud83e[\udd16-\udd19])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83e[\udd20-\udd21])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83e[\udd23-\udd24])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83e[\udd33-\udd36])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83e[\udd42-\udd43])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd11)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd13)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd30)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd81)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd84)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd8b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd1a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd1d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83e\udd1e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # --------
            sad_emoji = re.compile(
                u"(\ud83e[\udd14-\udd15])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e[\udd47-\udd49])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e[\udd24-\udd25])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e[\udd90-\udd91])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e[\udd87-\udd89])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e\udd26\u200d\u2640)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e\udd26\u200d\u2642)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e\udd37\u200d\u2640)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83e\udd37\u200d\u2642)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd10)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd22)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd27)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd12)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd1b)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd1c)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd8a)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd8c)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd8e)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd82)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83e\udd80)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)
            # --------------------------------------------------------------------------------------------------------------------------------------
            # --------------\u263a\----
            # -------------------------------------------------------------------------------------------------------------------------------------
            happy_emoji = re.compile(u"(\u263a\ufe0f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # --------------------------------------------------------------------------------------------------------------------------------------
            # --------------\u2615\----
            # -------------------------------------------------------------------------------------------------------------------------------------
            happy_emoji = re.compile(u"(\u2615\ufe0f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # -----------------------------------------
            # --------------\u2639\----
            sad_emoji = re.compile(u"(\u2639\ufe0f)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)
            # ----------------------------------------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------------------------------------
            # --------------\ud83d\udc---------------------------------------------------------------------------------------------------
            happy_emoji = re.compile(
                u"(\ud83d[\udc83-\udc85])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\udc91-\udc93])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\udc95-\udc99])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d[\udc70-\udc71])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc51)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc44)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc76)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc78)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc6f\u200d\u2642)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\u2764\ufe0f\u200d\ud83d\udc69)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\u2764\ufe0f\u200d\ud83d\udc68)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\u2764\ufe0f\u200d\ud83d\udc8b\u200d\ud83d\udc69)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\u2764\ufe0f\u200d\ud83d\udc8b\u200d\ud83d\udc68)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc66\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc69\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc69\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc69\u200d\ud83d\udc66\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc69\u200d\ud83d\udc66\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc68\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc68\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc68\u200d\ud83d\udc67\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc68\u200d\ud83d\udc66\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc68\u200d\ud83d\udc67\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc66\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc67\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc66\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc67\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc67\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc71\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc69\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc66)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83d\udc68\u200d\ud83d\udc67)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc6a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc6b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc6d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc6f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc9f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc9d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc9e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc4f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc4d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc4b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc4c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc8d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc8b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc8f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc8e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc9c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc9a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc9b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udcab)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udcaf)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udcaa)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83d\udc7c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # ------------------
            sad_emoji = re.compile(
                u"(\ud83d[\udc79-\udc80])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(
                u"(\ud83d[\udc36-\udc37])" "+", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc45)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc31)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc94)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc89)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc16)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc7a)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc7b)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc7d)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc7e)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc4e)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc4a)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc2d)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udc8a)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udca2)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udca3)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udca6)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83d\udca9)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            neutral_emoji = re.compile(u"(\ud83d\udc46)", flags=re.UNICODE)
            processed_text = neutral_emoji.sub(r'EMONEU', processed_text)

            # --------------------------------------------------------------------------------------------------------------------------------

            # --------------\ud83c\udf------------------------------------------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------------------------------------------------------------------------------
            happy_emoji = re.compile(
                u"(\ud83c[\udf80-\udf82])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c[\udf83-\udf87])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c[\udf75-\udf79])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c[\udf96-\udf97])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c[\udf69-\udf70])" "+", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf08)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf93)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf32)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf39)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf89)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf20)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf05)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c\udfcb\ufe0f\u200d\u2640\ufe0f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c\udfcc\ufe0f\u200d\u2640\ufe0f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c\udfc4\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(
                u"(\ud83c\udfca\u200d\u2640)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf7a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf7b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf7c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf7e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf7f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfc2)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfc4)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfc5)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfc6)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfc7)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfca)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfcb)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfcc)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfa1)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfa2)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfa9)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfad)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfae)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfaf)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf8a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfe9)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf1f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfb3)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udff5)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udfbf)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf6a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf6b)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf6c)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf6d)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf6e)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # ----------------------
            sad_emoji = re.compile(u"(\ud83c\udf35)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83c\udf2a)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83c\udf2b)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)

            sad_emoji = re.compile(u"(\ud83c\udf21)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)
            # -----------------------------------------
            neutral_emoji = re.compile(u"(\ud83c\udffb)", flags=re.UNICODE)
            processed_text = neutral_emoji.sub(r'EMONEU', processed_text)

            neutral_emoji = re.compile(u"(\ud83c\udffc)", flags=re.UNICODE)
            processed_text = neutral_emoji.sub(r'EMONEU', processed_text)
            # -----------------------------------------
            # --------------\u2620\ufe0f----
            sad_emoji = re.compile(u"(\u2620\ufe0f)", flags=re.UNICODE)
            processed_text = sad_emoji.sub(r'EMONEG', processed_text)
            # -----------------------------------------
            # --------------\u270a----
            happy_emoji = re.compile(u"(\u270a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # -----------------------------------------
            # --------------\\u270c\ufe0f----
            happy_emoji = re.compile(u"(\u270c\ufe0f)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
            # -----------------------------------------
            # --------------\ud83c\udf----
            happy_emoji = re.compile(u"(\ud83c\udf89)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf81)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)

            happy_emoji = re.compile(u"(\ud83c\udf8a)", flags=re.UNICODE)
            processed_text = happy_emoji.sub(r'EMOPOS', processed_text)
        except Exception as e:
            _debug and print('Handle Coded Emojies Error: ', e)
        return processed_text


"""
    API Class
"""


class API(object):
    def __init__(self):
        _debug and print("API"+_initiated_cls_msg)

    def __del__(self):
        _debug and print("API"+_distructed_cls_msg)

    def get_translate(self, input_text='', target_language='en', intermediate_language='ur'):
        # request input_text/target_language/intermediate_language
        _uri = "https://mtsys.herokuapp.com/" + \
            input_text.replace(" ", "%20") + '/' + \
            target_language+'/'+intermediate_language
        _debug and print("API URI: ", _uri)
        try:
            r = requests.get(_uri, headers={'accept': 'application/json'})
            if r.status_code == 200:
                res = r.json()['data']
                _debug and print("API Response: ", res)
                return res['output']
        except Exception as e:
            _debug and print("API Exception: ", e)
        return input_text


"""
    MTS Class inherted API class.
"""


class MTS(Cleaner, API):
    def __init__(self):
        self.__translator = Translator()
        self.__google_translator = google_translator()
        _debug and print("MTS"+_initiated_cls_msg)

    def __del__(self):
        _debug and print("MTS"+_distructed_cls_msg)

    def translate(self, input_text='', target_language='en', intermediate_language='hi'):
        if input_text == None:
            return None

        _debug and print("Text Cleaning: ", input_text)
        _debug and print("Traget Language: ", target_language)
        _debug and print("Intermediate Language: ", intermediate_language)
        
        input_text = self._clean(input_text)

        _debug and print("Text Demoj: ", input_text)
        input_text = self._demojis(input_text, True)

        _debug and print("Translating: ", input_text)
        input_text = self.get_translate(
            input_text, target_language, intermediate_language)
        _debug and print("API Translated: ", input_text)
        flag = False
        try:
            input_text = self.__google_translator.translate(
                input_text, lang_tgt=intermediate_language)
            _debug and print("Intermediate Translation: ", input_text)
            input_text = self.__google_translator.translate(
                input_text, lang_tgt=target_language)
            _debug and print("Intermediate Translation: ", input_text)
        except Exception as e:
            flag = flag ^ True
            _debug and print("Exception: ", e)
        try:
            _translated = self.__translator.translate(
                input_text, dest=intermediate_language)
            input_text = _translated.text
            _debug and print("Intermediate Translation: ", input_text)
            _translated = self.__translator.translate(
                input_text, dest=target_language)
            input_text = _translated.text
            _debug and print("Intermediate Translation: ", input_text)
        except Exception as e:
            flag = flag ^ True
            _debug and print("Exception: ", e)
        try:
            _gs = goslate.Goslate()
            input_text = _gs.translate(input_text, target_language)
            _debug and print("Intermediate Translation: ", input_text)
        except Exception as e:
            flag = flag ^ True
            _debug and print("Exception: ", e)
        try:
            input_text = str(TextBlob(input_text).translate(to=target_language))
            _debug and print("Text Intermediate Translation: ", input_text)
        except Exception as e:
            flag = flag ^ True
            _debug and print("Exception: ", e)
        if(flag):
            _debug and print("Exception: All Models Failed!!")
        # Base Models
        _debug and print("Text Translated: ", input_text)
        return input_text
