def print_system_info():
    ascii_art = '''
\033[0m
>=>       >=> >==>    >=> >=>     >=> >=>      >=>
>=>       >=> >> >=>  >=> >=>     >=>  >=>   >=>  
>=>       >=> >=> >=> >=> >=>     >=>   >=> >=>   
>=>       >=> >=>  >=>>=> >=>     >=>     >=>     
>=>       >=> >=>   > >=> >=>     >=>   >=> >=>   
>=>       >=> >=>    >>=> >=>     >=>  >=>   >=>  
>=======> >=> >=>     >=>   >====>    >=>      >=>
\033[0m
    '''

    def get_system_info():
        def read_file(filepath):
            with open(filepath, 'r') as file:
                return file.read().strip()

        def get_username():
            uid = next(line.split()[1] for line in read_file('/proc/self/status').split('\n') if line.startswith('Uid:'))
            with open('/etc/passwd', 'r') as file:
                for line in file:
                    parts = line.split(':')
                    if parts[2] == uid:
                        return parts[0]
            return "unknown"

        username = get_username()
        hostname = read_file('/etc/hostname')
        os_name = next(line.split('=')[1].strip('"') for line in read_file('/etc/os-release').split('\n') if line.startswith('PRETTY_NAME='))
        kernel_version = read_file('/proc/version').split()[2]
        product_name = read_file('/sys/devices/virtual/dmi/id/product_name')
        uptime_seconds = int(read_file('/proc/uptime').split(' ')[0].split('.')[0])
        uptime = f'{uptime_seconds // 86400}d {uptime_seconds // 3600 % 24}h {uptime_seconds // 60 % 60}m {uptime_seconds % 60}s'
        mem_info = {line.split(':')[0]: int(line.split(':')[1].strip().split()[0]) for line in read_file('/proc/meminfo').split('\n') if line}
        memory = f"{mem_info['MemFree'] // 1024}M / {mem_info['MemTotal'] // 1024}M"
        return f'''
\033[1;32m{username}@{hostname}
============================
os       \033[1;32m{os_name}
host     \033[1;32m{product_name}
kernel   \033[1;32m{kernel_version}
memory   \033[1;32m{memory}\033[0m
uptime   \033[1;32m{uptime}\033[0m
\033[1;32m
'''

    def calculate_width(text):
        import re
        # Calculate width ignoring ANSI color codes
        return max(len(re.sub(r'\x1b\[.*?m', '', line)) for line in text.split('\n'))

    def print_side_by_side(left, right, width):
        left_lines = left.split('\n')
        right_lines = right.split('\n')

        max_lines = max(len(left_lines), len(right_lines))
        left_lines.extend([''] * (max_lines - len(left_lines)))
        right_lines.extend([''] * (max_lines - len(right_lines)))

        for l, r in zip(left_lines, right_lines):
            print(f'{l:<{width}}{r}')

    ascii_art = f'\033[0m{ascii_art.strip()}\033[0m'
    system_info = get_system_info()

    # Calculate width of each section
    ascii_width = calculate_width(ascii_art) + 5
    system_info_width = calculate_width(system_info) + 5

    # Ensure both sections have the same width
    max_width = max(ascii_width, system_info_width)

    print_side_by_side(ascii_art, system_info, width=max_width)
    print("ᴾᵉⁿᵍᵘᶦⁿ ᵃʳᵐʸ ᵇᵃᵇʸ")

print_system_info()
