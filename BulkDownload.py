import os, sys
import arcpy
from datetime import datetime
import requests
import string


def download(input_list, output_directory):
    # creating target directory if needed
    try:
        os.mkdir(output_directory)
        arcpy.AddMessage("Created new directory " + output_directory)
    except OSError:
        arcpy.AddMessage("Using existing directory " + output_directory)

    # make a list of URLs to look at
    url_list = []
    with open(input_list,'r',encoding='utf8') as f:
        url_list = f.readlines()  # crack apart entries
    for i in range(len(url_list)):
        url_list[i] = url_list[i].replace('\n', '')  # strip off newlines
    url_list = [i for i in url_list if i]  # strip out blank entries

    # function for downloading each file
    def download_file(file_url, target_folder):
        r = requests.get(file_url, headers=headers)  # create HTTP response object
        file_name = get_filename(file_url)
        # send an HTTP request to the server and save the HTTP response in a response object called r
        with open(os.path.join(target_folder, file_name), 'wb') as f:
            # write the contents of the response (r.content) to a new file in binary mode.
            f.write(r.content)
        return 0

    def get_filename(file_url):
        i = len(file_url) - 1
        first_letter = 0
        while i >= 0:
            if file_url[i] == "/":
                first_letter = i + 1
                break
            else:
                i -= 1
        temp_filename = file_url[first_letter:]
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        true_filename = ''.join(c for c in temp_filename if c in valid_chars)
        return true_filename

    # make a "problem links" list in the output if needed
    def add_problem_url(problem_url):
        problem_url_list = os.path.join(output_directory, 'ProblemURLs.txt')
        f = open(problem_url_list, "a")
        f.write(problem_url + "\n")
        f.close()

    # download each file
    current_url = 0
    total_urls = len(url_list)
    had_problem_urls = False
    headers = {'User-Agent': "Clay's Bulk Downloader (claystestingaddress@gmail.com)"}
    # Wikimedia commons (and probably others) won't allow requests without an identifying header
    arcpy.SetProgressor("step", "Downloading Files", 0, total_urls, 1)
    for url in url_list:
        try:
            current_url += 1
            message =  "Fetching file %d / %d" % (current_url, total_urls)
            arcpy.SetProgressorLabel(message)
            arcpy.AddMessage(datetime.now().strftime("%H:%M:%S") + " | " + message)
            download_file(url, output_directory)
        # Invalid URL
        except requests.exceptions.MissingSchema:
            arcpy.AddWarning("Invalid URL")
            add_problem_url(url)
            had_problem_urls = True
        except requests.exceptions.InvalidSchema:
            arcpy.AddWarning("Invalid URL")
            add_problem_url(url)
            had_problem_urls = True
        # Trouble connecting
        except requests.exceptions.ConnectionError or socket.gaierror \
               or urllib3.exceptions.NewConnectionError or urllib3.exceptions.MaxRetryError:
            arcpy.AddWarning("Could not connect")
            add_problem_url(url)
            had_problem_urls = True
        arcpy.SetProgressorPosition()

    # end message
    arcpy.AddMessage("Downloads complete! Check '%s' to see your files."
                     % output_directory)
    if had_problem_urls:
        arcpy.AddWarning("File created at '%s' with a list of problem urls"
                         % os.path.join(output_directory, 'ProblemURLs.txt'))

if __name__ == '__main__':  # executed on its own
    try:  # if arguments are given, use those
        list = sys.argv[1]
        directory = sys.argv[2]
    except IndexError:  # otherwise, ask and verify through command line
        # Tell user the current directory and ask to specify where to put downloads
        current_dir = os.getcwd()
        print("Current Directory: " + current_dir)
        default_dir = "Downloads"
        new_dir = input("Enter new directory name (blank for ./% s): " % default_dir)
        # User can specify a local folder or put it somewhere else
        if new_dir == "":
            directory = os.path.join(current_dir, default_dir)
        elif new_dir[1] == ':':
            directory = new_dir
        else:
            directory = os.path.join(current_dir, new_dir)
        # Can be an existing or new folder
        try:
            os.mkdir(directory)
            print("Created new directory " + directory)
        except OSError:
            print("Using existing directory " + directory)
        # Ask user for file with url list
        list = ""
        file_is_valid = False
        while not file_is_valid:
            list = input("Enter location of link list: ")
            if list == "":
                sys.exit("bruh")
            elif list[1] == ':':
                pass
            else:
                text_file_path = os.path.join(current_dir, list)
            if os.path.exists(list):
                if list[-3:] != "txt":
                    print("please use a .txt file.")
                else:
                    print("Using file '% s'" % list)
                    file_is_valid = True
            else:
                print("File '% s' does not exist." % list)
    # execute script content
    download(list, directory)
