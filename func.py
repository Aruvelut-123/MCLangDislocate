import datetime
import json
import os
import random
import shutil

import requests

def input_log(text):
    result = input("[INFO] " + text)
    tempdir = "./"
    with open(tempdir + "/logs/latest.txt", "a", encoding="utf-8") as f:
        f.write("[INFO] " + text + "\n")
        f.write("[INFO] 获取到用户输入: " + result + "\n")
    return result

def error(text):
    #输出红色的文字
    print("\033[31m[ERROR] " + text + "\033[0m")
    tempdir = "./"
    if os.path.exists(tempdir + "/logs/latest.txt"):
        with open(tempdir + "/logs/latest.txt", "a", encoding="utf-8") as f:
            f.write("[ERROR] " + text + "\n")

def log(text, frisk=False):
    print("[INFO] " + text)
    tempdir = "./"
    if frisk:
        if not os.path.exists(tempdir + "/logs"):
            os.mkdir(tempdir + "/logs")
        if os.path.exists(tempdir + "/logs/latest.txt"):
            with open(tempdir + "/logs/latest.txt", "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
            if os.path.exists(tempdir + "/logs/" + first_line + ".txt"):
                os.rename(tempdir + "/logs/latest.txt", tempdir + "/logs/" + first_line + "-copied.txt")
            else:
                os.rename(tempdir + "/logs/latest.txt", tempdir + "/logs/" + first_line + ".txt")
        with open(tempdir + "/logs/latest.txt", "w", encoding="utf-8") as f:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d-%H-%M-%S-%M')
            f.write(formatted_time+ "\n")
            f.write("[INFO] " + text + "\n")
    else:
        with open(tempdir + "/logs/latest.txt", "a", encoding="utf-8") as f:
            f.write("[INFO] " + text + "\n")


def download_file(url, file_path):
    log("开始从 " + url + " 下载文件到 " + file_path)
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    log("下载完成")

def shuffle_normal_file(file, filename, origin, first, tempdir, has_mod, has_resourcepack):
    log("开始打乱文件"+filename)
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    shuffled_lines = []
    for line in lines:
        line = line.rstrip('\n')
        shuffled_line = ''.join(random.sample(line, len(line)))
        shuffled_lines.append(shuffled_line + '\n')
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(shuffled_lines)
    with open(file, "r", encoding="utf-8") as f:
        values = f.readlines()
    random.shuffle(values)
    with open(file, "w", encoding="utf-8") as f:
        f.writelines(values)
    if filename == "splashes.txt":
        with open(file, "a", encoding="utf-8") as f:
            f.write("全部打乱！")
    log("写出打乱文件对应源文件路径")
    fila = str(file).replace("\\", "\\\\")
    if has_mod == 'y':
        if first:
            with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
                f.write("{\n")
                f.write('"' + fila + '": "' + origin + '",\n')
        else:
            with open(tempdir + "/files.json", "a", encoding="utf-8") as f:
                f.write('"' + fila + '": "' + origin + '",\n')
    elif has_resourcepack == 'y':
        if first:
            with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
                f.write("{\n")
                f.write('"' + fila + '": "' + origin + '",\n')
        else:
            with open(tempdir + "/files.json", "a", encoding="utf-8") as f:
                f.write('"' + fila + '": "' + origin + '",\n')
    else:
        with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
            f.write("{\n")
            f.write('"' + file + '": "' + origin + '"\n')
    log("打乱完毕")

def shuffle_language_file(file, out, origin, first, tempdir, has_mod, has_resourcepack):
    with open(file, "r", encoding="utf-8") as f:
        log("分解语言文件")
        data = json.load(f)
        with open(tempdir + "/keys.txt", "w", encoding="utf-8") as f:
            for key in data:
                f.write(key + "\n")
        with open(tempdir + "/values.txt", "w", encoding="utf-8") as f:
            for key in data:
                f.write(data[key] + "\n")
        log("分解完成")
        log("打乱语言文件")
        with open(tempdir + "/values.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        shuffled_lines = []
        for line in lines:
            line = line.rstrip('\n')
            shuffled_line = ''.join(random.sample(line, len(line)))
            shuffled_lines.append(shuffled_line + '\n')
        with open(tempdir + "/values.txt", 'w', encoding='utf-8') as file:
            file.writelines(shuffled_lines)
        with open(tempdir + "/values.txt", "r", encoding="utf-8") as f:
            values = f.readlines()
        random.shuffle(values)
        with open(tempdir + "/values.txt", "w", encoding="utf-8") as f:
            f.writelines(values)
        with open(tempdir + "/values.txt", "r", encoding="utf-8") as f:
            values = f.readlines()
        with open(tempdir + "/keys.txt", "r", encoding="utf-8") as f:
            keys = f.readlines()
        with open(out, "w", encoding="utf-8") as f:
            f.write("{\n")
            c = len(list(zip(keys, values)))
            d = 0
            for key, value in zip(keys, values):
                a = value.rstrip()
                b = a.replace('\\', '\\\\')
                if d == c - 1:
                    f.write(f'"{key.rstrip()}" : "{b}"' + '\n')
                else:
                    f.write(f'"{key.rstrip()}" : "{b}",' + '\n')
                d += 1
            f.write("}")
            log("写出打乱文件对应源文件路径")
            if has_mod == 'y':
                if first:
                    with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
                        f.write("{\n")
                        f.write('"' + out + '": "' + origin + '",\n')
                else:
                    with open(tempdir + "/files.json", "a", encoding="utf-8") as f:
                        f.write('"' + out + '": "' + origin + '",\n')
            elif has_resourcepack == 'y':
                if first:
                    with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
                        f.write("{\n")
                        f.write('"' + out + '": "' + origin + '",\n')
                else:
                    with open(tempdir + "/files.json", "a", encoding="utf-8") as f:
                        f.write('"' + out + '": "' + origin + '",\n')
            else:
                with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
                    f.write("{\n")
                    f.write('"' + out + '": "' + origin + '"\n')
        os.remove(tempdir + "/values.txt")
        os.remove(tempdir + "/keys.txt")
        log("打乱完毕")

def clean(tempdir, is_lang, has_mod, has_resourcepack):
    log("删除临时文件")
    if os.path.exists("pack"):
        shutil.rmtree("pack")
    if os.path.exists("texts"):
        shutil.rmtree("texts")
    for files in os.listdir(tempdir):
        if files.endswith(".json"):
            os.remove(tempdir + "/" + files)
        elif files.endswith(".lang"):
            os.remove(tempdir + "/" + files)
        elif files.endswith(".txt"):
            os.remove(tempdir + "/" + files)
    if has_mod == "y":
        while True:
            delete = input_log("是否删除mods文件夹？(y/n)")
            if delete == "y" or delete == "n":
                break
            else:
                log("请输入y或n")
                continue
        if os.path.exists(tempdir + "/mods") and delete == "y":
            shutil.rmtree(tempdir + "/mods")
    if has_resourcepack == "y":
        while True:
             delete = input_log("是否删除czb文件夹？(y/n)")
             if delete == "y" or delete == "n":
                 break
             else:
                 log("请输入y或n")
                 continue
        if os.path.exists(tempdir + "/czb") and delete == "y":
             shutil.rmtree(tempdir + "/czb")
    log("删除完毕")