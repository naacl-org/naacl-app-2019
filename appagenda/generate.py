#!/usr/bin/env python3

"""
This script is used to generate the excel file for
the conference schedule on the Whova app. This script
uses the classes defined in the `orderfile.py` module
from the NAACL 2019 schedule repository that is integrated
as a submodule in this repository under the `agenda`
directory. For more details, run `generate.py --help`
and refer to the `README.md` file in this directory.

Note that this code is specific to the format that
Whova expects in its Excel template for the schedule.
For other app platforms such as GuideBook, this code
will need to be modified.

Author: Nitin Madnani
Date: May, 2019
"""


import argparse
import csv
import logging
import sys

from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, range_boundaries
from pandas import concat, DataFrame, read_excel

_THIS_DIR = Path(__file__).absolute().parent
AGENDA_SUBMODULE_DIR = _THIS_DIR.parent.joinpath('agenda', 'code')
sys.path.append(str(AGENDA_SUBMODULE_DIR))

from orderfile import Agenda, SessionGroup, Session, Item
from metadata import ScheduleMetadata


def write_rows_in_sheet_at_cell(sheet, cellstr, rows):
    """
    Write the given rows to the current sheet
    starting at the given cell. It is assumed
    that rows is is a list of lists with each
    child list being the same length.

    Note that nothing is returned since the `sheet`
    object is modified directly.

    Parameters
    ----------
    sheet :  openpyxl.worksheet.worksheet.Worksheet
        openpyxl Worksheet instance in which to
        write the given rows.
    cellstr : str
        Alphanumeric cell location in an Excel
        spreadsheet, e.g., 'A26'. The first element
        of the first list in `rows` is written at
        this location.
    rows : list of lists
        A list of lists with each list containing
        the same number of strings.
    """

    # figure out how many rows we are writing first
    num_rows_to_add = len(rows)

    # get the Cell object corresponding to the given
    # cell string
    starting_cell = sheet[cellstr]

    # compute the ending row index in the spreadsheet
    ending_row_index = starting_cell.row + num_rows_to_add - 1

    # compute the new column letter in the spreadsheet
    new_column_letter = get_column_letter(starting_cell.column + len(rows[0]) - 1)

    # get the cell range that we will be modifying
    cell_range = '{}:{}{}'.format(cellstr, new_column_letter, ending_row_index)

    # get the min and max rows and columns which openpyxl needs to
    # iterate over the rows
    (min_col, min_row, max_col, max_row) = range_boundaries(cell_range)

    # iterate over each spreadsheet row and write each data row
    # to the cells in the spreadsheet row
    for idx, sheet_row in enumerate(sheet.iter_rows(min_col=min_col,
                                                    max_col=max_col,
                                                    min_row=min_row,
                                                    max_row=max_row)):
        for cell, value in zip(sheet_row, rows[idx]):
            cell.value = value


class AppAgenda(Agenda):
    """
    Class encapsulating the agenda for the Whova app.
    Inherits from `orderfile.Agenda` and adds a
    `to_rows()` method to convert the parsed agenda
    into a list of rows that can then be written
    out into the Whova agenda template and
    imported into the app via the Whova EMS.
    """

    def __init__(self):
        super(AppAgenda, self).__init__()

    def to_rows(self,
                metadata,
                pdf_links=False,
                video_links=False,
                plenary_info={}):
        """
        Convert agenda to rows compatible
        with the Whova Agenda template.

        Parameters
        ----------
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        pdf_links : bool, optional
            Whether to generate the links to the
            anthology and other PDFs where appropriate.
            Defaults to `False`.
        video_links : bool, optional
            Whether to generate the links to
            the talk videos.
            Defaults to `False`.
        plenary_info : dict, optional
            Optional dictionary containing
            additional info for some plenary
            sessions. Defaults to an empty
            dictionary.

        Returns
        -------
        agenda_rows : list
            A list containing rows for the full schedule.
        """

        agenda_rows = []

        # iterate over the days in the agenda that should
        # already be in chronological order
        for day_index, day in enumerate(self.days):

            # now iterate over each day's contents
            for content in day.contents:

                # if it's a `SessionGroup`, cast it to the
                # `AppSessionGroup` class so that we can then
                # call its `to_rows()` method; we do this by
                # monkeypatching the `__class__` attribute which
                # is fine since we are just adding new behavior
                # (methods), not new attributes.
                if isinstance(content, SessionGroup):
                    content.__class__ = AppSessionGroup
                    session_group_rows = content.to_rows(day,
                                                         metadata,
                                                         pdf_links=pdf_links,
                                                         video_links=video_links,
                                                         plenary_info=plenary_info)
                    agenda_rows.extend(session_group_rows)

                # if it's a `Session`, then cast it to `WebSession`
                # and call its `to_html()` method and save that to
                # the agenda HTML.
                elif isinstance(content, Session):
                    content.__class__ = AppSession
                    session_rows = content.to_rows(day,
                                                   metadata,
                                                   pdf_links=pdf_links,
                                                   video_links=video_links,
                                                   plenary_info=plenary_info)
                    agenda_rows.extend(session_rows)

        # convert the list to a string and return
        return agenda_rows


