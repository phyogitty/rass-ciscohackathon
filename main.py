from track1 import EmailGenerator, EmailDatabase
# from track1 import EmailDatabases
from track2.CalendarConversion import CalendarConversion
from track2.TimeExtractor import TimeExtractor
import import_ipynb
from track3 import run_model
from track4 import notify


# Main program, build executable from here
def main():
    # Build the database for fetching emails
    database = EmailGenerator.main()
    # database = EmailDatabase.DatabaseHandler();

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
    is_useful = "YES" if run_model.predict_usefulness(msg['body']) else "NO"
    print("\nIs Useful? ", is_useful)
     
    
    if is_useful == "YES":
        summarized_text = summarize(msg['body'])
        print("\nExtracting Calendar Information....")
        extracted_time = TimeExtractor().extractTime(msg['body'])


        dict_obj = {"body": summarized_text, "datetime": extracted_time}

        CalendarConversion(dict_obj)

        print("\n", summarized_text)
        # print(extracted_time)
        # Notify the user
        print("Notifying the User....")
        msg_copy = msg.copy()
        msg_copy['summary'] = summarized_text   # replace with result from text summarization algo or track 2
        if is_useful == "YES":
            notify.user(msg_copy)
    # Results
 


from transformers import pipeline

def summarize(orig_text):
    summarization = pipeline("summarization")
    return summarization(orig_text)[0]['summary_text']

main()
# print(summarize("Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things.Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things. Can we meet for a meeting next Monday at 1:30pm? I would like to discuss officer things. "))
