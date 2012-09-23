import uuid

def unique_filename(filename):
    file_ext = filename[filename.rfind('.'):].lower()
    return '%s%s'%(str(uuid.uuid1()), file_ext)