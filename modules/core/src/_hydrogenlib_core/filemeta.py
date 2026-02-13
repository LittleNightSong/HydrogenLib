import os


class FileStatus:
    def __init__(self, fstat: os.stat_result):
        self.fstat = fstat

    @property
    def birthday(self):
        """
        创建时间
        """
        # 注意：st_birthtime在某些平台上可能不可用
        try:
            return self.fstat.st_birthtime
        except AttributeError:
            return None

    @property
    def last_access(self):
        """
        最后访问时间
        """
        return self.fstat.st_atime

    @property
    def last_modified(self):
        """
        最后修改时间
        """
        return self.fstat.st_mtime

    @property
    def size(self):
        """
        文件大小
        """
        return self.fstat.st_size

    @property
    def mode(self):
        """
        文件权限
        """
        return self.fstat.st_mode

    @property
    def inode(self):
        """
        文件ID
        """
        return self.fstat.st_ino

    @property
    def device(self):
        """
        文件设备
        """
        return self.fstat.st_dev

    @property
    def nlink(self):
        """
        链接数
        """
        return self.fstat.st_nlink

    @property
    def uid(self):
        """
        用户ID
        """
        return self.fstat.st_uid

    @property
    def gid(self):
        """
        组ID
        """
        return self.fstat.st_gid