class AppSessionGroup(SessionGroup):
    """
    Class encapsulating a session group for the Whova app.
    Inherits from `orderfile.SessionGroup` and adds a
    `to_rows()` method to convert the parsed group
    into rows that can then be inserted into the Whova
    agenda template.
    """

    def __init__(self):
        super(AppSessionGroup, self).__init__()

    def to_rows(self,
                day,
                metadata,
                pdf_links=False,
                video_links=False,
                plenary_info={}):
        """
        Convert session group to a list of rows compatible
        with the Whova agenda template.

        Parameters
        ----------
        day : orderfile.Day
            The `Day` instance on which the session
            group is scheduled.
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        index : int
            An index to be used in the HTML tags
            for the box representing this session group.
        pdf_links : bool, optional
            Whether to generate the links to the
            anthology and other PDFs where appropriate.
            Defaults to `False`.
        video_links : bool, optional
            Whether to generate the links
            to the talk videos.
            Defaults to `False`.
        plenary_info : dict, optional
            Optional dictionary containing
            additional info for some plenary
            sessions. Defaults to an empty
            dictionary.

        Returns
        -------
        generated_rows : list
            A list containing the rows for the
            session group. The fields in each row are:
            date, start time, end time, tracks, session title,
            location, description, authors, and a string
            indicating whether it's a session ("Session")
            or a sub-session ("Sub") where a sub-session
            denotes presentation items in a session.
        """

        # initialize the result variable
        generated_rows = []

        # iterate over the sessions in the group which should
        # already be in chronological order
        for session in self.sessions:

            # cast `Session` to `AppSession` to enable
            # the call to `to_rows()`.
            session.__class__ = AppSession

            # the sessions in session groups may not
            # have a start and end time defined in the
            # order file, so we need to inherit those
            # here since sessions _are_ displayed with
            # start and end times on the website
            if not session.start and not session.end:
                session.start = self.start
                session.end = self.end

            # call the respective `to_rows()` for the session
            # and save the rows
            session_rows = session.to_rows(day,
                                           metadata,
                                           pdf_links=pdf_links,
                                           video_links=video_links,
                                           plenary_info=plenary_info)
            generated_rows.extend(session_rows)

        return generated_rows


