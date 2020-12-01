import json
import re
import webbrowser

# from wox import Wox, WoxAPI


# from pypinyin import Style, pinyin, load_phrases_dict
def fuzzyfinder(user_input, collection):
    suggestions = []
    pattern = '.*?'.join(user_input)  # Converts ‘djm‘ to ‘d.*?j.*?m‘
    regex = re.compile(pattern)		 # Compiles a regex.
    for item in collection:
        # Checks if the current item matches the regex.
        match = regex.search(item)
        if match:
            suggestions.append((len(match.group()), match.start(), item))
    return [x for _, _, x in sorted(suggestions)]

class TipsOpen():
    def query(self, query):
        results = []
        args = query.split(' ')
        page_name = args[0].lower()
        with open('config.json', 'r', encoding='utf-8') as fio:
            config = json.loads(fio.read())
            page_keys = config.keys()
            fuzzyfinder_results = list(fuzzyfinder(page_name, page_keys))
            for result in fuzzyfinder_results:
                wox_result = {
                    "Title": "Open URL:" + result,
                    "SubTitle": "123",
                    "IcoPath":"Images/app.png",
                    "JsonRPCAction": {
                        "method": "openUrl",
                        "parameters": [result],
                        "dontHideAfterAction": False
                    }
                }
                results.append(wox_result)
        return results

    def openUrl(self, page=None, page_param=None):
        if page == None:
            return 

        with open('config.json', 'r', encoding='utf-8') as fio:
            config = json.loads(fio.read())
            page_keys = config.keys()
            if not any(fuzzyfinder(page, page_keys)):
                return "No result."
            webbrowser.open(config[page].get('url'))


if __name__ == "__main__":
    test = TipsOpen()
    print(test.query('in'))
