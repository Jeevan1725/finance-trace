# Sample Indian documents — sources and notes

All files below were collected as openly published samples, official blank forms, or public company filings. No leaked unredacted personal documents were included.

## 1. Bank statements

| File | Source page | Notes |
|---|---|---|
| bank_hdfc_statement_sample.pdf | https://bankfileconverter.net/bank-statement-examples/hdfc-bank | Fictional educational sample clearly marked “EDUCATIONAL SAMPLE - NOT ISSUED BY THE NAMED BANK”. 1 page. Layout is a generic synthetic design, not an official HDFC specimen. Direct PDF: https://bankfileconverter.net/bank-statement-examples/hdfc-bank-sample.pdf |
| bank_sbi_statement_sample.pdf | https://bankfileconverter.net/bank-statement-examples/sbi (or /sbi-sample.pdf) | Same series; fictional SBI-labelled educational sample. 1 page. Direct PDF: https://bankfileconverter.net/bank-statement-examples/sbi-sample.pdf |
| bank_icici_statement_sample.pdf | https://bankfileconverter.net/bank-statement-examples/icici-bank | Same series; fictional ICICI-labelled educational sample. 1 page. Direct PDF: https://bankfileconverter.net/bank-statement-examples/icici-bank-sample.pdf |

Axis and Kotak Mahindra educational samples also exist in the same library but were not copied, since 3 banks were requested.

**These three files are synthetic educational layouts, not official bank-issued statement formats.** Genuine bank-issued-format PDFs (official specimen or public regulatory filings) are in `real_format/` below.

## 1b. Genuine bank-issued-format statements (`real_format/`)

Collected after a follow-up request for original bank layouts (not generator samples). Official bank sites generally do not publish downloadable customer-statement specimens; the Axis file below is a rare official masked sample. HDFC, ICICI and Kotak files are genuine e-statement PDFs of **company/LLP RERA project accounts**, published as required disclosures on official state RERA portals (not leaked personal savings accounts). Unredacted statements of private individuals (full name + full account number + transactions) found on Scribd, IndiaMART, AskGamblers, and some RERA proprietor uploads were skipped. Synthetic ReportLab/FPDF “HDFC/ICICI” fixtures on GitHub (e.g. KharchaLens, local-finance) were also skipped because they are not bank-issued PDFs.

