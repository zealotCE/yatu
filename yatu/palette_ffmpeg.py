import argparse, os, sys, traceback, re, subprocess, time

# paraser setting
parser = argparse.ArgumentParser(
    prog = 'palette', add_help = False
)
parser.add_argument(
    '-h', action = 'help',
    help = 'show this help message and exit'
)
parser.add_argument(
    'input', metavar = 'input', nargs = '*', default = ['.'],
    help = 'png image file or folder path'
)
# store_true means if users  use -d , args.delete = True, else args.delete = False 
parser.add_argument(
    '-d', dest= 'delete', action= 'store_true',
    help = 'delete source after conversion'
)
parser.add_argument(
    '-o', metavar = 'output', dest = 'output',
    help = 'customize saving folder'
)


def validate_name(name):
    pattern = {u'\\': u'＼', u'/': u'／', u':': u'：', u'*': u'＊', u'?': u'？', u'"': u'＂', u'<': u'＜', u'>': u'＞', u'|': u'｜'}
    for character in pattern:
        name = name.replace(character, pattern[character])
    return name

def validate_collision(path):
    index = 1
    origin = path
    while os.path.exists(path):
        path = '_{}'.format(index).join(os.path.splitext(origin))
        index += 1
    return path

def name_format(path):
    name = os.path.splitext(os.path.split(path)[1])[0]
    name = validate_name(name)
    # name += '.' + meta['format']
    name += '.png'
    folder = args.output if args.output else os.path.dirname(path)
    save = os.path.join(folder, name)
    # if args.rename: save = validate_collision(save)
    save = validate_collision(save)
    return save

# gets the path to the specified format
def traverse(path,format= '.png'):
    # print('input: {}'.format(path))
    path = os.path.abspath(path)
    if not os.path.exists(path):
        # print("step1")
        return []
    elif os.path.isdir(path):
        #print("step2")
        return sum([traverse(os.path.join(path, name)) for name in os.listdir(path)], [])

    else:
        #print("step3")
        return [path] if os.path.splitext(path)[-1] == format else []



def compression_png(source, palette, output,max_colors=256, ffmpegPath):
    
    ffmpegPalette = ffmpegPath + ' -i {} -hide_banner -vf palettegen=max_colors={}:stats_mode=single -y {}'.format(source,max_colors,palette)
    ffmpegImageCompression = ffmpegPath + ' -i {} -i {} -hide_banner -lavfi "[0][1:v] paletteuse" -pix_fmt pal8 -y {}'.format(source,palette,output)
    # use capture_out= True to make ffmpeg output don't display
    subprocess.run(["powershell", ffmpegPalette], capture_output= True)
    subprocess.run(["powershell", ffmpegImageCompression], capture_output= True)
    # subprocess.run(["powershell", palette])
    os.remove(palette)
    return output

def main():
    
    if args.output:
        args.output = os.path.abspath(args.output)
    if args.output == None:
        # if not set output dir ，output = input
        args.output = os.getcwd()
        print('unspecified, default output path: {}'.format(args.output))
        # args.output = os.path.split(args)
    if not os.path.exists(args.output):
        print('output does not exist')
        exit()
    if not os.path.isdir(args.output):
        print('output is not a folder')
        exit()

    # initialization 
    # ffmpegPath = r'c:\Users\gygoo\OneDrive\software\media_tool\bin\ffmpeg.exe'
    ffmpegPath = r'.\ffmpeg\bin\ffmpeg.exe'
    args = parser.parse_args()
    # support image format png only
    img_format = '.png'
    

    # get path of source, palette, output
    input_files = sum([traverse(path, format= img_format) for path in args.input], [])
    files = sorted(set(input_files), key = input_files.index)
    palette_files = [validate_collision('_palette_ffmpeg'.join(os.path.splitext(path))) for path in files]
    output_files = [validate_collision('_ffmpeg'.join(os.path.splitext(os.path.join(args.output, os.path.split(path)[1])))) for path in files]
    source_palettes_ouput = zip(files, palette_files, output_files)
    
    
    # gogogo
    for source, palette, output in source_palettes_ouput:
        # print('*'*20)
        try:
            save= compression_png(source, palette, output,ffmpegPath)
            # save = dump(path, name_format, not args.cover)
            now_time_str = time.strftime('%H:%M:%S', time.localtime())
            # print('saving')
            if save: print('{}: saving {} '.format(now_time_str, os.path.split(save)[-1]))
            if args.delete: os.remove(source)
        except KeyboardInterrupt:
            exit()
        except:
            print(traceback.format_exc())
            
if __name__ == '__main__':
    main()