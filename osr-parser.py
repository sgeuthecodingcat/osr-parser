import struct
import os
import argparse

def read_uleb128(file):
    result = 0
    shift = 0
    while True:
        byte = file.read(1)[0]
        result |= (byte & 0x7F) << shift
        if byte & 0x80 == 0:
            break
        shift += 7
    return result

def read_string(file):
    indicator = file.read(1)[0]
    if indicator == 0x00:
        return ""
    elif indicator == 0x0b:
        length = read_uleb128(file)
        return file.read(length).decode('utf-8')
    else:
        raise ValueError(f"Invalid string format: {indicator}")

def parse_osu(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('osu file format'):
                data['file_format'] = line
            elif ':' in line:
                key, value = line.split(':', 1)
                key, value = key.strip(), value.strip()
                data[key] = value
    return data

def parse_osr(osr_path, osu_data):
    with open(osr_path, 'rb') as file:
        data = {}
        data['game_mode'] = struct.unpack('B', file.read(1))[0]
        data['osu_version'] = struct.unpack('<i', file.read(4))[0]
        data['beatmap_hash'] = read_string(file)
        data['player_name'] = read_string(file)
        data['replay_hash'] = read_string(file)
        data['num_300s'] = struct.unpack('<H', file.read(2))[0]
        data['num_100s'] = struct.unpack('<H', file.read(2))[0]
        data['num_50s'] = struct.unpack('<H', file.read(2))[0]
        data['num_gekis'] = struct.unpack('<H', file.read(2))[0]
        data['num_katus'] = struct.unpack('<H', file.read(2))[0]
        data['num_misses'] = struct.unpack('<H', file.read(2))[0]
        data['score'] = struct.unpack('<I', file.read(4))[0]
        data['combo'] = struct.unpack('<H', file.read(2))[0]
        data['full_combo'] = struct.unpack('B', file.read(1))[0]
        data['mods'] = struct.unpack('<I', file.read(4))[0]
        data['life_bar'] = read_string(file)
        data['timestamp'] = struct.unpack('<q', file.read(8))[0]
        replay_length = struct.unpack('<i', file.read(4))[0]
        data['replay_data'] = file.read(replay_length)
        file.read(1)  # Consume the additional byte, if exists.

        if data['beatmap_hash'] != osu_data.get('BeatmapHash'):
            raise ValueError("The OSR file does not correspond to the provided OSU file.")

        hit_timings = [int(h.split('|')[0]) for h in data['replay_data'].decode('utf-8').split(',') if '|' in h]
        mean = sum(hit_timings) / len(hit_timings)
        ur = (sum((t - mean) ** 2 for t in hit_timings) / len(hit_timings)) ** 0.5

    return data, ur

def main():
    parser = argparse.ArgumentParser(description="Parse osu! replay (.osr) and beatmap (.osu) files.")
    parser.add_argument('-osr', '--osr_path', required=True, help='Path to the .osr file')
    parser.add_argument('-osu', '--osu_path', required=True, help='Path to the .osu file')

    args = parser.parse_args()

    osu_data = parse_osu(args.osu_path)
    osr_data, ur = parse_osr(args.osr_path, osu_data)

    print(f"UR: {ur:.2f} 50s: {osr_data['num_50s']} 100s: {osr_data['num_100s']} 300s: {osr_data['num_300s']} Gekis: {osr_data['num_gekis']} Katus: {osr_data['num_katus']} Misses: {osr_data['num_misses']} Score: {osr_data['score']} Combo: {osr_data['combo']} Full Combo: {osr_data['full_combo']} Mods: {osr_data['mods']} Life Bar: {osr_data['life_bar']} Timestamp: {osr_data['timestamp']} Game Mode: {osr_data['game_mode']} Osu Version: {osr_data['osu_version']} Beatmap Hash: {osr_data['beatmap_hash']} Player Name: {osr_data['player_name']} Replay Hash: {osr_data['replay_hash']}")
    print("Extracted OSR Data:")
    for key, value in osr_data.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == '__main__':
    main()
