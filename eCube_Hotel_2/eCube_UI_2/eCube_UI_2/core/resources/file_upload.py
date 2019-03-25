import os


class FileUploadBase(object):

    UPLOAD_TO = None
    DOWNLOAD_BASE = None
    STORAGE = None

    def __init__(self, file_obj, filename=None):
        self._object = file_obj
        self._filename = filename or str(file_obj)
        self._uploaded_path = None
        self._download_link = None

    def _save_file(self):
        fs = self.STORAGE(location=self.UPLOAD_TO)
        new_filename = fs.save(self._filename, self._object)
        self._uploaded_path = os.path.join(self.UPLOAD_TO, new_filename)
        self._download_link = self.DOWNLOAD_BASE + new_filename

    @property
    def uploaded_path(self):
        if self._uploaded_path:
            return self._uploaded_path

        self._save_file()
        return self.uploaded_path

    @property
    def download_link(self):
        if self._download_link:
            return self._download_link

        self._save_file()
        return self.download_link


class AjaxFileUploaderBase(object):

    FILE_UPLOAD = None

    def __init__(self, request):
        self._request = request
        self._uploads = list()

    def _process(self):
        self._uploads = [self.FILE_UPLOAD(file_obj) for input_name, file_obj in self._request.FILES.items()]

    @property
    def uploads(self):
        if self._uploads:
            return self._uploads

        self._process()
        return self._uploads