| File | Source | Bank | What it is | Masking | Pages |
|---|---|---|---|---|---|
| real_format/axis_relationship_statement_official_sample.pdf | Official Axis Bank sample (live URL now redirects to the sitemap): https://www.axisbank.com/mailers/generic/OGS_Priority_Sample.pdf — retrieved from the Internet Archive capture of 19 Jul 2022: https://web.archive.org/web/20220719134412/https://www.axisbank.com/mailers/generic/OGS_Priority_Sample.pdf | Axis Bank | Official bank-published Priority “Relationship Statement” specimen (01-08-2015 to 31-08-2015), produced with Axis’s Style Report statement engine. Includes relationship summary, savings-account transaction tables, deposits, etc. | Holder name, address, PIN, landline, mobile, PAN, Aadhaar, Cust ID, account numbers, scheme name, joint holder, nominee, and RM name/contact/email are all replaced with X’s. Branch names, IFSC and MICR, and transaction amounts/narrations remain visible. | 7 |
| real_format/hdfc_statement_rera_pansari_builders.pdf | Official Bihar RERA project passbook filing: https://rera.bihar.gov.in/PassBook/RERAP231120170002304021133582022.pdf (saved without the original empty-user-password owner restriction so the file opens freely; text unchanged) | HDFC Bank | Genuine HDFC “Statement of account” e-statement layout (638×842 pt, Cust ID / Account No / IFSC / MICR / branch GSTIN footer). Company current account of M/S. Pansari Builders and Contractors Pvt Ltd for 01/11/2021–30/11/2021, with 6 charge transactions and official “computer generated statement” footer. | Not redacted. This is a company account published as a statutory RERA disclosure. Company name, address, Cust ID 55020727 and Account No 50200005036361 are visible. Not an individual’s personal savings account. | 1 |
| real_format/icici_statement_rera_samanvay_homes.pdf | Official Rajasthan RERA BankDoc filing: https://reraapp.rajasthan.gov.in/Content/uploads/BankDoc/1fdf7f4b-d769-4ef7-a97b-da420a25e0a5.pdf | ICICI Bank | Genuine ICICI e-statement layout (“Your Details With Us”, account summary, MICR/IFSC, “Team ICICI Bank”, Vadodara registered-office footer). Three LLP project accounts (collection, retention, promoter) of M/S. Samanvay Homes LLP “The Autograph”, as of 22 Jan 2026. Zero-balance / no transactions in the selected date range, but the official format is complete. | Not redacted. LLP name, address, Cust IDs and current-account numbers (e.g. 777705045656) are visible, as published on the RERA portal. | 3 |
| real_format/kotak_statement_rera_green_mountain_builders.pdf | Official Rajasthan RERA BankDoc filing: https://reraapp.rajasthan.gov.in/Content/uploads/BankDoc/3618a3af-5309-48f3-9935-a69004482195.pdf | Kotak Mahindra Bank | Genuine Kotak e-statement layout (Cust Reln No, Account No, branch/MICR/IFSC, Date / Narration / Chq-Ref / Withdrawal-Deposit / Balance, statement summary, “system generated report and does not require signature & stamp”). Three LLP project accounts of Green Mountain Builders LLP “The Forever Heights” for 29-04-2025 to 14-05-2025; the promoters account has two transactions (clearing credit and IMPS debit). | Not redacted. LLP name, address, Cust Reln No 971782693 and account numbers (7151292353 / 7151292346 / 7151292322) are visible, as published on the RERA portal. | 3 |

