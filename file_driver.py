import os

def take_latest_message(file):
    file_dir =  os.listdir(file)
    sorted_file = []
    for i in file_dir:
        i = i.split(".txt")
        sorted_file.append(int(i[0]))
    with open(file+"/"+str(max(sorted_file))+".txt", "r") as f:
        content = f.read()
        content_list = content.split(",")
        f.close()
    print(content_list)
    return content_list[0], content_list[-1]
while 1:
    take_latest_message("coordinate_file")