class AppSession(Session):
    """
    Class encapsulating a session for the Whova app.
    Inherits from `orderfile.Session` and adds a
    `to_rows()` method to convert the parsed session
    into rows that can then be written out into the
    Whova agenda template.

    """
    def __init__(self):
        super(AppSession, self).__init__()

    def to_rows(self,
                day,
                metadata,
                pdf_links=False,
                video_links=False,
                plenary_info={}):
        """
        Convert session to a list of rows compatible
        with the Whova agenda template.

        Parameters
        ----------
        day : orderfile.Day
            The `Day` instance on which the session
            is scheduled.
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        index : int, optional
            An index to be used in some of the HTML tags.
        pdf_links : bool, optional
            Whether to generate the links to the
            anthology and other PDFs where appropriate.
            Defaults to `False`.
        video_links : bool, optional
            Whether to generate the links to
            the talk videos.
            Defaults to `False`.
        plenary_info : dict, optional
            Optional dictionary containing
            additional info for some plenary
            sessions. Defaults to an empty
            dictionary.

        Returns
        -------
        generated_rows : list
            A list containing the rows values for
            the session. The fields in each row are:
            date, start time, end time, tracks, session title,
            location, description, authors, and a string
            indicating whether it's a session ("Session")
            or a sub-session ("Sub") where a sub-session
            denotes presentation items in a session.
        """
        # initialize the result variable
        generated_rows = []

        # convert the given day to a date string
        date = day.datetime.strftime('%m/%d/%Y')

        # initialize tracks,  description, and authors to be empty
        tracks = ''
        description = ''
        authors = ''

        # for tutorials, we may not have the start
        # and end times defined in the order file but we
        # need them for the website; if so just get them from
        # the first session item
        if self.type == 'tutorial':
            if not self.start and not self.end:
                self.start = self.items[0].start
                self.end = self.items[0].end

        # the best paper session may not have start
        # and end times defined in the order file but we
        # need them for the website; if so just get them from
        # the first and the last item
        elif self.type == 'best_paper':
            if not self.start and not self.end:
                self.start = self.items[0].start
                self.end = self.items[-1].end
            description = '<p>Chair: {}</p>'.format(self.chair) if self.chair else ''

        # get the values for the columns that are not
        # session attributes; first the session tracks
        # are defined by the kinds of items that are in
        # this paper/poster session. "Research" is always
        # one of the tracks
        elif self.type in ['paper', 'poster', 'best_paper']:
            track_display_dict = {'srw': 'SRW',
                                  'tacl': 'TACL',
                                  'demos': 'Demos',
                                  'industry': 'Industry'}
            tracks = 'Research'
            item_tracks = []
            item_tracks = {item.id_.split('-')[1] for item in self.items if '-' in item.id_}
            if len(item_tracks) > 0:
                item_tracks_str = '; '.join([track_display_dict[item_track] for item_track in item_tracks])
                tracks += '; {}'.format(item_tracks_str)
            description = '<p>Chair: {}</p>'.format(self.chair) if self.chair else ''

        # next use the extra plenary info provided, if appropriate
        elif self.type == 'plenary':
            self.abstract = ''
            self.person = ''
            self.person_url = ''
            self.pdf_url = ''
            self.video_url = ''
            for session_prefix in plenary_info:
                if self.title.startswith(session_prefix):
                    (self.abstract,
                     self.person,
                     self.person_affiliation,
                     self.person_url,
                     self.pdf_url,
                     self.video_url) = plenary_info[session_prefix]
                    break

            # initialize the desciption to be the abstract
            description = '<p>{}</p>'.format(self.abstract)
            authors = self.person

            # Add paper links and video links if we are asked to
            # and if we have the actual links to add
            if pdf_links and self.pdf_url:
                description += ' [<a href="{}">PDF</>]'.format(self.pdf_url)
            if video_links and self.video_url:
                description += ' [<a href="{}">VIDEO</a>]'.format(self.video_url)

        # this is always a 'Session'
        session_or_sub = 'Session'

        # all sessions get a row except for the tutorial
        # session since they are more like session groups
        # for those we only care about the items
        if self.type != 'tutorial':
            generated_rows.append([date,
                                   self.start,
                                   self.end,
                                   tracks,
                                   self.title,
                                   self.location,
                                   description,
                                   authors,
                                   '',
                                   session_or_sub])

        for item in self.items:

            # cast `Item` to `AppItem` to enable
            # the call to `to_rows()`.
            item.__class__ = AppItem

            # for tutorials and posters, we may not
            # have the start and end times but we need
            # to show these in the app, so get them
            # from the containing sessions
            if item.type in ['tutorial', 'poster']:
                item.start = self.start
                item.end = self.end

            # call `to_rows()` on each item and save
            # the resulting rows
            generated_rows.append(item.to_rows(day,
                                               metadata,
                                               pdf_links=pdf_links,
                                               video_links=video_links))

        return generated_rows


