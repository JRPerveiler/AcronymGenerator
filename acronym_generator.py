import click
import string

def get_input():
    """Get the sentence to generate the acronym from."""
    click.clear()
    document = ''
    while True:
        document += click.prompt("Enter the sentences to generate the acronym from. \033[31mEnd your document with ::: to submit\033[0m", type=str)
        if document.endswith(':::'):
            document = document[:-3]  # Remove the ':::' from the end of the document
            document += ' '  # Add a space after the document to separate it from any potential next input
            break
        document += ' \n'  # Add a space after each line to separate words
    return document

def split_document(document):
    """Split the sentence into an array of words."""
    translator = str.maketrans('', '', string.punctuation.replace('-', ''))  # Keep hyphens, remove other punctuation
    document = document.translate(translator)
    document = document.replace('-', ' ')  # Replace hyphens with spaces to split them into separate words
    words = document.split()
    return words

def number_to_letter(word):
    """Convert a number in the word to its corresponding letter."""
    number_map = {
        '0': 'Z',
        '1': 'O',
        '2': 'T',
        '3': 'T',
        '4': 'F',
        '5': 'F',
        '6': 'S',
        '7': 'S',
        '8': 'E',
        '9': 'N'
    }

    leading_digit = word[0]
    if leading_digit == '1' and len(word) == 2:
        if word[1] == 0:
            return 'T'
        elif word[1] == '1':
            return 'E'
        else:
            return number_map[word[1]]
    else:
        return number_map[word[0]]
    
def family_guy_wiki_document(document):
    """Process the document if it's in the format of a cutaway or gag from the Family Guy Wiki."""
    # Example format: "Brian: What the hell? Second line: We're all just blockin' the street We're all just blockin' the street"
    # We want to remove the character names and colons, and then split the remaining text into words.
    lines = document.splitlines()
    processed_document = ''
    for line in lines:
        if ':' in line:
            processed_document += line.split(':', 1)[1].strip() + ' '  # Take the part after the colon and add it to the processed document
        else:
            processed_document += line.strip() + ' '  # If there's no colon, just add the line as is
    return processed_document
    

@click.command()
@click.option('--fgwiki', is_flag=True, help='If set to True, the input string will be expected to be in the format of a cutaway or gag from the Family Guy Wiki.')
def acronym(fgwiki):
    """Main function to generate the acronym."""
    document = get_input()
    if fgwiki:
        document = family_guy_wiki_document(document)
    words = split_document(document.strip())  # Remove any extra whitespace at the beginning and end of the document
    acronym = ''
    for word in words:
        if word[0].isdigit():
            acronym += number_to_letter(word)
        else:
            acronym += word[0].upper()
    click.echo(f"The acronym is: {acronym}")

if __name__ == "__main__":
    acronym()