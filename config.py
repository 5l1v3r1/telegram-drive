# Bot's token
token = 'TOKEN'
# List of IDs of accepted users (as int)
accepted_users = []
# Name of folder, where your files are stored
default_path = 'share_files'

help_text = '''
**Hello, my Lord!**
You can get any of your files via Telegram.
These are commands that are used for downloading files:
***/file_list*** - _see the list of files_
'''

errors = {
    'empty_file': 'File is empty',
    'no_access': 'You haven\'t got access to this bot',
    'plain_text': 'Sorry, I don\'t understand you'
}
