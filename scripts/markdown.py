import os
import sys
import re


def remove_symbol(text: str):
    for s in ["$\n", "$", "# ", "#", "**"]:
        text = text.replace(s, "")
    return text

def replace_space(text: str):
    for s in ["\\", "{" ,"}"]:
        text = text.replace(s, " ")
    return text

def replace_symbol(text: str):
    d = {
        "\%": " percent",  # Percent symbols
        "\in": " belongs to ",
        "\cdots": " so on until ",
        "\\vdots": " so on until ",
        "\dots": " so on until ",
        "\sum": " summation of ",
        "\mapsto": " maps to ",
        "\subseteq": " subset equals ",
        "\subsetneq": " subset not equal ",
        "\Rightarrow": " implies ",
        "\\begin{bmatrix}": "",
        "\\end{bmatrix}": "",
        "^": " to the ",
        "_": " sub ",
        "=": " equals ",
        "+": " plus ",
    }
    for k, v in d.items():
        text = text.replace(k, v)
    return text

def subtitue_symbol(text: str):
    d = {
        r"\\mathcal{?(\w+)}?": "\g<1>",
        r"\\mathbf{?(\w+)}?": "\g<1>",
        r"\\mathbb{?(\w+)}?": "\g<1>",
        r"\\text{?(\w+)}?": "\g<1>",
        r"\((.+)\)\^T": " transpose of (\g<1>)",
        r"\((.+)\)\^{-1}": " inverse of (\g<1>)",
        r"(\w+)\^T": " transpose of \g<1>",
        r"(\w+)\^{-1}": " inverse of \g<1>"
    }
    for k, v in d.items():
        text = re.sub(k, v, text)
    return text

def markdown_to_txt(input_file: str):
    with open(input_file,'r',encoding = 'utf-8') as f:
        text = f.read()

    text = subtitue_symbol(text)
    text = replace_symbol(text)
    text = remove_symbol(text)
    text = replace_space(text)

    filename = os.path.basename(input_file)
    pos = filename.rindex('.')
    output_file = './out/' + filename[0:pos] + '.txt'
    with open(output_file, 'w', encoding = 'utf-8') as f:
        f.write(text)

def main():
    if len(sys.argv) != 2:
        print('Usage: python markdown.py <input_file>')
        return
    print('[Convert] ' + sys.argv[1])
    markdown_to_txt(sys.argv[1])


if __name__ == '__main__':
    main()