class AppItem(Item):
    """
    Class encapsulating a presentation item for
    the Whova app. Inherits from `orderfile.Item` and
    adds a `to_html()` method to convert the item
    into a row for the Whova app.

    """
    def __init__(self):
        super(AppItem, self).__init__()

    def to_rows(self,
                day,
                metadata,
                pdf_links=False,
                video_links=False):
        """
        Convert item to rows for the Whova app
        with the Whova Agenda template.

        Parameters
        ----------
        metadata : ScheduleMetadata
            An instance of `ScheduleMetadata`
            containing the title, authors,
            abstracts, and anthology URLs for
            each item, if applicable.
        pdf_links : bool, optional
            Whether to generate the links to the
            anthology and other PDFs where appropriate.
            Defaults to `False`.
        video_links : bool, optional
            Whether to generate the links to
            the talk videos.
            Defaults to `False`.

        Returns
        -------
        item_row : list of str
            A list of containing row values for the item.
            The fields in the row are: start time, end time,
            tracks, session title, location, description,
            authors, and a string indicating whether it's
            a session ("Session") or a sub-session ("Sub")
            where a sub-session denotes presentation items
            in a session.
        """

        # convert the given day to a date string
        date = day.datetime.strftime('%m/%d/%Y')

        # get the metadata for the item
        self.title = metadata[self.id_].title
        self.authors = '; '.join(metadata[self.id_].authors)
        self.pdf_url = metadata[self.id_].pdf_url
        self.video_url = metadata[self.id_].video_url

        # set the description to be the abstract
        description = '<p>{}</p>'.format(metadata[self.id_].abstract)

        # compute the tracks properly which we can get
        # based on the ID suffix
        if self.id_.endswith('-srw'):
            tracks = 'SRW'
        elif self.id_.endswith('-tacl'):
            tracks = 'TACL'
        elif self.id_.endswith('-demos'):
            tracks = 'Demos'
        elif self.id_.endswith('-industry'):
            tracks = 'Industry'
        elif self.id_.endswith('-tutorial'):
            tracks = 'Tutorial'
        else:
            tracks = 'Research'

        # Add paper links and video links if we are asked to
        # and if we have the actual links to add
        if pdf_links and self.pdf_url:
            description += ' [<a href="{}">PDF</>]'.format(self.pdf_url)
        if video_links and self.video_url:
            description += ' [<a href="{}">VIDEO</a>]'.format(self.video_url)

        # for everything except tutorials, we have "Sub"
        session_or_sub = 'Session' if self.type == 'tutorial' else 'Sub'

        # return the row
        return [date,
                self.start,
                self.end,
                tracks,
                self.title,
                self.location if hasattr(self, 'location') else '',
                description,
                self.authors,
                '',
                session_or_sub]


