from func import clean, download_file, shuffle_language_file, log, shuffle_normal_file, input_log, error
import json, os
import shutil
import time
import zipfile

tempdir = "./"
start_time = time.time()
has_mod = ""
has_resourcepack = ""
is_lang = False

try:
    log("初始化中...", True)
    log("语言打乱器，版本v0.1")
    download_file("https://piston-meta.mojang.com/mc/game/version_manifest.json", tempdir + "/temp.json")
    version = input_log("请输入MC版本：")
    while True:
        has_mod = input_log("是否包含mod？(y/n)")
        has_resourcepack = input_log("是否包含资源包？(y/n)")
        if has_mod == "y" or has_mod == "n":
            if has_resourcepack == "y" or has_resourcepack == "n":
                break
        else:
            log("请输入y或n！")
    if has_mod == "y":
        if not os.path.exists(tempdir + "/mods"):
            os.mkdir(tempdir + "/mods")
    if has_resourcepack == "y":
        if not os.path.exists(tempdir + "/czb"):
            os.mkdir(tempdir + "/czb")
    log("读取用户输入版本")
    log("读取成功")
    passed = False
    log("开始检查版本是否存在")
    with open(tempdir + "/temp.json", "r") as f:
        data = json.load(f)
    for i in data["versions"]:
        if i["id"] == version:
            passed = True
            break
    if not passed:
        log("版本不存在，请重新输入")
        log("按任意键退出")
        os.system('pause > nul')
        exit()
    log("版本存在，开始生成")
    for version_info in data["versions"]:
        if version_info["id"] == version:
            log("下载版本信息")
            download_file(version_info["url"], tempdir + "/temp2.json")
    with open(tempdir + "/temp2.json", "r") as f:
        data = json.load(f)
    log("获取资源文件索引")
    download_file(data["assetIndex"]["url"], tempdir + "/temp3.json")
    with open(tempdir + "/temp3.json", "r") as f:
        data = json.load(f)
    lang_file_key = "minecraft/lang/zh_cn.json"
    hash_str = ""
    log("获取完毕")
    log("获取语言文件哈希")
    if lang_file_key not in data["objects"]:
        hash_str = data["objects"]["minecraft/lang/zh_cn.lang"]["hash"]
    else:
        hash_str = data["objects"]["minecraft/lang/zh_cn.json"]["hash"]
    url = "https://resources.download.minecraft.net/" + hash_str[:2] + "/" + hash_str
    log("获取完毕")
    log("下载语言文件")
    if "w" in version:
        if int(version[:2]) > 18:
            download_file(url, tempdir + "/temp4.json")
            is_lang = False
        elif int(version[:2]) == 18:
            if int(version[3:5]) >= 2:
                download_file(url, tempdir + "/temp4.json")
                is_lang = False
            else:
                download_file(url, tempdir + "/temp4.lang")
                is_lang = True
        else:
            download_file(url, tempdir + "/temp4.lang")
            is_lang = True
    else:
        if version < "1.13":
            download_file(url, tempdir + "/temp4.lang")
            is_lang = True
        else:
            download_file(url, tempdir + "/temp4.json")
            is_lang = False
    if is_lang:
        with open(tempdir + "/temp4.lang", "r", encoding="utf-8") as f:
            log("开始打包材质包")
            if not os.path.exists("pack"):
                log("创建材质包文件夹")
                os.makedirs("pack")
                log("创建成功")
            with open(tempdir + "/temp2.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            log("下载客户端文件")
            download_file(data["downloads"]["client"]["url"], "client.zip")
            log("解压客户端文件到mc文件夹")
            with zipfile.ZipFile("client.zip", 'r') as zip_ref:
                zip_ref.extractall("mc")
            log("解压完成")
            has_mcmeta = False
            if os.path.exists("mc/version.json"):
                shutil.move("mc/version.json", "version.json")
                log("移动version.json至程序根目录")
                has_mcmeta = False
            elif os.path.exists("mc/pack.mcmeta"):
                shutil.move("mc/pack.mcmeta", "pack.mcmeta")
                log("移动pack.mcmeta至程序根目录")
                has_mcmeta = True
            log("删除客户端文件")
            shutil.rmtree("mc")
            os.remove("client.zip")
            log("删除完毕")
    else:
        not_first = True
        shuffle_language_file(tempdir + "/temp4.json", "temp5.json", "pack/assets/minecraft/lang/zh_cn.json", not_first, tempdir, has_mod, has_resourcepack)
        not_first = False
        log("开始打包材质包")
        pack_version = 0
        if not os.path.exists("pack"):
            log("创建材质包文件夹")
            os.makedirs("pack")
            log("创建成功")
        with open(tempdir + "/temp2.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        log("下载客户端文件")
        download_file(data["downloads"]["client"]["url"], "client.zip")
        log("解压客户端文件到mc文件夹")
        with zipfile.ZipFile("client.zip", 'r') as zip_ref:
            zip_ref.extractall("mc")
        log("解压完成")
        has_mcmeta = False
        if os.path.exists("mc/version.json"):
            shutil.move("mc/version.json", "version.json")
            log("移动version.json至程序根目录")
            has_mcmeta = False
        elif os.path.exists("mc/pack.mcmeta"):
            shutil.move("mc/pack.mcmeta", "pack.mcmeta")
            log("移动pack.mcmeta至程序根目录")
            has_mcmeta = True
        if os.path.exists("mc/assets/minecraft/texts"):
            if not os.path.exists("texts"):
                os.mkdir("texts")
            log("移动text文件夹至程序根目录")
            for file in os.listdir("mc/assets/minecraft/texts"):
                shutil.move("mc/assets/minecraft/texts/"+file, "texts")
        log("删除客户端文件")
        shutil.rmtree("mc")
        os.remove("client.zip")
        log("删除完毕")
        log("读取版本对应材质包版本")
        with open("version.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        pack_version = data["pack_version"]["resource"]
        log("读取完成，材质包版本为" + str(pack_version))
        log("开始创建材质包结构")
        if not os.path.exists("pack/assets"):
            os.makedirs("pack/assets")
        if not os.path.exists("pack/assets/minecraft"):
            os.makedirs("pack/assets/minecraft")
        if not os.path.exists("pack/assets/minecraft/lang"):
            os.makedirs("pack/assets/minecraft/lang")
        if not os.path.exists("pack/assets/minecraft/texts"):
            os.makedirs("pack/assets/minecraft/texts")
        log("创建完成")
        run_dir = os.path.dirname(os.path.abspath(__file__))
        log("打乱原版终末之诗等内容")
        i = 6
        for file in os.listdir("texts"):
            if not file.endswith(".json"):
                origin_path = "pack/assets/minecraft/texts/" + file
                shuffle_normal_file(run_dir + "\\texts\\" + file, file, origin_path, not_first, tempdir, has_mod, has_resourcepack)
        log("打乱完成")
        log("写入mcmeta")
        with open("pack/pack.mcmeta", "w", encoding="utf-8") as f:
            f.write(
                '{"pack":{"pack_format":' + str(pack_version) + ',"description":"文本打乱材质包\\n使用python自动生成"}}')
        log("写入完成")
        log(run_dir)
        if has_mod == "y":
            if not os.path.exists("mods"):
                os.makedirs("mods")
            log("请将mod文件放到mods文件夹内，按任意键继续")
            input()
            log("开始混淆mod，请确保mod内有中文的语言文件，如果没有则会跳过")
            for file in os.listdir("mods"):
                if file.endswith(".jar"):
                    log("开始混淆" + file)
                    os.chdir(run_dir + "\\mods")
                    with zipfile.ZipFile("./" + file, 'r') as zip_ref:
                        zip_ref.extractall("temp")
                        if os.path.exists("temp/assets"):
                            os.chdir(run_dir + "\\mods\\temp\\assets")
                            for folder in os.listdir():
                                folder_name = folder
                                if folder_name != "fabric":
                                    if os.path.isdir(run_dir + "\\mods\\temp\\assets\\" + folder):
                                        os.chdir(run_dir + "\\mods\\temp\\assets\\" + folder)
                                        if os.path.exists("lang"):
                                            os.chdir(run_dir + "\\mods\\temp\\assets\\" + folder + "\\lang")
                                            for fila in os.listdir():
                                                if fila == "zh_cn.json":
                                                    origin_path = "pack/assets/" + folder_name + "/lang/" + fila
                                                    shuffle_language_file(
                                                        run_dir + "\\mods\\temp\\assets\\" + folder + "\\lang\\" + fila,
                                                        "temp" + str(i) + ".json", origin_path, not_first, tempdir, has_mod, has_resourcepack)
                                                    i += 1
                                                    os.chdir(run_dir)
                                                elif fila == "zh_CN.json":
                                                    origin_path = "pack/assets/" + folder_name + "/lang/" + fila
                                                    shuffle_language_file(
                                                        run_dir + "\\mods\\temp\\assets\\" + folder + "\\lang\\" + fila,
                                                        "temp" + str(i) + ".json", origin_path, not_first, tempdir, has_mod, has_resourcepack)
                                                    i += 1
                                                    os.chdir(run_dir)
                                                else:
                                                    os.remove(run_dir + "\\mods\\temp\\assets\\" + folder + "\\lang\\" + fila)
                                                    os.chdir(run_dir)
                                                    log(fila+"不是中文语言文件，跳过")
                    try:
                        os.chdir(run_dir)
                        os.access(run_dir + "\\mods\\temp", os.W_OK)
                        shutil.rmtree(run_dir + "\\mods\\temp")
                    except PermissionError:
                        log("无法删除temp文件夹，请手动删除")
                        log("删除后按任意键继续")
                        os.system("explorer "+run_dir+"\\mods\\temp")
                        input()
            log("混淆完成")
        else:
            log("不包含mod，跳过")
        if has_resourcepack == "y":
            if not os.path.exists("czb"):
                os.makedirs("czb")
            log("请将材质包文件放到czb文件夹内（需为zip压缩包），按任意键继续")
            input()
            log("开始混淆资源包，请确保资源包内有正确的语言文件")
            for file in os.listdir("czb"):
                if file.endswith(".zip"):
                    log("开始混淆" + file)
                    os.chdir(run_dir + "\\czb")
                    with zipfile.ZipFile("./" + file, 'r') as zip_ref:
                        zip_ref.extractall("temp")
                        if os.path.exists("temp/assets"):
                            os.chdir(run_dir + "\\czb\\temp\\assets")
                            for folder in os.listdir():
                                folder_name = folder
                                if folder_name != "fabric":
                                    if os.path.isdir(run_dir + "\\czb\\temp\\assets\\" + folder):
                                        os.chdir(run_dir + "\\czb\\temp\\assets\\" + folder)
                                        if os.path.exists("lang"):
                                            os.chdir(run_dir + "\\czb\\temp\\assets\\" + folder + "\\lang")
                                            for fila in os.listdir():
                                                if fila == "zh_cn.json":
                                                    origin_path = "pack/assets/" + folder_name + "/lang/" + fila
                                                    shuffle_language_file(
                                                        run_dir + "\\czb\\temp\\assets\\" + folder + "\\lang\\" + fila,
                                                        "temp" + str(i) + ".json", origin_path, not_first, tempdir, has_mod, has_resourcepack)
                                                    i += 1
                                                    os.chdir(run_dir)
                                                elif fila == "zh_CN.json":
                                                    origin_path = "pack/assets/" + folder_name + "/lang/" + fila
                                                    shuffle_language_file(
                                                        run_dir + "\\czb\\temp\\assets\\" + folder + "\\lang\\" + fila,
                                                        "temp" + str(i) + ".json", origin_path, not_first, tempdir, has_mod, has_resourcepack)
                                                    i += 1
                                                    os.chdir(run_dir)
                                                else:
                                                    os.remove(run_dir + "\\czb\\temp\\assets\\" + folder + "\\lang\\" + fila)
                                                    os.chdir(run_dir)
                                                    log(fila+"不是中文语言文件，跳过")
                    try:
                        os.chdir(run_dir)
                        os.access(run_dir + "\\czb\\temp", os.W_OK)
                        shutil.rmtree(run_dir + "\\czb\\temp")
                    except PermissionError:
                        log("无法删除temp文件夹，请手动删除")
                        log("删除后按任意键继续")
                        os.system("explorer "+run_dir+"\\czb\\temp")
                        input()
            log("混淆完成")
        else:
            log("不包含资源包，跳过")
        log("复制语言文件")
        with open(tempdir + "/files.json", "r", encoding="utf-8") as f:
            data = f.read().rstrip(",\n")
        with open(tempdir + "/files.json", "w", encoding="utf-8") as f:
            f.write(data)
        with open(tempdir + "/files.json", "a", encoding="utf-8") as f:
            f.write("}")
        with open(tempdir + "/files.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            skip = False
            log("复制"+key+"到"+value)
            folder_name = ""
            path = ""
            if value[-11:] == "/zh_cn.json":
                path = value[:-11]
                folder_name = value[:-16]
            elif value[-8:] == "/end.txt":
                path = value[:-8]
                folder_name = value[:-14]
            elif value[-16:] == "/postcredits.txt":
                path = value[:-16]
                folder_name = value[:-22]
            elif value[-13:] == "/splashes.txt":
                path = value[:-13]
                folder_name = value[:-19]
            else:
                log("未知文件，跳过")
                skip = True
            if not skip:
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                    log("创建文件夹"+folder_name)
                if not os.path.isdir(path):
                    os.mkdir(path)
                    log("创建文件夹"+path)
                shutil.copy(key, value)
        log("复制完成")
        log("开始打包为zip")
        shutil.make_archive("文本打乱材质包", "zip", "pack")
        log("打包完成")
    clean(tempdir, is_lang, has_mod, has_resourcepack)
    use_time = time.time() - start_time
    log("生成成功！用时" + str(int(use_time)) + "秒")
    log("按任意键退出")
    input()
    exit()
except Exception as e:
    error("发生错误：" + str(e))
    clean(tempdir, is_lang, has_mod, has_resourcepack)
    use_time = time.time() - start_time
    log("生成失败！用时" + str(int(use_time)) + "秒")
    log("建议将日志发送至作者来修复bug")
    log("按任意键退出")
    input()
    exit(1)
except KeyboardInterrupt:
    log("用户取消操作")
    clean(tempdir, is_lang, has_mod, has_resourcepack)
    use_time = time.time() - start_time
    log("生成失败！用时" + str(int(use_time)) + "秒")
    log("按任意键退出")
    input()
    exit(2)