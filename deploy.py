import os
import shutil

SOURCE_FOLDER = 'D:\\Projects\\outlook2tracker'
TARGET_FOLDER = 'C:\\Users\\UseR\\Downloads\\Temp deploy'

IGNORE_FOLDERS = ['.git', '.idea', 'docker', '__pycache__']


if __name__ == '__main__':
    print("start")
    for dp, dn, filenames in os.walk(SOURCE_FOLDER):
        success = True
        for ignore in IGNORE_FOLDERS:
            if ignore in dp:
                success = False
        if not success:
            continue

        for f in filenames:
            source_full_path = os.path.join(dp, f)
            target_path = dp.replace(SOURCE_FOLDER, TARGET_FOLDER)
            target_full_path = os.path.join(target_path, f)
            isExist = os.path.exists(target_path)
            if not isExist:
                os.makedirs(target_path)

            shutil.copy(source_full_path, target_full_path)
    print("end")








