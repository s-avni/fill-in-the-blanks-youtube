import logging
import re

import pycountry

# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
old_iso_639 = {"iw": "Hebrew",
               "ji": "Yiddish"}


# todo: add user option to remove words followed by :, e.g. when different users are speaking and their name is listed before their speech
def generate_clean_solution(captions):
    '''
    @summary: returns clean solution string from captions vtt file
    :param captions:
    :return:
    '''
    # remove first 4 lines, which includes metadata
    print(captions)
    captions = captions[4:]
    # remove all timestamp lines, i.e lines including the symbol "-->"
    captions = [l.strip() for l in captions if "-->" not in l]
    # replace all \n in end of sentences with ""
    captions = [l.replace('\n', '') for l in captions]
    # remove all lines which are blank
    captions = [l for l in captions if len(l) > 0]
    # combine list into one string
    captions = " ".join(captions)
    # remove text in square brackets, as this describes the video but is not heard. e.g [theme music]
    # assumes no nested brackets, which is true for youtube videos
    captions = re.sub("[\[].*?[\]]", "", captions)

    logging.info("First 20 characters of captions")
    logging.info(captions[:20])

    return captions


def generate_caption_blanks(captions, skip):
    '''
    @summary: creates exercise string with blanks from the solution string
    '''
    # remove every xth word, using variable "skip"
    words = captions.split(" ")
    # remove all empty words
    words = [w for w in words if len(w) > 0]
    captions_blanks = []
    blank = "_________"
    for i, w in enumerate(words, start=1):  # don't want first word of captions missing
        try:
            if i % skip != 0:
                captions_blanks.append(w)
            elif not w[-1].isalpha():
                # Keep punctuations at the end of words
                captions_blanks.append(blank + w[-1])
            else:
                captions_blanks.append(blank)
        except:
            logging.error("Failed on word {}/{}: '{}'".format(i, len(words), w))
            raise

    return " ".join(captions_blanks)


def map_initials_to_language_word(initials):
    names = []
    for initial in initials:
        try:
            if len(initial) == 2:
                if initial in old_iso_639.keys():
                    name = old_iso_639[initial]
                    names.append((name, initial))
                else:
                    name = (pycountry.languages.get(alpha_2=initial)).name
                    names.append((name, initial))
            elif len(initial) == 3:
                name = (pycountry.languages.get(alpha_3=initial)).name
                names.append((name, initial))
            else:  # for a specific country, etc.
                # Chinese - zh-TW
                # Portuguese - pt-PT (Portugal)
                # Chinese - zh-Hans
                # Chinese - zh-Hant
                name = (pycountry.languages.get(alpha_2=initial[:2])).name
                print(name)
                print(initial)
                names.append((name + " " + initial, initial))
            # todo: Moshe, how would you do this more correctly?
        except KeyError as err:
            print(err)
            names.append((initial, initial))
    print(names)
    return names

# def get_initials(language):
#     possible_prefix = "(Automatic) "
#     if language.startswith(possible_prefix):
#         language = language[len(possible_prefix):]
#     if language in old_iso_639.values():
#         return [k for k,v in old_iso_639.items() if v == language][0]
#     lang_object = pycountry.languages.get(name=language)
#     try:
#         initial = lang_object.alpha_2
#     except AttributeError:
#         initial = lang_object.alpha_3
#     if initial is not None:
#         return initial
#     raise ValueError
