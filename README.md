# NAACL-HLT 2019 official app

This repsitory contains resources and scripts for the official Whova app for the 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT).

# Populating the App

(**Note**: For any questions, [contact](mailto:first initial then last name at gmail dot com) Nitin Madnani, the conference app chair for NAACL 2019.)

The following instructions are for the conference app chair who should be an admin on Whova EMS (Event Management System) for the corresponding conference event. The event itself is created by Whova folks (for NAACL 2019, this was Peter Howell from Whova) once the contract is signed and the payment has been made. The app chair is automatically given admin access assuming they are the one who negotiated communicated with Whova. Usually, they are also given admin access to the previous year's event to figure out how things were done the year before, which is quite helpful.

## Basics

The first thing to do is to fill out the Basics section under the "Event Content" tab of the Whova EMS. This is information like the the conference, name, dates, address of the venue, description, website address, twitter hashtag, etc. Some of this might be pre-populated by the Whova folks.

## Sponsors

Sponsors need to be added manually unlike GuideBook where they could be added as a custom list programmatically by using a zip file of images. To add a sponsor, go to the "Sponsor Banner" section under the "Event Content" tab and click on the "Add Sponsor" button. Fill out the information that is asked for in the pop-up and use the same logo that was used for the website. Although Whova has some logos that it offers up for the more famous companies, they might not be consistent or hi-res enough. **IMPORTANT**: make sure to click "No" for the "Show Banner" question since otherwise it would show ad banners while using the app which is quite intrusive. Click "Save" to save the information for this sponsor. Repeat this process for all other sponsors manually.

## Floormaps

Whova has a nice interface for adding floormaps. Go to the "Configure App" tab in the Whova EMS and click on "Floormap". Then click on "Set Up Floor Map" which will open a pop-up. You will need to obtain the actual floor maps for the venue from Priscilla which are usually PDF. For each floor, create an image of the floormap from the PDF and upload it. Next, manually add all of the rooms/locations for this floor by clicking on the "Add a Location/Booth Number" button at the bottom. For each location you added, click on the little map pin icon next to its name in the list that and then click on the corresponding location on the appropriate floor map to place a pin there.

## Attendees

Everything happens under the "Attendees" tab in the Whova EMS.

For most events on Whova, a user needs to not only have a Whova account but that Whova account must explicitly be part of the attendees list for that event. In order for a user to become an attendee for an event, one of the following must be true:

1. The email that they used to sign up for Whova must explicitly be on the pre-populated list of attendees if the app chair sets that up on the Whova EMS.
2. They must know the secret access code for the event that only the app chair can see on the Whova EMS. 
3. They request access to the event through the Whova app and their request is explicitly approved by the app chair via the Whova EMS.

For NAACL 2019, we get the list of folks who have registered for the conference from Priscilla and pre-populate the list of attendees by clicking on the "Import Attendees" button. This will provide an Excel template that can be populated using the information from Priscilla and uploaded to Whova.

**Notes**: 
- Some users might use a different email for conference registration and a different one for Whova, so option (3) is also likely to be quite popular among such users. 
- Option (2) is not very secure since users might make that access code public or share with other attendees who aren't registered for the conference. 
- The app chair might also need to add an attendee manually by clicking on the "Add Attendee" button in certain situations where it's just easier to add one or two records manually rather than uploading a whole spreadsheet again.

## Schedule

# License

Most of the content in this repository is under the MIT License _except_:

- `images/header.jpg` - Original Photo by Daniel McCullough on Unsplash was uploaded under the [Unsplash License](https://unsplash.com/license).
- `images/floormaps/*.png` - The floormaps are the property of Hyatt Regency and are extracted from the PDF of the [publicly available floorplans](https://assets.hyatt.com/content/dam/hyatt/hyattdam/documents/2014/12/08/1806/MSPRM_HR_Minneapolis_FP.pdf) on their website.