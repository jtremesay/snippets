#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

import ConfigParser
from email.mime.text import MIMEText
import logging
import re
import smtplib
import subprocess
import sys


class Commit(object):
    def __init__(self, repository, revision):
        self._repository = repository
        self._revision = revision

    def load(self):
        """
        Load commit informations
        return boolean Success
        """
        pipe = subprocess.Popen(['svn', 'log', '-v', '-r', str(self._revision), self._repository], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        commit_data, error = pipe.communicate()
        if len(commit_data) == 0:
            logging.getLogger().warning(error)
            return False

        # Cut message in lines
        commit_data = commit_data.splitlines()

        # Remove first and last line (svn decoration)
        commit_data = commit_data[1:-1]

        # Search usefull informations
        #'r2800 | jeydoux | 2014-10-31 17:29:45 +0100 (Fri, 31 Oct 2014) | 3 lines'
        line_of_informations = commit_data[0]
        informations = re.search("r\d+ \| (?P<author>\w+) \| .* \| (?P<message_lenght>\d+) lines?", line_of_informations)
        if informations is None:
            logging.getLogger().warning('Cannot get usefull information')
            return False

        informations = informations.groupdict()
        self._author = informations['author']
        message_lenght = int(informations['message_lenght'])
        self._modified_files = commit_data[2:-(message_lenght + 1)]
        self._message = '\n'.join(commit_data[-message_lenght:])

        return True

    def get_repository(self):
        """
        @return str Repository URL
        """
        return self._repository

    def get_revision(self):
        """
        @return int Revision
        """
        return self._revision

    def get_author(self):
        """
        @return str Author
        """
        return self._author

    def get_modified_files(self):
        """
        @return list<str> Modified files
        """
        return self._modified_files

    def get_message(self):
        """
        @return str Message
        """
        return self._message


def send_commit_by_mail(config, commit):
    logging.getLogger().info('sending mail...')

    sender = config.get('Mail', 'from')
    recipient = config.get('Mail', 'to')
    server = config.get('Mail', 'server')

    message = MIMEText('%s\n\nModified files:\n%s' % (commit.get_message(), '\n'.join(commit.get_modified_files())))
    message['Subject'] = '[SVN Notification] new commit on %s (r%d)' % (config.get('Repository', 'name'), commit.get_revision())
    message['From'] = sender
    message['To'] = recipient

    s = smtplib.SMTP(server)
    s.sendmail(sender, [recipient], message.as_string())
    s.quit()


def usage():
    print("svn-mailer.py <revision> <config file>")


def main(argc, argv):
    if argc != 3:
        usage()
        return False

    try:
        converted_revision = int(argv[1])
        if converted_revision < 0:
            raise ValueError
    except ValueError:
        print('"%s" is not an valid revision number' % argv[1])
        return False
    else:
        revision = converted_revision

    config_file_path = argv[2]
    config = ConfigParser.ConfigParser()
    result = config.read(config_file_path)
    if len(result) == 0:
        print('"%s" is not an valid configuration file' % argv[2])
        return False

    # Install logger handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = logging.FileHandler(config.get('Logging', 'log_file'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Get svn infos
    repository = config.get('Repository', 'url')
    commit = Commit(repository, revision)
    result = commit.load()
    if not result:
        logger.error('cannot load commit informations for revision %s in repository %s', revision, repository)
        return False

    send_commit_by_mail(config, commit)

    return True

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