| real_format/sbi_statement_cgrera_sankalp_realities.pdf | Official Chhattisgarh RERA passbook filing: https://rera.cgstate.gov.in/Content/ProjectDocuments/Application_2045/PASSBOOK_e2afc637-8e8a-4e85-8ff8-382bdb7f8706.pdf | State Bank of India | Genuine digital SBI "STATEMENT OF ACCOUNT" (SME Branch Raipur / SBIN0003577). Project current account "SANKALP REALITIES-PROJECT AISHWARYA GREATER", product REALTORS CURRENT ACCOUNT TWO, A/c 40595612144, period 01/04/2023-13/07/2023. Has 11 transactions (RERA fund transfers: 2 withdrawals, 9 deposits) plus brought-forward and closing balance 38,80,002.00 Cr. Ends with "*** END OF STATEMENT ***". | Not redacted. Developer-project account name, address and account number are visible as published on the RERA portal. | 1 |
| real_format/canara_statement_cgrera_jain_groundworks.pdf | Official Chhattisgarh RERA passbook filing: https://rera.cgstate.gov.in/Content/ProjectDocuments/Application_453/PASSBOOK_cec7a6b5-98a6-4853-aa74-2824e0b34169.PDF (promoter confirmed as Jain Groundworks Private Limited on the same project's CA certificate) | Canara Bank | Scanned genuine Canara "STATEMENT OF ACCOUNT" (Raipur MCB / CNRB0005107). Account title "JAIN GROUNDWORK RERA DESIGNAT BANK", A/c 5107201000040, current account, period 29/05/2018-29/05/2018. Has a cash-deposit transaction of Rs 5,000 (opening 0, closing 5,000). Official footer with canarabank.in phishing warning; stamp of Jain Groundworks Pvt. Ltd. | Not redacted. Company RERA designated-account name, address, customer ID and account number are visible. Joint holder/authorised signatory GAUTAM CHAND JAIN is named on the company account. | 1 |
| real_format/indian_bank_statement_cgrera_rcp_infratech.pdf | Official Chhattisgarh RERA passbook filing: https://rera.cgstate.gov.in/Content/ProjectDocuments/Application_1697/PASSBOOK_71c5fc20-84dd-4ec2-ad2a-cd393eeaa99a.pdf | Indian Bank | Genuine Indian Bank internet-banking "STATEMENT OF ACCOUNT" (Raipur Shyam Nagar Telibandha / IDIB000R521). Company current account of "RCP INFRATECH P LTD", A/c 50032985523, period 01/01/2022-31/01/2022. Has transactions (MICR cheque-book charges, two large credits and matching RTGS outwards, SMS charges). Footer: "END OF STATEMENT - from Internet Banking." | Not redacted. Company name, address and account number are visible as published on the RERA portal. | 1 |
| real_format/bank_of_baroda_statement_cgrera_shri_krishna_vatika.pdf | Official Chhattisgarh RERA passbook filing: https://rera.cgstate.gov.in/Content/ProjectDocuments/Application_1366/PASSBOOK_991cf921-4902-4a04-8222-c62e5f3d063d.pdf | Bank of Baroda (Vijaya Bank format; footer reads "Vijaya Bank : Now - Bank of Baroda") | Genuine digital Vijaya Bank / Bank of Baroda statement for developer current account "SHRI KRISHNA VATIKA DEVELOPERS", A/c 763100301000325, Pandri Raipur branch, period 01-10-2019 to 31-10-2019. Only an opening-balance row (30-09-2019 Balance 10,061.50); no new transactions in the period. Official computer-generated footer and vijayabank.com legend. | Not redacted. Developer-firm name, address, customer ID and account number are visible as published on the RERA portal. | 1 |
| real_format/pnb_statement_cgrera_shiva_prime.pdf | Official Chhattisgarh RERA passbook filing: https://rera.cgstate.gov.in/Content/ProjectDocuments/Application_269/PASSBOOK_504e24bd-894f-4043-896d-f124116cf16c.PDF | Punjab National Bank (similar public-sector bank) | Scanned genuine PNB CBS statement for project account "296600 RERA AC SHIVA PRIME", A/c 2966002100017101 (PNB Anupam Nagar, Raipur branch 2966), from account open date 08-06-2018 through Dec 2018. Many transactions (cheques, ledger folio charges, transfers to/from Shiva Homes / Shiva Prime, PNB Housing Finance credits). | Not redacted. Project RERA account title and full account number are visible as published on the RERA portal. | 1 |

Also collected in this round: public-sector / small-finance bank statements from official Chhattisgarh RERA project passbooks (company, firm, or project designated accounts only). Proprietor/individual RERA uploads and Scribd/IndiaMART-style leaks were skipped.

Banks searched but **not found** as an acceptable downloadable genuine-format statement (no official specimen; only letters/certificates, passbook covers, proprietor accounts, or unredacted personal leaks): **Union Bank of India**, **Equitas Small Finance Bank**, and Yes Bank. A Corporation Bank (now Union Bank) passbook front page for M/S Linc Property Developers Limited was found on CG-RERA but had no transaction table, so it was not copied.

## 2. ITR, AIS, Form 26AS

| File | Source page | Notes |
|---|---|---|
| itr1_sahaj_ay2025-26_official_blank.pdf | https://www.caalley.com/itr2025/itr1_english.pdf (republication of the CBDT Gazette ITR-1). Official downloads page (Akamai blocked direct fetch from this environment): https://incometaxindia.gov.in/Pages/downloads/income-tax-return.aspx | Official blank ITR-1 SAHAJ for AY 2025-26 as notified in the Gazette of India. 4 pages. Not a filled return. |
| itrv_and_acknowledgement_ay2026-27_official_blank.pdf | https://webtel.in/Image/ITR-V-2026-Eng_201.pdf (republication of the Gazette forms) | Official blank ITR-V (page 1) and Indian Income Tax Return Acknowledgement (page 2) for AY 2026-27. 2 pages. Not filled. |
| form26as_official_blank_template.pdf | https://www.indiafilings.com/learn/wp-content/uploads/2018/04/Form-26AS.pdf (footer: “Printed from www.incometaxindia.gov.in”) | Official blank Form 26AS (Annual Tax Statement) template, 3 pages, older rule 31AB layout. Not a filled taxpayer statement. |

