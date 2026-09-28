# MedTrace investigation report

Investigation: I-7d1453bf71fd

Created: 2026-09-28T00:21:26.455828+00:00

## Complaint

An infusion pump stopped medication delivery during treatment and displayed an occlusion alarm even though no blockage was found.

## Extracted facts

{
  "device": "Infusion pump",
  "manufacturer": "",
  "model": "",
  "problems": [
    "occlusion alarm",
    "delivery interruption"
  ],
  "alarm_issue": true,
  "patient_impact": "Not reported",
  "serious_outcome": false,
  "outcome": "Unknown",
  "severity_indicators": [],
  "evidence_spans": [
    {
      "field": "problem",
      "value": "occlusion alarm",
      "quote": "occlusion alarm",
      "start": 79,
      "end": 94,
      "source": "complaint"
    },
    {
      "field": "problem",
      "value": "delivery interruption",
      "quote": "stopped medication delivery",
      "start": 17,
      "end": 44,
      "source": "complaint"
    }
  ],
  "technical_terms": [
    "occlusion alarm",
    "delivery interruption"
  ],
  "token_count": 19,
  "method": "regex rules (spaCy unavailable)",
  "limitations": [
    "Rule extraction is not clinically validated.",
    "Missing fields remain unknown."
  ],
  "missing_evidence": [
    "Manufacturer",
    "Device model",
    "Patient outcome"
  ],
  "classification": {
    "status": "disabled",
    "backend": "rules",
    "note": "No trained classifier active; evidence extraction uses rules."
  }
}

## Historical evidence

- Report 21289524; similarity 0.1836 (tfidf); 2025-02-03

IT WAS REPORTED THAT THE DEVICE HAD FLUID SIDE OCCLUSION ALARM. EVEN AFTER REPLACING BOTH BOTTLE SIDE AND PATIENT SIDE PRESSURE SENSORS AND STILL GETTING ALARM. THERE WAS NO PATIENT INVOLVEMENT.

https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=21289524

- Report 21289597; similarity 0.164 (tfidf); 2025-02-03

IT WAS REPORTED THAT THE DEVICE DISPLAYED AN ERROR CODE 242.4030. THERE WAS NO PATIENT INVOLVEMENT.

https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=21289597

- Report 23677571; similarity 0.1504 (tfidf); 2025-12-01

IT WAS REPORTED THAT A SPECTRUM IQ INFUSION PUMP FAILED TO DETECT UPSTREAM OCCLUSION DURING HEPARIN THERAPY. THE PATIENT WAS ON HIGH DOSE OF HEPARIN AND EVEN THOUGH THE PUMP APPEARED TO BE FUNCTIONING, NONE OF THE MEDICATION HAD GONE INTO THE PATIENT. THERE WAS NO REPORT OF PATIENT INJURY OR MEDICAL INTERVENTION ASSOCIATED WITH THIS EVENT. NO ADDITIONAL INFORMATION IS AVAILABLE.

https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=23677571

- Report 21289606; similarity 0.1393 (tfidf); 2025-02-03

IT WAS REPORTED THAT THE DEVICE DISPLAYED AN ERROR CODE 352.6640. THERE WAS NO PATIENT INVOLVEMENT.

https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=21289606

- Report 22368616; similarity 0.1311 (tfidf); 2025-07-01

IT WAS REPORTED THAT THE DEVICE HAD DISPLAYED AN ERROR CODE 13-1064-1229. THERE WAS NO PATIENT INVOLVEMENT.

https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=22368616

## Reporting patterns

{
  "monthly": [
    {
      "month": "2025-01",
      "reports": 15
    },
    {
      "month": "2025-02",
      "reports": 15
    },
    {
      "month": "2025-03",
      "reports": 15
    },
    {
      "month": "2025-04",
      "reports": 15
    },
    {
      "month": "2025-05",
      "reports": 15
    },
    {
      "month": "2025-06",
      "reports": 15
    },
    {
      "month": "2025-07",
      "reports": 15
    },
    {
      "month": "2025-08",
      "reports": 15
    },
    {
      "month": "2025-09",
      "reports": 15
    },
    {
      "month": "2025-10",
      "reports": 15
    },
    {
      "month": "2025-11",
      "reports": 15
    },
    {
      "month": "2025-12",
      "reports": 115
    }
  ],
  "total_reports": 280,
  "scope": "all infusion-pump records in loaded corpus",
  "spike": true,
  "score_eligible": false,
  "interpretation": "Descriptive report counts only. Incomplete sampling and reporting bias prevent incidence estimates.",
  "last_month_vs_prior_mean": 100.0
}

## Investigation priority

20/100 (Low)

[
  {
    "factor": "serious_outcome",
    "points": 0,
    "active": false
  },
  {
    "factor": "delivery_interruption",
    "points": 20,
    "active": true
  },
  {
    "factor": "other_malfunction",
    "points": 0,
    "active": false
  },
  {
    "factor": "repeated_reports",
    "points": 0,
    "active": false
  },
  {
    "factor": "reporting_spike",
    "points": 0,
    "active": false
  },
  {
    "factor": "verified_recall",
    "points": 0,
    "active": false
  }
]

## SHAP / model explanation

{
  "status": "not_trained",
  "message": "Rule contributions are available. SHAP requires an independently trained priority model."
}

## Recall evidence

{
  "status": "insufficient_identifiers",
  "matches": [],
  "message": "Provide manufacturer and model to assess possible recall matches."
}

## Regulatory evidence

[REG-d3cfe78766c6] 820.35

