#!/usr/bin/env python

from scipy.io import wavfile
import argparse
import pygame
import sys
import warnings
import pickle as pk
from time import sleep
from sound_lib import pitchshift


def parse_arguments():
    description = ('Use your computer keyboard as a "piano"')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--wav', '-w',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='bowl.wav',
        help='WAV file (default: bowl.wav)')
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='typewriter.kb',
        help='keyboard file (default: typewriter.kb)')
    parser.add_argument(
        '--input', '-i',
        metavar='FILE',
        type=str,
        default=None,
        help='file to play music from')
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='file to save music to')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='verbose mode')

    return (parser.parse_args(), parser)


def main():
    # Parse command line arguments
    (args, parser) = parse_arguments()

    # Enable warnings from scipy if requested
    if not args.verbose:
        warnings.simplefilter('ignore')

    fps, sound = wavfile.read(args.wav.name)

    tones = range(-25, 25)
    sys.stdout.write('Transponding sound file... ')
    sys.stdout.flush()
    transposed_sounds = [pitchshift(sound, n) for n in tones]
    print('DONE')

    # So flexible ;)
    pygame.mixer.init(fps, -16, 1, 2048)
    # For the focus
    pygame.display.set_mode((150, 150))

    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
    is_playing = {k: False for k in keys}

    if args.input:
        print(args.input)
        try:
            data = load_data(args.input)
        except IOError as e:
            print(e)
            quit()
        for events in data:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and\
                        event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise KeyboardInterrupt

            for key, event in events:
                if event == 0:
                    key_sound[key].play(fade_ms=50)
                    is_playing[key] = True
                else:
                    # Stops with 50ms fadeout
                    key_sound[key].fadeout(50)
                    is_playing[key] = False
                sleep(0.001)
    elif args.output:
        events = []
        while True:
            real_events = pygame.event.get()
            hm = []

            for event in real_events:
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    key = pygame.key.name(event.key)

                if event.type == pygame.KEYDOWN:
                    if (key in key_sound.keys()) and (not is_playing[key]):
                        key_sound[key].play(fade_ms=50)
                        is_playing[key] = True
                        hm.append([key, 0])

                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        with open(args.output, 'wb') as handle:
                            pk.dump(events, handle)
                        raise KeyboardInterrupt

                elif event.type == pygame.KEYUP and key in key_sound.keys():
                    # Stops with 50ms fadeout
                    key_sound[key].fadeout(50)
                    is_playing[key] = False
                    hm.append([key, 1])
            events.append(hm)
            sleep(0.001)
    else:
        while True:
            event = pygame.event.wait()

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                key = pygame.key.name(event.key)

            if event.type == pygame.KEYDOWN:
                if (key in key_sound.keys()) and (not is_playing[key]):
                    key_sound[key].play(fade_ms=50)
                    is_playing[key] = True

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise KeyboardInterrupt

            elif event.type == pygame.KEYUP and key in key_sound.keys():
                # Stops with 50ms fadeout
                key_sound[key].fadeout(50)
                is_playing[key] = False


def load_data(path: str):
    """Reads data from file
    :returns: seg_data: data readed from the file

    """
    print("Loading", path, "to memory")
    try:
        with open(path, "rb") as f:
            seg_data = pk.load(f, fix_imports=True, encoding='latin-1')
    except IOError as e:
        print(e)
        quit()
    return seg_data


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')
