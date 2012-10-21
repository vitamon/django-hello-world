import os
import uuid
from django.core import urlresolvers
import settings

def unique_filename(filename):
    file_ext = filename[filename.rfind('.'):].lower()
    return '%s%s' % (str(uuid.uuid1()), file_ext)


def admin_page_url(item):
    return urlresolvers.reverse('admin:%s_%s_change' % (
        item._meta.app_label,
        item._meta.module_name, )
        , args=(item.id,))


def upload_path(filename):
    return os.path.join(settings.MEDIA_ROOT, filename)


def handle_uploaded_file(f, filename):
    destination = open(upload_path(filename), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)