### AIS — no downloadable open sample found

A genuine Annual Information Statement PDF is generated only after login on the Income Tax e-filing portal and is typically password-protected (lowercase PAN + DOB). No clearly labelled dummy/specimen AIS statement PDF was found on official sites or open educational repositories. GitHub copies that looked like real taxpayer AIS/26AS files (unredacted names/PANs) were intentionally not used.

Best official source pages:
- https://www.incometaxindia.gov.in/annual-information-statement
- Official AIS FAQs: https://www.incometax.gov.in/iec/foportal/sites/default/files/2022-07/Click%20Here_1.pdf
- Official AIS Portal User Guide (download was blocked in this environment): https://static.insight.gov.in/resources/pdf/AIS%20Portal%20User%20Guide_v5.0.0.pdf

## 3. GST return

| File | Source page | Notes |
|---|---|---|
| gstr3b_official_blank_form.pdf | Official CGST Rules, 2017 — Part B Forms: https://www.gstcouncil.gov.in/sites/default/files/2024-04/18052021-cgst-rules-2017-part-b-forms.pdf (FORM GSTR-3B extracted from PDF pages 152–153; also listed in the CBIC copy at https://cbic-gst.gov.in/pdf/18052021-CGST-Rules-2017-Part-B-Forms.pdf). Returns help: https://www.gst.gov.in/help/returns | Official blank FORM GSTR-3B [See rule 61(5)]. 2 pages. Not a filled return. A commercial “sample GSTR-3B PDF” at http://downloads.stacos.com/GST/GSTR-3B_sample.pdf (linked from https://gstplus.com/excel) returned HTTP 500 at collection time. |

## 4. MCA filing

| File | Source page | Notes |
|---|---|---|
| mca_mgt7_indo_count_fy2025-26_draft.pdf | Company IR page: https://www.indocount.com/Parents/annual-return-1 — direct PDF: https://www.indocount.com/images/investor/Draft-Annual-Return-Form-MGT-7-FY-2025-26.pdf | Publicly published draft Form MGT-7 annual return of Indo Count Industries Limited (CIN L72200PN1988PLC068972) for FY 01/04/2025–31/03/2026, watermarked “Draft before AGM”. 23 pages. Company PAN is already masked in the filing (AA******6P). |

## 5. Sale deed

| File | Source page | Notes |
|---|---|---|
| sale_deed_andhra_pradesh_model_template.pdf | Official AP registration templates: https://registration.ap.gov.in/igrs/pdfs/document-templates/saleDeed/SaledeedF.pdf | Official blank “Sale Deed for Flat” model draft from Andhra Pradesh Inspector General of Registration & Stamps. 7 pages. Blank placeholders, not a registered deed of a real person. |

Other official model deeds also exist (not copied): Goa https://www.goa.gov.in/wp-content/uploads/2017/10/Sale-Deed.pdf ; MoUD/DoLR model draft https://cdnbbsr.s3waas.gov.in/s3d69116f8b0140cdeb1f99a4d5096ffe4/uploads/2023/12/20231209681283888.pdf

## 6. UPI statement

| File | Source page | Notes |
|---|---|---|
| upi_gpay_statement_synthetic_sample.pdf | https://github.com/RohitSSolanki/synthetic-statement — fixture: https://raw.githubusercontent.com/RohitSSolanki/synthetic-statement/main/fixtures/sample_statements_seed7/gpay.pdf | Open-source synthetic Google Pay transaction statement for “Sample User” (sample.user@okhdfcbank), clearly marked “SYNTHETIC SAMPLE - NOT A REAL STATEMENT”. 4 pages. The same repo also has PhonePe and Paytm synthetic fixtures. |

Real-looking UPI PDFs found on Scribd / IndiaMART were not used because they appeared to be unredacted personal statements.
