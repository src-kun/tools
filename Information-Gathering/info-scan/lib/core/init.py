
#检测masscan report 文件夹 不存在则创建
chk_dir(masscan_report_path)
#检查map文件 不存在则创建
chk_file(masscan_report_map_path)
map_handle = write(masscan_report_map_path)
print map_handle