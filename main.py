import argparse
import logging
import datetime
import pytz
from query import execute_query
from email_sender import send_email

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action='store_true', help='Run in debug mode')
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logging.debug("Entering main function")
    logging.info("Starting daily email process...")
    logging.debug("Executing database query...")
    rows = execute_query()
    logging.info("Database query completed successfully, fetched %d rows.", len(rows))
    logging.debug("Query results:")
    for row in rows:
        logging.debug(row)

    tz = pytz.timezone('America/Toronto')

    logging.debug("Getting current timestamp...")
    timestamp = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    logging.debug(f"Current timestamp: {timestamp}")

    logging.debug("Sending email...")
    send_email(rows, timestamp)
    logging.info("Email sent successfully")

    logging.info("Daily email process completed successfully.")
    logging.debug("Exiting main function")

if __name__ == "__main__":
    main()