import os


def count_hard_linked_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for file_name in files:
            file = os.path.join(root, file_name)
            nlink = os.stat(file).st_nlink
            if nlink > 1:
                count += 1

            print("File:", file, "\033[33;1;32mWith\033[0m hardlink" if nlink > 1 else "\033[33;1;31mWithout\033[0m hardlink")
    return count


# 示例路径
directory_path = r'C:\Projects'
print(count_hard_linked_files(directory_path))
