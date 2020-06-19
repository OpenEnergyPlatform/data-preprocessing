---
name: Metadata and Data Review
about: Submit open data and an OEMetadata string for review
title: 'Review: NameOfDataset'
labels: review
assignees: christian-rli, jh-RLI, Ludee

---

## Issue description

I'm submitting an open dataset with a corresponding OEMetadata string for review. 
Please see **review_process.md** for technical detail.
Describe your dataset shortly here.


## Workflow checklist

1. GitHub
- [x] I have submitted this issue to have metadata and data review documented (Issue #NR)
- [ ] Create a new review-branch and push OEMetadata to new branch (review/project_nameofdata#NR)

2. OEP
- [ ] Upload data to the OEP in schema model_draft (see upload tutorial)
- [ ] Link URL of data in this issue (model_draft.project_nameofdata)

3. Start a Review
- [ ] Start a pull request (PR) from review-branch to master
- [ ] Assign a reviewer and get in contact

4. Reviewer section
- [ ] A reviewer starts working on the issue
- [ ] Review data license
- [ ] A reviewer finished working on this issue (and awarded a badge)
- [ ] Update metadata on table
- [ ] Data moved to its final schema
- [ ] Add OEP tags to table
- [ ] Merge PR and delete review-branch
- [ ] Document final links of metadata and data
- [ ] Close issue


## Metadata and data for review

Here are the links to my data and metadata. Naming follows the pattern model_draft.project_nameofdata:
**Metadata:** https://github.com/OpenEnergyPlatform/data-preprocessing/blob/review/project_nameofdata/data-review/project_nameofdata.json
**Data:** https://openenergy-platform.org/dataedit/view/model_draft/project_nameofdata


## Reviewed and published metadata and data

Final naming and location of the data and metadata after the review are as follows:
**schema.tablename**
* [Metadata]()
* [Data]()
