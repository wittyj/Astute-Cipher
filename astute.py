import click
import codecs
import os

# Define Astute cipher encryption function
def Astute_cipher(text, shift, option):
    if option == 'decrypt':
        shift = -shift
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            char_code = ord(char)
            char_code = (char_code - ord('a') + shift) % 26 + ord('a')
            if is_upper:
                char_code = chr(char_code).upper()
            else:
                char_code = chr(char_code)
            encrypted_text += char_code
        else:
            encrypted_text += char
    return encrypted_text

# Define ROT13 encryption function using codecs
def rot13_cipher(text):
    return codecs.encode(text, 'rot_13')

# Define Atbash cipher encryption function
def atbash_cipher(text):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            char_code = ord(char)
            char_code = ord('z') - (char_code - ord('a'))
            if is_upper:
                char_code = chr(char_code).upper()
            else:
                char_code = chr(char_code)
            encrypted_text += char_code
        else:
            encrypted_text += char
    return encrypted_text

def crot13(text, shift, option):
    if option == 'encrypt':
        res = Astute_cipher(text, shift, option)
        return rot13_cipher(res)
    
    elif option == 'decrypt':
        res = Astute_cipher(text, shift, option)  # Decrypt using Astute cipher with a negative shift
        return rot13_cipher(res)


VERSION = '1.0'

encryption_algorithms = {
    'Astute': Astute_cipher,
    'rot13': rot13_cipher,
    'atbash': atbash_cipher,
    'crot13': crot13
}

@click.command()
@click.option('--file', type=click.File('r'), help='Input file to read text from.')
@click.option('--text', help='Text to encrypt or decrypt.')
@click.option('--shift', type=int, help='Shift value for Astute cipher (default: 3).', default=3)
@click.option('--decrypt', is_flag=True, help='Decrypt the text (default is to encrypt).')
@click.option('--output', type=click.File('w'), help='Output file to write the result to.')
@click.option('--algorithm', type=click.Choice(['Astute', 'rot13', 'atbash', 'crot13'], case_sensitive=False), default='Astute', help='Encryption algorithm to use (default: Astute cipher).')
@click.version_option(version=VERSION)
@click.option('--uninstall', is_flag=True, help='Uninstall the program.')
def main(file, text, shift, decrypt, output, algorithm, uninstall):
    """
    Command-line tool for text encryption and decryption using various algorithms.

    This tool supports multiple encryption algorithms, including Astute cipher,
    ROT13, Atbash cipher, and a custom crot13 algorithm.

    Usage examples:
    - Encrypt text using Astute cipher:
      $ Astute.py --text "Hello, World!" --shift 3

    - Decrypt text using ROT13:
      $ Astute.py --text "Uryyb, Jbeyq!" --algorithm rot13 --decrypt

    - Encrypt text using the custom crot13 algorithm:
      $ Astute.py --text "Hello, World!" --algorithm crot13 --shift 3

    - Decrypt text using the custom crot13 algorithm:
      $ Astute.py --text "Uryyb, Jbeyq!" --algorithm crot13 --decrypt --shift 3

    - Encrypt text from a file and save the result to another file:
      $ Astute.py --file input.txt --output encrypted.txt --shift 5
    """

    if uninstall:
        response = click.prompt('Are you sure you want to uninstall the program? (y/n)', type=str, default='n')
        if response.lower() == 'y':
            try:
                os.remove('/usr/local/bin/Astute')
                click.echo('Uninstalled successfully.')
            except OSError:
                click.echo('Only System Administrators can uninstall the program. Run the command with sudo.')
        else:
            click.echo('Uninstallation aborted.')
        return

    if file and text: 
        click.echo("Error: Please provide either '--file' or '--text', not both.")
        return

    if not file and not text:
        text = click.prompt('Enter the text to encrypt/decrypt', hide_input=decrypt)

    input_text = text  # Initialize input_text with the value of text

    try:
        if file:
            input_text = file.read()

        if algorithm == 'Astute':
            result = Astute_cipher(input_text, shift, 'encrypt' if not decrypt else 'decrypt')
        elif algorithm == 'rot13':
            result = rot13_cipher(input_text)
        elif algorithm == 'atbash':
            result = atbash_cipher(input_text)
        elif algorithm == 'crot13':
            result = crot13(input_text, shift, 'encrypt' if not decrypt else 'decrypt')

        if output:
            output.write(result)
            output.close()
            click.echo(f'Result has been written to the file: {output.name}')
        else:
            click.echo(f'Result: {result}')
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    main()
