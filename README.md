# NAACL-HLT 2019 official app

This repository contains resources and scripts for the official Whova app for the 2019 Annual Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT).

# Cloning

Note that this repository uses submodules so to properly check out the submodule code, run `git submodule init` and `git submodule update` after you clone the repository. You will need the submodule to generate the schedule for the app.

# Populating the App

(**Note**: If you have any questions about the NAACL 2019 Whova app, [contact](mailto:first_initial_then_last_name_at_gmail_dot_com) Nitin Madnani, the conference app chair for NAACL 2019.)

The following instructions are for the conference app chair who should be an admin on Whova EMS (Event Management System) for the corresponding conference event. The event itself is created by Whova folks (for NAACL 2019, this was Peter Howell from Whova) once the contract is signed and the payment has been made. The app chair is automatically given admin access assuming they are the one who negotiated communicated with Whova. Usually, they are also given admin access to the previous year's event to figure out how things were done the year before, which is quite helpful.

## Basics

The first thing to do is to fill out the Basics section under the "Event Content" tab of the Whova EMS. This includes the following information: 
- the conference name
- dates
- address of the venue
- description
- welcome message
- website address
- twitter hashtag
- app logo image (see `images/app-logo.png` for NAACL 2019 logo)
- header image (see `images/header.jpg` for NAACL 2019 header image)  

Some of this might be pre-populated by the Whova folks.

## Sponsors

Sponsors need to be added manually unlike GuideBook where they could be added as a custom list programmatically by using a zip file of images. To add a sponsor, go to the "Sponsor Banner" section under the "Event Content" tab and click on the "Add Sponsor" button. Fill out the information that is asked for in the pop-up and use the same logo that was used for the website. Although Whova has some logos that it offers up for the more famous companies, they might not be consistent or hi-res enough. **IMPORTANT**: make sure to click "No" for the "Show Banner" question since otherwise it would show ad banners while using the app which is quite intrusive. Click "Save" to save the information for this sponsor. Repeat this process for all other sponsors manually.

Sponsors will show up under "Additional Resources" in the app.

## Floormaps

Whova has a nice interface for adding floormaps. Go to the "Configure App" tab in the Whova EMS and click on "Floormap". Then click on "Set Up Floor Map" which will open a pop-up. You will need to obtain the actual floor maps for the venue from Priscilla which are usually PDF. Create an image (I used a 300dpi PNG) of the floormap from the PDF and upload it in Whova. Next, manually add all of the rooms/locations by clicking on the "Add a Location/Booth Number" button at the bottom. For each location you added, click on the little map pin icon next to its name in the list that and then click on the corresponding location on the floor map to place a pin there.

"Floormap" will show up under "Additional Resources" in the app.

## Logistics

Although Whova provides an explicit way to provide "Logistics" – the "Logistics" section under the "Event Content" tab in the Whova EMS – an easier way might be to just add a new resource under "Additional Resources" and point it to the "Participants" page on the conference website. Since the NAACL 2019 website is responsive and provides a table of contents, this is a pretty good option and that's what we used. 

If you end up using the explicit Logistics section, you will need to provide HTML content to show under it by clicking on the "Create a new logistic from scratch" option and then clicking on "Add Logistics". If you do end up manually adding various logistics, they will show up under "Additional Resources" -> "Logistics" in the app.

## Attendees

Everything happens under the "Attendees" tab in the Whova EMS.

For most events on Whova, a user needs to not only have a Whova account but that Whova account must explicitly be part of the attendees list for that event. In order for a user to become an attendee for an event, one of the following must be true:

1. The email that they used to sign up for Whova must explicitly be on the pre-populated list of attendees if the app chair sets that up on the Whova EMS.

2. They must know the secret access code for the event that only the app chair can see on the Whova EMS. 

3. They request access to the event through the Whova app and their request is explicitly approved by the app chair via the Whova EMS.

For NAACL 2019, we pre-populate the list of attendees by clicking on the "Import Attendees" button. This will provide an Excel template that can be populated using the information from Priscilla and uploaded to Whova. We get the spreadsheet of folks who have registered for the conference from Priscilla and then massage that spreadsheet into this Whova template.

**Notes**: 
- Some users might use a different email for conference registration and a different one for Whova, so option (3) is also likely to be quite popular among such users. 

- Option (2) is not very secure since users might make that access code public or share with other attendees who aren't registered for the conference. 

- The app chair might also need to add an attendee manually by clicking on the "Add Attendee" button in certain situations where it's just easier to add one or two records manually rather than uploading a whole spreadsheet again.

Note that the massaging referred to above is done by the agenda generation script [`generate.py`](appagenda/generate.py). For more on this, refer to the next section.

## Schedule

The code and data for this lives under `appagenda`. For more details, refer to that [README](appagenda/README.md).

# License

Most of the content in this repository is under the MIT License _except_:

- `images/header.jpg` - Original Photo by Daniel McCullough on Unsplash was uploaded under the [Unsplash License](https://unsplash.com/license).

- `images/floormaps/*.png` - The floormaps are the property of Hyatt Regency and are extracted from the PDF of the floorplan provided to Priscilla as part of the signed contract. 