def main():

    # set up an argument parser
    parser = argparse.ArgumentParser(prog='generate.py')
    parser.add_argument("--order",
                        dest="orderfile",
                        required=True,
                        help="Manually combined order file")
    parser.add_argument("--xmls",
                        dest="xml_files",
                        required=True,
                        nargs='+',
                        type=Path,
                        help="Anthology XML files containing author "
                             "and title metadata")
    parser.add_argument("--mappings",
                        dest="mapping_files",
                        required=True,
                        nargs='+',
                        type=Path,
                        help="Files mapping order Anthology IDs "
                             "to order file IDs.")
    parser.add_argument("--attendees",
                        dest="attendee_info",
                        required=True,
                        type=Path,
                        help="Spreadsheet from Priscilla containing "
                             "information for conference registrants.")
    parser.add_argument("--extra-metadata",
                        dest="extra_metadata_file",
                        required=False,
                        default=None,
                        type=Path,
                        help="TSV file containing authors and "
                             "titles not in anthology XMLs")
    parser.add_argument("--plenary-info",
                        dest="plenary_info_file",
                        required=False,
                        default=None,
                        type=Path,
                        help="TSV file containing info "
                             "for plenary sessions")
    parser.add_argument("--output",
                        dest="output_file",
                        required=True,
                        help="Output Excel file containing agenda")
    parser.add_argument("--pdf-links",
                        action="store_true",
                        default=False,
                        dest="pdf_links",
                        required=False,
                        help="Generate links to paper and other"
                             "PDFs where appropriate")
    parser.add_argument("--video-links",
                        action="store_true",
                        default=False,
                        dest="video_links",
                        required=False,
                        help="Generate links to talk videos")

    # parse given command line arguments
    args = parser.parse_args()

    # set up the logging
    logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

    # parse the orderfile into a `WebAgenda` object
    logging.info('Parsing order file ...')
    app_agenda = AppAgenda()
    app_agenda.fromfile(args.orderfile)

    # parse the metadata files
    logging.info('Parsing metadata files ...')
    metadata = ScheduleMetadata.fromfiles(xmls=args.xml_files,
                                          mappings=args.mapping_files,
                                          non_anthology_tsv=args.extra_metadata_file)

    # parse and store any additional plenary session
    # info if provided
    plenary_info_dict = {}
    if args.plenary_info_file:
        logging.info("Parsing plenary info file ...")
        with open(args.plenary_info_file, 'r') as plenaryfh:
            reader = csv.DictReader(plenaryfh, dialect=csv.excel_tab)
            for row in reader:
                key = row['session'].strip()
                value = (row['abstract'].strip(),
                         row['person'].strip(),
                         row['person_affiliation'].strip(),
                         row['person_url'].strip(),
                         row['pdf_url'].strip(),
                         row['video_url'].strip())
                plenary_info_dict[key] = value

    # convert AppAgenda to rows
    logging.info("Converting parsed agenda to rows ...")
    agenda_rows = app_agenda.to_rows(metadata,
                                     pdf_links=args.pdf_links,
                                     video_links=args.video_links,
                                     plenary_info=plenary_info_dict)

    # read in the attendee info sheet
    logging.info("Reading in attendee info ...")
    df_attendees = read_excel(args.attendee_info, usecols=['Professional Name',
                                                           'Affiliation',
                                                           'Email'])

    # get all of the speakers in the agenda and look up
    # emails and affiliations in the attendee info for
    # names that are exact matches
    speakers = set()
    for row in agenda_rows:
        speaker_string = row[-3]
        speakers.update(speaker_string.split('; '))
    df_matched_speakers = df_attendees[df_attendees['Professional Name'].isin(speakers)]
    df_matched_speakers = df_matched_speakers[['Professional Name',
                                               'Email',
                                               'Affiliation']]

    # for those speakers who are not registered, just add their name
    missing_speaker_dicts = []
    for missing_speaker_name in speakers.difference(df_matched_speakers['Professional Name']):
        missing_speaker_dict = {'Professional Name': missing_speaker_name,
                                'Email': '',
                                'Affiliation': ''}
        missing_speaker_dicts.append(missing_speaker_dict)

    df_unmatched_speakers = DataFrame(missing_speaker_dicts)
    df_unmatched_speakers = df_unmatched_speakers[['Professional Name',
                                                   'Email',
                                                   'Affiliation']]
    # merge the two data frames
    df_speakers = concat([df_matched_speakers,
                          df_unmatched_speakers]).reset_index(drop=True)

    # drop any speakers that have the same name and email
    # since Whova does not like duplicates
    df_speakers.drop_duplicates(subset=['Professional Name', 'Email'],
                                inplace=True)

    # read in the Whova agenda template
    logging.info('Populating Whova template ...')
    workbook = load_workbook(str(_THIS_DIR / "Agenda_Track_Template.xlsx"))

    # write out the rows in "Agenda" sheet of the template
    sheet = workbook['Agenda']
    write_rows_in_sheet_at_cell(sheet, 'A26', agenda_rows)

    # now write out the speaker names and affiliations in the
    # "Speaker" sheet of the template
    sheet = workbook['Speaker']
    write_rows_in_sheet_at_cell(sheet, 'A6', df_speakers.to_numpy().tolist())

    # save the modified workbook to the given output file
    workbook.save(args.output_file)


if __name__ == '__main__':
    main()
