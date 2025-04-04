def calculate_directory_size(directory, cwd, sizes):
    size = 0
    for name, content in directory.items():
        current_name = cwd + name + "/"

        if isinstance(content, int):
            size += content
        else:
            size += calculate_directory_size(content, current_name, sizes)

        sizes[current_name] = size

    return size


def solve(test: str) -> str:
    commands = test.lstrip("$ ").strip().split("\n$ ")

    cwd = []
    filesystem = {"/": {}}
    for command in commands:
        command = command.splitlines(keepends=False)
        command, output = command[0], command[1:]

        command = command.split(" ")
        command, args = command[0], command[1:]

        if command == "cd":
            directory = args[0]
            if directory == "..":
                cwd.pop()
            else:
                cwd.append(directory)

        if command == "ls":
            container_directory = filesystem
            for cwd_part in cwd:
                container_directory = container_directory[cwd_part]

            for node in output:
                fst, snd = node.split(" ")
                if fst == "dir":
                    container_directory[snd] = {}
                else:
                    container_directory[snd] = int(fst)

    sizes = {}
    for _, content in filesystem.items():
        calculate_directory_size(content, "/", sizes)

    total = 0
    for _, size in sizes.items():
        if size <= 100000:
            total += size

    return str(total)
