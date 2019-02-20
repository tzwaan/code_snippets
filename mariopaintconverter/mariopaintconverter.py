import xml.etree.ElementTree as ET
from argparse import ArgumentParser
import sys
import re


notebook = dict(zip(['+', '-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'],
                    ['#', 'b', 'A2', 'B2', 'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']))

instrumentbook = dict(zip(['mario', 'toad', 'yoshi', 'star', 'flower', 'gameboy', 'dog', 'cat', 'pig', 'swan', 'face', 'plane', 'boat', 'car', 'heart', 'coin', 'plant', 'shyguy', 'ghost'],
                          ['MARIO', 'MUSHROOM', 'YOSHI', 'STAR', 'FLOWER', 'GAMEBOY', 'DOG', 'CAT', 'PIG', 'SWAN', 'FACE', 'PLANE', 'BOAT', 'CAR', 'HEART', 'COIN', 'PIRANHA', 'SHYGUY', 'BOO']))


def convert_from_file(input_filename, output_filename):
    tree = ET.parse(input_filename)
    root = tree.getroot()
    with open(output_filename, "w") as sys.stdout:

        print("TEMPO: {}, EXT: 0, TIME: {}/4, SOUNDSET: {}".format(root.attrib['tempo'], root.attrib['measure'], root.attrib['soundfont']))

        measure = int(root.attrib['measure'])

        for i, chord in enumerate(root):
            m = i // measure + 1
            b = i % measure
            if len(chord) is 0:
                continue
            print("{}:{},".format(m, b), end='')
            for instrument in chord:
                if instrument.tag == "bookmark" or instrument.tag == "speedmark":
                    continue
                if instrument.tag[0] == 'x':
                    name = instrumentbook[instrument.tag[1:]]
                    mute = "m1"
                else:
                    name = instrumentbook[instrument.tag]
                    mute = ""
                notes = re.findall(r'([\+|\-]?[a-zA-z])', instrument.text)
                for note in notes:
                    if len(note) > 1:
                        print('{} {}{}{},'.format(name, notebook[note[1]], notebook[note[0]], mute), end='')
                    else:
                        print('{} {}{},'.format(name, notebook[note], mute), end='')
            print('VOL: {}'.format(int(chord.attrib['volume']) * 8))


if __name__ == "__main__":
    from os import listdir
    from os.path import isfile, join
    parser = ArgumentParser(description="Convert a mario paint sequencer song to a super mario paint song.")
    parser.add_argument("-f", "--file", dest="filename", help="The file from which to read the mario paint sequencer song", metavar="FILE")
    parser.add_argument("-o", "--output", dest="output", help="The file to which to write the super mario paint song", metavar="FILE")
    parser.add_argument("-d", "--directory", dest="dir", help="Directory of files which to convert.", metavar="DIR", default="songs")
    parser.add_argument("-od", "--output-directory", dest="odir", help="Directory to write the results to.", metavar="DIR", default="output")

    args = parser.parse_args()

    if args.filename is None:
        files = [f for f in listdir(args.dir) if isfile(join(args.dir, f))]
        for f in files:
            if f[-3:] == 'mss':
                newfilename = f[:-3] + 'txt'
                # print("Converting {} to {}".format(f, newfilename))
                convert_from_file(join(args.dir, f), join(args.odir, newfilename))

    else:
        if args.output is None:
            newfilename = args.filename[:-3] + 'output.txt'
        else:
            newfilename = args.output

        convert_from_file(args.filename, newfilename)
