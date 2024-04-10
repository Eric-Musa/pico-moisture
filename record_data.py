import os
data_path = 'moisture_data.csv'


columns = [
    'depth',
    'samples',
    'mean_moisture',
    'std_moisture',
    'min_moisture',
    'max_moisture',
]

if not os.path.exists(data_path):
    with open(data_path, 'w') as f:
        f.write(', '.join(columns) + '\n')

try:
    with open(data_path, 'a') as f:
        while True:
            depth = float(input('depth: ')) / 100.
            samples = input('number of samples: ')
            if samples == '': 
                samples = 100
                print('100')
            else:
                samples = int(samples)
            stats = [float(_) for _ in input('moistures stats: ').split(' ')]
            mean_moisture, std_moisture, min_moisture, max_moisture = stats
            f.write(', '.join([str(_) for _ in [depth, samples] + stats]) + '\n')
except KeyboardInterrupt:
    print()
    print()
    print('Data writting completed.')

with open(data_path, 'r') as f:
    print(f.read())
