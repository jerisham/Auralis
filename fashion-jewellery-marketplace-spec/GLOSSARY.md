# Glossary

|Term|Meaning|
|-|-|
|**Platform**|This marketplace (product + company).|
|**Vendor / Tenant / Seller**|An independent jewellery business that lists and ships products. Used interchangeably; code uses `vendor`.|
|**Vendor Owner**|The vendor user who registered the business; controls bank, KYC, staff.|
|**Vendor Staff**|Extra vendor login with limited permissions (products, orders).|
|**Customer**|Shopper who buys on the platform.|
|**Admin / Platform Admin**|Platform employee who approves vendors, resolves disputes, configures fees.|
|**Super Admin**|Admin who can manage other admins, commission rules, and payout overrides.|
|**Order**|What the customer places at checkout. May contain items from several vendors. One payment.|
|**Vendor Order (sub-order)**|The part of an Order belonging to one vendor. Has its own status, shipment and payout.|
|**SKU / Variant**|A specific purchasable version of a product (e.g., "Jhumka – Gold / Green").|
|**Commission / Platform fee**|Amount the platform keeps from each vendor order.|
|**Vendor net**|Item total + vendor shipping fee − platform fee. What the vendor ultimately receives.|
|**Tranche**|A partial payout. T1 released on dispatch, T2 after delivery + return window.|
|**Linked account**|The vendor's sub-account at the payment gateway that receives split payments.|
|**Return window**|Period after delivery in which a customer can raise a return / complaint (default 48 h).|
|**Settlement**|Money actually moved to a vendor's bank account.|
|**Ledger**|The platform's double-entry record of every money movement. Source of truth for balances.|
|**SLA**|Time limits the vendor must meet (accept, dispatch).|
|**Look**|A curated set of products (often from different vendors) worn together — "Complete the look".|
|**Skin-safety tags**|Product attributes: nickel-free, lead-free, hypoallergenic, anti-tarnish.|
|**PWA**|Progressive Web App — website installable on phone home screen.|
|**RLS**|Row-Level Security in PostgreSQL — makes the database itself enforce that a vendor sees only their rows.|
|**KYC**|Know Your Customer — identity/business verification of vendors (PAN, GST, bank).|



