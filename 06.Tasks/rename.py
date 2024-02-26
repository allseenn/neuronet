import os
import shutil

def rename_folders(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if directory.startswith('Tile '):
                old_name = os.path.join(root, directory)
                new_name = os.path.join(root, 't' + directory.split('Tile ')[1])
                os.rename(old_name, new_name)


def rename_files1(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if directory.startswith('t'):
                images_dir = os.path.join(root, directory, 'images')
                if os.path.exists(images_dir):
                    for filename in os.listdir(images_dir):
                        if len(filename) > 3:
                            new_filename = filename[-7:]  # Оставляем только 3 последних символа + расширение
                            old_path = os.path.join(images_dir, filename)
                            new_path = os.path.join(images_dir, new_filename)
                            os.rename(old_path, new_path)


def rename_files2(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if directory.startswith('t'):
                images_dir = os.path.join(root, directory, 'masks')
                if os.path.exists(images_dir):
                    for filename in os.listdir(images_dir):
                        if len(filename) > 3:
                            new_filename = filename[-7:]  # Оставляем только 3 последних символа + расширение
                            old_path = os.path.join(images_dir, filename)
                            new_path = os.path.join(images_dir, new_filename)
                            os.rename(old_path, new_path)


def rename_files3(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if directory.startswith('t'):
                images_dir = os.path.join(root, directory, 'images')
                if os.path.exists(images_dir):
                    prefix = 'image_' + directory  # Префикс для переименования
                    for filename in os.listdir(images_dir):
                        old_path = os.path.join(images_dir, filename)
                        new_filename = prefix + '_' + filename  # Новое имя файла с префиксом
                        new_path = os.path.join(images_dir, new_filename)
                        os.rename(old_path, new_path)


def rename_files4(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for directory in dirs:
            if directory.startswith('t'):
                images_dir = os.path.join(root, directory, 'masks')
                if os.path.exists(images_dir):
                    prefix = 'image_' + directory  # Префикс для переименования
                    for filename in os.listdir(images_dir):
                        old_path = os.path.join(images_dir, filename)
                        new_filename = prefix + '_' + filename  # Новое имя файла с префиксом
                        new_path = os.path.join(images_dir, new_filename)
                        os.rename(old_path, new_path)


def move_files(root_dir):
    train_images_dir = os.path.join(root_dir, 'train_images')
    train_masks_dir = os.path.join(root_dir, 'train_masks')

    # Создаем директории train_images и train_masks, если они не существуют
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_masks_dir, exist_ok=True)

    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.jpg'):
                src_path = os.path.join(root, filename)
                dst_path = os.path.join(train_images_dir, filename)
                shutil.move(src_path, dst_path)
            elif filename.endswith('.png'):
                src_path = os.path.join(root, filename)
                dst_path = os.path.join(train_masks_dir, filename)
                shutil.move(src_path, dst_path)


if __name__ == "__main__":
    root_directory = 'dubai-aerial-imagery-dataset'
    rename_folders(root_directory)
    rename_files1(root_directory)
    rename_files2(root_directory)
    rename_files3(root_directory)
    rename_files4(root_directory)
    move_files(root_directory)

