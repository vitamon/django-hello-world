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


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)