from track1 import EmailGenerator, EmailDatabase
from track2 import CalendarConversion_V0
from track3 import *
from track4 import *


# Main program, build executable from here
def main():
    # Build the database for fetching emails
    database = EmailGenerator.main()

    """ Retrieve the next message, call as many as there are entries
    msg {
        id: Current message number
        label: Email labels, sep. by comma
        date: Datetime the email was sent
        from: Sender
        to: Receiver (usually us)
        subject: Email subject
        body: Parsed email body
    """
    msg = database.retrieveNext()
    print(msg)

    # Track 2
    # Track 3
    # Results


main()
