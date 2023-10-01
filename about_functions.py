import json


# load up the file here so both functions can see it
with open("functionSummary.json", "r") as json_file:
    function_json = json.load(json_file)


def summarize():
    # find the longest function name
    max_length = 0
    for function in function_json['functions']:
        if len(str(function['shortname'])) > max_length:
            max_length = len(str(function['shortname']))
    # print the basic blurb for each function
    for idx, function in enumerate(function_json['functions']):
        desc = "{0:>3}. {1:<%i} | {2}" % max_length
        print(desc.format(idx, function['shortname'], function['blurb']))
    print()


def detail(function_num):
    # detail the properties of a single function
    function = function_json['functions'][function_num]
    print("=== %s ===" % function['shortname'])
    print(" %s" % function['fullname'])
    print(" %s" % function['longdesc'])
    print("= Parameters =")
    for parameter in function['parameters']:
        print(" %s:  %s " % (parameter['name'], parameter['desc']))


if __name__ == "__main__":
    summarize()
    while True:
        user_input = input("Enter an index to learn more about a function, or just press enter to quit. ")
        if user_input == "":
            exit(0)
        else:
            try:
                detail(int(user_input))
            except TypeError or ValueError:
                print("Not a valid input. ")