§ 820.35 Control of records. In addition to the requirements of Clause 4.2.5 in ISO 13485 (incorporated by reference, see § 820.7 ), Control of Records, the manufacturer must include the following information in certain records: ( a ) Records of complaints. In addition to Clause 8.2.2 in ISO 13485, Complaint Handling, the manufacturer shall maintain records of the review, evaluation, and investigation for any complaints involving the possible failure of a device, labeling, or packaging to meet any of its specifications. If an investigation has already been performed for a similar complaint, another investigation is not necessary, and the manufacturer shall maintain records documenting justification for not performing such investigation. For complaints that must be reported to FDA under part 803 of this chapter , complaints that a manufacturer determines must be investigated, and complaints that the manufacturer investigated regardless of those requirements, the manufacturer must record the following information: ( 1 ) The name of the device; ( 2 ) The date the complaint was received; ( 3 ) Any unique device identifier (UDI) or universal product code (UPC), and any other device identification(s); ( 4 ) The name, address, and phone number of the complainant; ( 5 ) The nature and details of the complaint; ( 6 ) Any correction or corrective action taken; and ( 7

https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820/subpart-B/section-820.35

[REG-98391f8c7d14] 803.20

reportable event has occurred? ( 1 ) Any information, including professional, scientific, or medical facts, observations, or opinions, may reasonably suggest that a device has caused or may have caused or contributed to an MDR reportable event. An MDR reportable event is a death, a serious injury, or, if you are a manufacturer or importer, a malfunction that would be likely to cause or contribute to a death or serious injury if the malfunction were to recur. ( 2 ) If you are a user facility, importer, or manufacturer, you do not have to report an adverse event if you have information that would lead a person who is qualified to make a medical judgment reasonably to conclude that a device did not cause or contribute to a death or serious injury, or that a malfunction would not be likely to cause or contribute to a death or serious injury if it were to recur. Persons qualified to make a medical judgment include physicians, nurses, risk managers, and biomedical engineers. You must keep in your MDR event files (described in § 803.18 ) the information that the qualified person used to determine whether or not a device-related event was reportable.

https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803

[REG-6794d7168e51] 803.18

you are a device distributor, you must establish and maintain device complaint records (files). Your records must contain any incident information, including any written, electronic, or oral communication, either received or generated by you, that alleges deficiencies related to the identity (e.g., labeling), quality, durability, reliability, safety, effectiveness, or performance of a device. You must also maintain information about your evaluation of the allegations, if any, in the incident record. You must clearly identify the records as device incident records and file these records by device name. You may maintain these records in written or electronic format. You must back up any file maintained in electronic format. ( 2 ) You must retain copies of the required device incident records for a period of 2 years from the date of inclusion of the record in the file or for a period of time equivalent to the expected life of the device, whichever is greater. You must maintain copies of these records for this period even if you no longer distribute the device. ( 3 ) You must maintain the device complaint files established under this section at your principal business establishment. If you are also a manufacturer, you may maintain the file at the same location as you maintain your complaint file under part 820 of this chapter . You

https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803

[REG-d042f0dc36eb] 803.3

manufacturer or importer of the temporary MDR reporting number; ( 2 ) The four-digit calendar year in which the report is submitted; and ( 3 ) The five-digit sequence number of the reports submitted during the year, starting with 00001. (For example, the complete number will appear as follows: 1234567-2011-00001.) ( n ) MDR means medical device report. ( o ) MDR reportable event (or reportable event) means: ( 1 ) An event that user facilities become aware of that reasonably suggests that a device has or may have caused or contributed to a death or serious injury or ( 2 ) An event that manufacturers or importers become aware of that reasonably suggests that one of their marketed devices: ( i ) May have caused or contributed to a death or serious injury, or ( ii ) Has malfunctioned and that the device or a similar device marketed by the manufacturer or importer would be likely to cause or contribute to a death or serious injury if the malfunction were to recur. ( p ) Medical personnel means an individual who: ( 1 ) Is licensed, registered, or certified by a State, territory, or other governing body, to administer health care; ( 2 ) Has received a diploma or a degree in a professional or scientific discipline; ( 3

https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-803

## Suggested next steps

- Inspect the returned pump and delivery pathway if available.

- Inspect the alarm history and occlusion-detection subsystem if available.

- Review original complaint details and obtain missing device identifiers.

- Compare retrieved reports with the current event before treating them as related.

- Have a qualified investigator review the cited regulatory passages.

## Missing evidence

- Manufacturer

- Device model

- Patient outcome

- Provide manufacturer and model to assess possible recall matches.

## Claim-to-evidence record

[
  {
    "claim": "Complaint reports occlusion alarm",
    "kind": "reported_fact",
    "evidence": [
      {
        "source": "complaint",
        "quote": "occlusion alarm",
        "start": 79,
        "end": 94
      }
    ]
  },
  {
    "claim": "Complaint reports delivery interruption",
    "kind": "reported_fact",
    "evidence": [
      {
        "source": "complaint",
        "quote": "stopped medication delivery",
        "start": 17,
        "end": 44
      }
    ]
  },
  {
    "claim": "5 similar reports retrieved from loaded data",
    "kind": "retrieval_result",
    "evidence": [
      {
        "report_key": "21289524",
        "source_url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=21289524"
      },
      {
        "report_key": "21289597",
        "source_url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=21289597"
      },
      {
        "report_key": "23677571",
        "source_url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=23677571"
      },
      {
        "report_key": "21289606",
        "source_url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=21289606"
      },
      {
        "report_key": "22368616",
        "source_url": "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/detail.cfm?mdrfoi__id=22368616"
      }
    ]
  }
]

## Human decision

Pending qualified human review

Research prototype for decision support. Qualified humans make final regulatory decisions. MAUDE reports do not establish causality or incidence.