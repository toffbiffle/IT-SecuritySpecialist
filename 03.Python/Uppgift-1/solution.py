# Input is the encrypted ransom note
# Expected return value is a string
# Skriv din egen docstring till funktionen: vilket cipher är det, och hur fungerar det?

import string
import pytest

def solution(note:str) -> str:
    """Rotate characters in "note" according to their index position of the alphabet.

    cipher: Atbash
    Let all non-lowercase characters pass through without alteration.
    Substitute each letter with the same index in a reversed alphabet. 
    a->z, b->y, c->x...

    Invert digits by taking 9 - digit in string. ( 9 - 9 = 0 )
    9->0, 8->1, 7->2

    input: Encrypted text string
    return: Decrypted text string
    """

    NUMS = string.digits                                        # CONSTANT: '0123456789'
    LOWERCASE_ALPH = string.ascii_lowercase                     # CONSTANT: 'abcdefghijklmnopqrstuvwxyz'
    REVERSE_ALPH = LOWERCASE_ALPH[::-1]                         # CONSTANT: 'zyxwvutsrqponmlkjihgfedcba'

    decryptMessage = []

    for letter in note:
        if letter in LOWERCASE_ALPH:                            # Check if the letter is a part of the lowecase letter constant
            letterIndex = LOWERCASE_ALPH.find( letter )         # Figure out the index of the letter in the alphabet
            decryptMessage.append( REVERSE_ALPH[ letterIndex ] )# Add the letter that correspond to the index of the reversed list to the decryptMessage list
        elif letter in NUMS:                                    # Check if the letter is a digit in the NUMS Literal
            decryptMessage.append( str( 9 - int( letter ) ) )   # Typecast the resulting digit to a string to make it possible to join everything together later
        else: 
            decryptMessage.append( letter )                     # Let all characters that shouldnt be altered pass through

    return "".join( decryptMessage )

# Create a more complete parametarized test case
@pytest.mark.parametrize(
    "text, expected",
    [
        pytest.param(
            "abba",
            "zyyz",
            id="[TEST SUPPLIED]lowercase_letters",
        ),
        pytest.param(
            "Aoo blfi yzhv ziv yvolmt gl fh!",
            "All your base are belong to us!",
            id="[TEST SUPPLIED]mixed_case_sentence",
        ),
        pytest.param(
            "Eiz hvieizi äi oåhgz lxs yzxpfkvimz äi izwvizwv. Sprxpz 24 yrgxlrm uöiv nåmwzt po 90:99, zmmzih häoqvi er pfmwfkktrugvimz kå mägvg!",
            "Era servrar är låsta och backuperna är raderade. Skicka 75 bitcoin före måndag kl 09:00, annars säljer vi kunduppgifterna på nätet!",
            id="[TEST SUPPLIED]mixed_letters_case_and_digits",
        ),
        pytest.param(
            "JAG HAR 123 OCH INTE 456",
            "JAG HAR 876 OCH INTE 543",
            id="[USER SUPPLIED]mixed_capital_letters_and_digit_rotation_test",
        ),
        pytest.param(
            "0123456789",
            "9876543210",
            id="[USER SUPPLIED]all_digits_test",
        ),
        pytest.param(
            r"{}[]$?&<>;/(|#)",
            r"{}[]$?&<>;/(|#)",
            id="[USER SUPPLIED]Random_non_letter_or_digit_test",
        ),
    ],
)

def test_solution( text, expected ):
    # Skapa minst tre egna tester här, så att det blir minst sex totalt
    assert solution( text ) == expected
