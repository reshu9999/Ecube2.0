from resources.config_coordinator import config_fetcher


class SaveCachePage(object):

    FILE_PATH = config_fetcher.get_services_config['CACHE_PAGE']['MEDIA_FILE_PATH']
    SERVER_WEBSITE = config_fetcher.get_services_config['CACHE_PAGE']['SERVER_WEBSITE']

    def __init__(self, filename, filecontent):
        self.filename = filename
        self.filecontent = filecontent

    def send_to_cachepage(self, local_filepath, server_filename):
        port = 22
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        crawler_sftp = paramiko.SFTPClient.from_transport(transport)
        crawler_sftp.put(local_filepath, server_filename)

    def save_file(self):
        with open(self.FILE_PATH + self.filename, "w") as fileobject:
            fileobject.write(self.filecontent)
        cache_sftp = sftpOpration(c_server_name, c_username, c_password)

    @property
    def file_web_path(self):
        return self.SERVER_WEBSITE + self.filename
