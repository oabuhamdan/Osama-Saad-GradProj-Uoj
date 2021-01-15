import datetime

from . import JobHandler


def main():
    JobHandler.create_scrapping_and_analysis_job("Joker", "2019", "#Joker", datetime.date(2015, 1, 1),
                                                 datetime.date(2015, 1, 2))
    while True:  # TODO: Remove when django get implemented
        pass


if __name__ == '__main__':
    main()
