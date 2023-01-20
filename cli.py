import sys
import configparser as cpr
import getopt as gopt
import stock_framework as sf


def usage_s():
    print("Shares_tkchart Help")
    print("recommand use python3.9")
    print("useage:")
    print("python cli.py -opt[--option]")
    print("python cli.py -v[--version] 查看版本号")
    print("python cli.py -h[--help] 查看本帮助")
    print("------------------------------------------------")
    print("python cli.py -i[--init] 初始化csv文件的数据数据位置")
    print("位置从0开始选取")
    print("------------------------------------------------")
    print("python cli.py -f[--file] your_csv_file 绘制快照")


def cli_ui():
    opts, args = gopt.getopt(
        sys.argv[1:], "-i-v-h-f:", ["--init", "version", "help", "file="])
    if opts == []:
        print('Welcome to Shares_tkchart')
    for o1, o2 in opts:
        if o1 in ('-v', '--version'):
            print("Shares_tkchart 0.0.1 beta")
        if o1 in ('-h', "--help"):
            usage_s()
        if o1 in ('-f', "--file"):
            sf.technic_chart_matplotlib(csv_path=o2)
        if o1 in ('-i', "--init"):
            config = cpr.ConfigParser()
            config.read('config.ini', encoding='utf-8')
            print('现在的配置: ')
            print(config.items('csv_data_column'))
            print('请开始修改, 若没有指定列, 则直接回车')
            for item in config.items('csv_data_column'):
                print(item, end='-->')
                config.set('csv_data_column', item[0], input())
                config.write(open('config.ini', 'w'))
            print('现在的配置')
            print(config.items('csv_data_column'))


if __name__ == '__main__':
    cli_ui()
