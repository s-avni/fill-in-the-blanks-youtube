# Hebrew, Indonesian, Arabic, Kurdish, Urdu, Persian(Farsi), Dhivehi
RTL_langs_initials = {"iw", "he", "ji", "yi", "ar", "ku", "ur", "fa", "dv"}


def is_rtl(lang_initials):
    return lang_initials.lower() in RTL_langs_initials


def is_rtl_word(w):
    if any("\u0590" <= c <= "\u05EA" for c in w):  # Hebrew
        return True
    # todo: same for all languages in RTL_langs_initials
    # e.g. https://utf8-chartable.de/unicode-utf8-table.pl?start=1536&utf8=string-literal


def modify_bare(w):
    if w.isalpha() and is_rtl_word(w):  # regular rtl word
        return w[::-1]
    if w.isalpha():  # regular ltr word
        return w
    if w.isnumeric():  # regular number
        return w
    if len(w) == 1:  # weird parsing sometimes occurs
        return w
    return None


def modify(w):
    modified = modify_bare(w)
    if modified is not None:
        return modified

    # quotations, parenthesis, punctuation, etc:
    first_char = w[0]
    last_char = w[-1]

    start_index = 0  # for indexing
    end_index = len(w)

    if modify_bare(first_char) is None:
        start_index = 1
    if modify_bare(last_char) is None:
        end_index = end_index - 1

    modified = modify_bare(w[start_index:end_index])

    if start_index != 0:
        print("\n\n##")
        print(first_char)
        print(modified)
        modified = first_char + modified
    if end_index != len(w):
        print("\n\n$$")
        print(last_char)
        print(modified)
        modified = modified + last_char

    if modified is not None:
        return modified

    if '-' in w:  # previous errors: אף-אחד
        left_w, right_w = w.split('-')
        left_w = modify(left_w)
        right_w = modify(right_w)

        if left_w is not None and right_w is not None:
            s = right_w + "-" + left_w
            print(s)
            return (s)

    print(w)
    return w


def flip_rtl_string(captions, rtl):
    if not rtl:
        return captions
    # don't reverse numbers
    # don't reverse English words if they are included (todo: there order is getting flipped though)
    # assumes every word is comprised of letters from one alphabet only
    reversed = [modify(w) for w in captions.split()]
    # reversed = [w for w in reversed if w is not None] #todo: we're still getting these...
    reversed = " ".join(reversed)
    print(reversed)
    # todo: edit pyfpdf library directly to reverse every word in each line.
    return reversed


if __name__ == "__main__":
    # s = "\u202B" + "ךל! המ הרוק" + "\u202C\n"
    # print(s)
    flip_rtl_string("ייה. םוי בוט ךל! המ הרוק?", rtl=True)
    # flip_rtl_string("Hello. 'Yes' Please?", rtl=True)
    # flip_rtl_string("Hello my name is Sam 432 yes.", True)
    # flip_rtl_string("םולש המ ךומלש 489", True)
    # flip_rtl_string("נשיקות וחיבוקים, הכל טוב", True)
    # # flip_rtl_string("םולש המ ךומלש?", True)
    # flip_rtl_string("היי. יום טוב לך! מה קורה?", True)
