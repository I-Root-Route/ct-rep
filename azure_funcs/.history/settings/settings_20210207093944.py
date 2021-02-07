import configparser

config = configparser.ConfigParser()
config.read('settings/settings.ini')

num_table = eval(config['table']['numtable'])
# kanjitable = eval(config['table']['kanjitable'])
# exp = eval(config['table']['exp'])
# exp_base = eval(config['table']['exp_base'])
# base = eval(config['table']['base'])
# split_base = eval(config['table']['split_base'])
# chunk_base = eval(config['table']['chunk_base'])
# num2kanji = config['web']['num2kanji']
# kanji2num = config['web']['kanji2num']