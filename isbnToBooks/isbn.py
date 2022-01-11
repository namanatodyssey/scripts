import isbnlib
import click
import logging

isbnlist_file = "./isbnlist_1.txt"
books_details_file = './books_1.txt'
error_file = "./error_isbn.txt"
logger = logging.getLogger(__name__)

def convertToCsvLine(bookObj: dict) -> str:
    """Writes a csv line in the order of the fields of the book. At the time of this writing the book fields were
    {'ISBN-13', 'Title', 'Authors', 'Publisher', 'Year', 'Language'}.
    """
    # {'ISBN-13': '9780749395445', 'Title': 'The Island Of The Day Before', 'Authors': ['Umberto Eco'], 'Publisher': 'Vintage', 'Year': '1996', 'Language': 'en'}
    line = ''
    for key, value in bookObj.items():
        if type(value) == list:
            line += value[0] + ','
        else:
            line += value + ','
    line.strip(',')
    print("adding line:", line)
    return line


@click.option('--isbnfile',
              help='A relative or absolute path to a text file which contains one isbn on one line')
@click.option('--bookscsvfile',
              help='A relative or absolute path to an output csv file where books metadata will be stored in csv')
@click.command()
def isbn_to_books(isbnfile: str, bookscsvfile: str):
    with open(isbnfile, 'r') as isbnlines:
        with open(bookscsvfile, 'a') as books_details:
            with open(error_file, 'a') as error_isbns:
                for isbn in isbnlines:
                    try:
                        print("\n")
                        book = isbnlib.meta(isbn)
                        if not book:
                            logger.error(f"ERROR: Did not find any data for ISBN: {isbn.strip()}. Adding to Error file.")
                            error_isbns.write(isbn+"\n")
                            continue
                        print(book)
                        books_details.write(convertToCsvLine(book)+"\n")
                    except isbnlib._exceptions.NotValidISBNError as notIsbnErr:
                        logger.error(f"ERROR: Found an invalid ISBN: {isbn}. {notIsbnErr.message}. Adding to error file")
                        error_isbns.write(isbn+"\n")


if __name__ == "__main__":
    isbn_to_books()
