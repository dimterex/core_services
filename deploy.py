import os
import shutil

SOURCE_FOLDER = 'D:\\Projects\\outlook2tracker'
TARGET_FOLDER = 'C:\\Users\\UseR\\Downloads\\Temp deploy'

SOURCE_PAGES = 'D:\\Projects\\web_host_application\\build'
TARGET_PAGES = os.path.join(TARGET_FOLDER, 'web_host', 'pages')

IGNORE_FOLDERS = ['.git', '.idea', 'docker', '__pycache__']


if __name__ == '__main__':
    print("start")

    for dp, dn, filenames in os.walk(SOURCE_FOLDER):
        success = True

        for ignore in IGNORE_FOLDERS:
            if ignore in dp:
                success = False
        if not success:

            # if ".git" not in dp:
            #     print(dp, dn)
            continue

        for f in filenames:
            source_full_path = os.path.join(dp, f)
            target_path = dp.replace(SOURCE_FOLDER, TARGET_FOLDER)
            target_full_path = os.path.join(target_path, f)
            isExist = os.path.exists(target_path)
            if not isExist:
                os.makedirs(target_path)

            shutil.copy(source_full_path, target_full_path)

    shutil.rmtree(TARGET_PAGES)
    shutil.copytree(SOURCE_PAGES, TARGET_PAGES, dirs_exist_ok=True)
    os.startfile(TARGET_FOLDER)
    print("end")








