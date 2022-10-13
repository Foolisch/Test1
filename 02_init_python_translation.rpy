#python early:
translate chinese python:
    gui.text_font = "fonts/NotoSerifCJKsc-Regular.otf"
    gui.interface_text_font = "fonts/NotoSerifCJKsc-Regular.otf"
    gui.button_text_font = "fonts/NotoSerifCJKsc-Regular.otf"

#translate chinese python:
#    gui.text_size = 24
#    define gui.interface_text_font = "fonts/NotoSerifCJKsc-Regular.otf"
#    define gui.interface_text_font = "fonts/NotoSerifCJKsc-Regular.otf"
#    define gui.button_text_font = "fonts/NotoSerifCJKsc-Regular.otf"

init python:
    language_dict = {}
    list_files = renpy.list_files()
    language_files_list = []
    for fileName in list_files:
        if fileName[-5:] == ".json":
            if "language_" in fileName:
                language_files_list.append(fileName)
    language_files_list.sort()
    language_flag1 = False
    language_count1 = 0
    language_count_all = 0
    for langFileName in language_files_list:
        languageFile = json.loads(renpy.file(str(langFileName)).read())
        if language_flag1 == False:
            language_dict = languageFile
            hash1 = hashlib.md5(renpy.file(str(langFileName)).read()).hexdigest()
            language_count_all = len(language_dict)
            language_count1 = len(language_dict)
            language_flag1 = True
        else:
            for langLine in languageFile:
                langLine1 = langLine
                if "_!_" not in langLine1:
                    langLine1 = langLine1 + "_!_" + languageFile[langLine][0]
                language_dict[langLine1] = languageFile[langLine]
            language_count_all += len(languageFile)

    language_dict_len = len(language_dict)
    language_dict_fields_len = len(language_dict.items()[0][1])
    untranslated_lines = []
    if persistent.lang_suffixes is None or persistent.lang_count != len(json.dumps(language_dict)):
        language_completed_list = [0]*(max(language_fields.values())+1)
        for lang_line_key, lang_line in language_dict.items():
            for lang_key, lang_value in language_fields.items():
                if lang_value < len(lang_line):
                    if lang_line[lang_value] != "":
                        language_completed_list[lang_value] += 1
#                    else:
#                        if lang_key == "english":
#                            untranslated_lines.append(lang_line_key)
        lang_suffixes = {}
        for lang_key in language_fields:
            if language_completed_list[language_fields[lang_key]] != language_dict_len:
                lang_suffixes[lang_key] = " (" + str(int(float(language_completed_list[language_fields[lang_key]]) / float(language_dict_len)*100)) + "%)"
            else:
                lang_suffixes[lang_key] = ""
        persistent.lang_suffixes = lang_suffixes
        persistent.lang_count = len(json.dumps(language_dict))
    languageFile = False

    def parse_tstr(str1):
        global item1
        result = re.findall(r'\[(.*?)\]', str1)
        for var1 in result:
            var2 = var1
            translateVarFlag = False
            if var2[-2:] == "!t":
                var2 = var2[:-2]
                translateVarFlag = True
            if globals().has_key(var2):
                if translateVarFlag == True:
                    str1 = str1.replace("[" + var1 + "]", str(t__((globals()[var2]))))
                else:
                    str1 = str1.replace("[" + var1 + "]", str(globals()[var2]))
            else:
                if translateVarFlag == True:
                    str1 = str1.replace("[" + var1 + "]", "{c}" + t__(var2) + "{/c}")
                else:
                    str1 = str1.replace("[" + var1 + "]", "{c}" + var2 + "{/c}")
        return str1
    def clean_tstr(str1):
        str1 = re.sub(r'\[|\]|\$|\%', " ", str1)
        return str1
    def t_(s):
        return s
    def t__(s, speaker = None):
        global _preferences, language_fields, language_dict, last_dialogue_character
        if speaker == None:
            speaker = last_dialogue_character
        lang = _preferences.language
        if language_fields.has_key(lang) == False:
            lang = "english"
        st = s
        sKey = s
        if language_dict.has_key(s + "_!_" + speaker):
            sKey = s + "_!_" + speaker
        else:
            if language_dict.has_key(s):
                sKey = s
            else:
                sKey = False
        if sKey:
            if len(language_dict[sKey]) > language_fields[lang]:
                st = language_dict[sKey][language_fields[lang]]
                if st == "":
                    st = language_dict[s][language_fields[lang]]
                    if st == "":
                        st = language_dict[sKey][language_fields["english"]]
                        if st == "":
                            st = language_dict[s][language_fields["english"]]
                            if st == "":
                                st = s
            else:
                st = s
            st = st.split("#")[0]
        return parse_tstr(st)

    def ts__(s):
        global _preferences, language_fields, language_dict, last_dialogue_character
        lang = _preferences.language
        st = s
        sKey = s
        if language_dict.has_key(s + "_!_" + last_dialogue_character):
            sKey = s + "_!_" + last_dialogue_character
        else:
            if language_dict.has_key(s):
                sKey = s
            else:
                sKey = False
        if sKey:
            if len(language_dict[sKey]) > language_fields[lang]:
                st = language_dict[sKey][language_fields[lang]]
                if st == "":
                    st = language_dict[s][language_fields[lang]]
                    if st == "":
                        st = language_dict[sKey][language_fields["english"]]
                        if st == "":
                            st = language_dict[s][language_fields["english"]]
                            if st == "":
                                st = s
            else:
                st = s
            st = st.split("#")[0]
        return parse_tstr(st)

    def t___(s):
        global _preferences, language_fields, language_dict, last_dialogue_character
        s = re.sub(r'(\n\s*)', " ", s)
        lang = _preferences.language
        if language_fields.has_key(lang) == False:
            lang = "english"
        st = s
        sKey = s
        if language_dict.has_key(s + "_!_" + last_dialogue_character): #trying to find string of speaker
            sKey = s + "_!_" + last_dialogue_character
        else:
            if language_dict.has_key(s): #trying to find string w/o speaker
                sKey = s
            else:
                sKey = False
        if sKey == False: #trying to strip the string
            s = s.strip()
            if language_dict.has_key(s + "_!_" + last_dialogue_character): #trying to find string of speaker
                sKey = s + "_!_" + last_dialogue_character
            else:
                if language_dict.has_key(s): #trying to find string w/o speaker
                    sKey = s
        if sKey:
            if len(language_dict[sKey]) > language_fields[lang]:
                st = language_dict[sKey][language_fields[lang]]
                if st == "":
                    st = language_dict[s][language_fields[lang]]
                    if st == "":
                        st = language_dict[sKey][language_fields["english"]]
                        if st == "":
                            st = language_dict[s][language_fields["english"]]
                            if st == "":
                                st = s
            else:
                st = s
            st = st.split("#")[0]

        st = parse_tstr(st)
        st = st.replace(" ", " ")
        st = re.sub("\!\s{1,}", "!\n", st)
        st = re.sub("\?\s{1,}", "?\n", st)
        st = re.sub("\.\s{1,}", ".\n", st)
        st = re.sub("Mr\.\\n", "Mr. ", st)
        st = re.sub("Mrs\.\\n", "Mrs. ", st)
        st = re.sub("Ms\.\\n", "Ms. ", st)
        st = re.sub("M\.\\n", "M. ", st)
        st = re.sub("prof.\\n", "prof. ", st)
        return st
