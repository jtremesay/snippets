#!/usr/bin/env python2
#-*- coding: UTF-8 -*-

#
# Copyright Jonathan Tremesaygues <killruana@gmail.com> - 2014
#
# This software is governed by the CeCILL-B license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL-B
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
#

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
        line_of_informations = commit_data[0]
        informations = re.search("r\d+ \| (?P<author>\w+) \| (?P<date1>.+) \((?P<date2>.+)\) \| (?P<message_lenght>\d+) lines?", line_of_informations)
        if informations is None:
            logging.getLogger().warning('Cannot get usefull information')
            return False

        informations = informations.groupdict()
        self._author = informations['author']
        message_lenght = int(informations['message_lenght'])
        self._modified_files = commit_data[2:-(message_lenght + 1)]
        self._message = '\n'.join(commit_data[-message_lenght:])
        self._date1 = informations['date1']
        self._date2 = informations['date2']

        self._branch = None
        if len(self._modified_files) > 0:
            modified_file = self._modified_files[0]
            informations = re.search('\s+\w+\s+(?P<path>.*)', modified_file)
            if informations is not None:
                informations = informations.groupdict()
                path = informations['path']
                if path.startswith('/trunk/'):
                    self._branch = 'trunk'
                elif path.startswith('/branches/'):
                    self._branch = 'branches/' + path.split('/')[2]
                elif path.startswith('/tags/'):
                    self._branch = 'tags/' + path.split('/')[2]

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

    def get_branch(self):
        """
        @return str Branch
        """
        return self._branch

    def get_date1(self):
        """
        @return str Date
        """
        return self._date1


def send_commit_by_mail(config, commit):
    logging.getLogger().info('sending mail...')

    sender = config.get('Mail', 'from')
    recipients = config.get('Mail', 'to')
    server = config.get('Mail', 'server')
    port = config.getint('Mail', 'port')
    use_ssl = config.getboolean('Mail', 'ssl')
    use_authentification = config.getboolean('Mail', 'use_authentification')
    login = config.get('Mail', 'login')
    password = config.get('Mail', 'password')

    message = MIMEText('Repository: %s\nBranch: %s\nRevision: %s\nAuthor: %s\nDate: %s\n\n%s\n\nModified files:\n%s' % (
        config.get('Repository', 'url'),
        commit.get_branch(),
        commit.get_revision(),
        commit.get_author(),
        commit.get_date1(),
        commit.get_message(),
        '\n'.join(commit.get_modified_files())
    ))

    message['Subject'] = '[SVN][%s] %s | %s | %s | %s' % (
        config.get('Repository', 'name'),
        commit.get_revision(),
        commit.get_author(),
        ' '.join(commit.get_date1().split()[0:2]),
        commit.get_branch(),
    )
    message['From'] = sender
    message['To'] = recipients

    if use_ssl:
        SMTP_class = smtplib.SMTP_SSL
    else:
        SMTP_class = smtplib.SMTP

    s = SMTP_class(server, port)
    if use_authentification:
        s.login(login, password)
    s.sendmail(sender, recipients.split(','), message.as_string())
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
