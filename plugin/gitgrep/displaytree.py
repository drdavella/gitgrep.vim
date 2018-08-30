import vim
from collections import OrderedDict


class DisplayTree:

    def __init__(self, results):
        self.open = [False for _ in range(len(results))]
        self.index_map = {i:x for i, x in enumerate(results)}
        self._generate_result_tree(results)
        self.max_line = 0

    def _generate_result_tree(self, results):
        self._line_lookup = dict()
        self._result_tree = OrderedDict()

        for filename, result in results.items():
            self._result_tree[filename] = list()
            lineno_width = len(str(result[-1][0]))
            for lineno, content in result:
                new_string = "    {lineno:{width}}{content}".format(
                    lineno=lineno+':', width=lineno_width+1, content=content)
                self._result_tree[filename].append(new_string)
                self._line_lookup[new_string] = (filename, lineno)

    def _clear_current_buffer(self):
        # This is possibly a total hack
        while len(vim.current.buffer) > 1:
            del vim.current.buffer[0]

    def display(self):
        self._clear_current_buffer()

        index = 0
        for i, filename in enumerate(self._result_tree):
            num_results = len(self._result_tree[filename])
            plural = "s" if num_results > 1 else ""
            file_header = "  {} ({} result{})".format(filename, num_results, plural)

            if index == 0:
                vim.current.buffer[0] = file_header
            else:
                vim.current.buffer.append(file_header)

            if self.open[i]:
                for line in self._result_tree[filename]:
                    vim.current.buffer.append(line)
                    index += 1

            index += 1

        self.max_line = index - 1

    def process(self, selected_index):

        index = 0
        for i, filename in enumerate(self._result_tree):
            if index == selected_index:
                self.open[i] = not self.open[i]
                break
            if self.open[i]:
                for line in self._result_tree[filename]:
                    index += 1
                    if index == selected_index:
                        return self._line_lookup[line]
            index += 1

        self.display()
        return None

